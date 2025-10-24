# CSS3 核心知识复习记录
## 一、本文档目的
- 将 CSS3 的核心概念、高频用法与易错点提炼为速查式笔记，适配 10 分钟碎片化回顾、1 小时集中复习两种节奏，避免“学完就忘”。
- 提供可落地的实战练习与周期化复习计划，帮助将理论转化为实操能力，重点突破选择器、盒子模型、美化等核心模块。


## 二、宏观结构（快速导航）
- 基础认知（CSS 分类、书写规范）
- 选择器（基础、关系、分组、伪类/伪元素、属性选择器）
- CSS 三大特性（继承性、层叠性、优先级）
- 盒子模型（组成、box-sizing、margin 问题、圆角/阴影/过渡）
- 背景与美化（background、渐变、盒子阴影、文字渐变）
- 字体与图标（字体样式、字体图标、精灵图）
- 样式初始化（简单重置、Normalize.css）
- 实战案例（小米卡片、淘宝导航）


## 三、核心概念速查（记忆卡）
### 1. CSS 基础与分类
- **核心作用**：控制网页视觉表现（样式美化、布局定位、动画交互），与 HTML 分离（结构归 HTML，样式归 CSS）。
- **按书写位置分类**：
  - 内联样式：写在标签 `style` 属性（如 `<div style="color: red;">`），优先级最高，耦合度高，不推荐。
  - 内部样式：写在 `<head>` 内 `<style>` 标签，作用于当前页面，适合小型项目。
  - 外部样式：单独 `.css` 文件，通过 `<link rel="stylesheet" href="xxx.css">` 引入，作用于全站，推荐。
- **书写规范**：选择器与 `{` 间留 1 空格，属性名与值间留 1 空格，每个属性单独占一行。


### 2. 选择器（核心：选对元素）
#### （1）基础选择器
| 类型         | 语法          | 匹配范围                | 关键特点                          |
|--------------|---------------|-------------------------|-----------------------------------|
| 类型选择器   | `div { }`     | 所有指定标签            | 复用性低，易冲突                  |
| 类选择器     | `.nav { }`    | 含 `class="nav"` 的元素 | 可重复使用（核心），多类名共存（如 `class="card active"`） |
| ID 选择器    | `#header { }` | 含 `id="header"` 的元素 | 页面唯一，主要配合 JS 交互        |
| 通配符选择器 | `* { }`       | 所有元素                | 用于全局重置（清边距），性能较差    |

#### （2）关系选择器
| 类型         | 语法          | 匹配范围                          | 常用场景                  |
|--------------|---------------|-----------------------------------|---------------------------|
| 后代选择器   | `.box p { }`  | `.box` 内所有 `<p>`（不限层级）    | 导航栏文本样式（`nav li a`） |
| 子代选择器   | `.box > p { }`| `.box` 直接子级 `<p>`（仅一层）    | 精准控制子元素            |
| 邻接兄弟选择器 | `h2 + p { }` | `h2` 紧邻的下一个 `<p>`           | 标题后第一个段落样式      |
| 通用兄弟选择器 | `h2 ~ p { }` | `h2` 后所有同级 `<p>`              | 标题后所有段落样式        |

#### （3）伪类与伪元素
| 类型         | 语法示例                | 作用                                  |
|--------------|-------------------------|---------------------------------------|
| 链接伪类     | `a:link`/`:visited`/`:hover`/`:active` | 控制链接状态，需遵循 **LVHA 顺序**    |
| 结构伪类     | `li:nth-child(2)`       | 选第 2 个 `<li>`，`n` 支持数字/odd/even/公式 |
| 伪元素       | `div::before`           | 元素内最前插入虚拟内容，需 `content` 属性 |
| 表单伪类     | `input:disabled`        | 选禁用的输入框                        |

#### （4）优先级（权重规则）
- 权重层级（不进位）：`!important`（无限大）> 内联样式(1,0,0,0) > ID 选择器(0,1,0,0) > 类/属性/伪类(0,0,1,0) > 标签/伪元素(0,0,0,1) > 通配符/继承(0,0,0,0)。
- 权重叠加：如 `#nav .item a` 权重 = (0,1,0,0)+(0,0,1,0)+(0,0,0,1) = (0,1,1,1)。


### 3. CSS 三大特性
- **继承性**：子元素自动继承父元素“文字相关样式”（如 `color`、`font-size`），非文字样式（`width`、`margin`）不继承；浏览器默认样式（如 `<h1>` 加粗）需单独覆盖。
- **层叠性**：优先级相等时，后定义的样式覆盖先定义的（“就近原则”）。
- **优先级**：按权重规则，权重高的样式生效，`!important` 慎用（破坏优先级逻辑）。


### 4. 盒子模型（布局核心）
#### （1）组成（从内到外）
- 内容区（content）：`width`/`height` 控制，默认由内容决定。
- 内边距（padding）：内容与边框间距，顺时针简写（`padding: 上 右 下 左`）。
- 边框（border）：`border: 粗细 样式 颜色`（如 `1px solid #eee`），圆角用 `border-radius`（圆形需 `50%`+正方形）。
- 外边距（margin）：盒子与其他元素间距，水平居中用 `margin: 0 auto`（需块级+定宽）。

