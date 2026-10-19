/* 笔记 · app.js — vanilla, no deps */
(function () {
  "use strict";

  var root = document.documentElement;
  var base = root.dataset.base || "";
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  /* ---------- theme ---------- */
  var ICON_SUN = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2M12 19.5v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M2.5 12h2M19.5 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></svg>';
  var ICON_MOON = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z"/></svg>';

  function paintTheme() {
    var dark = root.dataset.theme !== "light";
    $$("[data-theme-toggle]").forEach(function (b) {
      b.innerHTML = dark ? ICON_SUN : ICON_MOON;
      b.setAttribute("aria-label", dark ? "切换到浅色" : "切换到深色");
      b.title = dark ? "浅色" : "深色";
    });
  }
  paintTheme();

  document.addEventListener("click", function (e) {
    var t = e.target.closest("[data-theme-toggle]");
    if (!t) return;
    var next = root.dataset.theme === "light" ? "dark" : "light";
    root.dataset.theme = next;
    store.set("theme", next);
    paintTheme();
  });

  /* ---------- font size ---------- */
  var SIZES = { s: "0.94", m: "1", l: "1.08" };
  var sizeKey = store.get("size") || "m";
  if (SIZES[sizeKey]) root.style.setProperty("--step", SIZES[sizeKey]);
  document.addEventListener("click", function (e) {
    var t = e.target.closest("[data-size-toggle]");
    if (!t) return;
    var order = ["s", "m", "l"];
    var cur = order.indexOf(store.get("size") || "m");
    var next = order[(cur + 1) % order.length];
    store.set("size", next);
    root.style.setProperty("--step", SIZES[next]);
    var label = t.querySelector("[data-size-label]");
    if (label) label.textContent = { s: "小", m: "中", l: "大" }[next];
  });

  /* ---------- drawer ---------- */
  var body = document.body;
  function drawer(open) {
    body.dataset.drawer = open ? "open" : "";
    var btn = $("[data-drawer-toggle]");
    if (btn) btn.setAttribute("aria-expanded", open ? "true" : "false");
  }
  document.addEventListener("click", function (e) {
    if (e.target.closest("[data-drawer-toggle]")) { drawer(body.dataset.drawer !== "open"); return; }
    if (e.target.closest(".scrim") || e.target.closest("[data-drawer-close]")) drawer(false);
    var link = e.target.closest(".sidebar a");
    if (link && window.innerWidth <= 900) drawer(false);
  });
  window.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && body.dataset.drawer === "open") drawer(false);
  });

  /* ---------- progress + toc + totop ---------- */
  var bar = $(".progress__bar");
  var tocLinks = $$(".toc a");
  var heads = tocLinks.map(function (a) {
    var id = decodeURIComponent(a.getAttribute("href").slice(1));
    return document.getElementById(id);
  }).filter(Boolean);
  var totop = $(".totop");

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      var doc = document.documentElement;
      var max = doc.scrollHeight - window.innerHeight;
      var p = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
      if (bar) bar.style.width = (p * 100).toFixed(2) + "%";
      if (totop) totop.classList.toggle("is-on", window.scrollY > 640);

      if (heads.length) {
        var active = heads[0];
        var top = window.scrollY + 120;
        for (var i = 0; i < heads.length; i++) {
          if (heads[i].offsetTop <= top) active = heads[i];
        }
        tocLinks.forEach(function (a) {
          var id = decodeURIComponent(a.getAttribute("href").slice(1));
          a.classList.toggle("is-active", active && active.id === id);
        });
      }
      ticking = false;
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();

  document.addEventListener("click", function (e) {
    if (e.target.closest(".totop")) { window.scrollTo({ top: 0, behavior: "smooth" }); }
    var copy = e.target.closest(".copybtn");
    if (copy) {
      var pre = copy.closest("pre");
      var code = pre && pre.querySelector("code");
      if (!code) return;
      var text = code.innerText;
      var done = function () {
        copy.textContent = "已复制";
        copy.classList.add("is-done");
        setTimeout(function () { copy.textContent = "复制"; copy.classList.remove("is-done"); }, 1400);
      };
      if (navigator.clipboard) { navigator.clipboard.writeText(text).then(done, done); }
      else {
        var ta = document.createElement("textarea");
        ta.value = text; document.body.appendChild(ta); ta.select();
        try { document.execCommand("copy"); } catch (err) {}
        document.body.removeChild(ta); done();
      }
    }
  });

  /* code copy buttons */
  $$(".prose pre").forEach(function (pre) {
    var b = document.createElement("button");
    b.className = "copybtn";
    b.type = "button";
    b.textContent = "复制";
    pre.appendChild(b);
  });

  /* ---------- lightbox ---------- */
  var lb = document.createElement("div");
  lb.className = "lightbox";
  lb.innerHTML = '<img alt="">';
  document.body.appendChild(lb);
  document.addEventListener("click", function (e) {
    var img = e.target.closest(".prose img");
    if (img) { lb.querySelector("img").src = img.src; lb.dataset.open = "true"; }
    else if (e.target.closest(".lightbox")) { lb.dataset.open = ""; }
  });
  window.addEventListener("keydown", function (e) {
    if (e.key === "Escape") lb.dataset.open = "";
  });

  /* ---------- search ---------- */
  var overlay = document.createElement("div");
  overlay.className = "search";
  overlay.innerHTML =
    '<div class="search__panel" role="dialog" aria-modal="true" aria-label="搜索笔记">' +
    '<div class="search__field">' +
    '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/></svg>' +
    '<input class="search__input" type="search" placeholder="搜索标题、标签、正文…" autocomplete="off" spellcheck="false">' +
    '<span class="search__esc">Esc</span></div>' +
    '<div class="search__results"><div class="search__hint">输入关键词，回车打开第一条</div></div>' +
    '<div class="search__foot"><span><kbd>↑</kbd><kbd>↓</kbd> 选择</span><span><kbd>Enter</kbd> 打开</span><span><kbd>/</kbd> 唤起搜索</span></div>' +
    "</div>";
  document.body.appendChild(overlay);

  var input = $(".search__input", overlay);
  var results = $(".search__results", overlay);
  var index = null;
  var loading = null;
  var cursor = -1;

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function hl(text, terms) {
    var out = esc(text);
    terms.forEach(function (t) {
      if (!t) return;
      var re = new RegExp("(" + t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "gi");
      out = out.replace(re, "<b>$1</b>");
    });
    return out;
  }

  function loadIndex() {
    if (index) return Promise.resolve(index);
    if (loading) return loading;
    loading = fetch(base + "search.json", { cache: "no-cache" })
      .then(function (r) { return r.json(); })
      .then(function (d) { index = d.notes || d; return index; })
      .catch(function () { index = []; return index; });
    return loading;
  }

  function openSearch() {
    overlay.dataset.open = "true";
    loadIndex().then(function () { input.focus(); input.select(); });
    document.body.style.overflow = "hidden";
  }
  function closeSearch() {
    overlay.dataset.open = "";
    document.body.style.overflow = "";
  }

  function run(q) {
    if (!index) return;
    var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) {
      results.innerHTML = '<div class="search__hint">输入关键词，回车打开第一条</div>';
      cursor = -1;
      return;
    }
    var scored = [];
    index.forEach(function (n) {
      var title = (n.t || "").toLowerCase();
      var tags = (n.k || []).join(" ").toLowerCase();
      var folder = (n.f || "").toLowerCase();
      var body = (n.x || "").toLowerCase();
      var score = 0, all = true;
      terms.forEach(function (t) {
        var s = 0;
        if (title.indexOf(t) >= 0) s += 12;
        if (tags.indexOf(t) >= 0) s += 5;
        if (folder.indexOf(t) >= 0) s += 3;
        var at = body.indexOf(t);
        if (at >= 0) { s += 2; var c = 0; while ((at = body.indexOf(t, at + 1)) >= 0 && c < 40) c++; s += Math.min(c, 6); }
        if (s === 0) all = false;
        score += s;
      });
      if (all && score > 0) scored.push({ n: n, score: score });
    });
    scored.sort(function (a, b) { return b.score - a.score; });
    var top = scored.slice(0, 40);
    if (!top.length) {
      results.innerHTML = '<div class="search__hint">没有找到「' + esc(q) + '」</div>';
      cursor = -1;
      return;
    }
    results.innerHTML = top.map(function (r, i) {
      var n = r.n;
      var bodyText = n.x || "";
      var low = bodyText.toLowerCase();
      var at = -1;
      terms.forEach(function (t) { var p = low.indexOf(t); if (p >= 0 && (at < 0 || p < at)) at = p; });
      var snip = at >= 0 ? bodyText.slice(Math.max(0, at - 30), at + 90) : (n.s || "");
      return '<a class="result' + (i === 0 ? " is-active" : "") + '" href="' + base + n.u + '">' +
        '<div class="result__title">' + hl(n.t, terms) + "</div>" +
        '<div class="result__path">' + esc(n.f || "") + "</div>" +
        (snip ? '<div class="result__snip">' + hl(snip, terms) + "</div>" : "") +
        "</a>";
    }).join("");
    cursor = 0;
  }

  function move(d) {
    var items = $$(".result", results);
    if (!items.length) return;
    cursor = (cursor + d + items.length) % items.length;
    items.forEach(function (el, i) { el.classList.toggle("is-active", i === cursor); });
    var el = items[cursor];
    if (el.scrollIntoView) el.scrollIntoView({ block: "nearest" });
  }

  input.addEventListener("input", function () { run(input.value); });
  input.addEventListener("keydown", function (e) {
    if (e.key === "ArrowDown") { e.preventDefault(); move(1); }
    else if (e.key === "ArrowUp") { e.preventDefault(); move(-1); }
    else if (e.key === "Enter") {
      var items = $$(".result", results);
      if (items[cursor]) window.location.href = items[cursor].getAttribute("href");
    } else if (e.key === "Escape") { closeSearch(); }
  });
  overlay.addEventListener("click", function (e) { if (e.target === overlay) closeSearch(); });

  window.addEventListener("keydown", function (e) {
    var tag = (e.target.tagName || "").toLowerCase();
    var typing = tag === "input" || tag === "textarea" || e.target.isContentEditable;
    if ((e.key === "/" && !typing) || ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k")) {
      e.preventDefault(); openSearch();
    }
    if (e.key === "Escape" && overlay.dataset.open === "true") closeSearch();
  });
  document.addEventListener("click", function (e) {
    if (e.target.closest("[data-search-open]")) { e.preventDefault(); openSearch(); }
  });

  /* ---------- math (only when present) ---------- */
  if (document.querySelector(".math-block, .math-inline")) {
    var css = document.createElement("link");
    css.rel = "stylesheet";
    css.href = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css";
    document.head.appendChild(css);
    var s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js";
    s.defer = true;
    s.onload = function () {
      $$("[data-tex]").forEach(function (el) {
        try {
          katex.render(el.getAttribute("data-tex"), el, {
            displayMode: el.classList.contains("math-block"),
            throwOnError: false
          });
          el.removeAttribute("data-tex");
        } catch (err) {}
      });
    };
    document.head.appendChild(s);
  }
})();
