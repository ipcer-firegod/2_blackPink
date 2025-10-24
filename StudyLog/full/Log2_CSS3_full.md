# CSS3 核心知识学习笔记
## 一、CSS 基础认知
### 1. 什么是 CSS
- **全称**：Cascading Style Sheets（层叠样式表），是用于控制网页**视觉表现**的标记语言，与 HTML 分工明确：
  - HTML：负责页面**结构**（“骨架”，展示内容）。
  - CSS：负责页面**样式与布局**（“皮肤”，控制外观、排列、交互效果）。
- **核心作用**：
  1. **样式美化**：控制文本颜色、字体、背景、边框等。
  2. **布局与定位**：实现元素排列（如导航栏、卡片）、响应式适配。
  3. **动画交互**：通过伪类、过渡、动画实现鼠标悬停、状态变化等效果。


### 2. CSS 的分类（按书写位置）
根据样式与 HTML 的关联方式，分为三类，实际开发中优先使用**外部样式表**（结构与样式完全分离）：

| 分类         | 书写位置                          | 作用范围       | 语法示例                                  | 优缺点                                  |
|--------------|-----------------------------------|----------------|-------------------------------------------|-----------------------------------------|
| 内联样式表   | HTML 标签的 `style` 属性内        | 仅当前标签     | `<p style="color: red; font-size: 14px;">文本</p>` | 优先级最高，但耦合度高，维护困难        |
| 内部样式表   | HTML 的 `<head>` 标签内的 `<style>` 中 | 仅当前页面     | `<style> p { color: red; } </style>`       | 耦合度较低，适合单页面小型项目          |
| 外部样式表   | 单独的 `.css` 文件，通过 `<link>` 引入 | 整个网站（多页面） | `<link rel="stylesheet" href="./css/index.css">` | 完全分离，可复用、易维护，适合中大型项目 |


## 二、CSS 选择器（核心：“选对元素，改对样式”）
选择器是 CSS 规则的核心，用于定位 HTML 中需要修改样式的元素。按使用场景分为**基础选择器、关系选择器、分组选择器、伪类/伪元素选择器、属性选择器**，以下为重点分类详解：


### 1. 基础选择器（单个选择器，最常用）
基础选择器是 CSS 选择器的基石，其中**类选择器**是实际开发中使用频率最高的选择器。

| 选择器类型   | 语法示例                | 匹配范围                 | 复用性       | 典型场景                          | 注意事项                          |
|--------------|-------------------------|--------------------------|--------------|-----------------------------------|-----------------------------------|
| 类型选择器   | `div { color: pink; }`  | 所有指定标签（如所有 `<div>`） | 低（某类标签） | 全局标签样式重置（如 `body`、`p`） | 避免滥用，易引发样式冲突          |
| 类选择器     | `.nav { color: pink; }` | 所有含 `class="nav"` 的元素 | 高（可多次使用） | 多元素共享样式（如导航项、卡片）  | 类名见名知义（如 `.btn`、`.card`），可多类名共存（如 `class="card card-active"`） |
| ID 选择器    | `#header { color: red; }` | 唯一含 `id="header"` 的元素 | 低（唯一）   | 单个特殊元素（如页面头部、登录框） | 同一页面 `id` 必须唯一，主要配合 JS 交互 |
| 通配符选择器 | `* { margin: 0; }`      | 所有 HTML 元素           | 无           | 全局样式重置（清除默认边距）      | 性能较差，仅用于重置，不用于样式定义 |


#### 关键区别：类选择器 vs ID 选择器
| 维度         | 类选择器（.class）               | ID 选择器（#id）                 |
|--------------|----------------------------------|----------------------------------|
| 语法         | 以 `.` 开头                     | 以 `#` 开头                     |
| 作用范围     | 多个元素（可重复使用）           | 单个元素（页面唯一）             |
| 核心用途     | CSS 样式定义                     | JS 交互（如获取元素、绑定事件）  |
| 权重         | 较低（0, 0, 1, 0）               | 较高（0, 1, 0, 0）               |


### 2. 关系选择器（通过位置关系定位，精准选择）
通过元素在 HTML 中的嵌套或同级关系定位目标元素，**后代选择器**是实际开发中最常用的关系选择器。

