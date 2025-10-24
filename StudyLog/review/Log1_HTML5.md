# HTML5 核心知识复习记录
## 一、本文档目的
- 将 HTML5 的核心概念、高频用法与易错点提炼为速查式笔记，适配 10 分钟碎片化回顾、1 小时集中复习两种节奏。
- 提供可落地的实战练习与周期化复习计划，帮助将理论转化为实操能力，避免“学完就忘”。


## 二、宏观结构（快速导航）
- 文档基础（DOCTYPE、html/head/body、meta 标签）
- 文本与语义标签（标题、段落、强调、块级/内联元素）
- 媒体标签（img、video、audio）
- 链接与路径（超链接、锚点、相对/绝对路径）
- 列表标签（无序列表、有序列表、描述列表）
- 表格标签（结构标签、合并单元格）
- 表单标签（容器、控件、辅助标签 label）
- 字符实体（常用特殊字符）
- 语义化布局标签（header、nav、main、aside、footer）


## 三、核心概念速查（记忆卡）
### 1. 文档基础
- **必含结构**：`<!DOCTYPE html>`（HTML5 声明，无闭合）→ `<html lang="zh-CN">`（根元素）→ `<head>`（元数据）+ `<body>`（内容）。
- **关键 meta 标签**：
  - `meta charset="UTF-8"`：避免中文乱码（必加）。
  - `meta name="viewport" content="width=device-width, initial-scale=1.0"`：移动端适配（避免缩放异常）。
- **title**：浏览器标签栏标题，不显示在页面内容区。

### 2. 文本与语义标签
- **标题**：`<h1>`~`<h6>`（h1 每页 1 次，层级≤3 级，块级，默认加粗）。
- **段落**：`<p>`（块级，自动换行，仅包裹文本/内联元素，不嵌套块级）。
- **强调标签**：
  - 有语义：`<strong>`（加粗，重要内容）、`<em>`（倾斜，语气强调）、`<del>`（删除线，旧内容）。
  - 无语义：`<b>`/`<i>`（仅视觉效果，不推荐）。
- **块级 vs 内联元素**：
  - 块级：独占一行，可设宽高（如 div、h1~h6、p、ul、table）。
  - 内联：不独占一行，不可直接设宽高（如 span、a、strong、img 特殊可设）。

### 3. 媒体标签
- **图片 `<img>`**（单标签）：
  - 核心属性：`src`（路径，必加）、`alt`（加载失败备用文本，提升可访问性）。
  - 其他：`title`（悬停提示）、`width`/`height`（建议用 CSS 控制）。
  - 格式：JPG（普通图）、PNG（透明图）、WebP（高压缩）。
- **视频 `<video>`**：
  - 核心属性：`src`、`controls`（显示播放控件）、`poster`（预览图）。
  - 兼容性写法：用 `<source>` 标签加载 mp4/ogg/webm 格式。
- **音频 `<audio>`**：
  - 核心属性：`src`、`controls`，兼容性写法同视频，支持 mp3/wav/ogg。

### 4. 链接与路径
- **超链接 `<a>`**：
  - 核心属性：`href`（跳转目标：外部 URL/内部页面/空链接 `#`/下载文件/邮件 `mailto:xxx`）、`target`（`_blank` 新窗口，外部链接推荐）。
  - 锚点链接：目标元素加 `id`，链接写 `#id`，加 `html { scroll-behavior: smooth; }` 实现平滑滚动。
- **路径**：
  - 相对路径（常用）：
    - 同级：`src="a.jpg"` 或 `src="./a.jpg"`。
    - 下级：`src="img/a.jpg"`（图片在 img 文件夹）。
    - 上级：`src="../a.jpg"`（返回上一级文件夹）。
  - 绝对路径：完整 URL（如 `https://xxx/a.jpg`）或本地盘符（不推荐）。

### 5. 列表标签
- **无序列表 `<ul>`+`<li>`**（最常用）：
  - 语法：`<ul>` 仅包含 `<li>`，`<li>` 可嵌套任意标签（如 a、img）。
  - 场景：导航栏、商品列表。
- **有序列表 `<ol>`+`<li>`**（了解）：
  - 场景：步骤说明（强调原生顺序，实际开发常用 ul+CSS 替代）。
- **描述列表 `<dl>`+`<dt>`+`<dd>`**（页脚常用）：
  - 语法：`<dl>` 含 `<dt>`（术语）和 `<dd>`（解释），1 个 dt 可对应多个 dd。
  - 场景：商品参数、页脚分类导航。

