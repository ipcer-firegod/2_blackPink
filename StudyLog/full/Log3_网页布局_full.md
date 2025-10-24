# 现代网页布局核心知识学习笔记
## 一、CSS 布局体系总览
CSS 布局是控制元素在页面中排列的核心技术，基于「正常布局流（标准流）」衍生出多种布局方式，每种方式有明确适用场景，需根据需求灵活选择：

| 布局类型       | 核心特点                                  | 适用场景                                  |
|----------------|-------------------------------------------|-------------------------------------------|
| 正常布局流     | 块级元素垂直排列、行内元素水平排列          | 基础文档结构（如上下排列的段落、标题）      |
| 模式转换（display） | 改变元素默认显示模式                      | 简单同行排列（如按钮组、小图标）            |
| 浮动布局（float） | 元素脱离文档流，左右浮动                  | 早期图文环绕、简单同行布局（现多被 flex 替代） |
| 弹性布局（flex）  | 一维布局（水平/垂直单方向），灵活对齐      | 导航栏、卡片布局、表单对齐（最常用）        |
| 定位布局（position） | 元素脱离/不脱离文档流，精准控制位置        | 弹窗、固定导航、吸顶效果、悬浮元素          |
| 网格布局（grid）  | 二维布局（同时控制行和列），复杂结构适配    | 页面框架、响应式多列布局、不规则分栏        |
| 多列布局（column） | 文本自动分栏，模拟报纸排版                | 长文章分栏、图片瀑布流（简单场景）          |


## 二、基础：正常布局流与模式转换
### 1. 正常布局流（Normal Flow）
- **核心规则**：浏览器默认的元素排列方式，是所有布局的基础：
  - 块级元素（如 `div`、`p`、`h1`）：独占一行，宽度默认撑满父容器，垂直排列。
  - 行内元素（如 `span`、`a`、`img`）：水平排列，宽度/高度由内容决定，超出父容器自动换行。
  - 文档流方向：默认「从上到下、从左到右」。


### 2. display 模式转换（改变元素默认显示）
通过 `display` 属性修改元素的显示模式，解决“块级元素同行排列”“行内元素设宽高”的需求：

| `display` 值     | 是否独占一行 | 能否设置宽高 | 默认宽度         | 核心场景                                  | 注意事项                                  |
|------------------|--------------|--------------|------------------|-------------------------------------------|-------------------------------------------|
| `block`          | 是           | 是           | 撑满父容器       | 需独占一行的容器（如卡片、导航栏）          | -                                        |
| `inline`         | 否           | 否           | 由内容决定       | 文本内局部元素（如高亮文本）                | 不可直接设宽高，垂直边距无效                |
| `inline-block`   | 否           | 是           | 由内容决定       | 同行且需设宽高的元素（如按钮、小图标）      | 元素间默认有空白缝隙（父元素设 `font-size: 0` 可消除） |

- **示例**：实现按钮同行排列（避免空白缝隙）：
  ```css
  .btn-group {
    font-size: 0; /* 消除 inline-block 空白缝隙 */
  }
  .btn {
    display: inline-block;
    width: 100px;
    height: 40px;
    font-size: 16px; /* 恢复按钮文本字号 */
  }
  ```


## 三、浮动布局（Float）
### 1. 浮动的核心特性
- **作用**：早期用于“图文环绕”，现多用于兼容旧浏览器的简单同行布局。
- **属性值**：
  - `left`：元素向左浮动，直到碰到父容器边缘或其他浮动元素。
  - `right`：元素向右浮动。
  - `none`：默认值，不浮动。
- **关键特点**：
  - 元素**脱离文档流**：不占据原位置，后续标准流元素会“向上填充”。
  - 浮动元素默认收缩为内容宽度（需手动设宽高）。


### 2. 浮动的问题与清除浮动
#### （1）浮动带来的问题
1. 父容器高度塌陷：浮动子元素不占空间，父容器若未设高度，会收缩为 0。
2. 影响后续布局：标准流元素被浮动元素覆盖或挤压。

