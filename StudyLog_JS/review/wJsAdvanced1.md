# JavaScript 高级第一天核心知识复习记录
## 一、本文档目的
- 梳理 JavaScript 高级第一天核心知识点（作用域、函数进阶、解构赋值、综合案例），重点突出闭包、箭头函数、解构赋值实战，非重点内容精简提炼，适配 10 分钟碎片化回顾与 1 小时集中复习。
- 解决“作用域混淆”“箭头函数 this 指向错误”“解构赋值场景遗漏”等高频问题，补充闭包内存泄漏优化、箭头函数适用场景限制等必要知识点，帮助扎实掌握 JS 高级语法基础。


## 二、宏观结构（快速导航）
- 核心基础：作用域（局部/全局/作用域链、变量提升）
- 核心重点：闭包（概念、作用、问题）、垃圾回收机制
- 核心进阶：函数进阶（函数提升、参数、箭头函数）
- 核心语法：解构赋值（数组解构、对象解构）
- 实战应用：综合案例（商品列表渲染、价格筛选）
- 补充知识点：闭包优化、箭头函数不适用场景


## 三、核心概念速查（记忆卡）
### 1. 作用域（核心基础）
作用域规定变量的访问范围，避免变量污染，分为三类：

#### （1）局部作用域（变量仅当前范围可访问）
| 类型         | 定义                                  | 关键特性                          | 示例                          |
|--------------|---------------------------------------|-----------------------------------|-----------------------------------|
| 函数作用域   | 函数内部声明的变量                    | 函数执行完毕后变量自动回收        | `function fn() { let a = 1; } console.log(a)` → 报错 |
| 块作用域     | `{}` 包裹区域（let/const 声明）        | let/const 产生，var 不产生        | `if (true) { let b = 2; } console.log(b)` → 报错 |

#### （2）全局作用域（所有范围可访问）
- 范围：`<script>` 标签最外层、.js 文件最外层。
- 注意事项：
  - 避免过多声明全局变量，防止污染。
  - 函数内未用关键字声明的变量（隐式全局）、window 动态添加的属性，默认是全局变量（不推荐）。

#### （3）作用域链（变量查找机制）
- 本质：嵌套作用域的串联，用于变量查找。
- 查找规则：
  1. 优先查找当前作用域变量。
  2. 未找到则逐级向上查找父级作用域，直到全局作用域。
  3. 子作用域可访问父作用域，反之不行。

#### （4）变量提升（仅 var 存在）
- 现象：var 声明的变量可在声明前访问，值为 `undefined`。
- 原理：变量声明被提升到当前作用域最顶部，赋值不提升。
- 注意：let/const 无变量提升，声明前访问会报“暂时性死区”错误。

#### （5）垃圾回收机制（GC）
- 定义：JS 自动分配和回收内存，避免内存泄漏。
- 内存生命周期：分配 → 使用 → 回收。
- 常见算法：
  1. 引用计数法：跟踪引用次数，次数为 0 回收（存在循环引用漏洞）。
  2. 标记清除法（现代浏览器使用）：从全局出发，标记可达对象，未标记则回收（解决循环引用问题）。
- 内存泄漏：不再使用的内存未释放（如闭包滥用、未清理的事件监听）。

#### （6）闭包（重点详细）

- 我的一点理解：类似于类的私有属性和方法，可以通过公共方法访问。闭包可以让函数内部的变量和函数不被外部直接访问，从而实现数据的封装和保护。

- 概念：`闭包 = 内层函数 + 外层函数的变量`，内层函数访问外层函数变量。
- 作用：
  1. 封闭数据，实现数据私有（外部无法直接修改）。
  2. 延长外层函数变量的生命周期。
- 示例（统计函数调用次数）：
  ```javascript
  function countFn() {
    let count = 0;
    return function() {
      count++;
      console.log(`调用${count}次`);
    };
  }
  // const callCount 是一个函数
  const callCount = countFn();
  callCount(); // 调用1次
  ```
- 问题：可能导致内存泄漏，需及时释放引用（如 `callCount = null`）。


### 2. 函数进阶（核心重点）
#### （1）函数提升
- 函数声明：存在提升，可在声明前调用（`function fn() {}`）。
- 函数表达式：无提升，声明前调用报错（`var fn = function() {}`）。

#### （2）函数参数
| 类型         | 定义                                  | 特性                          | 示例                          |
|--------------|---------------------------------------|-----------------------------------|-----------------------------------|
| 动态参数 arguments | 函数内置伪数组，存储所有实参          | 仅普通函数有，箭头函数无        | `function sum() { return [...arguments].reduce((a,b)=>a+b); }` |
| 剩余参数 ...args | 接收多余实参，返回真数组              | 普通函数和箭头函数都可用，需置于形参末尾 | `function sum(...args) { return args.reduce((a,b)=>a+b); }` |
| 展开运算符 ... | 展开数组/对象，用于函数传参、数组合并 | 非参数场景，用于数组展开        | `Math.max(...[1,3,5])` → 5；`[...arr1, ...arr2]`,前面===`[1,2,3 , 4,5,6]` |

