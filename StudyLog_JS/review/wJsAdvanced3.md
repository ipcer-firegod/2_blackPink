# JavaScript 进阶第三天核心知识复习记录
## 一、本文档目的
- 梳理 JavaScript 进阶第三天核心知识点（编程思想、构造函数、原型体系、综合案例），重点突出原型、原型继承、原型链三大核心概念，非重点内容精简提炼，适配 10 分钟碎片化回顾与 1 小时集中复习。
- 解决“构造函数内存浪费”“原型与对象原型关系混淆”“原型继承引用污染”等高频问题，补充 `Object.getPrototypeOf()` 替代非标准 `__proto__`、`instanceof` 原理等必要知识点，帮助扎实掌握面向对象编程核心逻辑。


## 二、宏观结构（快速导航）
- 核心基础：编程思想（面向过程 vs 面向对象）
- 核心铺垫：构造函数（封装特性与内存问题）
- 核心重点：原型体系（原型、constructor、对象原型、原型继承、原型链）
- 实战应用：综合案例（消息提示对象封装）
- 补充知识点：非标准属性替代方案、`instanceof` 原理


## 三、核心概念速查（记忆卡）
### 1. 编程思想（核心基础）
两种编程范式，按需选择，前端开发中两者结合使用。

| 编程思想       | 定义                                  | 核心特点                          | 优缺点                          |
|----------------|---------------------------------------|-----------------------------------|-----------------------------------|
| 面向过程（POP） | 按解决问题的步骤拆分，用函数实现步骤，依次调用 | 注重“步骤”，一步一步执行          | 优点：性能高；缺点：不易维护、复用性差、扩展性弱 |
| 面向对象（OOP） | 将事务拆分为对象，按对象功能分工合作       | 注重“对象”，功能封装在对象内      | 优点：易维护、复用性强、扩展性好；缺点：性能略低 |

- 面向对象三大特性：
  1. 封装性：将属性和方法组合到对象中，隐藏实现细节。
  2. 继承性：子对象可继承父对象的属性和方法，减少冗余。
  3. 多态性：同一方法在不同对象中有不同实现（JS 中通过原型链间接实现）。


### 2. 构造函数（核心铺垫）
#### （1）核心作用
通过 `new` 关键字实例化多个结构相同的对象，体现面向对象的**封装性**。

#### （2）语法示例
```javascript
function Star(uname, age) {
  this.uname = uname; // 实例属性
  this.age = age;
  this.sing = function() { // 实例方法
    console.log('我会唱歌');
  };
}
const ldh = new Star('刘德华', 18);
const zxy = new Star('张学友', 19);
```

#### （3）存在问题：内存浪费
- 每个实例对象的方法（如 `sing`）都是独立的函数（`ldh.sing !== zxy.sing`），重复创建导致内存浪费。
- 解决方案：将公共方法挂载到**原型对象**上，实现方法共享。


### 3. 原型体系（核心重点，分模块详细）
原型是 JS 实现面向对象继承的核心机制，需理清“构造函数-原型-实例对象”三者关系。

#### （3.1）原型（`prototype`）
- 定义：每个构造函数都自带一个 `prototype` 属性，指向**原型对象**（默认是空对象）。
- 核心作用：存储公共方法/属性，所有实例对象可共享，解决构造函数内存浪费问题。
- 语法示例（共享方法）：
  ```javascript
  // 构造函数
  function Star(uname, age) {
    this.uname = uname;
    this.age = age;
  }
  // 公共方法挂载到原型上
  Star.prototype.sing = function() {
    console.log('我会唱歌');
  };
  const ldh = new Star('刘德华', 18);
  const zxy = new Star('张学友', 19);
  console.log(ldh.sing === zxy.sing); // true（方法共享）
  ```
- `this` 指向：原型对象中的 `this` 与构造函数中的 `this` 一致，均指向**实例对象**。

#### （3.2）constructor 属性
- 位置：原型对象（`prototype`）和对象原型（`__proto__`）中均存在。
- 作用：指向当前原型对象对应的**构造函数**（“找爸爸”）。
- 注意事项：
  - 当直接给原型对象赋值新对象时，会覆盖原有 `constructor`，需手动指向原构造函数：
    ```javascript
    // 错误：覆盖原型后，constructor 指向 Object
    Star.prototype = {
      sing: function() {},
      dance: function() {}
    };
    console.log(Star.prototype.constructor); // Object

    // 正确：手动指向原构造函数
    Star.prototype = {
      constructor: Star, // 关键：指回 Star 构造函数
      sing: function() {},
      dance: function() {}
    };
    ```

#### （3.3）对象原型（`__proto__`）
- 定义：每个实例对象都自带一个 `__proto__` 属性（非标准属性，ES6 推荐用 `Object.getPrototypeOf(实例)` 替代）。
- 作用：指向创建该实例的构造函数的 `prototype` 原型对象，是实例访问原型方法的“桥梁”。
- 关系链：实例对象 → `__proto__` → 构造函数.prototype → 公共方法/属性。
- 示例验证：
  ```javascript
  console.log(ldh.__proto__ === Star.prototype); // true
  console.log(Object.getPrototypeOf(ldh) === Star.prototype); // true（推荐写法）
  ```