| 选择器类型   | 语法示例                  | 选择范围                                  | 实例                          | 注意事项                          |
|--------------|---------------------------|-------------------------------------------|-------------------------------|-----------------------------------|
| 后代选择器   | `.box p { color: pink; }` | 匹配 `.box` 内所有 `<p>`（不限层级，含子、孙元素） | `ul li { list-style: none; }`  | 父级与子级用**空格**分隔，父级可是任意选择器 |
| 子代选择器   | `.box > p { color: pink; }` | 匹配 `.box` 内**直接子级** `<p>`（仅一层） | `div > span { font-size: 14px; }` | 父级与子级用 `>` 分隔，仅匹配“亲儿子”元素 |
| 邻接兄弟选择器 | `h2 + p { color: red; }`  | 匹配 `h2` 紧邻的**下一个同级** `<p>`       | 标题后第一个段落样式调整       | 仅匹配“紧挨着”的下一个兄弟元素    |
| 通用兄弟选择器 | `h2 ~ p { color: blue; }`  | 匹配 `h2` 之后**所有同级** `<p>`           | 标题后所有段落样式调整         | 不包含 `h2` 之前的兄弟元素        |


### 3. 伪类选择器（选择“状态或位置特殊”的元素）
伪类选择器用 `:` 表示，按功能分为**状态伪类、结构伪类、表单伪类**，核心解决“元素特定状态/位置的样式”问题。

#### 3.1 状态伪类（用户交互相关）
- **链接伪类**：控制链接的不同状态，必须遵循 **LVHA 顺序**（否则样式不生效）：
  | 伪类         | 作用                                  | 示例代码                          |
  |--------------|---------------------------------------|-----------------------------------|
  | `a:link`     | 未访问链接的默认样式                  | `a:link { color: #333; }`         |
  | `a:visited`  | 已访问链接的样式                      | `a:visited { color: #666; }`       |
  | `a:hover`    | 鼠标悬停在链接上的样式（核心交互）      | `a:hover { color: #ff6700; text-decoration: underline; }` |
  | `a:active`   | 链接被点击时的瞬时样式（按下未松开）    | `a:active { color: #f00; }`       |

- **用户行为伪类**：
  | 伪类         | 作用                                  | 示例代码                          |
  |--------------|---------------------------------------|-----------------------------------|
  | `:hover`     | 鼠标经过任意元素（如按钮、卡片）      | `.btn:hover { background: #ff6700; }` |
  | `:focus`     | 表单元素获得焦点（如输入框、下拉框）  | `input:focus { border: 2px solid #ff6700; }` |


#### 3.2 结构伪类（按元素位置选择）
按元素在兄弟列表中的位置定位，核心是 `:nth-child(n)`，解决“选择第 N 个元素”的需求：

| 伪类               | 作用                                  | 示例代码（以 `<ul>` 下的 `<li>` 为例） |
|--------------------|---------------------------------------|-----------------------------------|
| `:first-child`     | 选择第一个兄弟元素                    | `ul li:first-child { color: pink; }` |
| `:last-child`      | 选择最后一个兄弟元素                  | `ul li:last-child { color: green; }` |
| `:nth-child(n)`    | 选择第 N 个兄弟元素（`n` 为参数）     | `ul li:nth-child(2) { color: blue; }` |

- **`n` 的取值规则**：
  1. 数字：直接指定位置（如 `n=3` 选择第 3 个元素）。
  2. 关键字：`odd`（奇数，1、3、5...）、`even`（偶数，2、4、6...）。
  3. 公式：`an+b`（`a` 为步长，`b` 为起始位置，`n` 从 0 开始）：
     - `nth-child(3n)`：3 的倍数（3、6、9...）。
     - `nth-child(n+2)`：第 2 个及以后（2、3、4...）。
     - `nth-child(-n+3)`：前 3 个（1、2、3）。


#### 3.3 表单伪类（控制表单元素状态）
| 伪类         | 作用                                  | 示例代码                          |
|--------------|---------------------------------------|-----------------------------------|
| `:disabled`  | 选择禁用的表单元素（如按钮、输入框）  | `button:disabled { background: #ccc; color: #999; }` |
| `:checked`   | 选择已选中的单选框/复选框            | `input:checked + span { color: #ff6700; }` |


### 4. 伪元素选择器（选择“元素的特定部分”）
伪元素用 `::` 表示，用于选择元素的某一部分（如首行文字、占位符）或插入虚拟内容，核心是 `::before` 和 `::after`。

