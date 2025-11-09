# Web APIs 第四天核心知识复习记录
## 一、本文档目的
- 梳理 Web APIs 第四天核心知识点（日期对象、节点操作、移动端事件、JS 插件、重绘与回流），重点突出日期处理、节点增删改查、学生信息表案例逻辑，非重点内容精简提炼，适配 10 分钟碎片化回顾与 1 小时集中复习。
- 解决“日期格式化踩坑”“节点操作性能差”“移动端事件冲突”等高频问题，补充日期补 0 技巧、节点操作优化、回流重绘避坑指南等必要知识点，帮助扎实掌握动态页面开发与移动端基础交互能力。


## 二、宏观结构（快速导航）
- 核心工具：日期对象（实例化、方法、时间戳、倒计时）
- 核心操作：节点操作（DOM 节点分类、查找/增加/删除/克隆节点）
- 拓展能力：移动端事件（touch 系列事件）
- 实用技巧：JS 插件使用流程
- 实战应用：综合案例（学生信息表、轮播图）
- 性能优化：重绘与回流（概念、区别、避坑）


## 三、核心概念速查（记忆卡）
### 1. 日期对象（核心重点）
日期对象用于表示和处理时间，是倒计时、时间显示等功能的基础。

#### （1）实例化（创建日期对象）
| 用法                          | 效果                                  | 示例                          |
|-------------------------------|---------------------------------------|-----------------------------------|
| `new Date()`                  | 获取当前系统时间                      | `const now = new Date();`          |
| `new Date('指定时间')`         | 获取指定时间（格式：'YYYY-MM-DD'/'YYYY-MM-DD HH:mm:ss'） | `const target = new Date('2025-12-31');` |

#### （2）核心方法（格式转换）
日期对象方法返回的数值需处理后才能使用，重点注意月份和星期的取值范围：

| 方法名          | 作用                                  | 取值范围/说明                          |
|-----------------|---------------------------------------|-----------------------------------|
| `getFullYear()`  | 获取年份                              | 四位数字（如 2025）                |
| `getMonth()`     | 获取月份                              | 0~11（需 +1 才是实际月份）          |
| `getDate()`      | 获取日期                              | 1~31（实际日期，无需转换）          |
| `getDay()`       | 获取星期                              | 0~6（0 代表周日，1~6 代表周一~周六） |
| `getHours()`     | 获取小时                              | 0~23（24 小时制）                  |
| `getMinutes()`   | 获取分钟                              | 0~59                              |
| `getSeconds()`   | 获取秒                                | 0~59                              |

- 关键技巧：数字补 0（如月份 3 → '03'）：
  ```javascript
  function padZero(num) {
    return num < 10 ? '0' + num : num;
  }
  ```

#### （3）时间戳（倒计时核心）
- 定义：从 1970 年 01 月 01 日 00:00:00 到目标时间的毫秒数，用于计算时间差。
- 三种获取方式：
  | 方式                          | 特点                                  | 示例                          |
  |-------------------------------|---------------------------------------|-----------------------------------|
  | `date.getTime()`              | 支持获取指定日期的时间戳              | `new Date('2025-12-31').getTime();` |
  | `+new Date()`                  | 简洁，支持指定日期（推荐）            | `+new Date('2025-12-31');`        |
  | `Date.now()`                   | 仅获取当前时间戳，不支持指定日期        | `Date.now();`                      |
- 倒计时计算逻辑：
  1. 计算时间差：`剩余毫秒数 = 目标时间戳 - 当前时间戳`（需转换为秒：`Math.floor(剩余毫秒数 / 1000)`）。
  2. 转换为天/时/分/秒：
     ```javascript
     const totalSec = Math.floor((targetTime - nowTime) / 1000);
     const d = Math.floor(totalSec / 60 / 60 / 24); // 天
     const h = Math.floor(totalSec / 60 / 60 % 24); // 时
     const m = Math.floor(totalSec / 60 % 60); // 分
     const s = Math.floor(totalSec % 60); // 秒
     ```


### 2. 节点操作（核心重点）
节点操作用于动态增删改查 DOM 元素，是实现动态页面的核心，重点优化操作性能。