#### （2）清除浮动的 4 种方法（核心必掌握）
| 方法               | 实现方式                                                                 | 优缺点                                  | 适用场景                  |
|--------------------|--------------------------------------------------------------------------|-----------------------------------------|---------------------------|
| 额外标签法         | 在最后一个浮动元素后添加块级标签（如 `<div style="clear: both;"></div>`）   | 简单直观；增加无意义标签                | 简单demo、快速调试        |
| 单伪元素法（京东） | 父容器添加类 `.clearfix`，通过伪元素清除浮动：<br>`.clearfix::after { content: "."; display: block; clear: both; visibility: hidden; height: 0; }` | 无多余标签；兼容旧浏览器                | 项目通用                  |
| 双伪元素法（小米） | 父容器添加类 `.clearfix`：<br>`.clearfix::before, .clearfix::after { content: ""; display: table; }` <br>`.clearfix::after { clear: both; }` | 兼顾清除浮动和解决margin塌陷；代码简洁  | 推荐，项目首选            |
| overflow 法        | 父容器设置 `overflow: hidden` 或 `auto`                                  | 代码最少；可能隐藏溢出内容              | 浮动元素无溢出需求的场景  |

- **示例（双伪元素法）**：
  ```css
  .clearfix::before,
  .clearfix::after {
    content: "";
    display: table; /* 触发BFC，解决margin塌陷 */
  }
  .clearfix::after {
    clear: both; /* 清除浮动 */
  }
  /* 使用：给父容器加 .clearfix 类 */
  <div class="parent clearfix">
    <div class="child" style="float: left;"></div>
  </div>
  ```


## 四、弹性布局（Flexbox）—— 一维布局核心
Flex 是**一维布局模型**（仅控制水平或垂直单方向），通过“父容器控制子项目”实现灵活对齐，是目前开发中最常用的布局方式。


### 1. Flex 核心概念
- **容器与项目**：
  - 容器：设置 `display: flex` 的父元素，控制子项目排列。
  - 项目：容器的直接子元素，受容器属性控制。
- **主轴与交叉轴**：
  - 主轴：默认水平方向（从左到右），由 `flex-direction` 控制方向。
  - 交叉轴：与主轴垂直，默认垂直方向（从上到下）。


### 2. 容器属性（父控子的核心）
| 属性                | 作用                                  | 常用取值及效果                                                                 | 示例代码                                  |
|---------------------|---------------------------------------|------------------------------------------------------------------------------|-------------------------------------------|
| `display`           | 定义容器为 Flex 布局                  | `flex`（块级容器）、`inline-flex`（行内容器）                                  | `.container { display: flex; }`            |
| `flex-direction`    | 控制主轴方向                          | `row`（默认，水平从左到右）、`row-reverse`（水平从右到左）、`column`（垂直从上到下）、`column-reverse`（垂直从下到上） | `.container { flex-direction: column; }`   |
| `flex-wrap`         | 控制项目是否换行                      | `nowrap`（默认，不换行，项目可能压缩）、`wrap`（换行，第一行在上）、`wrap-reverse`（换行，第一行在下） | `.container { flex-wrap: wrap; }`          |
| `justify-content`   | 主轴上项目的对齐方式                  | `flex-start`（左对齐）、`flex-end`（右对齐）、`center`（居中）、`space-between`（两端对齐，项目间无间隙）、`space-around`（项目两侧间隙相等）、`space-evenly`（项目间及与边界间隙相等） | `.container { justify-content: space-between; }` |
| `align-items`       | 交叉轴上**单行项目**的对齐方式        | `flex-start`（上对齐）、`flex-end`（下对齐）、`center`（居中）、`stretch`（默认，项目拉伸填满交叉轴，需项目无固定高度） | `.container { align-items: center; }`      |
| `align-content`     | 交叉轴上**多行项目**的对齐方式（需换行）| 取值同 `justify-content`，仅 `flex-wrap: wrap` 时生效                          | `.container { align-content: center; }`    |
| `gap`               | 控制项目间的间距（行+列）            | `gap: 10px`（行/列间距均为10px）、`gap: 10px 20px`（行10px，列20px）            | `.container { gap: 16px; }`               |


