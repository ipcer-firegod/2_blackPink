# Web APIs 第一天核心知识复习记录
## 一、本文档目的
- 梳理 Web APIs 第一天核心知识点（变量声明、DOM 操作、定时器），重点突出 DOM 元素获取与属性操作、定时器使用，非重点内容精简提炼，适配 10 分钟碎片化回顾与 1 小时集中复习。
- 解决“变量声明混淆”“DOM 操作踩坑”“定时器失控”等高频问题，补充必要细节（如伪数组遍历、样式单位规范），帮助扎实掌握基础，为后续交互开发铺垫。


## 二、宏观结构（快速导航）
- 基础铺垫：变量声明（const/let 选择原则）
- 核心基础：Web API 认知（DOM/BOM、DOM 树、DOM 对象）
- 核心操作：获取 DOM 对象（querySelector 系列为主）
- 核心操作：元素内容操作（innerText/innerHTML）
- 核心操作：元素属性操作（常用属性、样式、表单、自定义属性）
- 核心工具：定时器-间歇函数（setInterval/clearInterval）
- 实战应用：综合案例（抽奖、轮播图、倒计时）


## 三、核心概念速查（记忆卡）
### 1. 变量声明（基础重点）
#### （1）选择原则：优先 const，再用 let
- 核心逻辑：
  1. 声明时确定值不会修改 → 用 `const`（语义化更好，实际开发常用，如 React 框架）。
  2. 基本类型值需修改（如 `num++`）、引用类型地址需修改（如 `arr = [1,2,3]`）→ 用 `let`。
- 关键区别：
  - `const` 声明基本类型：值不可修改（如 `const num=1; num=2` 报错）。
  - `const` 声明引用类型（数组/对象）：地址不可修改，但内部属性/元素可修改（如 `const arr=[1]; arr.push(2)` 合法，`arr=[1,2]` 报错）。
- 总结：数组、对象优先用 `const`，基本类型需修改用 `let`，淘汰 `var`（问题多，如变量提升、作用域混乱）。

#### （2）常见疑问解答
| 代码示例                          | 能否改 const？ | 原因                                  |
|-----------------------------------|---------------|---------------------------------------|
| `let uname='刘德华'; console.log(uname)` | 能            | 基本类型值未修改                      |
| `let num=1; num=num+1`             | 不能          | 基本类型值被重新赋值                  |
| `let arr=['red']; arr.push('pink')` | 能            | 数组地址未变，仅内部元素修改          |
| `let obj={age:18}; obj.age=20`     | 能            | 对象地址未变，仅内部属性修改            |
| `let obj={age:18}; obj={name:'pink'}` | 不能          | 对象地址被重新赋值（指向新对象）        |


### 2. Web API 基本认知
#### （1）核心分类与作用
- Web API 是 JS 操作 HTML 和浏览器的接口，分为两类：
  1. **DOM（文档对象模型）**：操作网页内容（如修改文本、图片、样式），核心用于开发内容特效和用户交互。
  2. **BOM（浏览器对象模型）**：操作浏览器（如刷新、跳转、本地存储），当天暂未重点讲解。
- 关系：ECMAScript（JS 基础）+ Web APIs（DOM+BOM）= 完整前端 JS 能力。

#### （2）DOM 关键概念
- **DOM 树**：HTML 文档的树状结构，直观体现标签间的嵌套/兄弟关系（如 `<html>` 是根节点，`<head>` 和 `<body>` 是子节点）。
- **DOM 对象**：浏览器根据 HTML 标签生成的 JS 对象，标签的所有属性都映射到该对象上，修改对象属性会同步到标签。
- **document 对象**：DOM 核心对象，网页所有内容都包含在其中，提供操作 DOM 的方法（如 `querySelector`、`write`）。


### 3. 获取 DOM 对象（核心重点）
#### （1）优先使用：CSS 选择器方式
| 方法                  | 语法                          | 返回值                                  | 能否直接操作？ | 关键注意事项                          |
|-----------------------|-------------------------------|---------------------------------------|---------------|---------------------------------------|
| querySelector()        | `document.querySelector('CSS选择器')` | 匹配的**第一个**元素（HTMLElement 对象），无匹配返回 `null` | 能            | 选择器语法与 CSS 一致（如 `.box`、`#nav`、`ul li`），参数必须加引号 |
| querySelectorAll()     | `document.querySelectorAll('CSS选择器')` | 匹配的**所有元素**（NodeList 伪数组） | 不能          | 需通过遍历（for 循环）操作单个元素；即使只有1个元素，也返回伪数组 |

