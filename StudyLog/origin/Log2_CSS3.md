# CSS3 核心知识复习记录

> 基于课程资料（CSS3核心技术）整理，供复习使用。本文档以要点、速查、常见错误、练习与复习计划为主，便于短时间回顾与实战演练。

## 一、本文档目的（2句）
- 把教材中的核心概念与常用模式提炼成可复用笔记，便于 10 分钟、1 小时、1 天三种复习节奏。
- 提供实战练习与常见陷阱提醒，帮助把理论转为可复习的技能点。

## 二、宏观结构（让你知道去哪里学什么）
- 选择器与优先级（选择元素、组合、属性选择器、伪类/伪元素）
- 盒模型与布局基础（box-sizing、margin、padding、border）
- 现代布局（flex、grid）
- 可视化与美化（背景、渐变、阴影、圆角）
- 文本与字体（web fonts、行高、文字溢出）
- 响应式与单位（media query、rem/em、vw/vh）
- 动画与过渡（transition、transform、animation）
- 高级功能（滤镜、变量 CSS custom properties、calc、clip-path）
- 性能、兼容性与无障碍（性能优化、前缀、可访问性）

## 三、核心概念速查（快速记忆卡）
### 选择器与优先级
- 常用选择器：元素、类（.cls）、id（#id）、属性（[type="text"]）、后代（A B）、子代（A > B）、相邻兄弟（A + B）、通用兄弟（A ~ B）。
- 伪类/伪元素：`:hover`、`:active`、`:focus`、`:nth-child()`、`::before`、`::after`。
- 优先级：内联样式(1000) > id(100) > class/attribute/pseudo-class(10) > element/pseudo-element(1)。重要：!important 会覆盖正常优先级（慎用）。

### 盒模型
- box-sizing: content-box（默认）/ border-box（推荐，计算宽度包含 padding 和 border）。
- margin collapse（外边距塌陷）：相邻块级元素的垂直 margin 可能合并。

### 布局
- display: block/inline/inline-block/flex/grid/none。理解它们如何影响流布局。
- Flex（容器属性）：display:flex; flex-direction; justify-content; align-items; flex-wrap; gap; 子项：flex: 0 1 auto / flex: 1 等。
- Grid：display:grid; grid-template-columns/rows; gap; grid-auto-flow; place-items; grid-area。

### 文本与字体
- font-family、font-size、line-height（可使用无单位值使行高按字体大小缩放）
- 单位：px、em（相对于父元素字体）、rem（相对于根元素）、%（依赖上下文）、vw/vh（视窗）
- 文本溢出：white-space、overflow、text-overflow: ellipsis（配合单行/块级宽度）

### 背景与装饰
- background-image (url, linear-gradient, radial-gradient), background-position, background-size (cover/contain)
- border-radius, box-shadow
- 多背景：支持逗号分隔多个 background-layer

### 过渡与动画
- transition: property duration timing-function delay
- transform: translate/scale/rotate/skew（合并在 transform 中以提高性能）
- animation: @keyframes + animation-name/duration/iteration/timing-function/fill-mode
- 性能提示：尽量只动画 transform 与 opacity，避免布局触发（layout thrash）

### 响应式与媒体查询
- 常用写法：@media (max-width: 768px) { ... }
- 移动优先：先写基础样式（手机），再使用 min-width 增强

### CSS 变量（Custom Properties）
- 声明：:root { --main-color: #09f; }
- 使用：color: var(--main-color, #000);（可带 fallback）
- 变量是动态的，可在运行时通过 JS 修改，常用于主题色/间距规范化

### 常用函数
- calc(), clamp(), min(), max()
- 使用场景：响应式尺寸、固定最小/最大值

## 四、常见错误与陷阱（考试/实战高频）
- 忘记加 box-sizing: border-box 导致 width 计算混乱
- text-overflow: ellipsis 需要 white-space: nowrap + overflow: hidden
- 垂直居中理解错误：flex 容器是首选，旧方法有 line-height/transform 等技巧
- 优先级没搞清楚导致样式不生效：检查是否有更高优先级选择器或 !important
- 使用百分比高度时父元素无高度，导致子元素无效
- 动画卡顿：动画触发布局（例如改变 width/top）而非 transform/opacity

## 五、快速练习（把知识变成肌肉记忆）
1. 10 分钟任务（回顾）
   - 列出 5 个常用选择器和各自用例
   - 写出 flex 容器的 3 个常见对齐组合
   - 在 1 个 div 上实现圆角、阴影与背景渐变

2. 1 小时任务（动手）
   - 重做一个小卡片组件：图片、标题、描述、底部按钮，使用 flex 布局与 box-shadow
   - 添加 hover 过渡效果（scale 与 shadow 变化）
   - 使用 media query 使卡片在小屏变为单列

3. 半天到 1 天任务（深入）
   - 用 CSS Grid 实现一个响应式两栏→单栏布局
   - 用 @keyframes 做一个小型 loading 动画
   - 用 CSS 变量与 calc() 做一个主题切换（浅色/深色）示例

## 六、代码片段（常用模板，拷贝即用）
单行省略号：
```css
.ellipsis { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
```
flex 常用：
```css
.container { display: flex; gap: 12px; align-items: center; justify-content: space-between; }
.item { flex: 1 1 auto; }
```
响应式媒体查询（移动优先）：
```css
/* 手机基础样式 */
.card { width: 100%; }
@media (min-width: 768px) {
  .card { width: 48%; }
}
```
CSS 变量示例：
```css
:root { --gap: 16px; --bg: linear-gradient(90deg, #fff, #f0f0f0); }
.container { gap: var(--gap); background: var(--bg); }
```

## 七、与课程练习文件的映射（建议复习顺序）
- 先看 `02-CSS3核心技术/代码/index.html` 与 `my.js`（整体示例、演示脚本）
- 按主题看对应练习文件：
  - 盒模型/布局：`06-页面基本布局.html`, `23-盒子模型-边框设置.html` 等
  - 背景/渐变/阴影：`30-盒子背景.html`, `32-背景渐变.html`, `34-盒子阴影.html`
  - 文本/字体：`10-字体样式.html`, `11-文本布局.html`
  - 伪类/伪元素：`20-伪元素选择器.html`, `14-链接伪类选择器.html`
  - 综合案例：`36-盒子模型综合案例-小米卡片.html`（推荐做一遍）

## 八、复习计划（建议周期化）
- 每周（30 分钟）：翻看速查卡 + 完成 1 个 10 分钟练习
- 每两周（2 小时）：做 1 个 1 小时任务并写下遇到的问题与解法
- 每月（半天）：完整重做一个综合案例（例如卡片、导航或响应式页面）并用 CSS 变量重构样式

## 九、检测题（自测）
1. 什么情况下会发生 margin collapse？如何避免？
2. 写出使用 flex 实现垂直水平居中的最简 CSS。
3. text-overflow: ellipsis 要满足哪些条件？
4. 请说明使用 transform 与 top/left 动画性能差异及原因。

## 十、笔记收尾 — 复习小贴士
- 学 CSS 最好是“看—做—回顾”：看例子理解语义，做练习把 API 用起来，回顾把常见错误固化成经验。
- 使用浏览器开发者工具实时调试样式（右键→检查），调节样式、查看布局边界和渲染顺序。
- 把常用模板（如响应式栅格、卡片、导航）存为 snippets，复习时直接复用并改造。

---

更新时间：2025-10-09
来源：课程资料《CSS3核心技术》（整理）

文件关联：若你想把这份笔记并入 `00-StudyLog/index.html` 或导出为 PDF，告诉我我来帮你生成。
