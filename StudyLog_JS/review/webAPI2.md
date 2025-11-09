# Web APIs 第二天核心知识复习记录
## 一、本文档目的
- 梳理 Web APIs 第二天核心知识点（事件监听、事件类型、事件对象、环境对象、回调函数），重点突出事件绑定、事件对象应用、this 指向判断，非重点内容精简提炼，适配 10 分钟碎片化回顾与 1 小时集中复习。
- 解决“事件绑定覆盖”“this 指向混淆”“事件对象属性误用”等高频问题，补充事件流、阻止默认行为等必要知识点，帮助扎实掌握网页交互核心能力。


## 二、宏观结构（快速导航）
- 核心基础：事件监听（DOM L0/L2 方式、三要素）
- 核心分类：事件类型（鼠标/焦点/键盘/文本事件）
- 核心工具：事件对象（获取方式、常用属性）
- 核心概念：环境对象（this 指向规则）
- 核心语法：回调函数（定义、使用场景）
- 实战应用：综合案例（关闭广告、随机点名、Tab 栏切换）
- 补充知识点：事件流、阻止默认行为


## 三、核心概念速查（记忆卡）
### 1. 事件监听（核心重点）
事件监听是实现网页交互的基础，核心是“检测事件触发，执行对应函数”。

#### （1）核心三要素
1. 事件源：被触发的 DOM 元素（如按钮、输入框）。
2. 事件类型：触发方式（如点击、鼠标经过，需加引号）。
3. 事件处理程序：触发后执行的函数（匿名函数或命名函数）。

#### （2）两种绑定方式（DOM L0 vs DOM L2）
| 方式                | 语法                          | 特点                                  | 适用场景                          |
|---------------------|-------------------------------|---------------------------------------|-----------------------------------|
| DOM L0（on 方式）    | `元素.on事件类型 = 函数`       | 简单直观；同一事件只能绑定一个函数（后绑定覆盖前绑定） | 简单交互，无需多函数绑定          |
| DOM L2（推荐）      | `元素.addEventListener('事件类型', 函数)` | 同一事件可绑定多个函数（依次执行）；支持事件流；功能更全 | 复杂交互，需多函数响应同一事件      |

- 示例：
  ```javascript
  const btn = document.querySelector('button');
  // DOM L0 方式
  btn.onclick = function() { console.log('L0 点击'); };
  btn.onclick = function() { console.log('L0 覆盖前一个'); }; // 覆盖上一个点击事件

  // DOM L2 方式（推荐）
  btn.addEventListener('click', function() { console.log('L2 点击1'); });
  btn.addEventListener('click', function() { console.log('L2 点击2'); }); // 两个函数都执行
  ```

#### （3）关键注意事项
- 事件类型必须加引号（如 `'click'` 不能写 `click`）。
- 函数参数无需加括号（加括号会立即执行，而非事件触发后执行）。
- L2 方式绑定的函数需通过 `removeEventListener` 移除（需保留函数引用，匿名函数无法移除）。


### 2. 事件类型（核心分类）
按触发方式分类，需熟记常用事件及应用场景：

| 事件类别     | 常用事件                          | 触发场景                                  | 典型案例                          |
|--------------|-----------------------------------|-------------------------------------------|-----------------------------------|
| 鼠标事件     | click（点击）、mouseenter（鼠标经过）、mouseleave（鼠标离开） | 鼠标点击、悬浮、离开元素                  | 关闭广告、Tab 栏切换、轮播图暂停  |
| 焦点事件     | focus（获得焦点）、blur（失去焦点） | 输入框获取/失去光标                      | 搜索框显示/隐藏下拉菜单、表单验证  |
| 键盘事件     | keydown（键盘按下）、keyup（键盘抬起） | 按下/松开键盘按键                        | 回车发布评论、快捷键操作          |
| 文本事件     | input（用户输入）                  | 输入框实时输入文本                        | 评论字数统计、实时搜索提示        |