#### （2）了解即可：传统方法
- `document.getElementById('id名')`：根据 ID 获取单个元素（无需加 `#`）。
- `document.getElementsByTagName('标签名')`：根据标签名获取多个元素（返回 HTMLCollection 集合）。
- `document.getElementsByClassName('类名')`：根据类名获取多个元素（无需加 `.`）。

#### （3）补充知识点：NodeList 伪数组
- 特性：有长度、有索引，但无数组方法（如 `push`、`pop`）。
- 遍历方式：for 循环（推荐）、forEach 循环（部分浏览器支持）。
  ```javascript
  const lis = document.querySelectorAll('ul li');
  // for 循环遍历
  for (let i=0; i<lis.length; i++) {
    console.log(lis[i]); // 单个 li 元素
  }
  ```


### 4. 操作元素内容（核心重点）
两种方式对比，按需选择：
| 方式          | 语法                          | 核心区别                                  | 适用场景                          |
|---------------|-------------------------------|---------------------------------------|-----------------------------------|
| innerText     | `元素.innerText = '内容'`     | 只识别纯文本，不解析 HTML 标签            | 仅展示文本，无需格式化            |
| innerHTML     | `元素.innerHTML = '内容'`     | 识别 HTML 标签，支持多标签（需用模板字符串） | 需解析标签（如加粗、换行）、插入多元素 |

- 示例：
  ```javascript
  const box = document.querySelector('.box');
  box.innerText = '我是<strong>刘德华</strong>'; // 显示：我是<strong>刘德华</strong>（不解析标签）
  box.innerHTML = '我是<strong>刘德华</strong>'; // 显示：我是刘德华（解析 strong 标签，文字加粗）
  ```


### 5. 操作元素属性（核心重点）
#### （1）操作常用属性（href、src、title 等）
- 语法：`元素.属性名 = 新值`（直接点语法操作）。
- 示例：更换图片 src 和 title：
  ```javascript
  const img = document.querySelector('img');
  img.src = './images/b02.jpg'; // 修改图片路径
  img.title = '刘德华演唱会'; // 修改鼠标悬浮提示
  ```

#### （2）操作样式属性（重点高频）
三种方式，按需选择：
| 方式          | 语法                          | 特点                                  | 适用场景                          |
|---------------|-------------------------------|---------------------------------------|-----------------------------------|
| style 属性     | `元素.style.样式属性 = '值'`  | 行内样式，优先级高；需小驼峰命名；必须加单位 | 修改少量样式（1-2个）            |
| className     | `元素.className = '类名'`     | 替换原有类名；可一次性修改多个样式        | 修改大量样式；无需保留原有类名    |
| classList     | `元素.classList.add('类名')`  | 追加类名（不覆盖）；支持 add/remove/toggle | 修改大量样式；需保留原有类名      |

- 关键注意事项：
  1. style 属性：样式名含 `-` 需转小驼峰（如 `margin-top` → `marginTop`），数值必须加单位（如 `'20px'` 不能写 `20`）。
  2. className：直接赋值会覆盖原有类名（如需保留，需拼接：`元素.className = '原有类名 新增类名'`）。
  3. classList 常用方法：
     - `add('类名')`：追加类
     - `remove('类名')`：移除类
     - `toggle('类名')`：切换类（有则移除，无则添加）

#### （3）操作表单属性
- 普通属性（value、type）：直接点语法操作。
- 布尔属性（disabled、checked、selected）：值为布尔值（true 启用，false 禁用）。
- 示例：密码框显示/隐藏、按钮禁用：
  ```javascript
  const password = document.querySelector('input[type="password"]');
  const btn = document.querySelector('button');
  password.type = 'text'; // 密码框转为文本框（显示密码）
  btn.disabled = true; // 按钮禁用（不可点击）
  ```

#### （4）操作自定义属性（HTML5 规范）
- 标签定义：以 `data-` 开头（如 `data-id="10"`）。
- JS 获取：通过 `元素.dataset.属性名`（无需写 `data-`）。
- 示例：
  ```html
  <div class="box" data-id="10" data-name="box1"></div>
  <script>
    const box = document.querySelector('.box');
    console.log(box.dataset.id); // 输出：10
    console.log(box.dataset.name); // 输出：box1
  </script>
  ```


