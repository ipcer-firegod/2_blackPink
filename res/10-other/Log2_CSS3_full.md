# CSS3 全面学习笔记（详细版）

> 目标：在 Log2_CSS3.md 的精简速查基础上，扩展为一份全面、可操作的 CSS3 学习手册，包含详解、代码示例、兼容性/性能提示、常见陷阱与练习。适合中级学习者在系统复习与实战中使用。

更新时间：2025-10-10
来源：课程资料《CSS3核心技术》（整理）

---

## 一、为什么选择这个方案（简要）
- 基于精简速查扩展可以保持结构清晰，便于复习，同时补充必要的细节与示例，兼顾“速记”和“实战”。
- 直接从 PDF 逐字展开会产出内容冗长且复习效率低；而用速查做索引再扩展能更好地服务不同复习节奏的需求。

## 二、文档结构（便于导航）
- 选择器与优先级
- 盒模型与布局基础
- 弹性布局（Flex）详解
- 网格布局（Grid）详解
- 背景、渐变、边框与阴影
- 文本、字体与排版
- 响应式设计与单位
- 过渡、变换与动画
- CSS 自定义属性、函数与逻辑
- 可访问性、性能与兼容性
- 练习与复习计划

---

## 三、选择器与优先级（详解＋示例）
### 1. 基础选择器
- 元素选择器：div, p, a
  - 示例：
```css
p { color: #333; }
```
- 类选择器（.class）与 id 选择器（#id）：类更灵活，id 优先级更高但不建议频繁使用。
  - 示例：
```css
.btn { padding: 8px 12px; }
#submit { background: blue; }
```
- 属性选择器：
```css
input[type="text"] { border: 1px solid #ddd; }
a[target="_blank"] { color: red; }
```

### 2. 组合选择器
- 后代（A B） vs 子代（A > B）：
  - A B 会匹配任何后代，性能略差于 A > B（子代）
- 相邻兄弟（A + B） vs 通用兄弟（A ~ B）
  - 示例：
```css
h2 + p { margin-top: 0; }
```

### 3. 伪类与伪元素
- 伪类：:hover, :active, :focus, :nth-child(n)
- 伪元素：::before, ::after（用于添加装饰性内容）
  - 示例：
```css
.button::after { content: ""; display: inline-block; width: 8px; height: 8px; background: #333; }
```

### 4. 优先级与冲突解决
- 计算规则简化：内联(1000) > id(100) > class/attr/pseudo-class(10) > element/pseudo-element(1)
- !important：会覆盖正常优先级，但会引入维护难度，慎用。可以用 specificity 和组织结构解决。
- 调试技巧：使用浏览器 DevTools 查看元素计算样式（Computed）并定位冲突来源。

### 5. 性能注意点
- 选择器从右到左匹配，避免使用过于复杂或低效的选择器（如前缀选择器过多层次）
- 使用类选择器作为主力，既清晰又高效

---

## 四、盒模型（Box model）详解
### 1. 概念
- content（内容）→ padding → border → margin
- width/height 默认只影响 content（content-box）

### 2. box-sizing
- content-box（默认）：width=content
- border-box（推荐）：width=content+padding+border（更易于布局控制）
  - 常用全局设置：
```css
*, *::before, *::after { box-sizing: border-box; }
```

### 3. 外边距塌陷（margin collapse）
- 情形：相邻块级元素垂直方向的 margin 会合并为较大者
- 解决方式：使用 padding、边框、overflow 或者设置父元素为 flex 等
  - 示例：
```css
.parent { overflow: auto; }
.child { margin-top: 20px; }
```

### 4. 盒模型常见错误
- 在布局中混合使用 box-sizing 导致宽度不符合预期。建议全局统一设置为 border-box。

---

## 五、布局基础（display）与常见模式
### 1. display 类型
- block、inline、inline-block、none、flex、grid
- inline-block 与 inline 的差异：inline-block 可以设置宽高

### 2. 流式布局、浮动（legacy）、定位（position）简述
- 流式布局为默认文档流
- 浮动用于文字环绕与简单布局（老方法，但仍需理解）
- 定位：static、relative、absolute、fixed、sticky（sticky 在实际中非常实用）

---

## 六、Flex 布局（深入）
### 1. 基本概念
- 容器（display:flex）与主轴（main axis）/交叉轴（cross axis）
- 常用容器属性：flex-direction, justify-content, align-items, flex-wrap, gap
- 项目属性：order, flex-grow, flex-shrink, flex-basis (简写 flex)

### 2. 常见用法与示例
- 居中：
```css
.container { display:flex; justify-content:center; align-items:center; }
```
- 等分列：
```css
.item { flex: 1; }
```
- 横向溢出换行：
```css
.container { display:flex; flex-wrap:wrap; gap:12px; }
```

### 3. 常见坑与性能
- 使用 min-height 与 align-items: center 组合时，子元素可能影响容器高度；调试时用 devtools 查看每个元素的 box model
- Flex 布局本身性能良好，但频繁改变 DOM 或触发重排时仍会有开销

---

## 七、Grid 布局（深入）
### 1. 基本概念
- 二维布局系统：行（rows）与列（columns）同时控制
- 核心属性：grid-template-columns, grid-template-rows, gap, grid-auto-flow, grid-area

### 2. 常见示例
- 两栏布局：
```css
.container { display:grid; grid-template-columns: 1fr 3fr; gap: 16px; }
```
- 响应式栅格：
```css
.container { display:grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px; }
```

