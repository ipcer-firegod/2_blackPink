# HTML5 全面学习笔记（详细版）

> 目标：将 `Log1_HTML5.md` 的精简速查扩展为全面、可操作的 HTML5 学习手册，包含示例、兼容性说明、可访问性细节、常见陷阱与练习。适合需要系统复习或用于做题/重构时参考。

更新时间：2025-10-10
来源：课程资料《HTML5 核心知识点复习笔记》（整理）

---

## 一、为什么用精简版扩展为完整版
- 精简版适合快速回顾，完整版用于在复习或解决实际问题时参考细节与示例。
- 直接从 PDF 全盘复制会导致内容冗杂，不利于复习效率；本方案保留结构化索引并补充必要的代码片段、示例和最佳实践。

## 二、文档结构
- 文档骨架与 meta（doctype、charset、viewport、lang）详解
- 语义化标签与页面结构（header/nav/main/article/section/footer 等）
- 文本与内容标签（标题、段落、列表、强调、blockquote、pre/code）
- 媒体元素（img、picture、video、audio、source）与响应式图片
- 链接与导航（a、锚点、rel 属性、安全注意）
- 表格与数据（table/thead/tbody/tfoot/th/td、scope、caption）
- 表单详解（label、input 类型、验证、文件上传、可访问性）
- 多语言、字符实体与编码问题
- 可访问性（ARIA、键盘导航、语义化）
- 常见错误与调试技巧
- 练习任务与复习计划

---

## 三、文档骨架与 meta（必知）
### 基本模板
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>示例页面</title>
  <meta name="description" content="页面描述，利于SEO">
</head>
<body>
  <header>...header content...</header>
  <main>...main content...</main>
  <footer>...footer content...</footer>
</body>
</html>
```

### 重要说明
- DOCTYPE 告诉浏览器采用标准模式（避免 quirks mode）。
- `lang` 用于屏幕阅读器与搜索引擎；多语言页面应在相应元素上设置 `lang` 属性。
- `meta charset` 必须在 head 内尽早声明以避免解析错误。
- `viewport` 控制移动端缩放与布局，常用 mobile-first 设置为 `width=device-width, initial-scale=1`。

---

## 四、语义化标签与页面结构
### 1. 语义化区域标签
- header、nav、main、article、section、aside、footer 的语义与示例
```html
<header>
  <h1>网站标题</h1>
  <nav> <ul>...导航...</ul> </nav>
</header>
<main>
  <article>...文章内容...</article>
  <aside>...侧边栏...</aside>
</main>
<footer>...版权信息...</footer>
```
- 建议：每页只用一个 `main`，让屏幕阅读器更易定位主要内容

### 2. 何时用 div？
- `div` 仍然有用作布局容器，但优先使用语义化标签来表达结构

---

## 五、文本与内容标签（详解与示例）
### 标题与段落
- h1-h6 层级代表文档结构，应按逻辑使用（h1 一般仅一个）。

### 强调与语义
- strong（强调，语义粗体） vs b（无语义）；em vs i
- ins/del 用于标注插入/删除文本

### 代码与引用
- `pre` + `code` 用于代码块，记得加语言类名（如 `class="language-html"`）用于高亮工具
- `blockquote` 用于引用内容，配合 `cite` 使用可标注来源

---

## 六、媒体元素（图片、响应式图片、音视频）
### 图片（img）基础
- 必备属性：`src`, `alt`（必须），可选：`title`, `width`, `height`, `loading`（lazy）
- 使用宽高占位可以避免布局抖动：`width` 和 `height` 或通过 CSS 维护纵横比

### 响应式图片
- picture + source 用于在不同分辨率/格式下提供不同图像
```html
<picture>
  <source media="(min-width:800px)" srcset="large.jpg">
  <source media="(min-width:400px)" srcset="medium.jpg">
  <img src="small.jpg" alt="描述" loading="lazy">
