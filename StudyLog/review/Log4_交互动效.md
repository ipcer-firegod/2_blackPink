# 交互动效设计核心知识复习记录
## 一、本文档目的
- 将交互动效的核心技术（`transform` 变换、`transition` 过渡、`animation` 动画、3D 效果、实战案例）提炼为速查式笔记，适配 10 分钟碎片化回顾与 1 小时集中复习，攻克“变换顺序混乱”“3D 效果失效”“动画不流畅”等痛点。
- 提供可落地的实战练习与周期化复习计划，帮助将理论转化为实操能力，重点强化“变换+过渡+动画”的组合应用，避免“学完就忘”。


## 二、宏观结构（快速导航）
- 变换核心（2D 变换：平移/旋转/缩放/倾斜；3D 变换：坐标系/透视/旋转/位移）
- 过渡（`transition`：速度曲线、完整写法）
- 动画（`animation`：关键帧、逐帧动画、属性详解）
- 3D 专项（透视、`transform-style`、`backface-visibility`）
- 动效案例（流光边框、3D 卡片翻转、倒影效果）
- 辅助技术（`backdrop-filter`、`:has()` 选择器、`:not()` 选择器）


## 三、核心概念速查（记忆卡）
### 1. 2D 变换（`transform`）
通过函数改变元素平面位置、角度、尺寸，不破坏文档流，核心是“视觉变换，占位不变”。

| 变换类型 | 函数语法                  | 核心规则                                  | 应用场景                          |
|----------|---------------------------|-------------------------------------------|-----------------------------------|
| 平移     | `translate(x,y)`/`translateX(x)`/`translateY(y)` | 参数支持 `px` 或百分比（百分比相对元素自身）；`translate(-50%,-50%)` 配合 `top:50%;left:50%` 实现居中 | 悬停偏移、元素居中                |
| 旋转     | `rotate(angle)`           | 单位 `deg`（正值顺时针，负值逆时针）；`transform-origin` 改旋转基点（如 `left top`） | 图标旋转、加载动画                |
| 缩放     | `scale(sx,sy)`/`scaleX(sx)`/`scaleY(sy)` | 单参数等比缩放（`scale(1.2)` 放大 20%）；`sx/sy>1` 放大，`<1` 缩小 | 悬停放大、焦点突出                |
| 倾斜     | `skew(x-angle,y-angle)`/`skewX/Y(angle)` | 单参数时 Y 轴默认 0；`transform-origin` 改倾斜基点 | 斜切导航栏、动态装饰元素          |
| 复合写法 | `transform: A() B() C()`   | 执行顺序：**从右到左**（先 C()，再 B()，最后 A()） | 复杂动效（如“平移+旋转”）          |


### 2. 3D 变换（`transform`）
在 2D 基础上增加 Z 轴，实现立体效果，核心是“透视+3D 空间保留”。
- **三维坐标系**（左手法则）：
  - X 轴：左右（右正左负）
  - Y 轴：上下（下正上负）
  - Z 轴：远近（近正远负）
- **关键属性**：
  | 属性/函数                | 作用                                  | 注意事项                          |
  |--------------------------|---------------------------------------|-----------------------------------|
  | `perspective: 1000px`    | 模拟人眼透视（近大远小），给父元素添加 | 数值越小，透视越强                |
  | `rotateX(angle)`/`rotateY(angle)` | 沿 X/Y 轴旋转（立体翻转）              | `rotateZ` 同 2D `rotate`          |
  | `transform-style: preserve-3d` | 保留子元素 3D 位置，不压平            | 父元素必加，否则 3D 效果失效      |
  | `backface-visibility: hidden` | 隐藏元素背面（避免翻转时显示镜像）    | 3D 卡片翻转必加                  |
  | `translate3d(x,y,z)`      | 3D 平移（Z 轴值影响大小）              | 需配合 `perspective` 生效         |


### 3. 过渡（`transition`）
让属性变化平滑过渡，避免瞬间切换，常与 `transform` 搭配。
- **完整写法**：`transition: 过渡属性 时长 速度曲线 延迟`  
  示例：`transition: all 0.3s ease 0.1s`（所有属性过渡，0.3 秒，自然曲线，延迟 0.1 秒）