| 伪元素               | 作用                                  | 示例代码                          |
|----------------------|---------------------------------------|-----------------------------------|
| `::first-line`       | 选择文本的首行                        | `p::first-line { font-weight: 700; }` |
| `::first-letter`     | 选择文本的首字母                      | `p::first-letter { font-size: 24px; color: red; }` |
| `::placeholder`      | 选择输入框的占位符文字                | `input::placeholder { color: #999; font-size: 12px; }` |
| `::before`           | 在元素内部**最前面**插入虚拟内容      | `.box::before { content: "开头"; color: red; }` |
| `::after`            | 在元素内部**最后面**插入虚拟内容      | `.box::after { content: "结尾"; color: blue; }` |

- **关键注意**：
  1. `::before` 和 `::after` 插入的是“伪元素”，默认是内联元素，需通过 CSS 调整 display（如 `display: inline-block`）。
  2. `content` 属性**必须写**，无内容时填空引号（`content: ""`）。


### 5. 属性选择器（按元素属性定位）
根据元素的属性或属性值定位，灵活度高，常用于表单控制、图标适配等场景。

| 属性选择器         | 作用                                  | 示例代码                          |
|--------------------|---------------------------------------|-----------------------------------|
| `[属性]`           | 匹配包含指定属性的元素                | `[type] { box-sizing: border-box; }`（匹配所有含 `type` 属性的元素） |
| `[属性=值]`        | 匹配属性值**等于**指定值的元素        | `[type="text"] { padding: 8px; }`（匹配 `type="text"` 的输入框） |
| `[属性^=值]`       | 匹配属性值**以指定值开头**的元素      | `[class^="icon-"] { font-family: iconfont; }`（匹配类名以 `icon-` 开头的图标元素） |
| `[属性$=值]`       | 匹配属性值**以指定值结尾**的元素      | `[src$=".png"] { border: 1px solid #eee; }`（匹配 PNG 格式图片） |
| `[属性*=值]`       | 匹配属性值**包含指定子串**的元素      | `[class*="btn-"] { cursor: pointer; }`（匹配类名含 `btn-` 的按钮元素） |


### 6. 分组选择器（合并相同样式）
又称“并集选择器”，用**逗号**分隔多个选择器，实现“多个元素共享同一组样式”，减少代码冗余。

- 语法：`选择器1, 选择器2, 选择器3 { 样式声明; }`
- 示例：
  ```css
  /* 导航标题和内容区标题共享同一字体样式 */
  .nav-title, .content-title {
    font-size: 18px;
    font-weight: 700;
    color: #333;
  }
  ```


## 三、CSS 三大特性（核心：解决样式冲突与继承）
CSS 三大特性（继承、层叠、优先级）是控制样式生效规则的核心，直接影响最终页面表现。


### 1. 继承性（子元素自动继承父元素样式）
- **核心规则**：子元素会自动继承父元素中“与文字相关”的样式，非文字相关样式（如背景、边框）不继承。
- **可继承的样式**：`color`、`font-family`、`font-size`、`line-height`、`text-align` 等。
- **不可继承的样式**：`width`、`height`、`margin`、`padding`、`border`、`background` 等。
- **特殊情况**：部分标签有浏览器默认样式（如 `<h1>` 默认加粗、`<a>` 默认有下划线），无法通过继承取消，需单独给标签设置样式（如 `h1 { font-weight: 400; }`、`a { text-decoration: none; }`）。


### 2. 层叠性（样式冲突时的“就近原则”）
- **核心规则**：当多个 CSS 规则作用于同一元素，且**优先级相等**时，**后定义的样式会覆盖先定义的样式**（“谁后写，听谁的”）。
- 示例：
  ```css
  p { color: red; }   /* 先定义，被覆盖 */
  p { color: blue; }  /* 后定义，最终生效 */
  ```


### 3. 优先级（样式冲突时的“权重比拼”）
当多个选择器匹配同一元素，优先级由**选择器权重**决定，权重高的样式优先生效。权重是“4位一组”的层级值，**不进位**（如 (0,0,10,0) 不大于 (0,1,0,0)）。

#### 优先级权重表
| 选择器类型         | 权重值（a, b, c, d） | 示例                          | 优先级说明                          |
|--------------------|----------------------|-------------------------------|-----------------------------------|
| `!important`       | 无限大               | `color: red !important;`      | 强制覆盖所有规则，慎用（破坏优先级逻辑） |
| 内联样式（`style` 属性） | (1, 0, 0, 0)         | `<div style="color: red">`     | 优先级最高，仅作用于当前标签        |
| ID 选择器          | (0, 1, 0, 0)         | `#header { ... }`             | 每个 ID 贡献 0,1,0,0              |
| 类/属性/伪类选择器  | (0, 0, 1, 0)         | `.nav { ... }`、`[type] { ... }`、`:hover { ... }` | 每个类/属性/伪类贡献 0,0,1,0      |
| 类型（标签）/伪元素选择器 | (0, 0, 0, 1)       | `div { ... }`、`::after { ... }` | 每个标签/伪元素贡献 0,0,0,1        |
| 通配符/继承样式     | (0, 0, 0, 0)         | `* { ... }`、继承的 `color`    | 优先级最低                          |

