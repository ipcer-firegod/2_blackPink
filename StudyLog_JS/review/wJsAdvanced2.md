# JavaScript 高级第二天核心知识复习记录
## 一、本文档目的
- 梳理 JavaScript 高级第二天核心知识点（深入对象、内置构造函数、购物车综合案例），重点突出构造函数实例化、数组核心方法（reduce）、对象/字符串常用操作，非重点内容精简提炼，适配 10 分钟碎片化回顾与 1 小时集中复习。
- 解决“构造函数与普通函数混淆”“数组方法使用场景模糊”“小数精度计算错误”等高频问题，补充伪数组定义、小数精度优化方案等必要知识点，帮助扎实掌握对象与内置构造函数的实战应用能力。


## 二、宏观结构（快速导航）
- 核心基础：深入对象（创建对象、构造函数、实例成员&静态成员）
- 核心重点：内置构造函数（Object/Array/String/Number，含常用方法）
- 实战应用：综合案例（购物车展示，整合数组/对象/字符串方法）
- 补充知识点：伪数组定义、小数精度问题解决方案


## 三、核心概念速查（记忆卡）
### 1. 深入对象（核心基础）
#### （1）创建对象的三种方式
1. 对象字面量：`const obj = { name: '佩奇' }`（最常用）。
2. 内置构造函数：`const obj = new Object({ name: '佩奇' })`（了解）。
3. 自定义构造函数：`new 构造函数名(参数)`（批量创建类似对象，重点）。

#### （2）构造函数（重点详细）
- 核心作用：快速创建多个结构相同、值不同的对象（如多个商品、用户对象）。
- 两大约定：
  1. 函数名以**大写字母开头**（区分普通函数）。
  2. 必须通过 `new` 关键字调用（实例化）。
- 语法示例：
  ```javascript
  // 定义构造函数
  function Goods(name, price, count) {
    this.name = name; // 实例属性
    this.price = price;
    this.count = count;
  }
  // 实例化对象
  const phone = new Goods('小米手机', 1999, 20);
  ```
- 实例化执行过程：
  1. 创建空对象 → 2. 构造函数 `this` 指向空对象 → 3. 执行构造函数代码（添加属性） → 4. 返回新对象（无需手动写 return）。
- 注意：无参数时可省略 `()`（`new Goods()` 可写为 `new Goods`），但不推荐，可读性差。

#### （3）实例成员&静态成员
| 成员类型   | 定义                                  | 访问方式                          | 示例                          |
|------------|---------------------------------------|-----------------------------------|-----------------------------------|
| 实例成员   | 实例对象的属性/方法（构造函数内 `this` 绑定） | 实例对象.成员名                    | `phone.name`、`phone.count`        |
| 静态成员   | 构造函数自身的属性/方法（直接绑定构造函数） | 构造函数.成员名                    | `Goods.brand = '小米'`（静态属性）、`Goods.showInfo = () => {}`（静态方法） |
- 核心区别：实例成员属于单个对象，静态成员属于构造函数（公共特性，如默认属性、工具方法）。

#### class
“es6之后官方就推荐使用class替代传统构造函数，虽然这玩意儿还能用，但是没有class简洁灵活“
class语法糖只是让我们用更简洁的方式去创建构造函数和原型方法，底层依然是基于原型链实现的。
以下是class的基本语法：