#### （1）DOM 节点分类
DOM 树中所有内容都是节点，重点关注**元素节点**（标签）：
| 节点类型       | 示例                                  | 核心用途                          |
|----------------|---------------------------------------|-----------------------------------|
| 元素节点       | `<div>`、`<li>` 等标签                | 页面结构核心，动态增删改的主要对象  |
| 属性节点       | `class`、`href` 等属性                | 配合元素节点操作属性（如 `element.className`） |
| 文本节点       | 标签内的文字、空格、换行              | 动态修改文本内容（如 `element.innerText`） |

#### （2）查找节点（基于节点关系）
通过节点间的父子、兄弟关系查找，减少 `querySelector` 调用，提升性能：

| 查找目标       | 语法                          | 特点                                  |
|----------------|-------------------------------|---------------------------------------|
| 父节点         | `element.parentNode`           | 返回最近一级父元素节点，找不到返回 `null` |
| 子元素节点     | `element.children`（重点）     | 仅返回元素节点（过滤文本/注释节点），伪数组 |
| 所有子节点     | `element.childNodes`           | 包含文本、注释节点，不推荐使用        |
| 下一个兄弟节点 | `element.nextElementSibling`    | 仅返回元素节点，跳过文本/注释节点      |
| 上一个兄弟节点 | `element.previousElementSibling` | 仅返回元素节点，跳过文本/注释节点      |

- 示例（关闭二维码案例）：
  ```javascript
  // 点击关闭按钮，删除其父节点（二维码盒子）
  const closeBtn = document.querySelector('.close_btn');
  closeBtn.addEventListener('click', function() {
    this.parentNode.remove(); // this 指向关闭按钮，parentNode 是二维码盒子
  });
  ```

#### （3）增加节点（动态创建元素）
三步流程：创建 → 赋值内容 → 插入页面，重点避免频繁插入导致回流：

| 操作步骤       | 语法                          | 说明                                  |
|----------------|-------------------------------|---------------------------------------|
| 创建元素节点   | `document.createElement('标签名')` | 仅创建元素，未插入页面（不可见）        |
| 追加到父元素末尾 | `父元素.appendChild(新元素)`   | 新元素成为父元素最后一个子元素        |
| 插入到指定元素前 | `父元素.insertBefore(新元素, 参考元素)` | 新元素插入到参考元素之前              |
| 克隆已有节点   | `element.cloneNode(布尔值)`    | 布尔值 `true` 克隆后代节点，`false` 仅克隆自身（默认 `false`） |

- 示例（动态创建列表项）：
  ```javascript
  // 1. 创建 li 元素
  const li = document.createElement('li');
  // 2. 赋值内容
  li.innerText = '新列表项';
  // 3. 插入 ul 末尾
  const ul = document.querySelector('ul');
  ul.appendChild(li);
  ```

#### （4）删除节点
- 语法：`父元素.removeChild(要删除的元素)`（必须通过父元素删除，无父子关系则失败）。
- 区别：删除节点是从 DOM 树中移除（彻底消失），`display: none` 是隐藏（仍存在于 DOM 树）。


### 3. 移动端事件（拓展能力）
移动端专属触摸事件，适配手机端滑动、点击等交互：

| 事件名          | 触发场景                                  | 典型应用                          |
|-----------------|---------------------------------------|-----------------------------------|
| `touchstart`    | 手指触摸到 DOM 元素时触发                | 移动端点击、滑动开始                |
| `touchmove`     | 手指在 DOM 元素上滑动时持续触发          | 滑动轮播图、下拉刷新                |
| `touchend`      | 手指从 DOM 元素上移开时触发              | 滑动结束、点击完成                  |

- 注意：移动端事件可能与鼠标事件冲突（如 `click` 有 300ms 延迟），可通过 `touch` 事件替代或引入插件解决。


### 4. JS 插件（实用技巧）
插件是他人封装的现成代码，快速实现复杂效果（如轮播图），学习流程：
1. 查官网：了解插件功能（如 Swiper 官网 https://www.swiper.com.cn/）。
2. 找 Demo：找到符合需求的示例代码。
3. 引文件：引入插件的 CSS 和 JS 文件（本地或 CDN）。
4. 改配置：通过 API 文档修改参数（如轮播速度、自动播放）。
5. 避冲突：多个插件共存时，确保类名、变量名不重复。