#### 权重叠加计算示例
- 选择器 `#nav .item a` 的权重：(0,1,0,0) + (0,0,1,0) + (0,0,0,1) = **(0,1,1,1)**
- 选择器 `div.nav > p.active` 的权重：(0,0,0,1) + (0,0,1,0) + (0,0,1,0) = **(0,0,2,1)**


## 四、盒子模型（布局核心：“万物皆盒子”）
***所有 HTML 元素都可视为“盒子”***，盒子模型是实现页面布局的基础，决定元素的尺寸、边距和排列方式。


### 1. 盒子模型的组成（4部分）
盒子从内到外分为 **内容区（content）、内边距（padding）、边框（border）、外边距（margin）**，如下图所示：
```
+---------------------------+  ← 外边距（margin）
|                           |
|  +---------------------+  |  ← 边框（border）
|  |                     |  |
|  |  +---------------+  |  |  ← 内边距（padding）
|  |  |               |  |  |
|  |  |  内容区       |  |  |  ← 内容区（content，含文本、图片等）
|  |  | （width/height）|  |  |
|  |  |               |  |  |
|  |  +---------------+  |  |
|  |                     |  |
|  +---------------------+  |
|                           |
+---------------------------+
```


### 2. 核心组成部分详解
#### 2.1 内容区（content）
- 作用：显示元素的核心内容（文本、图片、子元素）。
- 尺寸控制：通过 `width`（宽度）和 `height`（高度）设置，默认由内容大小决定。
- 注意：块级元素默认宽度为父容器的 100%，内联元素宽度由内容决定（无法直接设置 `width`/`height`）。


#### 2.2 内边距（padding）
- 作用：控制**内容区与边框之间的距离**，用于调整内容在盒子内的位置，避免内容紧贴边框。
- 写法：支持简写（顺时针顺序：上→右→下→左）和单边设置，单位常用 `px`。

| 写法                          | 作用                                  | 示例代码                          |
|-------------------------------|---------------------------------------|-----------------------------------|
| `padding: 10px;`              | 上下左右内边距均为 10px               | `padding: 8px;`（按钮内边距）      |
| `padding: 10px 20px;`         | 上下 10px，左右 20px                  | `padding: 12px 16px;`（输入框内边距） |
| `padding: 10px 20px 30px;`    | 上 10px，左右 20px，下 30px           | `padding: 8px 16px 12px;`         |
| `padding: 10px 20px 30px 40px;`| 上 10px，右 20px，下 30px，左 40px    | `padding: 5px 10px 15px 20px;`    |
| 单边设置（如 `padding-top`）  | 单独控制某一边的内边距                | `padding-left: 20px;`（列表项左内边距） |


#### 2.3 边框（border）
- 作用：给盒子添加边框，用于分隔元素、强调区域。
- 核心属性：`border: 边框粗细 边框样式 边框颜色;`（三部分无顺序，空格分隔）。
- 边框样式（必选，否则边框不显示）：

| 样式值   | 描述                | 视觉效果                          | 示例代码                          |
|----------|---------------------|-----------------------------------|-----------------------------------|
| `solid`  | 实线（最常用）      | 单一线条                          | `border: 1px solid #eee;`（卡片边框） |
| `dashed` | 虚线                | 短横线组成的虚线                  | `border: 1px dashed #f00;`（警告边框） |
| `dotted` | 点状边框            | 圆点组成的虚线                    | `border: 1px dotted #999;`         |

- 单边边框：通过 `border-top`/`border-right`/`border-bottom`/`border-left` 单独设置某一边边框，示例：
  ```css
  /* 仅底部添加边框（常用作分割线） */
  .divider {
    border-bottom: 1px solid #eee;
    margin: 16px 0;
  }
  ```

- 圆角边框（`border-radius`）：
  - 作用：将盒子的直角改为圆角，提升页面美观度。
  - 写法：
    1. 统一圆角：`border-radius: 10px;`（所有角均为 10px 圆角）。
    2. 单独圆角：`border-radius: 10px 20px 30px 40px;`（左上→右上→右下→左下，顺时针）。
    3. 圆形/胶囊形：
       - 圆形：正方形盒子 + `border-radius: 50%;`（如头像）。
       - 胶囊形：长方形盒子 + `border-radius: 高度的一半;`（如按钮 `border-radius: 20px;`，按钮高度 40px）。