### 6. 定时器-间歇函数（核心工具）
#### （1）核心作用
每隔指定时间自动重复执行代码（如倒计时、轮播图自动切换）。

#### （2）基本使用
| 操作          | 语法                          | 关键说明                                  |
|---------------|-------------------------------|---------------------------------------|
| 开启定时器    | `let timerId = setInterval(函数, 间隔时间)` | 函数不加括号；间隔时间单位为毫秒（1000ms=1s）；返回定时器 ID（用于关闭） |
| 关闭定时器    | `clearInterval(timerId)`       | 需传入开启定时器时返回的 ID；关闭后不再执行 |

- 示例：每隔 1 秒打印日志，3 秒后关闭：
  ```javascript
  // 开启定时器
  let timer = setInterval(function() {
    console.log('每隔1秒执行一次');
  }, 1000);

  // 3秒后关闭定时器
  setTimeout(function() {
    clearInterval(timer);
    console.log('定时器已关闭');
  }, 3000);
  ```

#### （3）注意事项
1. 函数参数：直接写函数名（不加括号）或匿名函数，加括号会立即执行一次，而非定时执行。
2. 间隔时间：最小间隔约 16ms（浏览器渲染帧率限制），无法实现更短间隔。
3. 定时器叠加：多次开启同一定时器会导致执行频率翻倍，需先关闭再开启。


### 7. 综合案例核心思路
#### （1）年会抽奖案例
- 需求：从数组随机抽取一、二、三等奖并显示。
- 核心步骤：
  1. 声明获奖名单数组：`const personArr = ['周杰伦', '刘德华', '周星驰', 'Pink老师', '张学友']`。
  2. 随机生成索引：`Math.floor(Math.random() * personArr.length)`。
  3. 赋值到对应标签：`document.querySelector('.first').innerText = 随机名字`。

#### （2）注册协议倒计时案例
- 需求：按钮 60 秒后才可点击。
- 核心步骤：
  1. 初始禁用按钮：`btn.disabled = true`。
  2. 声明倒计时变量：`let second = 60`。
  3. 定时器内更新文字：`btn.innerText = `已阅读用户协议(${second}s)`。
  4. 秒数为 0 时关闭定时器，启用按钮：`btn.disabled = false; btn.innerText = '同意'`。

#### （3）轮播图自动切换案例
- 需求：每隔 1 秒切换图片、文字、高亮小圆点。
- 核心步骤：
  1. 声明轮播数据数组（含图片路径、标题、颜色）。
  2. 声明索引变量：`let index = 0`。
  3. 定时器内更新索引：`index++`，超出数组长度时重置为 0。
  4. 更换图片、文字、背景色，切换小圆点高亮类。


## 四、常见错误与陷阱（高频）
1. **querySelectorAll 直接操作**：
   - 错误：`document.querySelectorAll('li').style.color = 'red'`（伪数组不能直接操作）。
   - 解决：遍历伪数组，逐个修改元素。

2. **style 样式未加单位**：
   - 错误：`box.style.width = 200`（无单位，浏览器不识别）。
   - 解决：`box.style.width = '200px'`（加 px 单位）。

3. **className 覆盖原有类名**：
   - 错误：`box.className = 'active'`（覆盖原有类名，导致样式丢失）。
   - 解决：需保留则拼接（`box.className = 'box active'`）或用 `classList.add('active')`。

4. **定时器未关闭导致叠加**：
   - 错误：多次点击“开始轮播”按钮，未关闭原有定时器，导致切换加速。
   - 解决：开启新定时器前，先关闭旧定时器：`clearInterval(timer); timer = setInterval(...)`。

5. **const 修改引用类型地址**：
   - 错误：`const arr = [1]; arr = [1,2]`（修改数组地址，报错）。
   - 解决：需修改地址用 `let`，仅修改内部元素用 `const`。


## 五、快速练习（把知识变成肌肉记忆）
### 1. 10 分钟任务（基础回顾）
- 任务 1：用 querySelector 获取页面中 class 为 `nav` 的 `ul` 下的所有 `li`，并遍历打印每个 `li` 的文本内容。
- 任务 2：用 style 属性修改一个 div 的宽度 200px、背景色 pink、上外边距 15px（注意小驼峰）。
- 任务 3：写一个定时器，每隔 500ms 切换按钮文本为“切换中...”和“切换完成”，3 秒后关闭定时器。

### 2. 1 小时任务（综合应用）
- 需求：实现“随机图片+背景色”功能：
  1. 页面刷新时，随机显示 3 张图片中的一张（用数组存储图片路径）。
  2. 随机更换 body 背景色（用数组存储颜色值）。
  3. 给图片添加 class `active`（用 classList），设置边框 2px 实线白色。


## 六、代码片段（常用模板，拷贝即用）
### 1. DOM 获取与遍历
```javascript
// 获取单个元素
const box = document.querySelector('.box');