### 6. 表格标签
- **核心结构**：`<table>`（容器）→ `<tr>`（行）→ `<th>`（表头，加粗居中）/`<td>`（单元格）。
- **语义结构标签**（推荐）：`<thead>`（表头行）、`<tbody>`（数据行）、`<tfoot>`（合计行），增强可读性。
- **合并单元格**（慎用）：`colspan="n"`（跨列）、`rowspan="n"`（跨行），步骤：选目标单元格→加属性→删多余单元格。

### 7. 表单标签（用户交互核心）
- **三部分组成**：
  - 容器 `<form>`：`action`（提交地址，暂空）。
  - 控件：`input`（text/password/radio/checkbox/file）、`textarea`（多行文本）、`select`+`<option>`（下拉）、`button`（提交/重置）。
  - 辅助标签 `<label>`：关联控件（`for="id"` 或直接包裹），点击标签聚焦控件，提升可访问性。
- **关键控件属性**：
  - radio/checkbox：加 `name` 分组（同组互斥），`checked` 默认选中。
  - file：`accept="image/*"` 限制文件类型，`multiple` 允许多选。
  - button：`type="submit"`（提交）、`reset`（重置）、`button`（自定义）。

### 8. 字符实体（显示特殊字符）
- 常用：`&lt;`（<）、`&gt;`（>）、`&amp;`（&）、`&nbsp;`（不换行空格）、`&copy;`（©）。


## 四、常见错误与陷阱（高频）
1. **路径错误**：
   - 同级图片漏写文件名或多写 `./`（虽可省略，但不规范）。
   - 下级图片漏写文件夹名（如 `src="a.jpg"` 而非 `src="img/a.jpg"`）。
   - 上级图片多写 `../`（如返回 1 级却写 `../../a.jpg`）。
2. **标签嵌套错误**：
   - `<p>` 标签嵌套块级元素（如 `<p><div>错误</div></p>`，浏览器会自动解析异常）。
   - `<ul>`/`<ol>` 直接放文本或 `<div>`，未用 `<li>` 包裹（如 `<ul><div>列表项</div></ul>`）。
3. **表单控件问题**：
   - radio/checkbox 未加 `name` 分组，导致无法互斥。
   - 未用 `<label>` 关联控件，降低可访问性。
   - `input` 漏写 `type`，默认按 `text` 解析。
4. **媒体标签遗漏**：
   - `<img>` 漏写 `alt` 属性（影响 SEO 和可访问性）。
   - `<video>`/`<audio>` 未加 `<source>` 兼容性写法，部分浏览器无法播放。
5. **文档结构错误**：
   - 未加 `<!DOCTYPE html>`，浏览器进入怪异模式。
   - 漏写 `<meta charset="UTF-8">`，中文显示乱码。
   - `<head>` 内写内容标签（如 `<p>`、`<img>`），无法显示。


## 五、快速练习（把知识变成肌肉记忆）
### 1. 10 分钟任务（基础回顾）
- 任务 1：手写 HTML5 基础文档结构，包含 `DOCTYPE`、`html`、`head`（含 `charset`、`viewport`、`title`）、`body`（加 1 个 `<h1>` 和 1 个 `<p>`）。
- 任务 2：用 `<img>` 显示一张图片（存放在 `img` 文件夹），加 `alt` 和 `title`。
- 任务 3：写一个无序列表，含 3 个列表项，每个项包裹 `<a>` 标签（空链接 `#`）。

### 2. 1 小时任务（综合应用）
- 需求：制作一个“简单用户反馈页”，包含：
  1. 页面标题 `<h1>`（用户反馈）。
  2. 描述列表 `<dl>`：术语“反馈类型”，解释“建议/bug/其他”。
  3. 表单 `<form>`：
     - 单行输入框（`type="text"`，placeholder“您的昵称”，加 `<label>`）。
     - 多行文本框 `<textarea>`（placeholder“请输入反馈内容”）。
     - 单选框（`name="type"`，选项“建议”“bug”“其他”，加 `<label>`）。
     - 提交按钮（`type="submit"`，文字“提交反馈”）。
  4. 底部用 `<footer>` 包裹版权信息（`&copy; 2025 反馈平台`）。