### 5. 综合案例核心思路（重点）
#### （1）学生信息表
核心原则：**操作数据而非直接操作 DOM**，减少回流，提升性能：
1. 初始化空数组 `const students = []`，存储学生数据。
2. 录入功能：
   - 阻止表单默认提交，验证表单必填项（为空则提示）。
   - 收集表单数据，创建学生对象（含学号、姓名、年龄等），推入数组。
   - 清空表格 tbody，遍历数组动态生成 tr/td，插入 tbody。
3. 删除功能：
   - 事件委托给 tbody，点击删除按钮时，通过自定义属性 `data-index` 获取索引。
   - 用 `splice(索引, 1)` 删除数组对应数据，重新渲染表格。

#### （2）游乐园轮播图
基于 Swiper 插件实现，核心配置：自动播放、滑动切换、指示器，重点区分插件类名，避免冲突。


### 6. 重绘与回流（性能优化重点）
浏览器渲染流程：解析 DOM → 生成渲染树 → 布局（回流）→ 绘制（重绘）→ 显示。

| 概念       | 定义                                  | 关系                          | 常见触发操作                          |
|------------|---------------------------------------|-------------------------------|-----------------------------------|
| 回流（重排） | 元素尺寸、结构、布局改变，重新计算几何信息 | 回流必触发重绘                | 页面刷新、窗口resize、元素增删、修改宽高/margin/padding、修改字体大小 |
| 重绘       | 元素样式改变（不影响布局），重新绘制外观 | 重绘不一定触发回流            | 修改 color、background-color、outline、box-shadow |

- 优化技巧：
  1. 批量修改样式（如用 `class` 代替多次 `style` 赋值）。
  2. 动态创建元素时，先创建文档片段 `document.createDocumentFragment()`，批量插入后再追加到页面。
  3. 避免频繁读取 `offsetWidth`/`scrollTop` 等属性（触发回流）。


## 四、常见错误与陷阱（高频）
1. **日期对象月份/星期取值错误**：
   - 错误：`getMonth()` 返回 5 直接当作 5 月（实际是 6 月）。
   - 解决：月份需 +1，星期需转换（0→周日，1→周一）。

2. **节点删除未通过父元素**：
   - 错误：`element.removeChild(child)` 中 `element` 不是 `child` 的父元素。
   - 解决：先通过 `parentNode` 获取父元素，再删除（`child.parentNode.removeChild(child)`）。

3. **cloneNode 未克隆后代节点**：
   - 错误：`element.cloneNode(false)` 想克隆整个元素及子元素（实际仅克隆自身）。
   - 解决：需要克隆后代节点时，传入 `true`（`element.cloneNode(true)`）。

4. **表单验证位置错误**：
   - 错误：学生信息表中，表单验证写在阻止默认行为之前（无效）。
   - 解决：先阻止表单默认提交，再验证必填项，验证失败则中断流程。


## 五、快速练习（把知识变成肌肉记忆）
### 1. 10 分钟任务（基础回顾）
- 任务 1：编写函数，格式化当前时间为 `YYYY-MM-DD HH:mm:ss`（注意补 0）。
- 任务 2：用节点操作动态创建 3 个 li 元素，添加到 ul 中，内容分别为“Item 1”“Item 2”“Item 3”。
- 任务 3：实现简单倒计时，计算到 2025-12-31 23:59:59 的剩余天/时/分/秒。

### 2. 1 小时任务（综合应用）
- 需求：简化版学生信息表：
  1. 表单包含姓名、年龄输入框，提交按钮。
  2. 点击提交，验证表单不为空，新增学生到表格。
  3. 表格每行末尾有删除按钮，点击删除对应学生（事件委托）。


## 六、代码片段（常用模板，拷贝即用）
### 1. 日期格式化函数
```javascript
function formatDate(date = new Date()) {
  const year = date.getFullYear();
  const month = padZero(date.getMonth() + 1); // 月份+1
  const day = padZero(date.getDate());
  const hour = padZero(date.getHours());
  const minute = padZero(date.getMinutes());
  const second = padZero(date.getSeconds());
  return `${year}-${month}-${day} ${hour}:${minute}:${second}`;
}
// 数字补0
function padZero(num) {
  return num < 10 ? '0' + num : num;
}
// 使用
console.log(formatDate()); // 输出：2025-08-08 16:30:00
```

