# JavaScript 高级第四天核心知识复习记录
## 一、本文档目的
- 梳理 JavaScript 高级第四天核心知识点（深浅拷贝、异常处理、this 指向与修改、性能优化、综合案例），重点突出深浅拷贝差异、this 动态修改、防抖节流实现与区别，非重点内容精简提炼，适配 10 分钟碎片化回顾与 1 小时集中复习。
- 解决“拷贝引用类型相互影响”“this 指向混乱”“高频事件性能损耗”等高频问题，补充 JSON 深拷贝局限性、防抖节流原生实现细节等必要知识点，帮助扎实掌握 JS 高阶实战技巧。


## 二、宏观结构（快速导航）
- 核心重点：深浅拷贝（浅拷贝方法与局限、深拷贝三种实现）
- 核心基础：异常处理（throw 抛异常、try/catch/finally 捕获、debugger 调试）
- 核心难点：处理 this（默认指向、箭头函数 this、改变 this 的三种方法）
- 核心应用：性能优化（防抖、节流的定义、实现、场景）
- 实战应用：综合案例（视频播放位置记录）
- 补充知识点：JSON 深拷贝局限性、防抖节流边界情况处理


## 三、核心概念速查（记忆卡）
### 1. 深浅拷贝（重点详细）
仅针对**引用类型**（对象、数组），解决“直接赋值导致相互影响”的问题，核心区别在于是否拷贝引用类型的“地址”。

#### （1）浅拷贝
- 定义：拷贝对象时，**简单类型拷贝值，引用类型拷贝地址**（单层对象无影响，多层对象仍相互干扰）。
- 常用方法：
  1. 对象：`Object.assign(目标对象, 源对象)`、`{...obj}`
  2. 数组：`Array.prototype.concat()`、`[...arr]`
- 示例：
  ```javascript
  const obj = { name: 'pink', family: { mother: 'pink妈妈' } };
  const obj2 = { ...obj };
  obj2.name = 'red'; // 简单类型修改不影响原对象
  obj2.family.mother = 'red妈妈'; // 引用类型修改影响原对象
  console.log(obj.family.mother); // 'red妈妈'
  ```

#### （2）深拷贝
- 定义：拷贝对象时，**无论多少层嵌套，均拷贝值而非地址**（原对象与新对象完全独立）。
- 常用方法（重点掌握）：
  1. 递归实现（自定义，灵活可控）：
     ```javascript
     function deepCopy(newObj, oldObj) {
       for (let k in oldObj) {
         // 处理数组（数组 instanceof Object 也为 true，需优先判断）
         if (oldObj[k] instanceof Array) {
           newObj[k] = [];
           deepCopy(newObj[k], oldObj[k]);
         } 
         // 处理对象
         else if (oldObj[k] instanceof Object) {
           newObj[k] = {};
           deepCopy(newObj[k], oldObj[k]);
         } 
         // 简单类型直接赋值
         else {
           newObj[k] = oldObj[k];
         }
       }
     }
     const newObj = {};
     deepCopy(newObj, oldObj);
     ```
     关键：需判断数组和对象类型，递归拷贝嵌套结构，必须加退出条件（避免循环引用）。

  2. lodash 库 `_.cloneDeep()`（实际开发首选）：
     ```javascript
     const obj3 = _.cloneDeep(obj);
     obj3.family.mother = 'new妈妈';
     console.log(obj.family.mother); // 'red妈妈'（无影响）
     ```

  3. JSON 序列化（简单场景使用，有局限性）：
     ```javascript
     const obj4 = JSON.parse(JSON.stringify(obj));
     ```
     局限性（补充知识点）：
     - 不能拷贝函数、undefined、Symbol 类型。
     - 不能处理循环引用（如 `obj.self = obj`）。
     - 会忽略 `undefined` 和函数属性。

- 核心区别：浅拷贝解决单层引用类型拷贝，深拷贝解决多层引用类型拷贝。


### 2. 异常处理（核心基础）
预估代码执行错误，避免程序崩溃，提升代码健壮性。

#### （1）throw 抛异常
- 作用：主动抛出错误，终止程序执行，明确错误原因。
- 语法：`throw new Error('错误提示信息')`（配合 Error 对象，错误信息更规范）。
- 示例：
  ```javascript
  function add(x, y) {
    if (!x || !y) {
      throw new Error('参数不能为空'); // 抛异常，后续代码不执行
    }
    return x + y;
  }
  add(); // 报错：Uncaught Error: 参数不能为空
  ```