#### 2.4 外边距（margin）
- 作用：控制**当前盒子与其他元素之间的距离**，用于元素排版（如上下元素间距、居中对齐）。
- 写法：与 `padding` 一致，支持简写和单边设置，单位常用 `px`。
- 关键技巧：**块级元素水平居中**（核心布局技巧）：
  - 条件：块级元素必须设置 `width`（否则宽度为 100%，无需居中）。
  - 写法：`margin: 0 auto;`（上下外边距 0，左右自动，实现水平居中）。
  - 示例：
    ```css
    .container {
      width: 1200px;  /* 固定宽度 */
      margin: 0 auto; /* 水平居中 */
    }
    ```

- 常见问题：外边距折叠与塌陷（必须掌握解决方案）：
  1. **外边距折叠（兄弟元素）**：
     - 现象：两个上下相邻的块级元素，上方元素的 `margin-bottom` 和下方元素的 `margin-top` 会“合并”，最终间距为两者中的较大值（而非相加）。
     - 解决方案：只给其中一个元素设置单边外边距（如只给上方元素设 `margin-bottom`，或只给下方元素设 `margin-top`）。

  2. **外边距塌陷（父子元素）**：
     - 现象：给子元素设置 `margin-top`，会导致父元素一起向下移动（而非子元素在父元素内向下偏移）。
     - 解决方案（三选一）：
       - 给父元素添加上边框（如 `border-top: 1px solid transparent;`）。
       - 给父元素添加上内边距（如 `padding-top: 1px;`）。
       - 给父元素设置 `overflow: hidden;`（最常用，不影响布局）。


### 3. 盒子尺寸计算（`box-sizing`）
默认情况下，`width`/`height` 仅代表“内容区”尺寸，`padding` 和 `border` 会使盒子实际尺寸变大（如 `width: 200px` + `padding: 10px` + `border: 5px`，实际宽度为 230px），导致布局计算繁琐。

#### `box-sizing` 属性（解决尺寸计算问题）
| 属性值         | 描述                                  | 实际尺寸计算                          | 适用场景                          |
|----------------|---------------------------------------|-----------------------------------|-----------------------------------|
| `content-box`   | 默认值，`width`/`height` 仅含内容区   | 实际宽度 = width + padding + border | 无需精确控制盒子总尺寸的场景      |
| `border-box`    | `width`/`height` 包含内容区、padding、border | 实际宽度 = width（padding 和 border 不会撑大盒子） | 所有需要精确控制尺寸的场景（推荐全局使用） |

- 全局设置（推荐）：让所有元素都使用 `border-box`，避免尺寸计算问题：
  ```css
  /* 全局设置盒模型为 border-box */
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0; /* 同时清除默认边距 */
  }
  ```


## 五、CSS 文本样式（控制文字外观与布局）
文本样式是页面美化的基础，分为**字体样式**（控制文字本身）和**文本布局**（控制文字排列）。


### 1. 字体样式（控制文字外观）
| 属性               | 作用                                  | 常用取值                          | 示例代码                          |
|--------------------|---------------------------------------|-----------------------------------|-----------------------------------|
| `color`            | 设置文字颜色                          | 十六进制（#ff6700，最常用）、RGB（rgb(255,103,0)）、RGBA（rgba(255,103,0,0.5)，含透明度） | `color: #333;`（正文）、`color: #ff6700;`（强调色） |
| `font-family`      | 设置字体系列（字体）                  | 无衬线字体（如 "Microsoft YaHei", Arial, sans-serif，网页推荐） | `body { font-family: "Microsoft YaHei", sans-serif; }` |
| `font-size`        | 设置文字大小                          | `px`（像素，如 14px、16px，浏览器默认 16px） | `p { font-size: 14px; }`、`h1 { font-size: 24px; }` |
| `font-style`       | 设置文字风格（斜体/正常）             | `normal`（正常）、`italic`（斜体） | `em { font-style: normal; }`（取消 `<em>` 默认斜体） |
| `font-weight`      | 设置文字粗细                          | 数字（400=normal，700=bold，常用）、关键字（normal、bold） | `h2 { font-weight: 400; }`（取消标题默认加粗）、`.strong { font-weight: 700; }` |
| `text-decoration`  | 设置文字装饰（下划线/删除线等）       | `none`（无装饰，常用）、`underline`（下划线）、`line-through`（删除线） | `a { text-decoration: none; }`（取消链接下划线）、`.old-price { text-decoration: line-through; }`（原价删除线） |