</picture>
```
- webp 等现代格式能显著减小体积，使用 `picture` 或 `srcset` 提供回退

### 视频与音频
- 用 `<video controls preload="metadata" poster="...">` 并提供多格式 source
- `autoplay` 在现代浏览器通常需要 `muted` 才能自动播放

---

## 七、链接与导航（安全与可访问性）
- 外链建议使用 `target="_blank" rel="noopener noreferrer"` 以防 tabnabbing
- 使用 `title` 增强提示，但不要替代可见文本
- 锚点与内部跳转：为目标元素设置 id，使用 `href="#id"`，避免 `href="#"` 带来的滚动到顶部

---

## 八、表格与数据展示
- 使用 thead/tbody/tfoot 分隔语义区域
- 使用 `th` 并加 `scope="col"` 或 `scope="row"` 提升可访问性
- 显示大量数据时考虑分页或横向滚动，避免移动端拥挤

示例：
```html
<table>
  <caption>学生成绩表</caption>
  <thead><tr><th scope="col">姓名</th><th scope="col">成绩</th></tr></thead>
  <tbody><tr><td>小明</td><td>90</td></tr></tbody>
</table>
```

---

## 九、表单详解（重要，含可访问性）
### label 与控件关联
- 通过 for/id 或包裹控件
```html
<label for="email">邮箱</label>
<input id="email" type="email">
```

### 常用 input 类型与属性
- text, password, email, tel, number, url, file, checkbox, radio, date
- 验证属性：required, pattern, minlength, maxlength, min, max
- placeholder 仅为提示，不替代 label

### 文件上传与多文件
- `<input type="file" multiple accept="image/*">`

### 可访问性
- 对于复杂控件使用 ARIA（role、aria-label、aria-describedby）并保持语义控件优先

---

## 十、多语言、字符实体与编码
- 使用 UTF-8 编码以避免乱码
- 常见 HTML 实体：&amp;, &lt;, &gt;, &quot;, &nbsp;
- 对于多语言内容在相应块级元素上添加 `lang`，例如 `<p lang="en">Hello</p>`

---

## 十一、可访问性（A11Y）要点
- 使用语义化标签、label、alt、caption、role、aria-* 等
- 管理焦点（tabindex）时慎重，确保键盘用户可以遍历核心互动元素
- 对动态更新内容使用 `aria-live` 来提示屏幕阅读器
- 色彩对比遵循 WCAG 指南

---

## 十二、常见错误、调试技巧与性能
- 常见错误：忘记 `alt`、使用 `href="#"`、缺失 label、错误的相对路径
- 调试技巧：使用浏览器 DevTools 查看 DOM、元素 box model、控制台错误和网络请求
- 性能建议：延迟加载图片（loading="lazy"）、避免大量阻塞脚本、压缩静态资源

---

## 十三、练习题与任务（实战）
1. 30 分钟：构建一个简单的文章页（含 header/nav/article/aside/footer）并确保语义化与可访问性
2. 1 小时：实现响应式图片展示，使用 picture 或 srcset，并保证图片懒加载
3. 半天：实现一个包含表单（邮箱验证、文件上传）和表格的管理页面，并保持可访问性

---

## 十四、课程文件映射（建议学习顺序）
- 基础与语义标签：`01-HTML5语义标签/代码/index.html`
- 图片与路径：`01-HTML5语义标签/代码/09-图像标签.html`、`10-路径.html`
- 多媒体：`01-HTML5语义标签/代码/11-音视频标签.html`
- 表单：`01-HTML5语义标签/代码/18-表单标签.html`

---

附录：常用代码片段
```html
<!-- 安全外链 -->
<a href="https://example.com" target="_blank" rel="noopener noreferrer">示例</a>

<!-- 响应式图片 -->
<picture>
  <source media="(min-width:800px)" srcset="large.jpg">
  <source media="(min-width:400px)" srcset="medium.jpg">
  <img src="small.jpg" alt="描述" loading="lazy">
</picture>
```

---

完成后我会将 `00-StudyLog/index.html` 的 HTML 部分添加指向该附录完整版的链接，并保留精简版 `Log1_HTML5.md` 的卡片。