#### （2）关键属性 `box-sizing`
| 属性值         | 尺寸计算                          | 推荐场景                  |
|----------------|-----------------------------------|---------------------------|
| `content-box`   | 实际宽 = width + padding + border | 无需精确控制尺寸          |
| `border-box`    | 实际宽 = width（含 padding+border） | 所有场景（推荐全局设置）  |
- 全局设置：`* { box-sizing: border-box; margin: 0; padding: 0; }`

#### （3）margin 常见问题
- **margin 折叠（兄弟元素）**：上下相邻块级元素的 `margin` 合并为较大值，解决方案：只设单边 margin。
- **margin 塌陷（父子元素）**：子元素 `margin-top` 导致父元素下移，解决方案：父元素加 `border`/`padding`/`overflow: hidden`。


### 5. 背景与美化
- **background 复合写法**：`background: 颜色 图片 重复 固定 位置/尺寸`（如 `background: #f5f5f5 url(bg.png) no-repeat center/cover`）。
- **渐变**：
  - 线性渐变：`linear-gradient(to right, #ff6700, #4ecdc4)`（水平橙到蓝）。
  - 文字渐变：需配合 `background-clip: text` + `text-fill-color: transparent`。
- **盒子阴影**：`box-shadow: X偏移 Y偏移 模糊 扩散 颜色`（如 `0 10px 20px rgba(0,0,0,0.1)`）。
- **过渡**：`transition: 属性 时间`（如 `transition: all 0.3s`，实现 hover 平滑变化）。


### 6. 字体与图标
- **字体简写**：`font: style weight size/line-height family`（如 `font: 14px/1.5 "Microsoft YaHei", sans-serif`）。
- **字体图标（iconfont）**：
  - 步骤：下载图标文件 → 引入 `iconfont.css` → 用 `<i class="iconfont 图标类名"></i>` 调用。
  - 优势：矢量缩放、样式灵活（改 `color`/`font-size`）。
- **精灵图**：合并小图标到一张图，通过 `background-position` 显示指定部分，减少 HTTP 请求。


### 7. 样式初始化
- **小型项目**：通配符清边距 + 重置列表/链接样式（`ul { list-style: none; }`，`a { text-decoration: none; }`）。
- **中大型项目**：使用 `Normalize.css`（保留有用默认样式，兼容性好），通过 `<link>` 引入。


## 四、常见错误与陷阱（高频）
1. **选择器权重错误**：
   - 错误：用 `div` 标签选择器覆盖类选择器样式（如 `.box { color: red; }` 被 `div { color: blue; }` 覆盖）。
   - 解决方案：检查选择器权重，优先用类选择器，避免滥用标签选择器。

2. **margin 塌陷/折叠未处理**：
   - 错误：子元素加 `margin-top` 导致父元素下移，或兄弟元素上下 margin 合并。
   - 解决方案：父元素加 `overflow: hidden`，兄弟元素只设单边 margin。

3. **未设置 `box-sizing: border-box`**：
   - 错误：加 `padding` 后盒子被撑大，超出预期尺寸。
   - 解决方案：全局设置 `box-sizing: border-box`。

4. **链接伪类顺序错误**：
   - 错误：`a:hover` 写在 `a:link` 前面，导致 hover 样式不生效。
   - 解决方案：按 **LVHA 顺序**（`:link`→`:visited`→`:hover`→`:active`）。

5. **行内元素设置宽高无效**：
   - 错误：给 `<span>` 直接设 `width: 100px`，无效果。
   - 解决方案：将行内元素转为 `inline-block`/`block`（如 `span { display: inline-block; width: 100px; }`）。

6. **背景图片路径错误**：
   - 错误：`background-image: url(../img/bg.png)` 写成 `url(img/bg.png)`，图片加载失败。
   - 解决方案：确认图片相对于 CSS 文件的路径（上级用 `../`，下级用 `文件夹名/`）。


## 五、快速练习（把知识变成肌肉记忆）
### 1. 10 分钟任务（基础回顾）
- 任务 1：用基础选择器和关系选择器写样式：给 `class="nav"` 下的所有 `<a>` 标签设颜色 `#333`，hover 时变 `#ff6700`，无下划线。
- 任务 2：写一个盒子模型：宽 200px，高 200px，内边距 20px，边框 1px 实线 `#eee`，外边距水平居中，圆角 8px，hover 时加阴影 `0 5px 15px rgba(0,0,0,0.1)`。
- 任务 3：实现单行文字溢出省略：给 `class="title"` 的 `<p>` 标签设宽 200px，文字超出显示 `...`。

