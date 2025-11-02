# 现代网页布局（复习记录）

> 基于课程资料《现代网页布局》整理，供复习使用。本文档在要点速查、概念详解与实战练习之间取得平衡，便于 10 分钟 / 1 小时 / 半天 不同复习节奏。

更新时间：2025-10-11
来源：课程资料《现代网页布局》（整理）

## 一、本文档目的（简明）
- 提炼现代网页布局核心概念与常见模式，配可复用代码片段与练习。
- 给出排查思路与性能/兼容建议，方便在项目中快速定位与解决布局问题。

## 二、宏观结构（导航）
- 布局模型与 display
- 流式布局与文档流
- 浮动与清除（float / clear）——历史与兼容
- 定位（position）基础：static/relative/absolute/fixed/sticky
- 弹性布局（Flexbox）详解：用法、常见布局、陷阱
- 网格布局（CSS Grid）详解：模板、区域、自动布局
- 响应式布局策略（移动优先、断点、容器查询）
- 常见页面布局模式（Header+Nav+Content+Sidebar+Footer、卡片网格、瀑布流）
- 性能与可访问性注意
- 练习与课程文件映射

## 三、快速记忆卡（核心要点）
- display: block/inline/inline-block/flex/grid/none; flex 与 grid 为现代首选布局方式
- Flex：一维布局（主轴/交叉轴），常用属性：flex-direction, justify-content, align-items, gap, flex
- Grid：二维布局（行/列），核心：grid-template-columns/rows, gap, grid-auto-flow, place-items
- 定位：absolute 从最近定位祖先脱离文档流；sticky 在滚动达到阈值时固定
- 浮动常用于文字环绕与老布局，配合 clear 清除浮动
- 响应式：移动优先（先写基础），常用单位 rem/vw/vh，函数 clamp()、min()/max()

## 四、详细内容与示例

### 1. 文档流与 display
- 文档流：块级元素垂直排列，内联元素水平排列。改变 display 可改变布局行为。
- inline-block 可以像 inline 一样排列但可设置宽高。

示例：
```html
<div class="card">...</div>
<span class="badge">New</span>
```

### 2. 浮动（float）与清除（clear）
- float:left/right 将元素从文档流中部分脱离，常伴随文字环绕。
- 清除方法：使用 `.clearfix`（伪元素）或父元素 `overflow:auto` / `display:flex`。

clearfix 示例：
```css
.clearfix::after { content: ""; display: block; clear: both; }
```

注意：浮动会影响父容器高度，需清除以避免布局崩塌。

### 3. 定位（position）
- static（默认）、relative（相对定位，不脱离文档流）、absolute（绝对定位，脱离并以最近定位祖先为参考）、fixed（相对视窗）、sticky（在阈值吸附）

示例：
```css
.parent { position: relative; }
.child { position: absolute; top: 10px; right: 10px; }
```

陷阱：绝对定位会使元素不参与文档流，可能覆盖其他元素。

### 4. Flexbox（深入）
- 核心概念：主轴与交叉轴，容器决定主轴方向
- 容器常用属性：
  - display: flex
  - flex-direction: row|row-reverse|column|column-reverse
  - justify-content: flex-start|center|space-between|space-around|space-evenly
  - align-items: stretch|flex-start|center|baseline|flex-end
  - gap: 控制间距（现代浏览器支持）
- 子项常用属性：
  - flex: shorthand for flex-grow flex-shrink flex-basis (例如 flex:1 1 0)
  - order: 改变视觉顺序

常见布局：水平居中与垂直居中
```css
.container { display:flex; justify-content:center; align-items:center; }
```

等分列：
```css
.item { flex: 1; }
```

响应式换行：
```css
.container { display:flex; flex-wrap:wrap; gap:16px; }
```

性能提示：避免在大量元素上频繁修改样式，尽量动画 transform/opacity。

