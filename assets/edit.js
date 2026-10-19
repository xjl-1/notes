/* 站内编辑器 —— 直接读写 GitHub 上的源笔记，提交后由 Actions 自动重建站点。
   依赖：document.documentElement.dataset.base、style.css 的设计变量。 */
(function () {
  "use strict";

  var OWNER = "xjl-1";
  var REPO = "notes";
  var BRANCH = "main";
  var API = "https://api.github.com";
  var KEY = "notes.token";
  var SUFFIX = /\.(md|markdown|txt|docx)$/i;
  var TEXT = /\.(md|markdown|txt)$/i;
  var PREFIX = "vault/";

  var base = document.documentElement.dataset.base || "";
  var root = document.getElementById("editor");
  if (!root) return;

  var state = { token: "", files: [], current: null, sha: null, dirty: false, busy: false };
  var indexReady = null;

  /* ---------------------------------------------------------------- helpers */

  // vault/<源文件> → 站点里的相对路径，来自构建时写出的 search.json
  function loadIndex() {
    if (!indexReady) {
      indexReady = fetch(base + "search.json", { cache: "no-store" })
        .then(function (res) {
          return res.json();
        })
        .then(function (data) {
          var map = {};
          (data.notes || []).forEach(function (note) {
            if (note.p) map[note.p] = note.u;
          });
          return map;
        })
        .catch(function () {
          return {};
        });
    }
    return indexReady;
  }

  function el(tag, attrs, html) {
    var node = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === "class") node.className = attrs[k];
      else if (k.slice(0, 2) === "on") node.addEventListener(k.slice(2), attrs[k]);
      else node.setAttribute(k, attrs[k]);
    });
    if (html != null) node.innerHTML = html;
    return node;
  }

  function esc(text) {
    return String(text).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function encPath(path) {
    return String(path)
      .split("/")
      .map(encodeURIComponent)
      .join("/");
  }

  function b64enc(text) {
    var bytes = new TextEncoder().encode(text);
    var bin = "";
    var CH = 0x8000;
    for (var i = 0; i < bytes.length; i += CH) {
      bin += String.fromCharCode.apply(null, bytes.subarray(i, i + CH));
    }
    return btoa(bin);
  }

  function b64dec(text) {
    var bin = atob(String(text).replace(/\s+/g, ""));
    var bytes = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return new TextDecoder().decode(bytes);
  }

  function status(message, kind) {
    var box = document.getElementById("ed-status");
    if (!box) return;
    box.textContent = message || "";
    box.className = "ed-status" + (kind ? " ed-status--" + kind : "");
  }

  function api(path, options) {
    options = options || {};
    var init = {
      method: options.method || "GET",
      headers: {
        Authorization: "Bearer " + state.token,
        Accept: "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
      },
      cache: "no-store",
    };
    if (options.body) {
      init.headers["Content-Type"] = "application/json";
      init.body = JSON.stringify(options.body);
    }
    return fetch(API + path, init).then(function (res) {
      return res.text().then(function (raw) {
        var data = null;
        try {
          data = raw ? JSON.parse(raw) : null;
        } catch (e) {
          data = { message: raw.slice(0, 200) };
        }
        if (!res.ok) {
          var err = new Error((data && data.message) || res.status + " " + res.statusText);
          err.status = res.status;
          err.data = data;
          throw err;
        }
        return data;
      });
    });
  }

  function setBusy(flag) {
    state.busy = flag;
    document.body.classList.toggle("is-busy", flag);
  }

  /* ------------------------------------------------------------- token gate */

  function gate(message) {
    root.innerHTML = "";
    var card = el("div", { class: "ed-gate" });
    card.appendChild(el("h2", { class: "ed-gate__title" }, "连接 GitHub"));
    card.appendChild(
      el(
        "p",
        { class: "ed-gate__hint" },
        "粘贴一个有 <code>repo</code> 与 <code>workflow</code> 权限的 Classic token。它只保存在这台设备的浏览器里，不会上传到别处。"
      )
    );
    var input = el("input", {
      class: "ed-input",
      type: "password",
      placeholder: "ghp_…",
      autocomplete: "off",
      spellcheck: "false",
    });
    card.appendChild(input);
    var row = el("div", { class: "ed-row" });
    var go = el("button", { class: "btn btn--solid", type: "button" }, "连接");
    var clear = el("button", { class: "btn", type: "button" }, "清除已存 token");
    row.appendChild(go);
    row.appendChild(clear);
    card.appendChild(row);
    card.appendChild(el("p", { class: "ed-gate__hint ed-gate__hint--muted" }, "在 github.com/settings/tokens 生成或修改。"));
    if (message) card.appendChild(el("p", { class: "ed-status ed-status--err" }, esc(message)));
    root.appendChild(card);

    go.addEventListener("click", function () {
      var value = input.value.trim();
      if (!value) {
        input.focus();
        return;
      }
      state.token = value;
      connect();
    });
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") go.click();
    });
    clear.addEventListener("click", function () {
      localStorage.removeItem(KEY);
      input.value = "";
      status("已清除本机保存的 token");
    });
    input.focus();
  }

  function connect() {
    setBusy(true);
    status("正在验证 token…");
    api("/user")
      .then(function (me) {
        localStorage.setItem(KEY, state.token);
        return loadTree().then(function () {
          status("已连接 " + me.login + " · " + state.files.length + " 个文件", "ok");
          render();
        });
      })
      .catch(function (err) {
        state.token = "";
        localStorage.removeItem(KEY);
        gate(err.status === 401 ? "token 无效或已过期" : "连接失败：" + err.message);
      })
      .then(function () {
        setBusy(false);
      });
  }

  /* -------------------------------------------------------------- file list */

  function loadTree() {
    return api("/repos/" + OWNER + "/" + REPO + "/git/trees/" + BRANCH + "?recursive=1").then(function (data) {
      state.files = (data.tree || [])
        .filter(function (node) {
          return node.type === "blob" && node.path.indexOf(PREFIX) === 0 && SUFFIX.test(node.path);
        })
        .map(function (node) {
          return { path: node.path, size: node.size || 0 };
        })
        .sort(function (a, b) {
          return a.path.localeCompare(b.path, "zh");
        });
      return state.files;
    });
  }

  /* ---------------------------------------------------------------- toolbar */

  function toolbar() {
    var bar = el("div", { class: "ed-bar" });
    var filter = el("input", {
      class: "ed-input ed-input--search",
      type: "search",
      placeholder: "筛选文件…",
      id: "ed-filter",
    });
    bar.appendChild(filter);
    bar.appendChild(el("button", { class: "btn", type: "button", id: "ed-new" }, "新建"));
    bar.appendChild(el("button", { class: "btn", type: "button", id: "ed-refresh" }, "刷新"));
    bar.appendChild(el("button", { class: "btn btn--ghost", type: "button", id: "ed-forget" }, "退出"));
    return bar;
  }

  function fileList() {
    var wrap = el("div", { class: "ed-list", id: "ed-list" });
    if (!state.files.length) {
      wrap.appendChild(el("p", { class: "ed-empty" }, "还没有笔记。点「新建」写第一篇。"));
      return wrap;
    }
    state.files.forEach(function (file) {
      var label = file.path.slice(PREFIX.length);
      var item = el(
        "button",
        {
          class: "ed-item" + (state.current === file.path ? " is-active" : "") + (TEXT.test(file.path) ? "" : " is-binary"),
          type: "button",
          title: file.path,
        },
        '<span class="ed-item__name">' + esc(label) + "</span>" +
          '<span class="ed-item__meta">' + (TEXT.test(file.path) ? "" : "docx · ") + Math.max(1, Math.round(file.size / 1024)) + " KB</span>"
      );
      item.addEventListener("click", function () {
        open(file.path);
      });
      wrap.appendChild(item);
    });
    return wrap;
  }

  /* ----------------------------------------------------------------- editor */

  function open(path) {
    if (state.dirty && !confirm("当前修改还没保存，确定切换？")) return;
    state.current = path;
    state.sha = null;
    state.dirty = false;
    render();
    if (!TEXT.test(path)) {
      document.getElementById("ed-body").value = "";
      document.getElementById("ed-body").disabled = true;
      status("这是 Word 文档（.docx），只能查看不能在线编辑。要改内容请在电脑上用 Word 编辑后重新上传。", "info");
      return;
    }
    document.getElementById("ed-body").disabled = false;
    status("正在读取…");
    api("/repos/" + OWNER + "/" + REPO + "/contents/" + encPath(path) + "?ref=" + BRANCH)
      .then(function (data) {
        state.sha = data.sha;
        document.getElementById("ed-path").value = path;
        document.getElementById("ed-body").value = b64dec(data.content);
        document.getElementById("ed-body").focus();
        status("已读取 · 最后提交 " + (data.sha || "").slice(0, 7), "ok");
      })
      .catch(function (err) {
        status("读取失败：" + err.message, "err");
      });
  }

  function save(asNew) {
    if (state.busy) return;
    var path = (document.getElementById("ed-path").value || "").trim().replace(/^\/+/, "");
    if (!path) {
      status("路径不能为空", "err");
      return;
    }
    if (path.indexOf(PREFIX) !== 0) path = PREFIX + path.replace(/^vault\//, "");
    if (!SUFFIX.test(path)) path += ".md";
    var body = document.getElementById("ed-body").value;
    if (!body.trim()) {
      status("内容为空，没有保存", "err");
      return;
    }
    var moved = path !== state.current;
    setBusy(true);
    status(moved ? "正在移动/重命名…" : "正在提交…");

    var payload = {
      message: (asNew ? "新建 " : moved ? "移动 " : "编辑 ") + path.slice(PREFIX.length),
      content: b64enc(body),
      branch: BRANCH,
    };
    var target = "/repos/" + OWNER + "/" + REPO + "/contents/" + encPath(path);
    var request = state.sha && !moved ? api(target, { method: "PUT", body: Object.assign({ sha: state.sha }, payload) }) : null;
    var create = request || api(target, { method: "PUT", body: payload });

    create
      .then(function (res) {
        var newSha = res && res.content ? res.content.sha : null;
        if (!moved) {
          state.current = path;
          state.sha = newSha;
          state.dirty = false;
          status("已提交 · GitHub 正在重新生成站点，约 1 分钟后刷新页面即可看到", "ok");
          return loadTree().then(renderList);
        }
        var old = "/repos/" + OWNER + "/" + REPO + "/contents/" + encPath(state.current);
        return api(old, {
          method: "DELETE",
          body: { message: "移动后删除旧文件 " + state.current, sha: state.sha, branch: BRANCH },
        }).then(function () {
          state.current = path;
          state.sha = newSha;
          state.dirty = false;
          status("已移动并提交 · 约 1 分钟后生效", "ok");
          return loadTree().then(renderList);
        });
      })
      .catch(function (err) {
        if (err.status === 409) {
          status("远端已更新，请点「刷新」后重试（避免覆盖别处的修改）", "err");
        } else if (err.status === 404 && /workflow/i.test(err.message || "")) {
          status("这个 token 缺少 workflow 权限", "err");
        } else {
          status("提交失败：" + err.message, "err");
        }
      })
      .then(function () {
        setBusy(false);
      });
  }

  function remove() {
    if (!state.current || !state.sha) return;
    if (!confirm("删除 " + state.current.slice(PREFIX.length) + "？GitHub 上会有记录，可以找回。")) return;
    setBusy(true);
    status("正在删除…");
    api("/repos/" + OWNER + "/" + REPO + "/contents/" + encPath(state.current), {
      method: "DELETE",
      body: { message: "删除 " + state.current.slice(PREFIX.length), sha: state.sha, branch: BRANCH },
    })
      .then(function () {
        var gone = state.current;
        state.current = null;
        state.sha = null;
        state.dirty = false;
        status("已删除 " + gone.slice(PREFIX.length), "ok");
        return loadTree().then(render);
      })
      .catch(function (err) {
        status("删除失败：" + err.message, "err");
      })
      .then(function () {
        setBusy(false);
      });
  }

  function createFile() {
    var name = prompt("新笔记路径（可含目录，如 知识笔记/新想法）", "");
    if (name == null) return;
    name = name.trim().replace(/^\/+/, "");
    if (!name) return;
    if (!SUFFIX.test(name)) name += ".md";
    if (state.current && state.dirty && !confirm("当前修改还没保存，确定新建？")) return;
    state.current = PREFIX + name;
    state.sha = null;
    state.dirty = false;
    render();
    document.getElementById("ed-path").value = state.current;
    document.getElementById("ed-body").value = "---\ntitle: " + name.split("/").pop() + "\ncreated: " + new Date().toISOString().slice(0, 10) + "\nstatus: active\ntags: []\n---\n\n";
    document.getElementById("ed-body").focus();
    status("新笔记还没保存，写完点「保存」", "info");
  }

  /* ----------------------------------------------------------------- render */

  function applyFilter(value) {
    var needle = (value || "").trim().toLowerCase();
    Array.prototype.forEach.call(document.querySelectorAll(".ed-item"), function (node) {
      node.hidden = !!(needle && node.title.toLowerCase().indexOf(needle) === -1);
    });
  }

  // 只重画左侧列表，不动右侧正在编辑的内容
  function renderList() {
    var old = document.getElementById("ed-list");
    if (!old) return;
    old.replaceWith(fileList());
    var filter = document.getElementById("ed-filter");
    if (filter) applyFilter(filter.value);
  }

  function render() {
    root.innerHTML = "";
    var shell = el("div", { class: "ed" });
    var side = el("div", { class: "ed-side" });
    side.appendChild(toolbar());
    side.appendChild(fileList());
    shell.appendChild(side);

    var pane = el("div", { class: "ed-pane" });
    var actions = el("div", { class: "ed-actions" });
    actions.appendChild(el("input", { class: "ed-input ed-input--path", id: "ed-path", spellcheck: "false", placeholder: "vault/目录/笔记.md", value: state.current || "" }));
    actions.appendChild(el("button", { class: "btn btn--solid", type: "button", id: "ed-save" }, "保存"));
    actions.appendChild(el("button", { class: "btn", type: "button", id: "ed-delete" }, "删除"));
    actions.appendChild(el("a", { class: "btn btn--ghost", id: "ed-view", href: "#", target: "_blank", rel: "noopener" }, "看页面"));
    pane.appendChild(actions);
    var body = el("textarea", {
      class: "ed-body",
      id: "ed-body",
      spellcheck: "false",
      placeholder: "在这里写 Markdown…\n\n左侧选一篇，或点「新建」。",
    });
    body.value = "";
    pane.appendChild(body);
    pane.appendChild(el("p", { class: "ed-status", id: "ed-status" }));
    shell.appendChild(pane);
    root.appendChild(shell);

    body.addEventListener("input", function () {
      state.dirty = true;
    });
    document.getElementById("ed-save").addEventListener("click", function () {
      save(false);
    });
    document.getElementById("ed-delete").addEventListener("click", remove);
    document.getElementById("ed-refresh").addEventListener("click", function () {
      status("正在刷新…");
      loadTree().then(function () {
        status("已刷新 · " + state.files.length + " 个文件", "ok");
        renderList();
      }).catch(function (err) {
        status("刷新失败：" + err.message, "err");
      });
    });
    document.getElementById("ed-new").addEventListener("click", createFile);
    document.getElementById("ed-forget").addEventListener("click", function () {
      if (state.dirty && !confirm("当前修改还没保存，确定退出？")) return;
      localStorage.removeItem(KEY);
      state.token = "";
      gate();
    });
    var filter = document.getElementById("ed-filter");
    filter.addEventListener("input", function () {
      applyFilter(filter.value);
    });

    var view = document.getElementById("ed-view");
    view.hidden = true;
    if (state.current && TEXT.test(state.current)) {
      loadIndex().then(function (map) {
        var done = document.getElementById("ed-view");
        var out = map[state.current];
        if (!done || !out) return;
        done.href = base + out.split("/").map(encodeURIComponent).join("/");
        done.hidden = false;
      });
    }

    var path = document.getElementById("ed-path");
    path.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        open(path.value.trim());
      }
    });
  }

  /* ------------------------------------------------------------------- boot */

  function boot() {
    var stored = "";
    try {
      stored = localStorage.getItem(KEY) || "";
    } catch (e) {
      stored = "";
    }
    if (!stored) {
      gate();
      return;
    }
    state.token = stored;
    connect();
  }

  window.addEventListener("beforeunload", function (e) {
    if (state.dirty) {
      e.preventDefault();
      e.returnValue = "";
    }
  });

  boot();

  // 从笔记页「编辑此页」跳过来时，直接打开对应文件。
  var wanted = new URLSearchParams(location.search).get("path");
  if (wanted) {
    var tryOpen = setInterval(function () {
      if (state.token && state.files.length) {
        clearInterval(tryOpen);
        if (!state.current) open(wanted);
      }
    }, 120);
    setTimeout(function () {
      clearInterval(tryOpen);
    }, 8000);
  }
})();