- 关键区别：剩余参数用于“接收”多余实参（写在形参末尾），展开运算符用于“展开”数组/对象（写在数组里面）。

#### （3）箭头函数（重点详细）
- 核心目的：简洁语法，不绑定自身 this。
- 语法（多场景）：
  1. 无参数：`const fn = () => { 代码 }`。
  2. 单参数：可省略括号 `const fn = x => x * 2`。
  3. 单句返回：省略花括号和 return `const fn = (x,y) => x + y`。
  4. 返回对象：需加括号 `const fn = name => ({ name: name })`。
- 参数特性：无 arguments，需用剩余参数 `(...args)`。
- this 指向（核心差异）：
  1. 不创建自身 this，沿用作用域链上一层的 this。
  2. 普通函数 this 指向调用者，箭头函数 this 固定不变。
  3. 不适合场景：事件回调（this 指向 window）、构造函数（无法实例化）、对象方法（this 不指向对象）。

#### （4）数组方法（案例核心）
| 方法名   | 作用                                  | 语法                          | 示例                          |
|----------|---------------------------------------|-----------------------------------|-----------------------------------|
| forEach  | 遍历数组，执行回调函数                | `arr.forEach((item, index) => {})` | 商品列表渲染                    |
| filter   | 筛选符合条件的元素，返回新数组        | `arr.filter(item => 条件)`         | 商品价格筛选                    |


### 3. 解构赋值（核心语法）
快速批量赋值语法，分数组解构和对象解构，简化代码。

#### （1）数组解构
- 基本语法：`const [a,b,c] = 数组`。
- 关键场景：
  1. 变量多、单元值少：多余变量为 undefined。
  2. 变量少、单元值多：用剩余参数 `const [a,b,...rest] = 数组`。
  3. 默认值：`const [a='默认值', b] = [1]`。
  4. 按需导入：`const [a,,c] = [1,2,3]`（忽略第二个元素）。
  5. 多维解构：`const [a,[b,c]] = [1,[2,3]]`。
  6. 交换变量：`[a,b] = [b,a]`（前面有语句需加 `;`）。

#### （2）对象解构
- 基本语法：`const {name, age} = 对象`（变量名与属性名一致）。
- 关键场景：
  1. 重命名：`const {name: uname, age} = 对象`。
  2. 多级解构：`const {name, family: {mother, father}} = 对象`。
  3. 数组对象解构：`const [{goodsName, price}] = 数组对象`。
  4. 函数参数解构：`function render({data}) {}`（接收接口数据）。
```js
    // const { data } = msg
    // msg 虽然很多属性，但是我们利用解构只要 data值
    function render({ data }) {
      console.log(data)
    }
```

### 4. 综合案例核心思路
#### （1）商品列表渲染
- 核心：用 `forEach` 遍历数据，字符串拼接生成 DOM 结构，赋值给容器。
- 步骤：1. 定义数据；2. 遍历生成结构；3. 插入页面。
```js
    let str = ''
    goodsList.forEach(item => {
      // console.log(item)  // 可以得到每一个数组元素  对象 {id: '4001172'}
      // 对象解构
      const { name, price, picture } = item
      str += `
      <div class="item">
        <img src=${picture} alt="">
        <p class="name">${name}</p>
        <p class="price">${price}</p>
      </div>
      `
    })
    document.querySelector('.list').innerHTML = str
```

#### （2）商品价格筛选
- 核心：用 `filter` 筛选符合条件的数据，重新渲染页面。
- 步骤：1. 事件委托绑定点击事件；2. 根据条件筛选数据；3. 调用渲染函数。


## 四、常见错误与陷阱（高频）
1. **块作用域混淆**：
   - 错误：用 var 声明变量，块级作用域不生效（`if (true) { var a = 1; } console.log(a)` → 1）。
   - 解决：优先用 let/const 声明变量，产生块作用域。

2. **闭包内存泄漏**：
   - 错误：长期持有闭包引用，导致外层函数变量无法回收。
   - 解决：不需要时释放引用（`fn = null`）。

3. **箭头函数 this 误用**：
   - 错误：事件回调用箭头函数（`btn.addEventListener('click', () => { console.log(this) })` → window）。
   - 解决：事件回调用普通函数，或手动绑定 this。

4. **解构赋值语法错误**：
   - 错误：数组解构前面有语句未加分号（`let a=1; [a,b] = [2,3]` 正确；`let a=1 [a,b] = [2,3]` 报错）。
   - 解决：数组解构前面有语句时，前面加 `;`。

5. **剩余参数位置错误**：
   - 错误：剩余参数未置于形参末尾（`function fn(...args, a) {}` 报错）。
   - 解决：剩余参数必须是最后一个形参。


## 五、快速练习（把知识变成肌肉记忆）
### 1. 10 分钟任务（基础回顾）
- 任务 1：用闭包实现计数器，调用一次加 1，支持重置功能。
- 任务 2：用箭头函数改写普通函数，对比 this 指向差异。
- 任务 3：解构接口数据 `const res = { code:200, data: { name:'小明', age:18 } }`，提取 name 和 age。