## 六、代码片段（常用模板，拷贝即用）
### 1. HTML5 基础文档结构
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>页面标题</title>
</head>
<body>
  <!-- 页面内容 -->
  <h1>欢迎页面</h1>
  <p>这是一个基础 HTML5 文档</p>
</body>
</html>
```

### 2. 图片标签（含路径与属性）
```html
<!-- 下级文件夹图片 -->
<img src="img/avatar.png" alt="用户头像" title="点击查看个人资料" width="100">
```

### 3. 视频标签（兼容性写法）
```html
<video controls poster="img/cover.jpg" width="400">
  <source src="video/movie.mp4" type="video/mp4">
  <source src="video/movie.webm" type="video/webm">
  <p>您的浏览器不支持 HTML5 视频，请升级浏览器</p>
</video>
```

### 4. 无序列表（导航示例）
```html
<nav>
  <ul>
    <li><a href="index.html">首页</a></li>
    <li><a href="about.html">关于我们</a></li>
    <li><a href="contact.html">联系我们</a></li>
  </ul>
</nav>
```

### 5. 描述列表（页脚分类）
```html
<footer>
  <dl>
    <dt>服务支持</dt>
    <dd>申请售后</dd>
    <dd>维修价格</dd>
    <dd>服务网点</dd>
    
    <dt>关注我们</dt>
    <dd>微信公众号</dd>
    <dd>官方微博</dd>
  </dl>
</footer>
```

### 6. 表单（登录示例）
```html
<form action="" method="post">
  <div>
    <label for="username">用户名：</label>
    <input type="text" id="username" name="username" placeholder="请输入用户名" required>
  </div>
  <div>
    <label for="password">密码：</label>
    <input type="password" id="password" name="password" placeholder="请输入密码" required>
  </div>
  <div>
    <label><input type="checkbox" name="remember"> 记住我</label>
  </div>
  <button type="submit">登录</button>
  <button type="reset">重置</button>
</form>
```

### 7. 常用字符实体
```html
<p>1. HTML 标签语法：&lt;标签名&gt;（如 &lt;div&gt;）</p>
<p>2. 版权声明：&copy; 2025 技术团队</p>
<p>3. 不换行空格：&nbsp;&nbsp;这里有两个空格</p>
```


## 八、复习计划（建议周期化）
### 1. 每周（30 分钟）
- 回顾“核心概念速查”，重点记忆路径规则、表单控件属性、列表语法。
- 完成 1 个“10 分钟任务”，如写表单或媒体标签代码，验证是否掌握核心属性。

### 2. 每两周（2 小时）
- 完成 1 个“1 小时任务”，如制作带列表、表单、媒体的简单页面。
- 整理本周遇到的错误（如路径、嵌套问题），记录到错题本，避免重复踩坑。

### 3. 每月（半天）
- 做 1 个综合案例（如“个人博客首页”），包含文档结构、文本、图片、列表、表单，检验综合应用能力。
- 用浏览器调试工具（F12）检查页面结构，修复标签嵌套、路径等问题。


## 九、自测题（检验掌握情况）
1. HTML5 文档结构中，必须包含的标签有哪些？`<!DOCTYPE html>`、`<html>`、`<head>`、`<body>` 分别有什么作用？
2. `<img>` 标签的核心属性有哪些？`alt` 属性的作用是什么？
3. 相对路径分为哪三种情况？分别写出“图片在当前文件夹的 img 子文件夹”和“图片在当前文件夹的上一级文件夹”的路径写法。
4. 表单由哪三部分组成？`<label>` 标签有两种关联控件的方式，分别是什么？
5. 块级元素和内联元素的核心区别是什么？请各举 3 个常见的块级元素和内联元素。


## 十、复习小贴士
1. **用浏览器调试工具辅助**：右键页面→“检查”，在 Elements 面板中查看标签结构，可实时修改标签/属性，观察效果（修改不影响原代码），快速排查嵌套、路径错误。
2. **“写+改”比“看”更有效**：不要只看笔记，每次复习都动手写代码，比如写表单时故意漏 `label`，观察体验差异，再修复，加深记忆。
3. **整理“个人模板库”**：将常用的文档结构、表单、列表代码整理到一个 `.html` 文件中，后续开发或复习时直接复用，减少重复书写，同时强化记忆。
4. **关注语义化**：复习时多思考“为什么用这个标签”（如用 `<h1>` 而非 `<div>` 做标题），语义化不仅利于 SEO，也让代码更易维护。