# Web APIs 第三天核心知识复习记录
## 一、本文档目的
- 梳理 Web APIs 第三天核心知识点（事件流、事件委托、拓展事件、元素尺寸与位置），重点突出事件委托优化、元素尺寸属性区别、滚动事件应用，非重点内容精简提炼，适配 10 分钟碎片化回顾与 1 小时集中复习。
- 解决“事件冒泡干扰交互”“多元素事件绑定性能差”“元素位置/尺寸属性混淆”等高频问题，补充 `offsetParent` 定义、`getBoundingClientRect()` 细节等必要知识点，帮助扎实掌握复杂交互开发能力。


## 二、宏观结构（快速导航）
- 核心基础：事件流（捕获/冒泡/阻止冒泡/解绑事件）
- 核心优化：事件委托（原理/好处/实现/案例）
- 拓展事件：页面加载事件、滚动事件、尺寸事件（语法/应用）
- 核心工具：元素尺寸与位置（offset/client/scroll 系列属性）
- 实战应用：综合案例（全选反选、电梯导航、固定导航栏）
- 补充知识点：`offsetParent` 定义、事件流执行顺序细节


## 三、核心概念速查（记忆卡）
### 1. 事件流（核心重点）
事件流是事件触发后的完整执行路径，分为**捕获阶段**和**冒泡阶段**，是复杂交互的基础。

#### （1）核心阶段说明
| 阶段       | 执行顺序                          | 触发时机                                  | 语法控制                          |
|------------|-----------------------------------|-------------------------------------------|-----------------------------------|
| 事件捕获   | 从 DOM 根元素 → 目标元素（从外到里） | 事件触发时先执行父级捕获逻辑，再到子级      | `addEventListener` 第三参数为 `true`（极少使用） |
| 事件冒泡   | 从目标元素 → DOM 根元素（从里到外） | 事件触发时先执行子级逻辑，再向上传播父级    | 默认行为（`addEventListener` 第三参数为 `false` 或省略） |

- 示例（父子元素点击事件）：
  ```javascript
  const father = document.querySelector('.father');
  const son = document.querySelector('.son');
  // 捕获阶段（从外到里：document → father → son）
  document.addEventListener('click', () => console.log('爷爷捕获'), true);
  father.addEventListener('click', () => console.log('爸爸捕获'), true);
  son.addEventListener('click', () => console.log('儿子捕获'), true);
  // 冒泡阶段（从里到外：son → father → document）
  son.addEventListener('click', () => console.log('儿子冒泡'));
  father.addEventListener('click', () => console.log('爸爸冒泡'));
  document.addEventListener('click', () => console.log('爷爷冒泡'));
  // 点击 son 执行顺序：爷爷捕获 → 爸爸捕获 → 儿子捕获 → 儿子冒泡 → 爸爸冒泡 → 爷爷冒泡
  ```

#### （2）阻止冒泡（高频应用）
- 问题：默认冒泡会导致父级同名事件被触发，干扰交互（如子元素点击触发父元素点击）。
- 语法：`事件对象.stopPropagation()`（需在事件处理函数中接收事件对象 `e`）。
- 示例（阻止子元素点击冒泡到父元素）：
  ```javascript
  son.addEventListener('click', (e) => {
    console.log('儿子点击');
    e.stopPropagation(); // 阻止冒泡，父元素点击事件不执行
  });
  ```

#### （3）解绑事件（两种方式区别）
| 绑定方式                | 解绑语法                          | 关键注意事项                                  |
|-------------------------|-----------------------------------|---------------------------------------|
| DOM L0（on 方式）        | `元素.on事件 = null`              | 简单直接，覆盖绑定可直接解绑                |
| DOM L2（addEventListener）| `元素.removeEventListener(事件类型, 函数名)` | 1. 必须传入绑定的同名函数（匿名函数无法解绑）；2. 第三参数（捕获/冒泡）需与绑定一致 |

- 示例：
  ```javascript
  // L2 方式解绑（需保留函数引用）
  function handleClick() { console.log('点击'); }
  btn.addEventListener('click', handleClick);
  btn.removeEventListener('click', handleClick); // 成功解绑
  ```

#### （4）鼠标事件区别（避免冒泡干扰）
| 事件对       | 是否有冒泡效果 | 推荐使用 | 适用场景                          |
|--------------|---------------|----------|-----------------------------------|
| mouseover/mouseout | 是            | 否       | 需冒泡传递的鼠标经过场景（极少）    |
| mouseenter/mouseleave | 否          | 是       | 仅目标元素触发（如导航栏菜单项悬浮） |


