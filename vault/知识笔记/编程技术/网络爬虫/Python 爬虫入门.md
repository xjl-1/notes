---
title: Python 爬虫入门
tags: [爬虫, Python, HTTP]
created: 2026-06-04
type: note
status: active
summary: HTTP/HTTPS 协议、浏览器请求过程与 URL 组成。
---

什么是http和https协议: 
HTTP协议:全称是 yperTextiransfer protoce1，中文意思是超文本传输协议，是一种发布和接收HTML页面的方法。服务器端口 号是 80 口。
HTTPS协议:是HTTP协议的加密版本，在HTTP下加入了SSL层。服务器端口号是 443 端口。

在浏览器中发送一个http请求的过程: 
1.当用户在浏览器的地址栏中输入一个URL并按回车键之后，浏览器会向HTTP服务器发送HTTP请求。HTTP请求主要分 为“Get和“Post 两种方法。
2.当我们在浏览器输入URL http:/www.baldu.com 的时候，浏览器发送一个Request请求去获取 hitp://www.baidu.com 的html文 件，服务器把Response文件对象发送回给浏览器。
3.浏览器分析Respons@中的 HTML，发现其中引用了很多其他文件，比如!mages文件，CSS文件，JS文件。浏览器会自动再次发 送Request去获取图片，CSS文件，或者JS文件。
4.当所有的文件都下载成功后，网页会根据HTML语法结构，完整的显示出来了。

URL详解
一个 URL由以下几部分组成: scheme://host:port/path/?query-stringexxx#anchor 
schame:代表的是访问的协议，一般为 http或者 nttps以及 ftp 等。
host:主机名，域名，比如.baidu.coa port:端口号。当你访问一个网站的时候，浏览器默认使用80口。
path:查找路径。比如:mnn.jianshu.com/trending/now ，后面的 trending/now 就是 path 。
query-string:查询字符串，比如: mm.baidu.cca/s>md=python ，后面的 wd=python 就是查询字符串。
anchor:锚点，后台一般不用管，前端用来做页面定位的。
在浏览器中请求一个 ur1，浏览器会对这个ur进行一个编码。除英文字母，数字和部分符号外，其他的全部使用百分号+十六进制码 值进行编码。

常用的请求方法:
在 http协议中，定义了八种请求方法。这里介绍两仲常用的方法，分别是 get请求和 post请求。
1、get请求:一般情况下，只从服务器获取数据下来，并不会对服务器资源产生任何影响的时候会使用 get请求。
2、post请求:向服务器发送数据(登录)、上传文件等，会对服务器资源产生影响的时候会使用 post请求。
以上是在网站开发中常用的两种方法，并且一般情况下都会遵循使用的原则。但是有的网站和服务器为了做反爬虫机制，也经常会不 按常理出牌，有可能一个应该使用get方法的请求就一定要改成 post请求，这个视情况而定。

请求头常见参数: 在 nttp 协议中，向服务器发送一个请求，数据分为三部分，第一个是把数据放在url中，第二个是把数据放在 body中(在 post 请求中)，第三个就是把数据放在head中。经常会用到的一些请求头参数:
1.User-Agent:浏览图名称,经常会被使用到。请求一个网页的时候，服务图通过这个参数就可以知道这个请求是由哪种测览器发送的。如果我们是通过爬虫发送请求，那么我们的 User-Agent 就是python ，这对于那些有反爬虫机制的网站来说，可以轻易的判断你这个请求是爬虫。因此我们要经常设这个值为一些浏览器的值，来伪装我们的爬虫。
2 Referer :来明当前这个请求是从哪个 url 过来的。这个一般也可以用来做反爬虫技术。如果不是从指定页面过来的，那么就不做相关的响应。
3、cookie :http协议是无状态的。也就是同一个人发送了两次请求，服务器没有能力知道这两个请求是否来自同一个人。因此这时候用 cookie 来标识。一般如果想登录后才能访问的网站，那么就需要发送 cookie信息了。
