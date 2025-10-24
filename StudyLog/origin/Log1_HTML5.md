# HTML5 核心知识复习记录

> 基于现有课程笔记整理，供快速复习与实战演练使用。本文档去掉了开发准备部分，重点聚焦 HTML 语义、常用标签、易错点与练习。

## 一、本文档目的（2句）
- 将 HTML5 的核心概念、常见用法与高频错误提炼为便于回顾的速查卡。
- 提供实战练习与复习计划，帮助在短时间内巩固并应用知识。

## 二、宏观结构（快速导航）
- 文档结构与 meta（DOCTYPE、lang、charset、viewport）
- 标签语义与关系（块级/内联、嵌套规则）
- 常用元素速查（标题、段落、图片、表格、表单、链接、列表）
- 多媒体（audio、video）
- 可访问性与语义化要点（label、alt、aria）
- 常见错误与陷阱
- 练习与复习计划

## 三、核心概念速查（记忆卡）
### 文档骨架（必背）
- 最简模板：
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>页面标题</title>
</head>
<body>

</body>
</html>
```
- 要点：doctype 声明、`lang` 用于可访问性与搜索，`charset` 防止乱码，`viewport` 适配移动端。

### 标签语义与层次
- 块级元素（例如 `div`, `p`, `h1-h6`, `ul`, `ol`, `section`, `article`）：独占一行、可包含内联元素。
- 内联元素（例如 `span`, `a`, `strong`, `em`, `img`）：不独占行，适合局部标记。
- 规则：`p` 不应包含块级元素；语义化优先于样式（用 `header`, `nav`, `main`, `footer` 替代纯 `div`）。

### 常用元素速查
- 标题：`<h1>` 每页尽量唯一，语义化层级控制重要性。
- 段落：`<p>` 表示语义段落。
- 链接：`<a href="..." target="_blank" rel="noopener">`（外链加 `rel`）
- 图片：`<img src="..." alt="描述" title="提示">`（`alt` 必填，提升可访问性）
- 列表：`ul/ol + li`；`dl/dt/dd` 用于术语-描述对。
- 表格：`table` + `thead/tbody/tfoot`；`th` 用于表头，考虑 `scope` 属性提升可访问性。
- 表单控件：`label` 关联 `for` + `id` 或**包裹控件**；常用 `input` 类型：text/password/email/file/checkbox/radio；`textarea`、`select`。

### 多媒体
- Video 示例：
```html
<video controls poster="preview.jpg">
  <source src="video.mp4" type="video/mp4">
  <p>浏览器不支持视频标签</p>
</video>
```
- Audio：主流使用 `mp3`，同样建议加 `controls`。
- 自动播放注意：多数浏览器仅允许静音自动播放（`muted`）。

### 无障碍和语义化要点
- `alt` 描述图片内容或功能；装饰性图片可用 `alt=""`。
- `label` 提高表单可用性，辅助键盘操作。
- 对重要交互元素使用 `role`/`aria-*` 属性以改善屏幕阅读器体验。

## 四、常见错误与陷阱（高频）
- 忘记设置 `meta charset` 导致中文乱码。
- `href="#"` 未阻止默认行为会滚动到顶部（用 `javascript:void(0)` 或 `href="#id"`）。
- 图片缺少 `alt`，影响无障碍与 SEO。
- `p` 内嵌块级元素（例如直接放 `div`），会导致语义错误与渲染差异。
- 表单未使用 `label`，影响可用性；未指定 `type=email`/`type=tel` 等降低移动端体验。
- 锚点链接路径错误：相对路径基于当前 HTML 文件位置，容易出错。

## 五、快速练习（把知识变成肌肉记忆）
1. 10 分钟任务
   - 写出最简 HTML 模板并解释每个 meta 的作用。
   - 为一张图片写合适的 `alt` 文本（场景：产品展示图）。

2. 1 小时任务
   - 做一个包含导航（ul/li）、主体（article）、侧边栏（aside）和页脚（footer）的简单页面。
   - 为表单添加 `label`，实现基本校验（HTML 属性如 `required`, `type=email`）。

3. 半天任务
   - 实现一个长文章页，添加锚点目录（toc）、平滑滚动与可访问性优化（焦点样式）。

## 六、代码片段（常用模板，拷贝即用）
- 基本链接（外链新窗口、安全写法）：
```html
<a href="https://example.com" target="_blank" rel="noopener">外部链接</a>
```
- 图片（装饰性 vs 内容性）：
```html
<!-- 装饰性图片 -->
<img src="decoration.png" alt="">
<!-- 内容图片 -->
<img src="product.jpg" alt="黑色运动鞋，男款，尺码 42">
```
- 表单 label 示例：
```html
<label for="email">邮箱</label>
<input id="email" type="email" required>
<!-- 或包裹方式 -->
<label><input type="radio" name="sex"> 男</label>

```

## 七、与课程文件的映射（建议复习顺序）
- 先看 `01-HTML5语义标签/代码/index.html`（入门示例）
- 图片与路径练习：`01-HTML5语义标签/代码/09-图像标签.html`、`10-路径.html`
- 多媒体：`01-HTML5语义标签/代码/11-音视频标签.html`
- 表单：`01-HTML5语义标签/代码/18-表单标签.html`

## 八、复习计划（建议周期）
- 每周 30 分钟：翻看速查卡 + 1 个 10 分钟练习
- 每两周 1-2 小时：做 1 个 1 小时任务并记录遇到的问题
- 每月 1 次：用语义化重构一个已有页面

## 九、自测题
1. 写出最简 HTML5 模板并解释 `viewport` 的作用。
2. 为什么要为图片添加 `alt`？什么时候可以留空 `alt`？
3. 如何让表单控件对屏幕阅读器更友好？

## 十、复习小贴士
- 阅读时优先关注语义和可访问性而不是外观样式。
- 使用浏览器的“检查”工具实时查看 DOM 结构与属性。
- 把常用结构（模板、导航、表单）保存为 snippets 以便复用。

---

更新时间：2025-10-09
来源：课程资料《HTML5 核心知识点复习笔记》（整理）