### 3. 项目属性（子元素自身控制）
| 属性                | 作用                                  | 常用取值及效果                                                                 | 示例代码                                  |
|---------------------|---------------------------------------|------------------------------------------------------------------------------|-------------------------------------------|
| `flex-grow`         | 项目的放大比例（剩余空间分配）        | 默认 `0`（不放大）；`1` 表示占1份剩余空间，`2` 占2份（同容器内项目按比例分配） | `.item { flex-grow: 1; }`                 |
| `flex-shrink`       | 项目的缩小比例（空间不足时）          | 默认 `1`（等比缩小）；`0` 表示不缩小（固定尺寸）                               | `.item { flex-shrink: 0; }`               |
| `flex-basis`        | 项目在主轴上的初始尺寸                | 默认 `auto`（由内容决定）；`200px` 表示初始宽度200px（优先级高于 `width`）     | `.item { flex-basis: 200px; }`            |
| `flex`              | 上述三者的简写                        | `flex: 1` → `1 1 auto`（等比放大/缩小）；`flex: 0 0 200px` → `0 0 200px`（不放大不缩小，固定200px） | `.item { flex: 1; }`                     |
| `order`             | 项目的排列顺序                        | 默认 `0`，数值越小越靠前（可负）                                             | `.item { order: -1; }`                    |
| `align-self`        | 单独覆盖容器的 `align-items`          | 取值同 `align-items`，仅作用于当前项目                                      | `.item { align-self: center; }`           |


### 4. Flex 实战技巧（小兔鲜案例提炼）
1. **公共样式拆分**：将复用样式（如单行溢出省略号）封装为类，提高复用性：
   ```css
   .ellipsis {
     white-space: nowrap;
     overflow: hidden;
     text-overflow: ellipsis;
   }
   ```
2. **Logo 优化**：用 `h1` 提升 SEO 权重，背景图显示 Logo，文本缩进隐藏：
   ```css
   .logo {
     width: 120px;
     height: 40px;
     background: url(logo.png) no-repeat;
     text-indent: -9999px; /* 隐藏文本 */
     overflow: hidden;
   }
   ```
3. **垂直居中**：容器设 `display: flex` + `align-items: center`，轻松实现单行项目垂直居中（无需计算行高）。


## 五、定位布局（Position）—— 精准控制位置
定位布局通过 `position` 属性让元素脱离或不脱离文档流，实现“悬浮、固定、层叠”等特殊效果，核心是“定位基准”和“偏移控制”。


### 1. 四种定位类型对比
| 定位类型       | 脱离文档流 | 定位基准                          | 核心属性（偏移）       | 典型场景                                  |
|----------------|------------|-----------------------------------|------------------------|-------------------------------------------|
| `static`       | 否         | 默认文档流（无定位）              | 无（top/right等无效）  | 普通元素（默认）                          |
| `relative`     | 否         | 元素自身的正常位置                | top/right/bottom/left   | 微调元素位置、给绝对定位做“父容器”（子绝父相） |
| `absolute`     | 是         | 最近的已定位祖先（非static）；无则为视口 | top/right/bottom/left   | 弹窗、下拉菜单、悬浮提示、子元素悬浮父元素 |
| `fixed`        | 是         | 浏览器视口（滚动时位置不变）      | top/right/bottom/left   | 固定导航栏、返回顶部按钮、全屏广告        |
| `sticky`       | 否         | 视口或滚动祖先（滚动到阈值后固定） | top/right/bottom/left   | 吸顶导航栏、表格表头固定                  |

常见组合：
- 固定导航栏：`position: fixed + z-index `
- 弹窗：`position: fixed + 居中技巧 + 高z-index`
- 吸顶效果：`position: sticky + top: 0`

注意，某些定位必须使用 `top/right/bottom/left` 之一才能生效（如 `absolute`、`fixed`、`sticky`），否则元素会回到默认位置。

### 2. 核心技巧：子绝父相（最常用组合）
#### （1）原理
- 子元素 `position: absolute`：脱离文档流，不占空间，可悬浮在父元素上方。
- 父元素 `position: relative`：不脱离文档流，保留原位置，作为子元素的定位基准（避免子元素相对于视口定位）。