### 2. 节点批量创建（避免回流）
```javascript
const ul = document.querySelector('ul');
const fragment = document.createDocumentFragment(); // 文档片段，临时存储元素
// 批量创建 5 个 li
for (let i = 1; i <= 5; i++) {
  const li = document.createElement('li');
  li.innerText = `批量创建项 ${i}`;
  fragment.appendChild(li); // 先插入片段（无回流）
}
ul.appendChild(fragment); // 一次性插入页面（仅 1 次回流）
```

### 3. 学生信息表核心代码（简化版）
```html
<form class="student-form">
  姓名：<input type="text" name="uname" required>
  年龄：<input type="number" name="age" required>
  <button type="submit">提交</button>
</form>
<table>
  <tbody class="student-tbody"></tbody>
</table>
```
```javascript
const form = document.querySelector('.student-form');
const tbody = document.querySelector('.student-tbody');
let students = []; // 存储学生数据

// 提交表单
form.addEventListener('submit', (e) => {
  e.preventDefault(); // 阻止默认提交
  // 收集表单数据
  const uname = form.uname.value.trim();
  const age = form.age.value.trim();
  if (!uname || !age) {
    alert('姓名和年龄不能为空');
    return;
  }
  // 新增数据
  students.push({ uname, age, id: Date.now() });
  // 渲染表格
  renderTable();
  // 重置表单
  form.reset();
});

// 渲染表格
function renderTable() {
  tbody.innerHTML = ''; // 清空表格
  students.forEach((stu, index) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${stu.uname}</td>
      <td>${stu.age}</td>
      <td><button data-index="${index}">删除</button></td>
    `;
    tbody.appendChild(tr);
  });
}

// 删除学生（事件委托）
tbody.addEventListener('click', (e) => {
  if (e.target.tagName === 'BUTTON') {
    const index = e.target.dataset.index;
    students.splice(index, 1); // 删除数据
    renderTable(); // 重新渲染
  }
});
```


## 八、复习计划（建议周期）
### 1. 每周（30 分钟）
- 回顾“核心概念速查”，重点记忆日期格式化、节点增删流程、回流重绘触发条件。
- 完成 1 个“10 分钟任务”，如日期格式化、节点批量创建，巩固基础操作。

### 2. 每两周（2 小时）
- 完成 1 个“1 小时任务”，如简化版学生信息表，整合表单验证、节点操作、事件委托。
- 用浏览器性能面板（Performance）查看节点操作是否触发频繁回流，优化代码。

### 3. 每月（半天）
- 独立完成完整学生信息表案例，包含表单验证、数据增删、本地存储（预习内容），检验综合应用能力。
- 学习 Swiper 插件，实现移动端轮播图，掌握插件使用流程。


## 九、自测题（检验掌握情况）
1. 日期对象中 `getMonth()` 和 `getDay()` 的取值范围是什么？如何转换为实际月份和星期？
2. 获取时间戳的三种方式是什么？各自的特点是什么？
3. 节点查找中 `children` 和 `childNodes` 的区别是什么？推荐使用哪个？
4. 动态创建元素的三步流程是什么？如何避免频繁创建导致的回流？
5. 移动端常用的触摸事件有哪些？分别对应什么触发场景？
6. 回流和重绘的区别是什么？哪些操作会导致回流？如何优化？
7. 学生信息表案例中，为什么优先操作数据而非直接操作 DOM？


## 十、复习小贴士
1. **日期处理必补 0**：月份、日期、小时等小于 10 时补 0，保证格式统一（如 '08' 而非 '8'）。
2. **节点操作优化**：批量创建元素时用 `documentFragment`，减少页面插入次数，降低回流概率。
3. **事件委托优先用**：列表、表格等动态元素的事件，优先委托给父元素，避免重复绑定。
4. **回流重绘避坑**：尽量用 `class` 批量修改样式，避免频繁修改 `width`、`margin` 等布局属性。
5. **插件使用看文档**：JS 插件重点关注“引入文件”和“核心配置”，遇到问题先查 API 文档。