### 2. 文本布局（控制文字排列）
| 属性               | 作用                                  | 常用取值                          | 示例代码                          |
|--------------------|---------------------------------------|-----------------------------------|-----------------------------------|
| `text-align`       | 文本水平对齐                          | `left`（左对齐，默认）、`center`（居中）、`right`（右对齐）、`justify`（两端对齐） | `h1 { text-align: center; }`（标题居中）、`.article { text-align: justify; }`（文章两端对齐） |
| `text-indent`      | 首行文本缩进                          | `em`（相对单位，1em = 当前字体大小，常用 2em 实现“首行缩进 2 字符”） | `p { text-indent: 2em; font-size: 14px; }`（段落首行缩进） |
| `letter-spacing`   | 字符间距（字与字之间的距离）           | `px`（如 2px、-1px，负值使字符紧凑） | `h2 { letter-spacing: 2px; }`（标题字符间距） |
| `line-height`      | 行高（行与行之间的垂直距离）           | `px`（固定值，如 24px）、倍数（如 1.5，当前字体大小的 1.5 倍，推荐） | `p { line-height: 1.6; }`（文章行高，提升可读性）、`.btn { line-height: 40px; height: 40px; }`（按钮单行文字垂直居中） |

- **单行文字垂直居中原理**：当 `line-height = 盒子高度` 时，单行文字会在盒子内垂直居中（核心技巧）。


### 3. `font` 简写属性（简化代码）
将多个字体属性合并为一个声明，需遵循固定顺序，**必须包含 `font-size` 和 `font-family`**，其他属性可省略（默认值生效）。

- 语法：`font: font-style font-weight font-size/line-height font-family;`
- 示例（小米官网字体设置）：
  ```css
  body {
    font: 14px/1.5 "Microsoft YaHei", Arial, sans-serif;
    /* 等同于：
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    line-height: 1.5;
    font-family: "Microsoft YaHei", Arial, sans-serif;
    */
  }
  ```


## 六、CSS 背景与阴影（美化盒子外观）
### 1. 背景属性（`background`）
控制元素背景的颜色、图片、位置等，支持单个属性设置和复合写法。

| 单个属性           | 作用                                  | 常用取值                          | 示例代码                          |
|--------------------|---------------------------------------|-----------------------------------|-----------------------------------|
| `background-color` | 设置背景颜色                          | 颜色值（如 #f5f5f5、transparent（透明）） | `.box { background-color: #f5f5f5; }` |
| `background-image` | 设置背景图片                          | `url(图片路径)`（如 `url(bg.png)`） | `.banner { background-image: url(banner.jpg); }` |
| `background-repeat`| 控制背景图片是否重复                  | `repeat`（默认，重复）、`no-repeat`（不重复）、`repeat-x`（水平重复）、`repeat-y`（垂直重复） | `.icon { background-repeat: no-repeat; }` |
| `background-position` | 背景图片定位                      | 方位词（如 `center center`、`left top`）、`px`（如 `50px 30px`）、`%`（如 `50% 50%`） | `.icon { background-position: center; }`（图片居中） |
| `background-size`  | 背景图片尺寸                          | `auto`（默认）、`cover`（覆盖盒子，可能裁剪）、`contain`（包含在盒子内，可能留空）、`px`（如 `200px 100px`） | `.banner { background-size: cover; }`（ banner 图覆盖容器） |
| `background-attachment` | 背景是否随页面滚动              | `scroll`（默认，随滚动）、`fixed`（固定，不随滚动） | `.bg-fixed { background-attachment: fixed; }`（固定背景，实现视差效果） |

- **复合写法**（顺序无关，推荐顺序：颜色 图片 重复 固定 位置/尺寸）：
  ```css
  .banner {
    background: #f5f5f5 url(banner.jpg) no-repeat fixed center/cover;
  }
  ```


### 2. 背景渐变（`linear-gradient`/`radial-gradient`）
无需图片，通过 CSS 生成渐变背景，提升页面美观度，支持线性和径向两种渐变。

#### 2.1 线性渐变（`linear-gradient`，常用）
- 语法：`linear-gradient(方向, 颜色1 位置, 颜色2 位置, ...)`
- 关键参数：
  - 方向：可写方位词（`to right` 右向、`to bottom` 下向）或角度（`90deg` 水平向右，`0deg` 垂直向上）。
  - 颜色位置：可选，如 `#ff6700 30%` 表示“30% 位置处为橙色”。