### 3. 影响可访问性的注意
- 使用 grid 布局时保持 DOM 顺序的语义，避免只通过视觉顺序传递重要信息

---

## 八、背景、边框、圆角与阴影
### 1. 背景
- background-image 支持多层（逗号分隔）
- background-size: cover|contain|auto
- 线性/径向渐变（linear-gradient、radial-gradient）可作为背景图片
  - 示例：
```css
.header { background: linear-gradient(90deg,#fff,#f0f0f0); }
```

### 2. 边框与圆角
- border-radius 简明：四角可分别设置
- 边框合并及边框样式（solid/dashed等）

### 3. 阴影
- box-shadow: x y blur spread color
  - 示例：
```css
.card { box-shadow: 0 6px 18px rgba(0,0,0,0.08); }
```

### 4. 性能和兼容
- box-shadow 在大型元素或大量阴影时可能影响渲染性能；尽量使用简洁的阴影或使用图片替代

---

## 九、文本、字体与排版
### 1. 字体加载与性能
- webfont 加载策略：font-display（swap/fallback/optional）影响首屏渲染
- preload 与 link rel=preload 可提升字体加载速度

### 2. 文字样式
- line-height 使用无单位值能按字体缩放
- text-rendering 和 font-smoothing 可微调渲染效果（浏览器差异）

### 3. 文本溢出与排版技巧
- 单行省略号：white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
- 多行省略方案（webkit-line-clamp）兼容性需注意

---

## 十、响应式设计与单位
### 1. 常见单位
- px、%（相对容器）、em（相对父字体）、rem（相对根字体）、vw/vh
- 推荐：布局使用 rem/vw，组件内间距使用 rem，避免全部用 px

### 2. 媒体查询与移动优先
- 移动优先策略：先写基础样式（手机），再使用 min-width 增加样式
- 示例：
```css
.card { width:100%; }
@media (min-width: 768px) { .card{ width:48%; } }
```

### 3. 复杂布局的适配策略
- 使用容器查询（container queries，部分浏览器已支持）作为进阶方案
- 使用 clamp() 与 min()/max() 做流式字体与尺寸

---

## 十一、过渡、变换与动画（性能与制作）
### 1. transition（过渡）
- 语法：transition: property duration timing-function delay
- 示例：
```css
.btn { transition: transform 0.2s ease, box-shadow 0.2s ease; }
.btn:hover { transform: translateY(-2px); box-shadow: 0 6px 14px rgba(0,0,0,0.12); }
```

### 2. transform（变换）
- transform: translate/scale/rotate/skew；合并 transform 提升性能
- 尽量动画 transform 与 opacity，避免触发布局（width/height/top/left）

### 3. animation（关键帧动画）
- @keyframes 控制复杂动画
- animation-fill-mode 控制动画结束状态

### 4. 性能建议
- 使用 will-change 提示渲染器优化，但慎用；只在短时和关键元素使用
- 使用 GPU 加速（transform: translateZ(0) 等），但会增加显存开销

---

## 十二、CSS 自定义属性（变量）、函数与计算
### 1. 变量（Custom Properties）
- 声明与用法：
```css
:root { --main: #09f; }
.btn { background: var(--main); }
```
- 变量的作用域与继承：变量遵循 DOM 树的级联与继承，可以通过 JS 动态修改

### 2. 常用函数
- calc()：动态计算长度
- clamp(min, val, max)：限制在区间内
- min()/max()：取最小/最大值

### 3. 应用示例
- 流式间距：padding: calc(var(--gap) * 1.5);
- 字体自适应：font-size: clamp(14px, 1.6vw, 18px);

---

## 十三、高级视觉：滤镜、混合模式、裁剪
- filter: blur()/grayscale()/drop-shadow() 等
- mix-blend-mode: 多层元素混合效果
- clip-path: 非矩形裁剪（注意兼容性）

---

## 十四、可访问性、兼容性与性能实战建议
### 1. 可访问性（A11Y）
- 为图片加 alt，表单加 label，使用语义化标签（header/nav/main/footer），为动态内容提供公告（aria-live）
- 使用合理的 contrast（WCAG 对比度标准）

### 2. 兼容性
- 使用 Autoprefixer 构建生产代码，避免手写前缀
- 对于新特性（container queries、subgrid 等），加 feature-detection 或回退

### 3. 性能
- 减少重排与重绘：避免频繁读写 layout（getComputedStyle 后立即修改样式）
- 合理使用 CSS 动画（transform/opacity）与 will-change
- 精简样式表，使用按需加载与 critical CSS 技术

---

## 十五、练习题与任务（实战练习）
1. 30 分钟：写一个卡片组件（图片、标题、描述、按钮），实现 hover 动画与响应式单列→多列
2. 2 小时：用 Grid 实现一个响应式画廊，图片按比例自适应并带懒加载
3. 半天：重做课程中的 "36-盒子模型综合案例-小米卡片.html"，把样式替换成 CSS 变量并实现主题切换

---

## 十六、附录 — 常用代码片段与模板
- 全局 box-sizing：
```css
*, *::before, *::after { box-sizing: border-box; }
```
- 单行省略号：
```css
.ellipsis { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
```
- flex 居中：
```css
.center { display:flex; justify-content:center; align-items:center; }
```

---

如果你希望：
- 我把这份文档加到 `00-StudyLog/index.html` 的 CSS 部分（作为完整版链接）；
- 或者我把精简版和完整版分别归档到 `appendix/` 文件夹并更新索引；
告诉我你的偏好，我会继续操作。