### 2. 事件委托（核心优化，重点详细）
事件委托是利用**事件冒泡**特性，将子元素的事件绑定到父元素，实现“一次绑定，多元素响应”。

#### （1）核心原理与好处
- 原理：子元素触发事件后冒泡到父元素，通过 `事件对象.target` 找到真正触发事件的子元素。
- 好处：
  1. 减少事件注册次数，提升性能（如 100 个 li 仅需绑定 1 次父元素事件）。
  2. 支持动态新增子元素（新增 li 无需重新绑定事件）。

#### （2）实现步骤
1. 给父元素绑定事件（L2 方式）。
2. 通过 `e.target` 获取真正触发事件的子元素。
3. 判断子元素是否为目标元素（如通过 `tagName`、类名、自定义属性）。
4. 执行对应逻辑。

#### （3）示例（ul 下 li 点击事件委托）
```javascript
const ul = document.querySelector('ul');
ul.addEventListener('click', (e) => {
  // 判断触发元素是否为 li（tagName 大写）
  if (e.target.tagName === 'LI') {
    e.target.style.color = 'pink'; // 仅点击的 li 变色
  }
});
```

#### （4）实战改造：Tab 栏切换（事件委托版）
- 核心思路：
  1. 给 Tab 父容器绑定点击事件。
  2. 通过自定义属性 `data-id` 给 Tab 项标记索引。
  3. 点击时通过 `e.target.dataset.id` 获取索引，切换对应内容。


### 3. 拓展事件（重点应用）
#### （1）页面加载事件（2 种核心事件）
用于等待页面资源加载完成后执行逻辑，避免 DOM 未加载导致的操作失败。

| 事件名            | 触发时机                                  | 绑定对象 | 适用场景                          |
|-------------------|-------------------------------------------|----------|-----------------------------------|
| load              | 页面所有资源（DOM、图片、CSS、JS）加载完成 | window   | 需依赖图片、CSS 的交互（如图片轮播初始化） |
| DOMContentLoaded  | DOM 解析完成（无需等待图片、CSS）          | document | 仅依赖 DOM 的操作（如绑定事件、修改文本） |

- 示例：
  ```javascript
  // DOM 解析完成后执行（推荐，效率高）
  document.addEventListener('DOMContentLoaded', () => {
    const btn = document.querySelector('button');
    btn.addEventListener('click', () => alert('DOM 已加载'));
  });
  ```

#### （2）页面滚动事件（scroll）
滚动条滚动时持续触发，用于固定导航栏、显示返回顶部按钮等场景。

- 核心属性（获取/设置滚动距离）：
  - `document.documentElement.scrollTop`：页面被卷去的顶部距离（可读写）。
  - `document.documentElement.scrollLeft`：页面被卷去的左侧距离（可读写）。
- 关键应用：
  1. 滚动显示/隐藏侧边栏（滚动 > 300px 显示）。
  2. 返回顶部（设置 `scrollTop = 0` 或 `scrollTo(0, 0)`）。
- 示例（返回顶部）：
  ```javascript
  const backTopBtn = document.querySelector('.back-top');
  backTopBtn.addEventListener('click', () => {
    window.scrollTo(0, 0); // 滚动到页面顶部（x=0, y=0）
  });
  ```

#### （3）页面尺寸事件（resize）
窗口尺寸改变时触发，用于响应式布局、动态调整元素尺寸。

- 核心属性（获取元素可视尺寸）：
  - `document.documentElement.clientWidth`：页面可视宽度（不含滚动条、边框）。
  - `document.documentElement.clientHeight`：页面可视高度。
- 示例（动态计算 Rem 基准值）：
  ```javascript
  function setRem() {
    const clientWidth = document.documentElement.clientWidth;
    document.documentElement.style.fontSize = clientWidth / 10 + 'px'; // 1rem = 可视宽 1/10
  }
  setRem(); // 初始执行
  window.addEventListener('resize', setRem); // 窗口改变时重新计算
  ```


### 4. 元素尺寸与位置（核心工具，重点详细）
用于获取元素的尺寸和页面位置，支撑滚动触发、元素定位等复杂交互。