### 5. CSS Grid（深入）
- 语义：用于二维布局，能精准控制行列与区域
- 基本语法：
  - grid-template-columns: 定义列轨道，例如 `1fr 2fr` 或 `repeat(3, 1fr)`
  - grid-template-rows
  - gap: 行列间隙
  - grid-auto-flow: 控制自动放置的方向

示例：两栏布局
```css
.container { display:grid; grid-template-columns: 250px 1fr; gap:16px; }
```

响应式自动填充：
```css
.container { display:grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap:12px; }
```

命名区域：
```css
.grid { grid-template-areas: "header header" "sidebar main" "footer footer"; }
.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
```

注意：Grid 中也应保持 DOM 顺序的语义，避免仅通过视觉重排传达重要信息。

### 6. 常见页面布局模式
- 经典结构：Header + Nav + Content + Sidebar + Footer
- 卡片网格：使用 Grid 或 Flex 实现响应式卡片布局
- 瀑布流（masonry）：原生 CSS 解决方案有限，可用 JS 或 column 布局、或 Grid + JS 补充

### 7. 响应式策略
- 移动优先：先写基础样式（手机），再通过 `@media (min-width: ...)` 逐步增强
- 断点：根据设计和内容设置常用断点（例如 480/768/1024/1200）而非完全依赖设备
- 单位：rem 用于一致排版；vw 用于流式宽度；clamp() 用于限制范围

### 8. 可访问性与布局
- 确保焦点顺序符合逻辑（DOM 顺序）
- 大屏视觉重排不应影响键盘导航顺序
- 提高对比度并为互动元素提供明显焦点样式

### 9. 调试技巧
- 在 DevTools 中使用元素面板查看 box model（padding/margin/border）
- 利用 outline 或临时背景颜色快速定位元素
- 检查 computed styles 与 layout 报表找出重排/重绘触发点

## 五、练习（10 分钟 / 1 小时 / 半天）
1. 10 分钟：用 Flex 实现一个水平导航栏并垂直居中
2. 1 小时：用 Grid 实现一个响应式两列→单列的文章布局（左侧 sidebar + 右侧 content）
3. 半天：实现一个响应式卡片网格，带懒加载图片、hover 动效与主题变量（CSS custom properties）

## 六、课程文件映射（建议顺序）
- `03-现代网页布局/代码/01-display显示模式转换.html` — display 与基本示例
- `03-现代网页布局/代码/02-浮动.html` — 浮动与清除示例
- `03-现代网页布局/代码/03-清除浮动.html` — 清除浮动技巧
- `03-现代网页布局/代码/04-弹性布局示例.html` — Flex 练习
- `03-现代网页布局/代码/05-弹性布局-容器flex.html` — Flex 容器属性
- `03-现代网页布局/代码/06-弹性布局-主轴对齐.html` — 对齐实例
- `03-现代网页布局/代码/07-弹性布局-交叉轴对齐.html` — 交叉轴对齐
- `03-现代网页布局/代码/08-兄弟选择器.html` — 选择器补充
<!-- - 这里文件映射已经在乱说了，最后一个 -->

## 七、常见陷阱速查（快速定位）
- 父元素高度为 0：可能是子元素浮动未被清除
- 绝对定位元素遮挡：检查 z-index 与定位上下文
- flex 项目过度伸展：检查 flex-basis 与 min-width
- grid 自动放置与溢出：检查 grid-auto-flow 与 grid-auto-rows

## 八、复习计划建议
- 每周 30 分钟：翻看速查卡 + 做 1 个 10 分钟任务
- 每两周 1 小时：做 1 个 1 小时任务并记录问题
- 每月 半天：完成一个综合练习（卡片网格或响应式文章页），并用 CSS 变量优化样式

---

如需，我可以：
- 将这份笔记加入 `00-StudyLog/index.html`（现代网页布局部分）的笔记卡并指向对应附录或主笔记；
- 生成 PDF 导出；
- 继续把每个练习链接到具体课程示例文件（并在笔记中加入一键打开路径）。