### 2. 1 小时任务（综合应用）
- 需求：实现商品列表渲染与筛选：
  1. 定义商品数据（含名称、价格）。
  2. 用 forEach 渲染商品列表。
  3. 用 filter 实现 0-100 元、100-300 元、300 元以上筛选功能。


## 六、代码片段（常用模板，拷贝即用）
### 1. 闭包计数器
```javascript
function createCounter() {
  let count = 0;
  return {
    increment: () => count++,
    reset: () => count = 0,
    getCount: () => count
  };
}
const counter = createCounter();
counter.increment();
console.log(counter.getCount()); // 1
counter.reset();
console.log(counter.getCount()); // 0
```

### 2. 箭头函数 vs 普通函数 this 对比
```javascript
const user = {
  name: '小明',
  // 普通函数：this 指向 user
  sayHi1: function() { console.log(this.name); },
  // 箭头函数：this 指向外层作用域（window）
  sayHi2: () => { console.log(this.name); }
};
user.sayHi1(); // 小明
user.sayHi2(); // undefined
```

### 3. 数组/对象解构实战
```javascript
// 数组解构：交换变量+默认值
let a = 1, b = 2;
;[a, b] = [b, a]; // 前面加分号（若前面有语句）
const [x, y = 3] = [4]; // x=4, y=3

// 对象解构：重命名+多级解构
const res = {
  data: {
    goods: [{ name: '手机', price: 1999 }]
  }
};
const { data: { goods: [product] } } = res;
console.log(product.name); // 手机
```

### 4. 商品筛选案例核心代码
```javascript
const goodsList = [
  { name: '白酒杯', price: 99 },
  { name: '茶具', price: 288 },
  { name: '酒具套装', price: 488 }
];

// 渲染函数
// function renderGoods(goods) {
//       const list = document.querySelector('.goods-list');
//       let str = ''
//       goods.forEach(item => {
//         const { name, price } = item
//         str += `
//         <div>
//          <h3 class="name">${name}</h3>
//          <p class="price">¥${price}</p>
//         </div> 
//         `
//       })
//       list.innerHTML = str
// }

// 渲染函数
function renderGoods(goods) {
  const list = document.querySelector('.goods-list');
  list.innerHTML = '';
  goods.forEach(item => {
    const div = document.createElement('div');
    div.innerHTML = `<h3>${item.name}</h3><p>¥${item.price}</p>`;
    list.appendChild(div);
  });
}

// 筛选功能（事件委托）
document.querySelector('.filter').addEventListener('click', (e) => {
  // dataset.type 获取 data-type 自定义属性值
  const type = e.target.dataset.type;
  let filtered = goodsList;
  switch(type) {
    case '0-100': filtered = goodsList.filter(g => g.price <= 100); break;
    case '100-300': filtered = goodsList.filter(g => g.price >100 && g.price <=300); break;
    case '300+': filtered = goodsList.filter(g => g.price >300); break;
  }
  renderGoods(filtered);
});

// 初始渲染
renderGoods(goodsList);
```


## 八、复习计划（建议周期）
### 1. 每周（30 分钟）
- 回顾“核心概念速查”，重点记忆闭包、箭头函数 this 指向、解构赋值场景。
- 完成 1 个“10 分钟任务”，如闭包计数器、解构实战。

### 2. 每两周（2 小时）
- 完成 1 个“1 小时任务”，如商品列表筛选，整合箭头函数、解构、数组方法。
- 用浏览器调试工具查看箭头函数的 this 指向，验证闭包的变量生命周期。

### 3. 每月（半天）
- 独立完成综合案例，添加新功能（如价格排序、搜索功能），巩固知识点。
- 学习闭包的实际应用场景（如模块化、防抖节流），拓展知识边界。


## 九、自测题（检验掌握情况）
1. 局部作用域分为哪两种？let/const 和 var 的作用域差异是什么？
2. 闭包的定义是什么？作用和可能引发的问题分别是什么？
3. 箭头函数和普通函数的核心差异有哪些？为什么事件回调不推荐用箭头函数？
4. 剩余参数和展开运算符的区别是什么？各自的使用场景是什么？
5. 数组解构中，如何处理变量数量和单元值数量不匹配的情况？
6. forEach 和 filter 方法的作用是什么？返回值有何不同？
7. 对象解构中，如何给变量重命名？如何解构多级对象？


## 十、复习小贴士
1. **作用域记忆技巧**：let/const 有块作用域，var 没有；函数作用域仅函数内部可访问。
2. **闭包使用原则**：避免不必要的闭包，用完及时释放引用，防止内存泄漏。
3. **箭头函数判断**：只要涉及 this 指向调用者，就不用箭头函数（如对象方法、事件回调）。
4. **解构赋值避坑**：数组解构前面有语句必须加分号，对象解构变量名需与属性名一致（或重命名）。
5. **案例多练**：商品列表案例是数组方法、解构、事件委托的综合应用，至少独立写 2 遍，熟练掌握流程。