#### （3.4）原型继承（面向对象继承特性实现）
- 核心目的：子构造函数的实例继承父构造函数的属性和方法，减少代码冗余。
- 实现步骤（以“人类→男人/女人”为例）：
  1. 定义父构造函数（公共属性和方法）：
     ```javascript
     function Person() {
       this.head = 1;
       this.eyes = 2;
       this.legs = 2;
     }
     // 公共方法挂载到父构造函数原型
     Person.prototype.say = function() {
       console.log('会说话');
     };
     ```
  2. 子构造函数原型指向父构造函数实例（避免引用污染）：
     ```javascript
     function Man() {}
     // 关键：子原型 = 父实例（每个子构造函数有独立原型对象）
     Man.prototype = new Person();
     // 手动指回子构造函数
     Man.prototype.constructor = Man;
     // 子构造函数独有方法
     Man.prototype.smoking = function() {
       console.log('会吸烟');
     };
     ```
  3. 实例化子对象，继承父属性/方法：
     ```javascript
     const pink = new Man();
     console.log(pink.head); // 1（继承父属性）
     pink.say(); // 会说话（继承父方法）
     pink.smoking(); // 会吸烟（自身方法）
     ```
- 原理解析：子实例 → `__proto__` → 父实例 → `__proto__` → 父构造函数.prototype → 公共方法。

#### （3.5）原型链
- 定义：基于原型继承，不同构造函数的原型对象形成的**链状关联结构**（最终指向 `Object.prototype`，其 `__proto__` 为 `null`）。
- 查找规则（访问对象属性/方法时）：
  1. 先查找对象**自身**是否有该属性/方法。
  2. 无则通过 `__proto__` 查找其**原型对象**。
  3. 仍无则继续查找原型对象的原型（父构造函数原型）。
  4. 依次类推，直到 `Object.prototype`，仍无则返回 `undefined`。
- 核心示意图：
  ```
  实例对象 → __proto__ → 子构造函数.prototype（父实例） → __proto__ → 父构造函数.prototype → __proto__ → Object.prototype → __proto__ → null
  ```
- `instanceof` 运算符：检测构造函数的 `prototype` 是否在实例对象的原型链上（如 `pink instanceof Man` → `true`，`pink instanceof Person` → `true`）。

- 弹幕补充
对象原型（对象）  只要是对象，就有__proto__
原型对象（原型）  只要是原型对象，就有constructor

### 4. 综合案例：消息提示对象封装（面向对象实战）
#### （1）核心需求
封装模态框插件，支持打开（`open`）、关闭（`close`）功能，实现方法共享。

#### （2）核心步骤
1. 定义构造函数（创建 DOM 结构，存储公共属性）：
   ```javascript
   function Modal(title = '温馨提示', message = '默认信息') {
     // 创建模态框 DOM
     this.modalBox = document.createElement('div');
     this.modalBox.className = 'modal';
     this.modalBox.innerHTML = `
       <div class="header">${title}<i class="close">×</i></div>
       <div class="body">${message}</div>
     `;
   }
   ```
2. 原型上挂载 `open` 方法（添加 DOM 到页面，绑定关闭事件）：
   ```javascript
   Modal.prototype.open = function() {
     document.body.appendChild(this.modalBox);
     // 绑定关闭事件（指向实例自身，避免 this 丢失）
     this.modalBox.querySelector('.close').addEventListener('click', () => {
       this.close();
     });
   };
   ```
3. 原型上挂载 `close` 方法（从页面移除 DOM）：
   ```javascript
   Modal.prototype.close = function() {
     document.body.removeChild(this.modalBox);
   };
   ```
4. 实例化使用：
   ```javascript
   // 点击按钮打开模态框
   document.querySelector('.btn').addEventListener('click', () => {
     const modal = new Modal('权限提示', '您没有删除操作权限');
     modal.open();
   });
   ```


## 四、常见错误与陷阱（高频）
1. **原型重新赋值后丢失 constructor**：
   - 错误：`Star.prototype = { sing: () => {} }` 导致 `constructor` 指向 `Object`。
   - 解决：手动添加 `constructor: Star`。

2. **原型继承引用污染**：
   - 错误：子原型直接指向父对象（`Man.prototype = People`），多个子构造函数共享同一对象，修改相互影响。
   - 解决：子原型指向父构造函数实例（`Man.prototype = new Person()`）。

3. **误将 `__proto__` 作为标准属性使用**：
   - 错误：`__proto__` 是非标准属性，部分环境可能不支持。
   - 解决：用 `Object.getPrototypeOf(实例)` 获取原型，`Object.setPrototypeOf(实例, 原型)` 设置原型。