#### （2）try/catch/finally 捕获异常
- 作用：捕获代码执行中的错误，不终止程序，可自定义错误处理逻辑。
- 语法结构：
  ```javascript
  try {
    // 可能出错的代码（如 DOM 查找、数据处理）
    const p = document.querySelector('.p');
    p.style.color = 'red';
  } catch (error) {
    // 捕获错误，error 为错误对象，error.message 获取错误信息
    console.log('错误原因：', error.message);
  } finally {
    // 无论是否出错，必执行（如关闭加载动画）
    console.log('执行完毕');
  }
  ```

#### （3）debugger 调试
- 作用：手动打断点，在浏览器开发者工具（Sources 面板）中逐步调试代码，查看变量值和执行流程。
- 用法：在需调试的代码行添加 `debugger;`，代码执行到此处会暂停。


### 3. 处理 this（核心难点）
#### （1）this 默认指向（回顾总结）
| 函数类型       | this 指向规则                                  | 示例                          |
|----------------|---------------------------------------|-----------------------------------|
| 普通函数       | 谁调用指向谁；无调用者（非严格模式）指向 window；严格模式下指向 undefined | `function fn() {} fn()` → window（非严格模式） |
| 箭头函数       | 无自身 this，沿用上一级作用域的 this（不随调用方式改变） | `const fn = () => {}` → 外层 this |
| 构造函数/原型函数 | 指向实例对象                                  | `new Person()` → 实例对象        |
| DOM 事件函数   | 指向触发事件的 DOM 元素                        | `btn.addEventListener('click', fn)` → btn |

- 箭头函数不适用场景（重点）：
  1. DOM 事件回调（this 指向 window，无法操作 DOM）。
  2. 构造函数/原型函数（this 指向外层，无法绑定实例）。
  3. 字面量对象中的方法（this 指向外层，无法访问对象属性）。

#### （2）改变 this 指向的三种方法（重点详细）
| 方法名   | 核心特点                                  | 语法                          | 应用场景                          |
|----------|---------------------------------------|-----------------------------------|-----------------------------------|
| call()    | 调用函数；改变 this；参数逐个传递          | `fn.call(thisArg, arg1, arg2, ...)` | 立即调用函数，需传递多个参数        |
| apply()   | 调用函数；改变 this；参数以数组传递        | `fn.apply(thisArg, [arg1, arg2])`  | 立即调用函数，参数为数组（如求数组最大值） |
| bind()    | 不调用函数；改变 this；返回新函数；参数逐个传递 | `const newFn = fn.bind(thisArg, arg1, ...)` | 不立即调用函数（如定时器回调、事件防抖节流） |

- 对比示例：
  ```javascript
  const obj = { name: 'pink' };
  function fn(x, y) { console.log(this.name, x + y); }

  fn.call(obj, 1, 2); // 调用函数，输出 'pink 3'
  fn.apply(obj, [1, 2]); // 调用函数，输出 'pink 3'
  const newFn = fn.bind(obj, 1, 2); // 不调用，返回新函数
  newFn(); // 调用新函数，输出 'pink 3'
  ```

- 核心区别总结：
  1. call/apply 立即调用函数，bind 不调用。
  2. call 传参为逗号分隔，apply 为数组，bind 传参与 call 一致。
  3. bind 返回新函数，可重复调用，适用于需要延迟执行的场景。


### 4. 性能优化：防抖与节流（核心应用）
解决“高频事件（如滚动、输入、鼠标移动）触发次数过多导致性能损耗”的问题。

#### （1）防抖（debounce）
- 定义：触发事件后，**n 秒内只执行一次函数**；若 n 秒内重复触发，重新计算计时（类似“连续触发则重新等待”）。
- 核心思路：利用定时器，触发事件时清除原有定时器，重新设置新定时器。
- 原生实现：
  ```javascript
  function debounce(fn, delay = 500) {
    let timeId;
    return function () {
      // 重复触发时清除定时器，重新计时
      if (timeId) clearTimeout(timeId);
      // 延迟执行函数
      timeId = setTimeout(() => {
        fn();
      }, delay);
    };
  }
  // 应用：搜索框输入防抖
  input.addEventListener('input', debounce(searchFn, 300));
  ```
- 适用场景：搜索框输入联想、窗口 resize 事件、按钮重复点击防重复提交。

#### （2）节流（throttle）
- 定义：连续触发事件时，**n 秒内只执行一次函数**；无论触发多少次，n 秒内仅执行一次（类似“固定频率执行”）。
- 核心思路：利用时间差，记录上次执行时间，当前时间 - 上次执行时间 ≥ 间隔时间才执行。
- 原生实现：
  ```javascript
  function throttle(fn, interval = 500) {
    let startTime = 0;
    return function () {
      const now = Date.now();
      // 时间差 ≥ 间隔时间则执行
      if (now - startTime >= interval) {
        fn();
        startTime = now; // 更新上次执行时间
      }
    };
  }
  // 应用：鼠标移动节流
  box.addEventListener('mousemove', throttle(moveFn, 500));
  ```