#### （1）核心属性对比（高频重点）
| 属性系列         | 包含范围（宽高）                          | 位置参考                          | 读写性 | 核心用途                          |
|------------------|-------------------------------------------|-----------------------------------|--------|-----------------------------------|
| offsetWidth/offsetHeight | 内容 + padding + border（含滚动条）        | -                                 | 只读   | 获取元素实际占位尺寸（如判断元素大小） |
| offsetLeft/offsetTop   | 距离**定位父级**（offsetParent）的左/上距离 | 最近带定位（relative/absolute/fixed）的父元素，无则为文档 | 只读   | 元素定位、滚动到指定元素          |
| clientWidth/clientHeight | 内容 + padding（不含 border、滚动条）      | -                                 | 只读   | 获取元素可视区域尺寸（如自适应宽高） |
| scrollWidth/scrollHeight | 元素内容总尺寸（含隐藏部分）              | -                                 | 只读   | 判断元素是否有滚动条              |
| scrollLeft/scrollTop   | 元素内容被卷去的左/上距离                | 元素自身                          | 可读写 | 元素内部滚动、页面滚动控制          |

- 补充知识点：`offsetParent`（定位父级）：元素最近的带定位（`relative`/`absolute`/`fixed`）的祖先元素，若无则为 `<html>` 元素。

#### （2）拓展方法：getBoundingClientRect()
- 作用：返回元素相对于**视口**的位置和尺寸，包含 `left`/`top`/`width`/`height` 等属性。
- 特点：`left`/`top` 随页面滚动变化，适合判断元素是否在视口内（如滚动加载）。
- 示例：
  ```javascript
  const box = document.querySelector('.box');
  const rect = box.getBoundingClientRect();
  console.log('元素视口位置：', rect.left, rect.top);
  ```


### 5. 综合案例核心思路
#### （1）全选反选案例
- 核心逻辑：
  1. 全选框点击：所有小复选框 `checked` 与全选框一致。
  2. 小复选框点击：判断选中个数是否等于总个数，同步全选框状态（`input:checked` 选择器统计）。

#### （2）电梯导航案例
- 核心逻辑：
  1. 点击导航项：通过自定义属性关联目标模块，滚动到模块 `offsetTop` 位置。
  2. 页面滚动：判断模块是否进入视口，同步导航项高亮状态（移除所有高亮，给对应项添加）。

#### （3）京东固定导航栏案例
- 核心逻辑：
  1. 监听页面滚动，获取秒杀模块 `offsetTop`。
  2. 滚动距离 ≥ 模块位置：导航栏滑入（`position: fixed`）；否则滑出。


## 四、常见错误与陷阱（高频）
1. **阻止冒泡与阻止默认行为混淆**：
   - 错误：用 `e.stopPropagation()` 阻止表单提交（应阻止默认行为）。
   - 解决：阻止冒泡用 `e.stopPropagation()`，阻止默认行为（表单提交、链接跳转）用 `e.preventDefault()`。

2. **事件委托时 `target` 判断错误**：
   - 错误：`e.target.tagName === 'li'`（tagName 是大写，应为 `'LI'`）。
   - 解决：统一用大写判断，或通过类名（`e.target.classList.contains('li-class')`）判断。

3. **offsetParent 定位父级判断错误**：
   - 错误：认为 `offsetLeft` 始终相对于文档（实际相对于最近带定位的父级）。
   - 解决：先确认父级是否有定位，无则 `offsetLeft` 相对于文档。

4. **scrollTop 获取失败**：
   - 错误：在 `DOMContentLoaded` 前获取 `scrollTop`（DOM 未加载）。
   - 解决：将滚动相关逻辑放入 `DOMContentLoaded` 或 `load` 事件中。


## 五、快速练习（把知识变成肌肉记忆）
### 1. 10 分钟任务（基础回顾）
- 任务 1：用事件委托给 ul 下所有 li 绑定点击事件，点击后添加红色边框（区分 target 元素）。
- 任务 2：实现页面滚动 > 500px 显示返回顶部按钮，否则隐藏（用 scrollTop 判断）。
- 任务 3：获取一个元素的 offsetWidth、clientWidth、scrollWidth，打印并对比差异。

### 2. 1 小时任务（综合应用）
- 需求：实现简易电梯导航：
  1. 导航项 3 个（“模块1”“模块2”“模块3”），对应页面 3 个模块。
  2. 点击导航项，页面平滑滚动到对应模块（添加 `scroll-behavior: smooth`）。
  3. 页面滚动时，模块进入视口，对应导航项添加高亮类（`active`）。