```js
class Person {
  constructor(name, age) { // 构造函数
    this.name = name;
    this.age = age;
  }

  // 原型方法
  greet() {
    console.log(`Hello, my name is ${this.name} and I'm ${this.age} years old.`);
  }

  // 静态方法
  static info() {
    console.log('This is a Person class.');
  }
}
const alice = new Person('Alice', 30);
alice.greet(); // Hello, my name is Alice and I'm 30 years old.
Person.info(); // This is a Person class.
```


### 2. 内置构造函数（核心重点）
JavaScript 内置构造函数用于创建对应类型数据，提供大量实用方法，重点掌握 Object/Array/String/Number 的常用方法。

#### （1）Object 构造函数（操作对象）
核心用于获取对象属性/值、拷贝对象，重点掌握 3 个静态方法：
| 方法名        | 作用                                  | 语法                          | 示例                          |
|---------------|---------------------------------------|-----------------------------------|-----------------------------------|
| Object.keys()  | 获取对象所有属性名，返回数组          | `Object.keys(对象)`              | `Object.keys({ name: '佩奇', age: 6 })` → `['name', 'age']` |
| Object.values()| 获取对象所有属性值，返回数组          | `Object.values(对象)`            | `Object.values({ name: '佩奇', age: 6 })` → `['佩奇', 6]` |
| Object.assign()| 对象拷贝/合并，浅拷贝                | `Object.assign(目标对象, 源对象)`  | `Object.assign(obj, { gender: '女' })`（给 obj 新增属性） |
- 常用场景：遍历对象（替代 for...in）、合并对象属性、批量获取对象数据。

#### （2）Array 构造函数（操作数组）
数组核心方法分“核心方法”（高频实战）和“其他方法”（按需使用），重点掌握前 4 个核心方法：

##### ① 核心方法（重点详细）
| 方法名   | 作用                                  | 语法                          | 核心特点                          |
|----------|---------------------------------------|-----------------------------------|-----------------------------------|
| forEach  | 遍历数组，执行回调（无返回值）        | `arr.forEach((item, index) => {})` | 仅用于遍历打印，不修改原数组        |
| filter   | 筛选符合条件的元素，返回新数组        | `arr.filter(item => 条件)`         | 不修改原数组，返回筛选后新数组      |
| map      | 迭代处理数组元素，返回新数组          | `arr.map(item => 处理逻辑)`        | 批量处理数据（如格式化、转换）      |
| reduce   | 累计处理数组，返回最终结果            | `arr.reduce((prev, item) => 逻辑, 起始值)` | 求和、求总、数据汇总（核心高频）    |

- reduce 深度解析（购物车求和核心）：
  - 无起始值：prev 初始为数组第 1 个元素，从第 2 个元素开始遍历。
  - 有起始值（推荐）：prev 初始为起始值，从第 1 个元素开始遍历。
  - 示例（员工涨薪 30% 总成本）：
    ```javascript
    const staff = [{ salary: 10000 }, { salary: 20000 }];
    const total = staff.reduce((prev, item) => prev + item.salary * 0.3, 0); // 起始值 0
    // 如果无起始值，第一个prev为一个对象 { salary: 10000 }，会导致计算错误；所以推荐使用有初始值的形式
    ```

##### ② 其他常用方法（精简列出）
| 方法名        | 作用                                  | 关键说明                          |
|---------------|---------------------------------------|-----------------------------------|
| join()        | 数组元素拼接为字符串                  | `arr.join('/')`（分隔符自定义）    |
| find()        | 查找第一个符合条件的元素              | 返回元素本身，无则返回 undefined   |
| findIndex()   | 查找第一个符合条件的元素索引          | 返回索引，无则返回 -1              |
| every()       | 检测所有元素是否符合条件              | 全符合返回 true，否则 false        |
| some()        | 检测是否有元素符合条件                | 有一个符合返回 true，否则 false    |
| concat()      | 合并数组                              | 返回新数组，不修改原数组            |
| sort()        | 数组排序                              | 修改原数组，需传比较函数（`(a,b) => a - b` 升序） |
| splice()      | 删除/替换数组元素                      | 修改原数组，返回删除元素组成的数组  |
| reverse()     | 反转数组                              | 修改原数组                        |
| Array.from()  | 伪数组转换为真数组                    | 静态方法，`Array.from(伪数组)`     |

##### ③ 伪数组补充知识点
- 定义：有 length 属性、按索引存储数据，但无数组方法（如 `arguments`、DOM 集合）。
- 转换方式：`Array.from(伪数组)` 或 `[...伪数组]`。

#### （3）String 构造函数（操作字符串）
字符串为基本类型，但底层会“包装”为对象，支持以下常用方法：
| 方法名          | 作用                                  | 语法/示例                          |
|-----------------|---------------------------------------|-----------------------------------|
| length（属性）  | 获取字符串长度                        | `'hello'.length` → 5              |
| split()         | 字符串拆分为数组                      | `'50g茶叶,清洗球'.split(',')` → `['50g茶叶', '清洗球']` |
| substring(start[, end]) | 截取字符串                          | `'abcde'.substring(1, 3)` → 'bc'  |
| startsWith()    | 检测是否以某字符开头                  | `'hello'.startsWith('he')` → true  |
| endsWith()      | 检测是否以某字符结尾                  | `'hello'.endsWith('lo')` → true    |
| includes()      | 检测是否包含某字符                    | `'hello'.includes('ll')` → true    |
| toUpperCase()   | 转为大写                              | `'abc'.toUpperCase()` → 'ABC'     |
| toLowerCase()   | 转为小写                              | `'ABC'.toLowerCase()` → 'abc'     |
| replace()       | 替换字符串（支持正则）                | `'hello'.replace('l', 'x')` → 'hexxo' |
| match()         | 查找字符串（支持正则）                | `'hello'.match('ll')` → `['ll']`   |

#### （4）Number 构造函数（操作数值）
重点掌握 1 个核心方法：
- `toFixed(n)`：保留 n 位小数，返回字符串（四舍五入）。
  - 示例：`12.345.toFixed(2)` → '12.35'。
  - 注意：返回值为字符串，需转数值用 `Number(...)`；存在四舍五入偏差，精密计算需处理。
- 补充：小数精度问题（如 `0.1 + 0.2 = 0.30000000000000004`），解决方案：转换为整数计算（`(0.1*100 + 0.2*100)/100`）。


### 3. 综合案例：购物车展示（核心实战）
案例核心：整合数组（map/reduce）、对象（keys/values）、字符串（split/join）方法，渲染购物车数据并计算总价。

#### （1）核心思路
1. **数据渲染**：用 `map` 遍历商品数组，批量生成 DOM 结构字符串，`join('')` 后赋值给容器。
2. **数据处理**：
   - 规格拼接：`Object.values(spec).join('/')`（如 `{ size: '40cm*40cm', color: '黑色' }` → '40cm*40cm/黑色'）。
   - 赠品处理：判断 `gift` 属性，`split(',')` 拆分后 `map` 生成赠品标签。
   - 价格格式化：`toFixed(2)` 保留 2 位小数（单价、小计、总价）。
3. **总价计算**：用 `reduce` 累计“单价 × 数量”，得到总金额。

#### （2）关键步骤代码片段
```javascript
const goodsList = [
  { id: '4001172', name: '咖啡磨豆机', price: 289.9, count: 2, spec: { color: '白色' } },
  { id: '4001649', name: '茶叶罐', price: 139, count: 1, spec: { size: '小号', color: '紫色' }, gift: '50g茶叶,清洗球' }
];