- 适用场景：鼠标移动、滚动条滚动、轮播图点击切换、视频播放进度记录。

#### （3）防抖与节流区别（重点）
| 特性       | 防抖                                  | 节流                                  |
|------------|---------------------------------------|---------------------------------------|
| 核心逻辑   | 触发后延迟执行，重复触发重新计时        | 固定间隔执行，重复触发不重新计时        |
| 执行次数   | 高频触发后仅执行一次（最后一次）        | 高频触发后按间隔执行多次                |
| 适用场景   | 输入、点击提交、窗口 resize            | 滚动、鼠标移动、轮播图点击            |
| lodash 用法 | `_.debounce(fn, delay)`               | `_.throttle(fn, interval)`             |


### 5. 综合案例：视频播放位置记录
- 核心需求：页面刷新后，视频从上次播放位置继续播放。
- 实现思路：
  1. 利用**节流**处理 `ontimeupdate` 事件（1 秒记录一次播放位置，避免高频触发）。
  2. 播放位置存储到本地存储 `localStorage`。
  3. 页面加载时（`onloadeddata` 事件），从本地存储读取位置并设置视频播放进度。
- 核心代码：
  ```javascript
  const video = document.querySelector('video');
  // 节流记录播放位置
  video.ontimeupdate = _.throttle(() => {
    localStorage.setItem('currentTime', video.currentTime);
  }, 1000);
  // 加载时恢复播放位置
  video.onloadeddata = () => {
    video.currentTime = localStorage.getItem('currentTime') || 0;
  };
  ```


## 四、常见错误与陷阱（高频）
1. **浅拷贝多层引用类型相互影响**：
   - 错误：认为 `Object.assign` 能拷贝多层对象。
   - 解决：多层对象必须用深拷贝（递归、lodash.cloneDeep）。

2. **JSON 深拷贝拷贝函数/循环引用**：
   - 错误：用 `JSON.parse(JSON.stringify)` 拷贝含函数或循环引用的对象。
   - 解决：函数/循环引用场景用递归深拷贝或 lodash.cloneDeep。

3. **箭头函数误用导致 this 指向错误**：
   - 错误：DOM 事件回调用箭头函数（this 指向 window，无法操作 DOM）。
   - 解决：DOM 事件、构造函数、原型函数中用普通函数，需上层 this 时用箭头函数。

4. **bind 方法未调用新函数**：
   - 错误：`fn.bind(obj)` 后未调用新函数，误以为已改变 this 并执行。
   - 解决：`const newFn = fn.bind(obj); newFn();`（bind 不调用函数，仅返回新函数）。

5. **防抖节流混淆使用场景**：
   - 错误：搜索框用节流（导致多次发送请求），滚动用防抖（导致仅最后一次执行）。
   - 解决：输入/提交用防抖，滚动/移动用节流。


## 五、快速练习（把知识变成肌肉记忆）
### 1. 10 分钟任务（基础回顾）
- 任务 1：用递归实现深拷贝，拷贝含数组和多层对象的复杂数据。
- 任务 2：用 call/apply/bind 分别改变函数 this 指向，传递参数并执行。
- 任务 3：用原生代码实现防抖函数，绑定到输入框 input 事件。

### 2. 1 小时任务（综合应用）
- 需求：实现带防抖节流的搜索功能：
  1. 搜索框输入防抖（300ms 后发送请求，重复输入重新计时）。
  2. 滚动页面加载更多数据（节流 1 秒，避免高频触发请求）。
  3. 处理请求异常（try/catch 捕获网络错误）。


## 六、代码片段（常用模板，拷贝即用）
### 1. 深拷贝递归实现
```javascript
function deepCopy(newObj, oldObj) {
  for (let k in oldObj) {
    if (oldObj[k] instanceof Array) {
      newObj[k] = [];
      deepCopy(newObj[k], oldObj[k]);
    } else if (oldObj[k] instanceof Object) {
      newObj[k] = {};
      deepCopy(newObj[k], oldObj[k]);
    } else {
      newObj[k] = oldObj[k];
    }
  }
}
```

### 2. 防抖/节流原生实现
```javascript
// 防抖
function debounce(fn, delay = 500) {
  let timeId;
  return function (...args) {
    if (timeId) clearTimeout(timeId);
    timeId = setTimeout(() => {
      fn.apply(this, args); // 保留 this 和参数
    }, delay);
  };
}

// 节流
function throttle(fn, interval = 500) {
  let startTime = 0;
  return function (...args) {
    const now = Date.now();
    if (now - startTime >= interval) {
      fn.apply(this, args);
      startTime = now;
    }
  };
}
```