- 补充知识点：事件流（文档未详细提及，必要补充）
  - 事件冒泡：事件从触发元素向上传播到父元素（默认行为）。
  - 事件捕获：事件从父元素向下传播到触发元素（需通过 `addEventListener` 第三参数 `true` 开启）。
  - 阻止冒泡：`e.stopPropagation()`（避免父元素事件被触发）。


### 3. 事件对象（核心工具，重点详细）
事件对象包含事件触发时的关键信息，是实现复杂交互的核心。

#### （1）获取方式
事件处理函数的**第一个参数**即为事件对象，常用命名 `e`/`event`/`ev`：
```javascript
btn.addEventListener('click', function(e) {
  console.log(e); // 事件对象，包含点击相关信息
});
```

#### （2）常用属性及应用场景
| 属性名        | 作用                                  | 应用场景                          |
|---------------|---------------------------------------|-----------------------------------|
| type          | 获取当前事件类型（如 `'click'`/`'input'`） | 判断触发的事件类型，统一处理多事件    |
| clientX/clientY | 获取光标相对于**浏览器可视窗口**左上角的坐标 | 鼠标位置相关交互（如拖拽、自定义弹窗） |
| offsetX/offsetY | 获取光标相对于**当前元素**左上角的坐标 | 元素内精准交互（如点击元素特定区域）  |
| key           | 获取按下的键盘按键值（如 `'Enter'`/`'a'`） | 键盘快捷键（如回车发布、ESC 关闭）    |

- 补充属性：`target`（触发事件的具体元素），用于事件委托（如列表项点击）。
- 示例：回车发布评论
  ```javascript
  const textarea = document.querySelector('textarea');
  textarea.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') { // 判断按下的是回车键
      const content = this.value.trim();
      if (content) {
        console.log('发布评论：', content);
        this.value = ''; // 清空输入框
      }
      e.preventDefault(); // 阻止回车换行（补充：阻止默认行为）
    }
  });
  ```

#### （3）补充：阻止默认行为
部分元素有默认行为（如表单提交、a 标签跳转），需用 `e.preventDefault()` 阻止：
```javascript
// 阻止表单默认提交行为
const form = document.querySelector('form');
form.addEventListener('submit', function(e) {
  e.preventDefault(); // 阻止页面刷新提交
  // 自定义提交逻辑
});
```


### 4. 环境对象（this 指向，重点详细）
环境对象 `this` 代表函数运行时的所处环境，核心规则：**谁调用函数，this 就指向谁**。

#### （1）常见场景 this 指向
| 函数调用方式                | this 指向                          | 示例                                  |
|-----------------------------|-----------------------------------|---------------------------------------|
| 事件监听回调函数            | 触发事件的事件源（DOM 元素）        | `btn.addEventListener('click', function() { console.log(this); })` → 指向 btn |
| 普通函数直接调用            | window 对象（浏览器全局对象）        | `function fn() { console.log(this); } fn();` → 指向 window |
| 定时器回调函数              | window 对象                        | `setInterval(function() { console.log(this); }, 1000)` → 指向 window |
| 对象方法调用                | 该对象                            | `const obj = { fn: function() { console.log(this); } }; obj.fn();` → 指向 obj |

- 关键注意：箭头函数没有自己的 `this`，会继承外层作用域的 `this`（文档未提，补充常用场景）。

#### （2）实战应用：简化代码
利用 `this` 可替代获取的 DOM 元素，简化代码：
```javascript
// 无需重复获取 btn 元素
const btn = document.querySelector('button');
btn.addEventListener('click', function() {
  this.style.backgroundColor = 'pink'; // this 指向 btn
});
```


### 5. 回调函数（核心语法）
#### （1）定义
将**函数 A 作为参数传递给函数 B**，函数 A 即为回调函数，在函数 B 执行到特定时机时自动调用。

#### （2）常见使用场景
| 应用场景                | 示例                                  |
|-------------------------|---------------------------------------|
| 事件监听                | `btn.addEventListener('click', 回调函数)` |
| 定时器（间歇/延时）      | `setInterval(回调函数, 1000)`          |
| 异步操作（后续学习）      | 数据请求成功后执行回调函数              |