// 获取多个元素并遍历
const lis = document.querySelectorAll('ul li');
for (let i = 0; i < lis.length; i++) {
  console.log(lis[i].innerText); // 打印每个 li 文本
}
```

### 2. 样式操作（classList 推荐）
```css
/* CSS 类 */
.active {
  width: 200px;
  height: 200px;
  background: pink;
  margin-top: 15px;
}
```
```javascript
const box = document.querySelector('.box');
box.classList.add('active'); // 追加类（不覆盖原有样式）
box.classList.toggle('active'); // 切换类（点击时常用）
```

### 3. 表单属性操作（密码显示/隐藏）
```html
<input type="password" id="pwd">
<button id="toggleBtn">显示密码</button>
```
```javascript
const pwd = document.getElementById('pwd');
const toggleBtn = document.getElementById('toggleBtn');
let isShow = false;

toggleBtn.addEventListener('click', function() {
  isShow = !isShow;
  pwd.type = isShow ? 'text' : 'password';
  toggleBtn.innerText = isShow ? '隐藏密码' : '显示密码';
});
```

### 4. 定时器倒计时
```html
<button id="agreeBtn" disabled>已阅读用户协议(60s)</button>
```
```javascript
const agreeBtn = document.getElementById('agreeBtn');
let second = 60;

const timer = setInterval(function() {
  second--;
  agreeBtn.innerText = `已阅读用户协议(${second}s)`;
  if (second === 0) {
    clearInterval(timer); // 关闭定时器
    agreeBtn.disabled = false;
    agreeBtn.innerText = '同意';
  }
}, 1000);
```


## 八、复习计划（建议周期）
### 1. 每周（30 分钟）
- 回顾“核心概念速查”，重点记忆 DOM 获取方法、样式操作三种方式、定时器使用规范。
- 完成 1 个“10 分钟任务”，如 DOM 遍历、样式切换，巩固基础操作。

### 2. 每两周（2 小时）
- 完成 1 个“1 小时任务”，如综合案例（随机图片+背景色），整合 DOM 获取、属性操作、数组随机。
- 用浏览器调试工具（F12→Elements）查看 DOM 结构，验证样式修改是否生效。

### 3. 每月（半天）
- 独立完成轮播图自动切换案例，包含图片切换、文字更新、小圆点高亮、定时器控制，检验综合应用能力。
- 总结常见错误（如定时器叠加、伪数组遍历），形成个人错题本。


## 九、自测题（检验掌握情况）
1. 声明变量时，const 和 let 的选择原则是什么？const 声明的对象为什么能修改内部属性？
2. querySelector 和 querySelectorAll 的区别是什么？querySelectorAll 返回的伪数组如何遍历？
3. innerText 和 innerHTML 的核心区别是什么？如何用 innerHTML 实现“文字加粗+换行”？
4. 用 style 属性修改 `margin-top: 20px` 时，JS 中应如何写？为什么？
5. classList 有哪些常用方法？如何实现“点击按钮切换元素的 active 类”？
6. 开启和关闭定时器的语法是什么？如何避免定时器叠加问题？
7. 如何获取标签上的 `data-age="18"` 自定义属性？


## 十、复习小贴士
1. **善用调试工具**：F12→Elements 面板查看 DOM 结构，Console 面板测试代码（如 `document.querySelector('.box')` 验证是否获取成功）。
2. **样式操作优先 classList**：修改多个样式时，用 CSS 类+classList 更简洁，避免 style 属性堆砌代码。
3. **定时器必关**：涉及“开始/暂停”功能时，先关闭旧定时器再开启新定时器，防止叠加。
4. **自定义属性规范**：始终以 `data-` 开头命名，用 `dataset` 获取，避免直接操作非标准属性。
5. **多练案例**：轮播图、倒计时是高频面试题，至少独立写 3 遍，熟练掌握核心逻辑。