### 3. 改变 this 指向示例
```javascript
const user = { name: 'pink' };
function sayHi(x, y) {
  console.log(this.name, x + y);
}
// call
sayHi.call(user, 1, 2); // pink 3
// apply
sayHi.apply(user, [1, 2]); // pink 3
// bind
const newSayHi = sayHi.bind(user, 1, 2);
newSayHi(); // pink 3
```


## 八、复习计划（建议周期）
### 1. 每周（30 分钟）
- 回顾“深浅拷贝区别”“this 指向规则”“防抖节流实现”，重点记忆核心方法和应用场景。
- 完成 1 个“10 分钟任务”，如递归深拷贝、原生防抖实现。

### 2. 每两周（2 小时）
- 完成 1 个“1 小时任务”，如搜索功能防抖节流+异常处理，整合多个知识点。
- 对比 lodash 库的防抖节流与原生实现，理解源码核心逻辑。

### 3. 每月（半天）
- 独立实现复杂场景：如带防抖的表单提交、带节流的滚动加载+下拉刷新，检验综合应用能力。
- 补充学习：循环引用的深拷贝处理、防抖节流的立即执行版（文档未提及，拓展学习）。


## 九、自测题（检验掌握情况）
1. 浅拷贝和深拷贝的核心区别是什么？浅拷贝的方法有哪些？
2. JSON.stringify 实现深拷贝有哪些局限性？
3. 普通函数和箭头函数的 this 指向规则分别是什么？
4. call、apply、bind 的区别和各自的应用场景是什么？
5. 防抖和节流的定义、核心逻辑、适用场景分别是什么？
6. 如何用原生代码实现防抖函数？
7. 视频播放位置记录案例中，为什么用节流而非防抖？




### 1. 浅拷贝与深拷贝核心区别；浅拷贝方法
- 核心区别：**浅拷贝只拷贝一层，深层引用类型共享**；**深拷贝拷贝所有层级，完全独立**。
- 浅拷贝方法：`...` 展开运算符、`Object.assign()`、数组 `slice()`/`concat()`。

### 2. JSON.stringify 深拷贝的局限性
- 无法拷贝 **函数、undefined、Symbol**（会丢失）；
- 无法拷贝 **循环引用**（报错）；
- 无法拷贝 **正则、Date、Set、Map**（类型丢失）。

### 3. 普通函数与箭头函数 this 指向
- 普通函数：**谁调用指向谁**，默认指向 window，严格模式指向 undefined。
- 箭头函数：**无自己的 this**，继承**定义时所在作用域的 this**。

### 4. call、apply、bind 区别与场景
- **call**：立即执行，参数**逐个传递**，用于**临时修改 this**。
- **apply**：立即执行，参数**数组/伪数组**，用于**数组相关操作**。
- **bind**：不立即执行，返回**新函数**，用于**事件/定时器绑定 this**。

### 5. 防抖与节流定义、逻辑、场景
- **防抖**：频繁触发时**只执行最后一次**，核心：清空定时器重新计时；场景：搜索框输入、窗口 resize。
- **节流**：频繁触发**固定时间只执行一次**，核心：加锁控制频率；场景：滚动加载、鼠标移动。

### 6. 原生防抖函数实现
```js
function debounce(fn, delay) {
  let timer = null
  return function (...args) {
    clearTimeout(timer)
    timer = setTimeout(() => fn.apply(this, args), delay)
  }
}
```

### 7. 视频播放记录用节流不用防抖
- 视频播放**需要持续记录位置**，防抖需等停止才执行，会丢失中间状态；
- 节流**每隔一段时间记录一次**，既能保证数据准确，又不频繁执行。




## 十、复习小贴士
1. **深浅拷贝记忆**：浅拷贝“抄地址”（多层干扰），深拷贝“抄内容”（完全独立），优先用 lodash.cloneDeep 开发。
2. **this 指向技巧**：普通函数“谁调用指向谁”，箭头函数“找爸爸的 this”，改变 this 用 bind（延迟执行）、call/apply（立即执行）。
3. **防抖节流选择**：“输入/提交”用防抖，“滚动/移动”用节流，记不住就想“防抖是等最后一次，节流是固定频率”。
4. **异常处理习惯**：网络请求、DOM 操作、数据解析等易出错场景，必用 try/catch 捕获，避免程序崩溃。
5. **案例多练**：防抖节流是面试高频题，至少独立写 2 遍原生实现，结合实际场景（如搜索、滚动）理解应用价值。