- 示例：
  ```css
  /* 水平渐变（左橙右蓝） */
  .btn {
    background: linear-gradient(to right, #ff6700, #4ecdc4);
  }
  /* 角度渐变（45度，带颜色位置） */
  .card {
    background: linear-gradient(45deg, #ff6700 0%, #f90 50%, #ff6700 100%);
  }
  ```

#### 2.2 文字渐变（进阶技巧）
将渐变作为文字背景，实现“文字颜色渐变”效果：
```css
.text-gradient {
  /* 1. 设置背景渐变 */
  background: linear-gradient(to right, #ff6700, #4ecdc4);
  /* 2. 裁剪背景到文字范围 */
  -webkit-background-clip: text;
  background-clip: text;
  /* 3. 文字填充为透明，显示背景渐变 */
  -webkit-text-fill-color: transparent;
  text-fill-color: transparent;
}
```


### 3. 盒子阴影（`box-shadow`）
给盒子添加阴影，实现立体效果，常用于鼠标悬停交互。

- 语法：`box-shadow: X轴偏移量 Y轴偏移量 模糊半径 扩散半径 颜色 内阴影标识;`
- 参数说明：
  - X轴偏移量（必选）：正数向右，负数向左（如 `8px`）。
  - Y轴偏移量（必选）：正数向下，负数向上（如 `15px`）。
  - 模糊半径（可选）：值越大阴影越模糊（如 `30px`）。
  - 扩散半径（可选）：值越大阴影范围越大（如 `5px`，负数缩小）。
  - 颜色（可选）：常用半透明色（如 `rgba(0,0,0,0.1)`）。
  - 内阴影标识（可选）：`inset`，表示内阴影（默认外阴影）。
- 示例（鼠标悬停卡片阴影）：
  ```css
  .card {
    transition: all 0.3s; /* 过渡效果，平滑变化 */
  }
  .card:hover {
    box-shadow: 8px 15px 30px rgba(0,0,0,0.1); /* 外阴影 */
  }
  ```


### 4. 过渡效果（`transition`，实现平滑变化）
使元素属性变化（如颜色、阴影、尺寸）时“平滑过渡”，而非瞬间切换，提升交互体验。

- 语法：`transition: 过渡属性 过渡时间;`
- 参数说明：
  - 过渡属性：指定哪些属性需要过渡（如 `box-shadow`、`background`），`all` 表示所有属性变化都过渡。
  - 过渡时间：单位 `s`（秒）或 `ms`（毫秒），如 `0.3s`。
- 示例（按钮 hover 平滑变色）：
  ```css
  .btn {
    background: #ff6700;
    transition: background 0.3s; /* 背景色过渡 0.3 秒 */
  }
  .btn:hover {
    background: #f90; /*  hover 时背景色变化，平滑过渡 */
  }
  ```


## 七、样式初始化（统一浏览器默认样式）
不同浏览器对 HTML 元素有默认样式（如 `body` 默认有 `margin: 8px`、`ul` 默认有 `padding-left: 40px`），导致跨浏览器显示不一致，需通过“样式初始化”消除差异。

### 1. 小型项目（简单重置）
适合练手或单页面项目，通过通配符和标签选择器清除默认样式：
```css
/* 全局重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box; /* 统一盒模型 */
}

/* 重置列表样式 */
ul, ol {
  list-style: none; /* 去除列表默认圆点/数字 */
}

/* 重置链接样式 */
a {
  text-decoration: none; /* 去除链接下划线 */
  color: #333; /* 统一链接默认颜色 */
}

/* 重置表单元素 */
input, button {
  outline: none; /* 去除聚焦外边框 */
  border: none; /* 去除默认边框 */
}
```

### 2. 中大型项目（Normalize.css）
适合工程化项目，推荐使用 `Normalize.css`（保留有用的默认样式，而非全部清除，兼容性更好）：
- 引入方式：下载 `normalize.css` 文件，通过 `<link>` 引入：
  ```html
  <link rel="stylesheet" href="./css/normalize.css">
  ```
- 官网地址：https://necolas.github.io/normalize.css/


## 八、精灵图与字体图标（优化图标加载）
### 1. 精灵图（CSS Sprite）
将多个小图标合并到一张大图中，通过 `background-position` 显示指定图标，减少 HTTP 请求，提升性能。