#### （2）示例：子元素悬浮在父元素右上角
```html
<div class="parent" style="position: relative; width: 300px; height: 200px;">
  <div class="child" style="position: absolute; top: 10px; right: 10px; width: 50px; height: 50px;"></div>
</div>
```

#### （3）绝对定位垂直居中
方法1：`top: 50%` + `margin-top: -自身高度一半`（需知自身高度）：
```css
.child {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 200px;
  height: 100px;
  margin-top: -50px; /* 自身高度的一半 */
  margin-left: -100px; /* 自身宽度的一半 */
}
```
方法2：`top: 50%` + `transform: translate(-50%, -50%)`（无需知自身高度，推荐）：
```css
.child {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
```


### 3. 层叠顺序（z-index）
- **作用**：控制定位元素（relative/absolute/fixed/sticky）的层叠优先级，数值越大越靠上。
- **规则**：
  - 默认值 `auto`（等同于 0，后定义的元素覆盖前者）。
  - 仅对定位元素生效。
  - 父元素 z-index 不影响子元素（子元素可突破父元素层级）。
- **示例**：弹窗层级高于背景遮罩：
```css
.mask { z-index: 10; } /* 背景遮罩 */
.modal { z-index: 20; } /* 弹窗（层级更高） */
```


## 六、网格布局（Grid）—— 二维布局核心
Grid 是**二维布局模型**（同时控制行和列），适合复杂页面框架（如多列响应式布局、不规则分栏），灵活性远超 Flex。


### 1. Grid 核心概念
- **容器与项目**：容器设 `display: grid`，直接子元素为项目。
- **网格轨道**：行轨道（row）和列轨道（column），构成网格的“行高”和“列宽”。
- **网格线**：划分轨道的线（3列有4根列线，3行有4根行线，从1开始编号）。
- **单元格**：行轨道与列轨道交叉形成的区域（项目默认占1个单元格）。


### 2. 容器属性（核心）
| 属性                | 作用                                  | 常用取值及效果                                                                 | 示例代码                                  |
|---------------------|---------------------------------------|------------------------------------------------------------------------------|-------------------------------------------|
| `display`           | 定义容器为 Grid 布局                  | `grid`（块级容器）、`inline-grid`（行内容器）                                  | `.container { display: grid; }`            |
| `grid-template-columns` | 定义列轨道（列宽）                  | 固定值（`100px 200px`，2列）、百分比（`30% 70%`）、`fr`单位（`1fr 2fr`，剩余空间按比例分配）、`repeat`函数（`repeat(3, 1fr)`，3列等宽）、`minmax`函数（`minmax(200px, 1fr)`，列宽最小200px，最大1fr） | `.container { grid-template-columns: repeat(3, 1fr); }` |
| `grid-template-rows`    | 定义行轨道（行高）                  | 取值同 `grid-template-columns`（可省略，默认1行，高度由内容决定）              | `.container { grid-template-rows: 100px 200px; }` |
| `justify-content`   | 轨道在容器中的水平对齐（轨道总宽 < 容器宽） | 同 Flex 的 `justify-content`（`center`、`space-between` 等）                  | `.container { justify-content: center; }`  |
| `align-content`     | 轨道在容器中的垂直对齐（轨道总高 < 容器高） | 同 Flex 的 `align-content`                                                  | `.container { align-content: center; }`    |
| `justify-items`     | 项目在单元格中的水平对齐              | `stretch`（默认，拉伸填满）、`start`（左对齐）、`center`（居中）、`end`（右对齐） | `.container { justify-items: center; }`    |
| `align-items`       | 项目在单元格中的垂直对齐              | 同 `justify-items`                                                          | `.container { align-items: center; }`      |
| `gap`               | 轨道间的间距（行+列）                | `gap: 10px`（行/列间距均10px）、`gap: 10px 20px`（行10px，列20px）            | `.container { gap: 16px; }`               |
| `grid-auto-flow`    | 项目的填充顺序                        | `row`（默认，先行后列）、`column`（先列后行）                                  | `.container { grid-auto-flow: column; }`   |