### 2. 1 小时任务（综合应用）
- 需求：制作“小米风格商品卡片”，包含：
  1. 卡片宽 240px，内边距 20px，hover 时加阴影和过渡（0.3s）。
  2. 图片 160x160px，水平居中。
  3. 商品标题（`<h3>`）：16px，颜色 `#333`，单行溢出省略。
  4. 商品描述（`<p>`）：14px，颜色 `#b0b0b0`，单行溢出省略。
  5. 价格区：现价 `#ff6700`（16px），原价 `#b0b0b0`（14px，删除线）。


## 六、代码片段（常用模板，拷贝即用）
### 1. 选择器与样式基础
```css
/* 1. 导航栏样式（关系选择器） */
.nav {
  width: 1200px;
  margin: 0 auto;
}
.nav ul li {
  float: left;
  margin: 0 15px;
}
.nav ul li a {
  color: #333;
  text-decoration: none;
  transition: color 0.3s;
}
.nav ul li a:hover {
  color: #ff6700;
}

/* 2. 链接伪类（LVHA 顺序） */
a:link { color: #333; text-decoration: none; }
a:visited { color: #666; }
a:hover { color: #ff6700; text-decoration: underline; }
a:active { color: #f00; }
```

### 2. 盒子模型与初始化
```css
/* 1. 全局初始化（border-box + 清边距） */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
ul { list-style: none; }
a { text-decoration: none; color: #333; }

/* 2. 块级元素水平居中 */
.container {
  width: 1200px;
  margin: 0 auto;
}

/* 3. 单行文字溢出省略 */
.single-ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 4. 多行文字溢出省略（WebKit 内核） */
.multi-ellipsis {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
  text-overflow: ellipsis;
}
```

### 3. 背景与美化
```css
/* 1. 背景图片 + 居中覆盖 */
.banner {
  width: 100%;
  height: 400px;
  background: url(banner.jpg) no-repeat center/cover;
}

/* 2. 线性渐变（按钮） */
.btn {
  width: 120px;
  height: 40px;
  background: linear-gradient(to right, #ff6700, #f90);
  color: #fff;
  border: none;
  border-radius: 20px;
  cursor: pointer;
}

/* 3. 盒子阴影 + 过渡 */
.card {
  width: 240px;
  padding: 20px;
  border-radius: 8px;
  transition: box-shadow 0.3s;
}
.card:hover {
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}
```

### 4. 字体图标引入（iconfont）
```html
<!-- 1. 引入 iconfont.css -->
<link rel="stylesheet" href="./iconfont/iconfont.css">

<!-- 2. 使用图标 -->
<i class="iconfont icon-gouwuche" style="color: #ff6700; font-size: 20px;"></i>
```


## 八、复习计划（建议周期化）
### 1. 每周（30 分钟）
- 回顾“核心概念速查”，重点记忆选择器权重、盒子模型 `box-sizing`、margin 问题解决方案。
- 完成 1 个“10 分钟任务”，如写选择器组合或盒子模型样式，验证是否掌握核心属性。

### 2. 每两周（2 小时）
- 完成 1 个“1 小时任务”，如制作商品卡片或导航栏，重点练习 hover 过渡、溢出省略、阴影效果。
- 整理本周遇到的错误（如路径、选择器权重），记录到错题本，避免重复踩坑。

### 3. 每月（半天）
- 做 1 个综合案例（如“淘宝风格导航栏 + 商品列表”），整合选择器、盒子模型、背景美化、字体图标，检验综合应用能力。
- 用浏览器调试工具（F12）检查盒子模型和选择器权重，修复样式冲突。


## 九、自测题（检验掌握情况）
1. 请计算选择器 `#nav .item li a` 的权重，并说明权重叠加规则。
2. `box-sizing: content-box` 和 `border-box` 的核心区别是什么？为什么推荐全局使用 `border-box`？
3. 子元素 `margin-top` 导致父元素下移（margin 塌陷），有哪 3 种解决方案？
4. 链接伪类的正确书写顺序是什么？为什么要遵循这个顺序？
5. 实现“单行文字溢出显示省略号”需要哪些 CSS 属性？请写出完整代码。
6. 如何用 CSS 实现“水平线性渐变（左橙右蓝）”的按钮，且 hover 时渐变方向反转？


## 十、复习小贴士
1. **善用浏览器调试工具**：右键页面→“检查”，在 Elements 面板查看盒子模型（Layout 标签）、选择器权重（Styles 面板），实时修改样式验证效果，快速定位问题。
2. **优先使用 `border-box`**：全局设置 `box-sizing: border-box`，避免 padding 和 border 撑大盒子，减少尺寸计算麻烦。
3. **整理“常用代码模板”**：将选择器组合、溢出省略、背景渐变等高频代码整理到文档，复习时直接复用，强化记忆。
4. **“动手写”比“看”更有效**：不要只看笔记，每次复习都动手写代码，比如故意写错选择器顺序，观察效果后修复，加深对优先级的理解。
5. **结合实战案例**：学完模块后立即做对应案例（如学完盒子模型做小米卡片），将理论转化为实操，避免“眼会手不会”。