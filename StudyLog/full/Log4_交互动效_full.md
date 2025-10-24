# CSS 交互动效设计学习笔记
## 一、核心概述
CSS 交互动效是通过 `transform`（变换）和 `animation`（动画）实现元素动态视觉效果的技术，核心优势是**不破坏文档流、GPU 加速渲染、代码简洁**，广泛用于按钮悬停、卡片翻转、加载动画、页面过渡等场景。


## 二、变换（transform）—— 动效基础
`transform` 支持 2D/3D 变换，通过函数控制元素的位置、角度、尺寸和形状，仅视觉上改变元素状态，不影响文档流布局。


### 1. 坐标系基础
无论是 2D 还是 3D 变换，都依赖坐标系定位，需先明确坐标方向：
- **2D 坐标系**：
  - X 轴：水平方向，右为正，左为负。
  - Y 轴：垂直方向，下为正，上为负。
- **3D 坐标系**（左手法则记忆）：
  - X 轴/ Y 轴：同 2D。
  - Z 轴：垂直屏幕方向，靠近屏幕为正（元素放大），远离为负（元素缩小）。


### 2. 2D 变换（核心常用）
2D 变换是基础，包含平移、旋转、缩放、倾斜四类核心函数，需掌握语法、作用及场景：

| 变换类型 | 函数语法                          | 核心描述                                                                 | 应用场景                          | 注意事项                                  |
|----------|-----------------------------------|--------------------------------------------------------------------------|-----------------------------------|-------------------------------------------|
| 平移     | `translate(x,y)`<br>`translateX(x)`<br>`translateY(y)` | 沿 X/Y 轴移动，参数支持 `px` 或百分比（百分比相对于**元素自身尺寸**）       | 元素微调、悬停偏移、水平垂直居中    | 百分比相对自身，非父容器；配合 `top:50%;left:50%` 实现居中（`translate(-50%,-50%)`） |
| 旋转     | `rotate(angle)`<br>`transform-origin: 基点` | 以基点顺时针旋转，单位 `deg`（负值逆时针）；`transform-origin` 控制旋转中心（如 `left top`、`50% 50%`） | 图标旋转、卡片翻转、加载动画        | 行内元素需转为 `inline-block`/`block` 才生效 |
| 缩放     | `scale(sx,sy)`<br>`scaleX(sx)`<br>`scaleY(sy)` | 沿 X/Y 轴按比例缩放，单参数时等比例（`>1` 放大，`<1` 缩小）               | 悬停放大、焦点突出、按钮点击反馈    | 不改变元素占位，仅视觉缩放                |
| 倾斜     | `skew(x-angle,y-angle)`<br>`skewX(angle)`<br>`skewY(angle)` | 沿 X/Y 轴扭曲元素，参数为倾斜角度（负值反向倾斜）                         | 斜切导航栏、动态图表装饰            | 倾斜后元素形状改变，需注意布局兼容性      |

#### 关键补充：2D 变换复合写法
多个变换函数组合使用时，**执行顺序从右到左**（右侧函数先执行）：
```css
/* 先旋转45deg，再平移100px（而非先平移再旋转） */
.transform {
  transform: translate(100px) rotate(45deg);
}
```


### 3. 3D 变换（实现立体效果）
3D 变换在 2D 基础上增加 Z 轴维度，核心是「透视」和「3D 空间保留」，常用于卡片翻转、3D 轮播等场景。

#### 3.1 核心属性与函数
| 核心知识点          | 语法/函数                          | 作用说明                                                                 |
|---------------------|-----------------------------------|--------------------------------------------------------------------------|
| 透视（近大远小）    | `perspective: 1000px`（父元素）<br>`transform: perspective(1000px)`（子元素） | 模拟人眼视角，数值越小透视越强；父元素添加时，所有子元素生效；子元素添加时需作为 `transform` 第一个函数 |
| 3D 旋转             | `rotateX(angle)`<br>`rotateY(angle)`<br>`rotateZ(angle)` | 沿 X/Y/Z 轴旋转，`rotateZ` 同 2D 的 `rotate`；正值方向遵循左手法则       |
| 3D 位移             | `translate3d(x,y,z)`<br>`translateZ(z)` | 沿 3D 轴平移，`translateZ(z)` 需配合 `perspective` 才显效果（z 正→放大） |
| 保留 3D 空间         | `transform-style: preserve-3d`（父元素） | 让子元素保留 3D 位置，避免被压平（默认 `flat` 压平）；实现 3D 卡片必需   |
| 隐藏元素背面         | `backface-visibility: hidden`（子元素） | 隐藏元素背面（默认镜像显示），用于卡片翻转时隐藏背面内容（如扑克牌效果）    |