- 示例：
  ```javascript
  // 命名回调函数
  function callback() {
    console.log('我是回调函数');
  }
  // 传递给 setInterval，1 秒执行一次
  setInterval(callback, 1000);

  // 匿名回调函数（更常用）
  btn.addEventListener('click', function() {
    console.log('匿名回调函数');
  });
  ```

#### （3）核心特点
- 回调函数本质是函数，仅因“作为参数传递”而得名。
- 不立即执行，需等待触发条件（如事件触发、定时器到期）。


### 6. 综合案例核心思路
#### （1）京东关闭顶部广告
- 需求：点击关闭按钮，隐藏广告父盒子。
- 核心：`display: none` 隐藏元素，`this.parentElement` 获取父盒子。
  ```javascript
  const closeBtn = document.querySelector('.close');
  closeBtn.addEventListener('click', function() {
    this.parentElement.style.display = 'none'; // this 指向关闭按钮
  });
  ```

#### （2）随机点名案例
- 需求：点击开始随机抽取，点击结束停止，最后一个数据时禁用按钮。
- 核心：定时器控制快速切换，停止时删除当前数据，判断数组长度禁用按钮。

#### （3）Tab 栏切换
- 需求：鼠标经过选项卡，显示对应内容，高亮当前选项。
- 核心：类名切换（移除其他选项卡的高亮类，给当前添加），内容联动显示。
  ```javascript
  const tabs = document.querySelectorAll('.tab');
  const panels = document.querySelectorAll('.panel');
  tabs.forEach((tab, index) => {
    tab.addEventListener('mouseenter', function() {
      // 切换选项卡高亮
      tabs.forEach(t => t.classList.remove('active'));
      this.classList.add('active');
      // 切换对应内容
      panels.forEach(p => p.style.display = 'none');
      panels[index].style.display = 'block';
    });
  });
  ```


## 四、常见错误与陷阱（高频）
1. **事件类型漏加引号**：
   - 错误：`btn.addEventListener(click, function() {})`（click 未加引号）。
   - 解决：事件类型必须是字符串，`btn.addEventListener('click', function() {})`。

2. **this 指向混淆**：
   - 错误：定时器回调中用 `this` 操作 DOM 元素（`this` 指向 window）。
   - 解决：保存事件源到变量，或用箭头函数（继承外层 `this`）。
     ```javascript
     const btn = document.querySelector('button');
     btn.addEventListener('click', function() {
       // 正确：保存 this 到变量
       const self = this;
       setInterval(function() {
         self.style.opacity = 0.5;
       }, 1000);
     });
     ```

3. **事件对象未使用参数**：
   - 错误：想获取键盘按键却未声明事件对象参数（`function() { if (key === 'Enter') {} }`）。
   - 解决：回调函数必须接收事件对象参数（`function(e) { if (e.key === 'Enter') {} }`）。

4. **L0 方式绑定多个事件被覆盖**：
   - 错误：`btn.onclick = fn1; btn.onclick = fn2;`（fn1 被覆盖）。
   - 解决：改用 L2 方式 `addEventListener` 绑定多个函数。


## 五、快速练习（把知识变成肌肉记忆）
### 1. 10 分钟任务（基础回顾）
- 任务 1：给 3 个按钮绑定点击事件，点击后各自改变背景色（用 this 实现）。
- 任务 2：实现搜索框焦点事件：获得焦点时边框变蓝色，失去焦点时恢复默认（focus/blur 事件）。
- 任务 3：实现文本域回车发布评论，发布后清空输入框（keydown 事件 + e.key + 阻止默认行为）。

### 2. 1 小时任务（综合应用）
- 需求：实现简易 Tab 栏切换：
  1. 选项卡 3 个（“首页”“商品”“我的”），内容区 3 个对应模块。
  2. 鼠标经过选项卡：当前选项卡添加红色边框+加粗，其他恢复默认。
  3. 同步显示对应内容区，隐藏其他内容区。
  4. 点击选项卡时，打印当前事件类型（用事件对象 e.type）。