- **核心原理**：
  1. 给盒子设置固定宽高（与单个图标尺寸一致）。
  2. 将精灵图设为盒子背景（`background-image: url(sprite.png)`）。
  3. 通过 `background-position` 调整背景位置，使目标图标显示在盒子内（网页坐标：X 轴向右为正，Y 轴向下为正，需用负值调整图标位置）。

- **示例**（假设精灵图中“首页图标”位于 X: -20px，Y: 0px，图标尺寸 24x24px）：
  ```css
  .icon-home {
    width: 24px;
    height: 24px;
    background: url(sprite.png) no-repeat;
    background-position: -20px 0; /* 显示“首页图标” */
  }
  ```

- **适用场景**：复杂彩色小图标（如游戏图标、自定义按钮图标）。


### 2. 字体图标（Icon Font）
将图标以“字体”形式嵌入网页，可通过 CSS 控制颜色、大小、阴影，灵活性远高于精灵图。

- **核心优势**：
  1. 矢量缩放：无损放大，适配高清屏。
  2. 样式灵活：通过 `color`、`font-size` 直接修改样式。
  3. 减少请求：一个字体文件包含多个图标。

- **常用图标库**：
  | 图标库         | 特点                                  | 官网地址                          |
  |----------------|---------------------------------------|-----------------------------------|
  | Font Awesome   | 图标最全，支持免费/Pro 版            | https://fontawesome.com/          |
  | iconfont（阿里）| 免费，含淘宝/阿里妈妈图标库，适合中文项目 | https://www.iconfont.cn/          |
  | Bootstrap Icons | 轻量，适配 Bootstrap 生态            | https://icons.getbootstrap.com/    |

- **使用步骤（以 iconfont 为例）**：
  1. 下载图标：在 iconfont 选择图标，添加到项目，下载字体文件（含 `.woff`、`.css` 等）。
  2. 引入文件：将字体文件放入项目，在 HTML 中引入 `iconfont.css`：
     ```html
     <link rel="stylesheet" href="./iconfont/iconfont.css">
     ```
  3. 使用图标：通过 `<i>` 标签+类名调用（类名在 `iconfont.css` 中定义）：
     ```html
     <!-- 显示“购物车图标”，并设置颜色和大小 -->
     <i class="iconfont icon-gouwuche" style="color: #ff6700; font-size: 20px;"></i>
     ```

- **适用场景**：单色图标（如导航图标、按钮图标、表单图标）。


## 九、实用技巧与案例
### 1. 单行文字溢出显示省略号（常用）
当文字超出盒子宽度时，显示“...”，需同时设置三个属性：
```css
.single-ellipsis {
  white-space: nowrap; /* 文字不换行 */
  overflow: hidden;    /* 溢出内容隐藏 */
  text-overflow: ellipsis; /* 溢出文字显示省略号 */
}
```

### 2. 多行文字溢出显示省略号（进阶）
适用于文章摘要、卡片描述等场景（仅支持 WebKit 内核浏览器，如 Chrome、Safari）：
```css
.multi-ellipsis {
  display: -webkit-box; /* 旧版弹性盒子 */
  -webkit-box-orient: vertical; /* 文本垂直排列 */
  -webkit-line-clamp: 3; /* 限制显示 3 行 */
  overflow: hidden;
  text-overflow: ellipsis;
}
```

### 3. 小米卡片案例（综合应用）
需求：实现商品卡片，鼠标悬停显示阴影，文字溢出省略。
```html
<div class="card">
  <img src="buds5.jpg" alt="Xiaomi Buds 5" class="card-img">
  <h3 class="card-title">Xiaomi Buds 5</h3>
  <p class="card-desc">舒适无感佩戴|高通全链路无损音频|长效续航</p>
  <div class="card-price">
    <span class="now-price">659元</span>
    <span class="old-price">699元</span>
  </div>
</div>
```
```css
.card {
  width: 240px;
  padding: 20px;
  transition: box-shadow 0.3s; /* 阴影过渡 */
}
.card:hover {
  box-shadow: 0 15px 30px rgba(0,0,0,0.1); /* 悬停阴影 */
}
.card-img {
  width: 160px;
  height: 160px;
  margin: 0 auto; /* 图片居中 */
}
.card-title {
  font-size: 16px;
  color: #333;
  margin: 10px 0;
}
.card-desc {
  font-size: 14px;
  color: #b0b0b0;
  /* 单行溢出省略 */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.card-price .now-price {
  font-size: 16px;
  color: #ff6700;
}
.card-price .old-price {
  font-size: 14px;
  color: #b0b0b0;
  text-decoration: line-through; /* 原价删除线 */
  margin-left: 8px;
}
```