- **常用速度曲线**：
  | 曲线参数          | 效果                                  | 场景                          |
  |-------------------|---------------------------------------|-------------------------------|
  | `ease`（默认）    | 慢→快→慢                              | 按钮悬停                      |
  | `linear`          | 匀速                                  | 进度条、机械动画              |
  | `cubic-bezier(x1,y1,x2,y2)` | 自定义曲线（通过 [cubic-bezier.com](https://cubic-bezier.com) 编辑） | 创意动效（弹跳、骤停）        |


### 4. 动画（`animation`）
解决过渡“仅两帧”的局限，通过关键帧实现多状态动画，支持循环、反向播放。
#### （1）核心流程：先定义关键帧，再使用动画
- **定义关键帧**：
  ```css
  /* 方式1：百分比（多帧） */
  @keyframes move {
    0% { transform: translateX(0); }
    50% { transform: translateX(100px) rotate(45deg); }
    100% { transform: translateX(200px); }
  }
  /* 方式2：from/to（两帧） */
  @keyframes fade {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  ```
- **使用动画**：`animation: 名称 时长 速度曲线 延迟 次数 方向 结束状态`  
  必写项：**动画名称 + 时长**，示例：`animation: move 2s linear infinite alternate forwards`（无限循环，交替方向，保留最后一帧）

#### （2）逐帧动画（`steps` 函数）
用于精灵图动画，将动画分割为离散步骤，无平滑过渡：
- **语法**：`animation: 名称 时长 steps(步数) 循环`  
- **原理**：精灵图含 N 个帧，`steps(N)` 对应 N 步，通过 `background-position` 移动帧图像。
- **示例**：精灵图有 8 帧，`animation: run 1s steps(8) infinite`。


## 四、常见错误与陷阱（高频）
1. **transform 复合顺序搞反**：
   - 错误：`transform: rotate(45deg) translate(100px)` 认为“先旋转再平移”，实际执行顺序是“先平移再旋转”（从右到左）。
   - 解决：明确需求，如需“先旋转再平移”，应写 `transform: translate(100px) rotate(45deg)`。

2. **行内元素旋转/缩放无效**：
   - 错误：给 `<span>` 直接加 `transform: rotate(45deg)`，因行内元素无法设置宽高、transform 基准异常，效果混乱。
   - 解决：先将行内元素转为 `inline-block` 或 `block`（如 `span { display: inline-block; }`）。

3. **3D 效果失效**：
   - 错误：仅给子元素加 `rotateY(45deg)`，未给父元素加 `perspective` 和 `transform-style: preserve-3d`，无立体效果。
   - 解决：父元素必加 `perspective: 1000px; transform-style: preserve-3d;`，子元素加 3D 变换。

4. **animation 动画不生效**：
   - 错误：漏写 `@keyframes` 关键帧，或 `animation` 漏写“动画名称”“时长”。
   - 解决：确保先定义关键帧，`animation` 至少包含“名称+时长”（如 `animation: move 2s;`）。

5. **逐帧动画 steps 步数不匹配**：
   - 错误：精灵图有 25 帧，`steps(20)`，导致动画缺失帧或重复。
   - 解决：`steps(步数)` 必须与精灵图帧数一致，且 `background-position` 移动距离=单帧宽度×帧数。


## 五、快速练习（把知识变成肌肉记忆）
### 1. 10 分钟任务（基础回顾）
- 任务 1：2D 悬停效果——按钮 hover 时向右平移 10px + 放大 1.1 倍 + 过渡 0.3s，用 `transform`+`transition` 实现。
- 任务 2：3D 卡片翻转——创建正面/背面卡片，父元素加透视和 3D 空间，hover 时父元素 `rotateY(180deg)`，子元素加 `backface-visibility: hidden`。

### 2. 1 小时任务（综合应用）
- 需求：制作“精灵图加载动画+流光边框按钮”组合效果：
  1. 精灵图加载：10 帧精灵图，用 `animation`+`steps(10)` 实现无限循环旋转。
  2. 流光边框按钮：3 层嵌套（父容器+渐变层+文字层），渐变层用 `animation` 旋转，配合 `inset` 定位和 `z-index: -1`。


## 六、代码片段（常用模板，拷贝即用）
### 1. 2D 元素水平垂直居中（transform+定位）
```css
.center-box {
  position: absolute;
  top: 50%;
  left: 50%;
  /* 基于自身尺寸偏移，无需知宽高 */
  transform: translate(-50%, -50%);
  width: 200px;
  height: 200px;
  background: pink;
}
```

### 2. 3D 卡片翻转（核心代码）
```css
/* 父容器：透视+3D空间 */
.card-container {
  perspective: 1000px;
  transform-style: preserve-3d;
  width: 300px;
  height: 400px;
}
/* 卡片：过渡+定位 */
.card {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}
/* 正面/背面：隐藏背面+定位 */
.card-front, .card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden; /* 隐藏背面 */
  border-radius: 8px;
}
.card-back {
  transform: rotateY(180deg); /* 初始翻转背面 */
  background: #ff6700;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}
/* hover 翻转卡片 */
.card-container:hover .card {
  transform: rotateY(180deg);
}
```

### 3. 逐帧动画（精灵图示例，8 帧）
```css
/* 容器：固定尺寸（单帧尺寸） */
.sprite-box {
  width: 100px;
  height: 100px;
  background: url(./sprite.png) no-repeat; /* 精灵图 */
  animation: run 1s steps(8) infinite; /* 8 帧，无限循环 */
}
/* 关键帧：移动背景位置（总距离=单帧宽度×帧数） */
@keyframes run {
  0% { background-position: 0 0; }
  100% { background-position: -800px 0; } /* 单帧100px，8帧=800px */
}
```

### 4. 流光渐变边框按钮
```css
/* 父容器：定位 */
.btn {
  position: relative;
  width: 200px;
  height: 60px;
  border-radius: 30px;
  overflow: hidden;
}
/* 渐变层：旋转动画 */
.btn-gradient {
  position: absolute;
  inset: -2px; /* 等价 top/left/right/bottom: -2px */
  background: linear-gradient(45deg, #4fcf70, #fad648, #a767e5);
  animation: rotate 2s linear infinite;
  z-index: -1; /* 被文字层遮挡 */
}
/* 文字层：白色背景遮挡中间 */
.btn-text {
  position: absolute;
  inset: 2px;
  background: #fff;
  border-radius: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}
/* 渐变旋转关键帧 */
@keyframes rotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
```


## 八、复习计划（建议周期）
### 1. 每周（30 分钟）
- 回顾“核心概念速查”，重点记忆 2D 变换函数、3D 效果三要素（perspective、transform-style、backface-visibility）、animation 关键帧写法。
- 完成 1 个“10 分钟任务”，如 3D 卡片翻转，记录 3D 效果失效的排查过程（是否加透视、是否保留 3D 空间）。

### 2. 每两周（2 小时）
- 完成 1 个“1 小时任务”，如精灵图逐帧动画+流光边框，整合 `transform`+`animation`+`transition`，练习多技术组合。
- 用浏览器调试工具（Elements→Animations）查看动画帧，调整速度曲线（如将 `ease` 改为 `cubic-bezier` 自定义曲线）。

### 3. 每月（半天）
- 做 1 个综合案例：“3D 导航栏+滚动触发动画”，包含：
  - 3D 导航：子元素 `translateZ`+父元素 `rotateX`，hover 时 `translateZ` 增大。
  - 滚动触发：结合 JS 监听滚动，当元素进入视口时触发 `animation`（如 `fadeIn` 动画）。
- 总结案例中遇到的兼容性问题（如 `box-reflect` 加 `-webkit-`），整理解决方案。


## 九、自测题（检验掌握情况）
1. `transform: translate(100px) rotate(45deg)` 的实际执行顺序是什么？为什么？若需“先旋转再平移”，应如何修改？
2. 实现 3D 卡片翻转效果，需给父元素和子元素分别添加哪些关键属性？缺少这些属性会导致什么问题？
3. `animation: move 3s steps(5) infinite alternate forwards` 中，各属性的含义是什么？“steps(5)” 的作用是什么？
4. 逐帧动画的核心原理是什么？精灵图有 25 帧，单帧宽度 100px，关键帧中 `background-position` 的 100% 位置应设为多少？
5. `transition: all 0.5s cubic-bezier(0.25, 0.1, 0.25, 1)` 中，`cubic-bezier` 代表什么？如何自定义符合需求的贝塞尔曲线？
6. 行内元素添加 `transform: scale(1.2)` 效果异常，原因是什么？解决方案是什么？


## 十、复习小贴士
1. **善用浏览器调试工具**：
   - Chrome 浏览器：Elements→Animations 可查看动画帧、调整速度曲线；Elements→Styles 中勾选 `transform` 可实时预览变换效果，快速定位顺序问题。
2. **优先 GPU 加速**：
   - 动画属性优先选择 `transform` 和 `opacity`，这两个属性触发 GPU 加速，避免 `width`、`top` 等属性（触发重排重绘，性能差）。
3. **注意兼容性**：
   - 3D 相关属性（如 `backface-visibility`）、`box-reflect` 需加 `-webkit-` 前缀（适配 Chrome/Safari）；精灵图动画确保 `background-size` 与精灵图尺寸匹配。
4. **性能优化**：
   - 无限循环动画（如加载）可加 `will-change: transform` 提前告知浏览器优化；避免过多同时执行的动画，减少 GPU 占用。
5. **结合案例记忆**：
   - 复杂概念（如 3D 变换）通过“3D 卡片翻转”案例记忆，将属性与效果绑定，避免死记硬背。