## 六、代码片段（常用模板，拷贝即用）
### 1. 事件监听基础模板（L2 方式）
```javascript
// 获取事件源
const element = document.querySelector('.target');
// 绑定事件
element.addEventListener('事件类型', function(e) {
  // 事件处理逻辑
  console.log('事件触发', e.type); // 获取事件类型
  console.log('当前元素', this); // this 指向事件源
});
```

### 2. 回车发布评论
```javascript
const textarea = document.querySelector('textarea');
const commentList = document.querySelector('.comment-list');

textarea.addEventListener('keydown', function(e) {
  // 按下 Enter 且未按住 Shift（避免换行）
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault(); // 阻止默认换行
    const content = this.value.trim();
    if (!content) return; // 空内容不发布
    // 创建评论元素
    const li = document.createElement('li');
    li.textContent = content;
    commentList.appendChild(li);
    this.value = ''; // 清空输入框
  }
});
```

### 3. Tab 栏切换（鼠标经过）
```css
/* 高亮类 */
.tab.active {
  border-bottom: 2px solid #ff6700;
  font-weight: 700;
}
.panel {
  display: none;
  margin-top: 10px;
}
.panel.active {
  display: block;
}
```
```javascript
const tabs = document.querySelectorAll('.tab');
const panels = document.querySelectorAll('.panel');

tabs.forEach((tab, index) => {
  tab.addEventListener('mouseenter', function() {
    // 切换选项卡高亮
    tabs.forEach(t => t.classList.remove('active'));
    this.classList.add('active');
    // 切换内容区
    panels.forEach(p => p.classList.remove('active'));
    panels[index].classList.add('active');
  });
});
```

### 4. 阻止事件冒泡
```javascript
// 子元素
const child = document.querySelector('.child');
// 父元素
const parent = document.querySelector('.parent');

child.addEventListener('click', function(e) {
  e.stopPropagation(); // 阻止事件冒泡到父元素
  console.log('子元素被点击');
});

parent.addEventListener('click', function() {
  console.log('父元素被点击'); // 子元素点击时不会触发
});
```


## 八、复习计划（建议周期）
### 1. 每周（30 分钟）
- 回顾“核心概念速查”，重点记忆事件监听三要素、this 指向规则、事件对象常用属性。
- 完成 1 个“10 分钟任务”，如回车发布评论、Tab 切换，巩固事件绑定与 this 应用。

### 2. 每两周（2 小时）
- 完成 1 个“1 小时任务”，如综合 Tab 栏+评论发布，整合事件类型、事件对象、回调函数。
- 用浏览器调试工具（F12→Sources）打断点，观察事件对象属性和 this 指向。

### 3. 每月（半天）
- 独立完成随机点名案例，包含开始/停止、数据删除、按钮禁用，检验综合应用能力。
- 补充学习事件委托（利用事件冒泡，给父元素绑定事件处理子元素），为后续学习铺垫。


## 九、自测题（检验掌握情况）
1. 事件监听的三要素是什么？DOM L0 和 L2 方式的核心区别是什么？
2. 常用的鼠标事件、焦点事件、键盘事件各有哪些？分别对应什么触发场景？
3. 如何获取事件对象？`clientX` 和 `offsetX` 的区别是什么？
4. 事件处理函数中，this 指向什么？定时器回调函数中的 this 指向什么？
5. 什么是回调函数？举两个实际开发中的使用场景。
6. 如何阻止表单默认提交行为？如何阻止事件冒泡？
7. 实现“鼠标经过选项卡切换内容”的核心逻辑是什么？


## 十、复习小贴士
1. **善用调试工具**：F12→Elements 选中元素→Event Listeners 查看绑定的事件，Sources 打断点观察事件对象和 this 变化。
2. **事件类型记忆技巧**：按“触发方式”分类记忆（鼠标/键盘/焦点/文本），结合案例场景（如输入用 input 事件）。
3. **this 指向判断**：牢记“谁调用谁就是 this”，不确定时用 `console.log(this)` 验证，避免想当然。
4. **优先使用 L2 事件绑定**：addEventListener 支持多函数绑定和事件流控制，是实际开发标准。
5. **积累常用模板**：把回车发布、Tab 切换、阻止默认行为的代码片段整理成册，开发时直接复用。