// 1. 渲染商品列表
const goodsStr = goodsList.map(goods => {
  const { name, price, count, spec, gift } = goods;
  // 规格拼接
  const specStr = Object.values(spec).join('/');
  // 赠品处理
  const giftStr = gift ? gift.split(',').map(item => `<span>【赠品】${item}</span>`).join('') : '';
  // 小计计算
  const subTotal = (price * count).toFixed(2);
  return `
    <div class="goods-item">
      <h3>${name}</h3>
      <p>规格：${specStr}</p>
      <p>单价：¥${price.toFixed(2)}</p>
      <p>小计：¥${subTotal}</p>
      ${giftStr}
    </div>
  `;
}).join('');
document.querySelector('.goods-list').innerHTML = goodsStr;

// 2. 计算总价
const total = goodsList.reduce((prev, goods) => {
  return prev + goods.price * goods.count;
}, 0).toFixed(2);
document.querySelector('.total-price').textContent = `合计：¥${total}`;
```


## 四、常见错误与陷阱（高频）
1. **构造函数未用 new 调用**：
   - 错误：`const goods = Goods('手机', 1999, 20)`（this 指向 window，全局污染）。
   - 解决：必须用 `new Goods(...)` 实例化。

2. **reduce 未传起始值**：
   - 错误：空数组调用 reduce 无起始值会报错；非空数组可能导致计算偏差（如求和时 prev 为数组第一个元素）。
   - 解决：求和、求总时必传起始值（如 `0`）。

3. **toFixed 返回字符串误用**：
   - 错误：`const sum = 12.34.toFixed(2) + 5`（字符串拼接，结果为 '12.345'）。
   - 解决：先转数值 `const sum = Number(12.34.toFixed(2)) + 5`。

4. **splice 修改原数组**：
   - 错误：用 splice 筛选数组（`arr.splice(0, 2)` 会删除原数组元素）。
   - 解决：筛选用 filter，删除元素才用 splice。

5. **伪数组直接调用数组方法**：
   - 错误：`document.querySelectorAll('li').forEach(...)`（伪数组无 forEach）。
   - 解决：先转真数组 `Array.from(document.querySelectorAll('li')).forEach(...)`。


## 五、快速练习（把知识变成肌肉记忆）
### 1. 10 分钟任务（基础回顾）
- 任务 1：用构造函数 `User` 创建 2 个用户对象（name/age/gender），添加静态属性 `type = '人类'`。
- 任务 2：用 reduce 计算数组 `[{ score: 80 }, { score: 90 }, { score: 70 }]` 的平均分。
- 任务 3：将字符串 `'苹果,香蕉,橙子'` 拆分为数组，再用 join 拼接为 '苹果-香蕉-橙子'。

### 2. 1 小时任务（综合应用）
- 需求：简化版购物车：
  1. 定义 3 个商品数据（name/price/count/spec，含 1 个带赠品的商品）。
  2. 渲染商品列表（含名称、规格、单价、小计、赠品）。
  3. 计算并显示总价，价格保留 2 位小数。


## 六、代码片段（常用模板，拷贝即用）
### 1. 构造函数创建对象
```javascript
// 定义构造函数
function User(name, age, gender) {
  this.name = name;
  this.age = age;
  this.gender = gender;
}
// 静态属性
User.type = '人类';
// 实例化
const user1 = new User('小明', 18, '男');
const user2 = new User('小红', 17, '女');
console.log(user1.name, User.type);
```

### 2. reduce 求和/求总模板
```javascript
// 数组对象求和
const arr = [{ num: 10 }, { num: 20 }, { num: 30 }];
const total = arr.reduce((prev, item) => prev + item.num, 0);
console.log(total); // 60
```

### 3. 字符串拆分+拼接（赠品处理）
```javascript
const gift = '50g茶叶,清洗球';
const giftHtml = gift.split(',').map(item => `<span class="gift">【赠品】${item}</span>`).join('');
document.querySelector('.gift-box').innerHTML = giftHtml;
```

### 4. 伪数组转换+遍历
```javascript
// DOM 伪数组转换
const lis = document.querySelectorAll('ul li');
const liArr = Array.from(lis);
liArr.forEach(li => li.style.color = 'red');
```


## 八、复习计划（建议周期）
### 1. 每周（30 分钟）
- 回顾“核心概念速查”，重点记忆构造函数实例化、Array 核心方法（map/filter/reduce）、Object 静态方法。
- 完成 1 个“10 分钟任务”，如构造函数创建对象、reduce 求和。

### 2. 每两周（2 小时）
- 完成 1 个“1 小时任务”，如简化版购物车，整合数组/对象/字符串方法。
- 练习小数精度问题处理（如 `0.1 + 0.2` 优化）、伪数组转换。

### 3. 每月（半天）
- 独立完成购物车完整案例，添加“删除商品”“修改数量”功能（用 splice/filter 修改数组，重新渲染）。
- 拓展学习：Array 的 flat() 方法（多维数组扁平化）、String 的 trim() 方法（去除首尾空格）。


## 九、自测题（检验掌握情况）
1. 构造函数的两大约定是什么？实例化的执行过程是什么？
2. 实例成员和静态成员的访问方式有何不同？
3. Object.keys()、Object.values()、Object.assign() 的作用分别是什么？
4. reduce 方法的起始值有什么作用？无起始值会有什么问题？
5. 如何将伪数组转换为真数组？举例说明伪数组的特点。
6. toFixed(2) 的作用是什么？返回值类型是什么？
7. 购物车案例中，规格拼接和赠品处理分别用到了哪些方法？


## 十、复习小贴士
1. **构造函数记忆**：大写开头+new 调用，this 指向实例对象，无需 return。
2. **数组方法选择**：遍历用 forEach，筛选用 filter，处理数据用 map，求和用 reduce。
3. **字符串处理**：拆分用 split，拼接用 join，包含判断用 includes，截取用 substring。
4. **小数精度避坑**：涉及金额计算时，先转整数再运算，避免直接小数相加。
5. **案例多练**：购物车案例是数组、对象、字符串方法的综合应用，至少独立写 2 遍，熟练掌握数据处理流程。