### 3. 项目属性（核心）
| 属性                | 作用                                  | 常用取值及效果                                                                 | 示例代码                                  |
|---------------------|---------------------------------------|------------------------------------------------------------------------------|-------------------------------------------|
| `grid-column`       | 控制项目跨列（基于网格线）            | `1 / 3`（从第1列线到第3列线，跨2列）、`1 / span 2`（从第1列线开始，跨2列）     | `.item { grid-column: 1 / 3; }`            |
| `grid-row`          | 控制项目跨行（基于网格线）            | 取值同 `grid-column`                                                          | `.item { grid-row: 1 / span 2; }`          |
| `align-self`        | 单独覆盖容器的 `align-items`          | 同 Flex 的 `align-self`                                                      | `.item { align-self: center; }`            |


### 4. Grid 响应式布局（核心实战）
通过 `repeat(auto-fill, minmax(210px, 1fr))` 实现“列数随容器宽度自动调整”，无需媒体查询：
```css
.container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(210px, 1fr)); /* 列宽最小210px，自动填充列数 */
  gap: 16px;
}
```
- **效果**：容器变宽时自动增加列数，变窄时自动减少列数，适配所有屏幕尺寸。


## 七、多列布局（Column）
### 1. 核心作用
将文本或元素自动分割为垂直列，模拟报纸排版，适合长文章分栏或简单瀑布流。

### 2. 核心属性
| 属性                | 作用                                  | 示例代码                                  |
|---------------------|---------------------------------------|-------------------------------------------|
| `column-count`       | 定义分栏数量                          | `.article { column-count: 3; }`（分3栏） |
| `column-gap`         | 定义栏间间距                          | `.article { column-gap: 20px; }`         |
| `column-rule`       | 定义栏间分隔线（宽度+样式+颜色）      | `.article { column-rule: 1px solid #ccc; }` |

### 3. 解决子元素跨列切断
默认情况下，子元素可能被分割到两栏，通过 `break-inside: avoid-column` 强制元素不跨列：
```css
.article .card {
  break-inside: avoid-column; /* 卡片不跨列 */
}
```


## 八、其他实用知识点
### 1. 鼠标样式（cursor）
通过 `cursor` 改变鼠标指针形态，提升交互体验：
| 取值          | 效果                                  | 适用场景                                  |
|---------------|---------------------------------------|-------------------------------------------|
| `default`     | 默认箭头                              | 普通元素                                  |
| `pointer`     | 手型（指尖朝下）                      | 可点击元素（链接、按钮）                  |
| `text`        | 文本光标（竖线）                      | 可编辑文本（输入框、文本域）              |
| `wait`        | 等待（旋转圆圈）                      | 加载中、提交中                            |
| `not-allowed` | 禁止（圆圈带斜线）                    | 禁用按钮、不可操作元素                    |
| `zoom-in`/`zoom-out` | 放大/缩小（+/-）                  | 图片预览放大/缩小                          |


### 2. CSS 书写顺序（规范）
遵循“布局→盒模型→视觉→交互→其他”逻辑，提高代码可读性：
1. **布局相关**：`display`、`position`、`float`、`overflow`、`z-index`。
2. **盒模型相关**：`box-sizing`、`width`/`height`、`margin`、`padding`、`border`。
3. **视觉样式**：`color`、`background`、`font`、`line-height`、`text-align`。
4. **交互与动画**：`cursor`、`transition`、`animation`、`transform`。
5. **其他**：`filter`、`clip-path`、`scroll-behavior`。


## 九、布局选择指南
| 需求场景                  | 推荐布局          | 理由                                  |
|---------------------------|-------------------|---------------------------------------|
| 导航栏、表单对齐、单行卡片 | Flex              | 一维布局，对齐灵活，代码简洁          |
| 页面框架、多列响应式、不规则分栏 | Grid            | 二维布局，控制行和列，适配复杂结构    |
| 弹窗、固定导航、吸顶效果    | Position          | 精准控制位置，支持层叠                |
| 长文章分栏、简单瀑布流      | Column            | 自动分栏，无需手动控制列数            |
| 兼容旧浏览器、图文环绕      | Float             | 历史布局方案，兼容性好                |