#### 3.2 经典案例：3D 卡片翻转
```css
/* 父容器：透视 + 3D 空间 */
.card-container {
  perspective: 1000px;
  transform-style: preserve-3d;
}
/* 卡片：添加过渡 */
.card {
  transition: transform 0.5s;
  position: relative;
  width: 300px;
  height: 200px;
}
/* 正面/背面：定位 + 隐藏背面 */
.card-front, .card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
}
/* 背面：初始翻转 */
.card-back {
  transform: rotateY(180deg);
}
/*  hover 时翻转卡片 */
.card-container:hover .card {
  transform: rotateY(180deg);
}
```


### 4. 过渡进阶（transition）
`transition` 用于让变换效果平滑过渡，避免瞬间切换，完整语法：
```css
/* 过渡属性 时长 速度曲线 延迟时间 */
transition: all 1s ease 0.5s;
```

#### 关键参数：速度曲线
| 速度曲线        | 效果描述                                                                 | 适用场景                  |
|-----------------|--------------------------------------------------------------------------|---------------------------|
| `ease`（默认）  | 慢速开始 → 加速 → 慢速结束，自然过渡                                      | 按钮悬停、元素偏移        |
| `linear`        | 匀速运动，无加速/减速                                                    | 进度条、机械感动画        |
| `ease-in-out`   | 慢速开始 + 慢速结束，对称过渡                                            | 页面切换、弹窗动画        |
| `cubic-bezier(x1,y1,x2,y2)` | 自定义贝塞尔曲线（通过 [cubic-bezier.com](https://cubic-bezier.com) 可视化编辑） | 创意动效（弹跳、骤停）    |


## 三、动画（animation）—— 复杂动效核心
`animation` 解决 `transition` 仅支持“两帧状态”的局限，通过「关键帧（@keyframes）」定义多帧状态，实现复杂动画（如加载、逐帧动画）。

（我感觉就是 把多个transform连起来做动画，每一个transform都对应一个关键帧，然后通过动画播放）

### 1. 核心流程：先定义关键帧，再使用动画
#### 1.1 定义关键帧（@keyframes）
通过百分比或 `from/to` 定义动画的关键状态（中间帧由浏览器自动生成）：
```css
/* 方式1：from（0%）→ to（100%），适合简单两帧 */
@keyframes move {
  from { transform: translateX(0); }
  to { transform: translateX(200px); }
}

/* 方式2：多关键帧，适合复杂动画 */
@keyframes flash {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}
```

#### 1.2 使用动画（animation 属性）
`animation` 是复合属性，**动画名称和时长为必写项**，其他属性可选但需遵循顺序：
```css
/* 动画名称 时长 速度曲线 延迟 播放次数 方向 填充模式 播放状态 */
.animate {
  animation: move 2s linear 0.5s infinite alternate forwards running;
}
```

#### 关键子属性详解
| 子属性                | 默认值       | 说明                                                                 |
|-----------------------|--------------|----------------------------------------------------------------------|
| `animation-name`      | -            | 关联的关键帧名称（必写）                                              |
| `animation-duration`  | 0s           | 动画时长（必写，如 `1s`、`300ms`）                                      |
| `animation-timing-function` | `ease` | 速度曲线，支持 `steps(n)`（逐帧动画，`n` 为步数）                     |
| `animation-delay`     | 0s           | 延迟执行时间，支持负值（跳过前 N 时间的动画，如 `-0.5s`）              |
| `animation-iteration-count` | `1`    | 播放次数，`infinite` 表示无限循环                                    |
| `animation-direction` | `normal`     | 播放方向：`reverse`（反向）、`alternate`（交替：正→反→正...）          |
| `animation-fill-mode` | `none`       | 动画结束后状态：`forwards`（保留最后一帧）、`backwards`（回到第一帧）  |
| `animation-play-state` | `running`   | 播放状态：`paused`（暂停），需通过 JS 控制（如 `element.style.animationPlayState = 'paused'`） |


### 2. 重点：逐帧动画（steps 函数）
逐帧动画通过 `steps(n)` 将动画分割为 `n` 个离散步骤，无平滑过渡，适合精灵图（多个小图合成一张）动画。

#### 2.1 原理
1. 精灵图包含 `n` 个连续小图（如 25 个加载帧）。
2. 动画中通过 `background-position` 移动精灵图，每次移动一个小图宽度。
3. `steps(n)` 步数 = 小图数量，确保每步对应一个小图。

#### 2.2 示例：精灵图加载动画
```css
/* 1. 定义关键帧：移动背景位置（总宽度 = 小图宽度 × 数量） */
@keyframes load {
  0% { background-position: 0 0; }
  100% { background-position: -13700px 0; } /* 精灵图总宽13700px，25个小图 */
}

/* 2. 使用动画：steps(25) 对应25个小图 */
.loader {
  width: 548px; /* 单个小图宽度 */
  height: 513px; /* 单个小图高度 */
  background: url(loader-sprite.png) no-repeat;
  animation: load 1s steps(25) infinite; /* 1秒完成25步，无限循环 */
}
```


## 四、典型动效案例与新知识
### 1. 流光渐变边框（高频场景）
#### 原理
通过“父容器 + 渐变子元素 + 内容子元素”实现，利用定位和 `z-index` 遮挡，渐变子元素做旋转/平移动画：
```css
/* 父容器：定位 */
.btn {
  position: relative;
  width: 200px;
  height: 60px;
  border-radius: 30px;
  overflow: hidden;
}
/* 渐变子元素：旋转动画 */
.btn-gradient {
  position: absolute;
  top: 0; left: 0;
  width: 200%; height: 100%;
  background: linear-gradient(115deg, #4fcf70, #fad648, #a767e5);
  animation: rotate 2s linear infinite;
}
/* 内容子元素：白色背景遮挡，只露边框 */
.btn-content {
  position: absolute;
  top: 3px; left: 3px; right: 3px; bottom: 3px; /* inset:3px 简写 */
  background: #fff;
  border-radius: 27px;
  z-index: 1; /* 高于渐变层 */
}
/* 渐变旋转关键帧 */
@keyframes rotate {
  0% { transform: translateX(-50%); }
  100% { transform: translateX(50%); }
}
```
#### 新知识：`inset` 属性
`inset: 3px` 等价于 `top:3px; left:3px; right:3px; bottom:3px`，简化定位写法。


### 2. 元素倒影（视觉增强）
通过 `box-reflect` 实现元素倒影，常用于图片、按钮增强视觉效果（需加 `-webkit-` 兼容）：
```css
.reflection {
  /* 方向（below=下方） 距离（1px） 渐变过渡（避免生硬） */
  -webkit-box-reflect: below 1px linear-gradient(transparent, rgba(0,0,0,0.2));
}
```
#### 语法说明
- 方向：`above`（上）、`below`（下，常用）、`left`（左）、`right`（右）。
- 距离：倒影与元素的间距（如 `1px`、`10px`）。
- 渐变：可选，用于实现倒影“从清晰到透明”的过渡。


### 3. 毛玻璃效果（背景模糊）
通过 `backdrop-filter: blur(px)` 模糊元素背后的内容，常用于弹窗、导航栏：
```css
.modal {
  background: rgba(255,255,255,0.8);
  backdrop-filter: blur(10px); /* 模糊半径10px，数值越大越模糊 */
}
```


### 4. 父选择器 `:has()`
`has()` 允许“根据子元素状态反向选择父元素”，实现交互联动（如 hover 子元素改变父元素布局）：
```css
/* 当 .nav 包含 hover 的 .item 时，修改 grid 列宽 */
.nav:has(.item:hover) {
  grid-template-columns: 2fr 1fr 1fr; /* hover 的 item 占2份，其他1份 */
}
```


## 五、核心重点总结
1. **transform 关键**：
   - 2D 变换：`translate` 居中、`rotate` 基点、`scale` 比例、`skew` 倾斜。
   - 3D 变换：父元素 `perspective + transform-style: preserve-3d`，子元素 `backface-visibility: hidden`。
   - 复合顺序：从右到左执行。

2. **animation 关键**：
   - 关键帧 `@keyframes` 定义多帧状态。
   - `steps(n)` 实现逐帧动画，步数 = 精灵图小图数量。
   - 必写属性：动画名称 + 时长。

3. **实用案例技巧**：
   - 流光边框：渐变 + 定位 + 动画。
   - 倒影：`box-reflect` + 渐变过渡。
   - 毛玻璃：`backdrop-filter: blur()`。

4. **性能提示**：
   - 优先使用 `transform` 和 `opacity` 做动画（GPU 加速），避免修改 `width`/`top` 等触发布局的属性。