## 六、代码片段（常用模板，拷贝即用）
### 1. 事件委托实现 li 点击
```javascript
const ul = document.querySelector('ul');
ul.addEventListener('click', (e) => {
  // 类名判断更灵活（推荐）
  if (e.target.classList.contains('list-item')) {
    e.target.style.backgroundColor = 'skyblue';
  }
});
```

### 2. 滚动显示隐藏侧边栏
```css
.sidebar {
  position: fixed;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none; /* 隐藏时不可点击 */
}
.sidebar.show {
  opacity: 1;
  pointer-events: auto;
}
```
```javascript
window.addEventListener('scroll', () => {
  const sidebar = document.querySelector('.sidebar');
  // 滚动 > 300px 显示
  sidebar.classList.toggle('show', document.documentElement.scrollTop > 300);
});
```

### 3. 电梯导航点击滚动
```javascript
const nav = document.querySelector('.elevator-nav');
nav.addEventListener('click', (e) => {
  if (e.target.tagName === 'A') {
    // 移除所有高亮
    nav.querySelectorAll('a').forEach(a => a.classList.remove('active'));
    // 当前项高亮
    e.target.classList.add('active');
    // 获取目标模块索引（自定义属性 data-target）
    const targetId = e.target.dataset.target;
    const targetModule = document.getElementById(targetId);
    // 滚动到模块位置
    window.scrollTo({
      top: targetModule.offsetTop,
      behavior: 'smooth' // 平滑滚动
    });
  }
});
```

### 4. 全选反选功能
```javascript
const allCheck = document.querySelector('#allCheck');
const itemChecks = document.querySelectorAll('.item-check');

// 全选框点击
allCheck.addEventListener('click', () => {
  itemChecks.forEach(check => check.checked = allCheck.checked);
});

// 小复选框点击
itemChecks.forEach(check => {
  check.addEventListener('click', () => {
    // 统计选中个数
    const checkedCount = document.querySelectorAll('.item-check:checked').length;
    allCheck.checked = checkedCount === itemChecks.length;
  });
});
```


## 八、复习计划（建议周期）
### 1. 每周（30 分钟）
- 回顾“核心概念速查”，重点记忆事件委托实现步骤、元素尺寸属性对比、滚动事件应用。
- 完成 1 个“10 分钟任务”，如事件委托、滚动显示侧边栏，巩固基础操作。

### 2. 每两周（2 小时）
- 完成 1 个“1 小时任务”，如简易电梯导航，整合事件委托、滚动事件、元素位置获取。
- 用浏览器调试工具（Elements→Box Model）查看元素 offset/client/scroll 尺寸，验证属性值。

### 3. 每月（半天）
- 独立完成电梯导航完整案例，包含点击滚动、滚动高亮、模块显示隐藏，检验综合应用能力。
- 补充学习“滚动加载”（结合 `getBoundingClientRect()` 判断元素是否在视口）。


## 九、自测题（检验掌握情况）
1. 事件流的两个阶段是什么？执行顺序如何？如何阻止事件冒泡？
2. 事件委托的核心原理和好处是什么？如何通过事件委托实现 li 点击事件？
3. load 和 DOMContentLoaded 事件的区别是什么？分别绑定在哪个对象上？
4. offsetWidth、clientWidth、scrollWidth 的核心区别是什么？各自包含哪些部分？
5. 如何获取页面被卷去的顶部距离？如何实现页面平滑滚动到顶部？
6. 电梯导航的核心逻辑是什么？如何判断模块是否进入视口？
7. 全选反选案例中，如何同步全选框和小复选框的状态？


## 十、复习小贴士
1. **属性记忆技巧**：
   - offset：含 border（占位尺寸）、定位父级位置。
   - client：不含 border/滚动条（可视尺寸）。
   - scroll：含隐藏内容（总尺寸）、被卷去距离。
2. **事件委托优先用类名判断**：`e.target.classList.contains('类名')` 比 `tagName` 更灵活，适配动态添加的子元素。
3. **滚动事件优化**：滚动事件持续触发，可通过 `requestAnimationFrame` 优化性能（避免频繁计算）。
4. **调试工具辅助**：F12→Elements→Box Model 实时查看元素 offset/client/scroll 尺寸，快速验证属性值。
5. **案例多练**：电梯导航、全选反选是面试高频题，至少独立写 3 遍，熟练掌握核心逻辑。