4. **原型方法中 this 指向错误**：
   - 错误：事件回调中 `this` 指向 DOM 元素（如关闭按钮），而非实例对象。
   - 解决：用箭头函数绑定 `this`，或提前保存 `const self = this`。


## 五、快速练习（把知识变成肌肉记忆）
### 1. 10 分钟任务（基础回顾）
- 任务 1：用构造函数 `Animal` 创建“猫”和“狗”对象，公共方法 `eat` 挂载到原型，验证方法共享。
- 任务 2：实现原型继承：`Animal` 为父构造函数（`legs: 4`），`Cat` 为子构造函数（独有方法 `catchMouse`），实例化 `Cat` 并调用继承和自身方法。
- 任务 3：验证原型链：`cat.__proto__ === Cat.prototype`、`Cat.prototype.__proto__ === Animal.prototype`。

### 2. 1 小时任务（综合应用）
- 需求：封装简易确认框插件 `Confirm`，继承 `Modal` 构造函数：
  1. 新增“确认”“取消”按钮，点击确认执行回调函数。
  2. 原型继承 `Modal` 的 `open` 方法，重写 DOM 结构。
  3. 实例化时传入标题、消息、确认回调，支持关闭和取消功能。


## 六、代码片段（常用模板，拷贝即用）
### 1. 原型继承完整模板
```javascript
// 父构造函数
function Parent() {
  this.pubProp = '公共属性';
}
// 父公共方法
Parent.prototype.pubMethod = function() {
  console.log('公共方法');
};

// 子构造函数
function Child() {
  this.subProp = '子属性'; // 子独有属性
}
// 原型继承：子原型 = 父实例
Child.prototype = new Parent();
// 手动指回子构造函数
Child.prototype.constructor = Child;
// 子独有方法
Child.prototype.subMethod = function() {
  console.log('子独有方法');
};

// 实例化
const child = new Child();
console.log(child.pubProp); // 公共属性（继承）
child.pubMethod(); // 公共方法（继承）
child.subMethod(); // 子独有方法
```

### 2. 数组扩展原型方法
```javascript
// 原型扩展数组求和方法
Array.prototype.sum = function() {
  return this.reduce((prev, item) => prev + item, 0);
};
// 原型扩展数组求最大值方法
Array.prototype.max = function() {
  return Math.max(...this);
};

console.log([1,2,3].sum()); // 6
console.log([4,1,9].max()); // 9
```

### 3. 消息提示框封装模板
```javascript
function Modal(title, message) {
  this.modalBox = document.createElement('div');
  this.modalBox.className = 'modal';
  this.modalBox.innerHTML = `
    <div class="header">${title}<i class="close">×</i></div>
    <div class="body">${message}</div>
  `;
}
// 打开方法
Modal.prototype.open = function() {
  document.body.appendChild(this.modalBox);
  this.modalBox.querySelector('.close').addEventListener('click', () => {
    this.close();
  });
};
// 关闭方法
Modal.prototype.close = function() {
  this.modalBox.remove();
};
// 使用
new Modal('提示', '操作成功').open();
```


## 八、复习计划（建议周期）
### 1. 每周（30 分钟）
- 回顾“原型体系”核心概念，重点记忆“构造函数-原型-实例”关系、原型链查找规则。
- 完成 1 个“10 分钟任务”，如原型继承、原型方法扩展。

### 2. 每两周（2 小时）
- 完成 1 个“1 小时任务”，如确认框插件封装，整合原型继承、事件绑定。
- 画图梳理原型链结构（从实例到 `null`），加深理解。

### 3. 每月（半天）
- 独立完成复杂插件封装（如分页插件），运用面向对象的封装、继承特性。
- 学习 ES6 `class` 语法（语法糖，底层仍是原型），对比传统原型继承的异同。


## 九、自测题（检验掌握情况）
1. 面向对象的三大特性是什么？面向过程和面向对象的核心区别是什么？
2. 构造函数存在什么问题？如何通过原型解决？
3. `prototype`、`__proto__`、`constructor` 三者的关系是什么？
4. 原型继承的实现步骤是什么？如何避免引用污染？
5. 原型链的查找规则是什么？`Object.prototype.__proto__` 指向什么？
6. `instanceof` 运算符的原理是什么？如何判断一个对象是否是某个构造函数的实例？
7. 如何安全地获取/设置对象的原型（替代非标准 `__proto__`）？


## 十、复习小贴士
1. **原型关系记忆技巧**：实例的 `__proto__` 指向构造函数的 `prototype`，原型的 `constructor` 指向构造函数。
2. **原型继承核心**：子原型必须指向父实例，而非父原型对象，避免多个子构造函数共享同一原型。
3. **避免原型污染**：不修改原生对象（如 `Array`、`Object`）的原型，防止覆盖原生方法。
4. **ES6 衔接**：原型是 ES6 `class` 的底层原理，掌握原型后学习 `class`、`extends` 会更轻松。
5. **案例多练**：消息提示框案例是面向对象封装的典型应用，至少独立写 2 遍，熟练掌握“构造函数+原型方法”的封装思路。