# Web APIs 第五天核心知识复习记录
## 一、本文档目的
- 梳理 Web APIs 第五天核心知识点（BOM 操作、本地存储、JS 执行机制、数组方法、学生信息表案例），重点突出 JS 异步同步逻辑、本地存储实战、学生信息表完整流程，非重点内容精简提炼，适配 10 分钟碎片化回顾与 1 小时集中复习。
- 解决“JS 执行顺序混淆”“本地存储复杂数据失败”“学生信息表渲染性能差”等高频问题，补充本地存储容量限制、JSON 转换注意事项等必要知识点，帮助扎实掌握 BOM 交互与数据持久化能力。


## 二、宏观结构（快速导航）
- 核心基础：Window 对象（BOM 核心、延时函数、JS 执行机制）
- 核心操作：BOM 关键对象（location、navigator、history）
- 核心能力：本地存储（localStorage/sessionStorage、复杂数据存储）
- 辅助工具：数组方法（map、join，案例核心依赖）
- 实战应用：综合案例（学生信息表，本地存储+动态渲染）
- 补充知识点：本地存储限制、JSON 转换注意事项


## 三、核心概念速查（记忆卡）
### 1. Window 对象与 BOM（核心基础）
BOM（Browser Object Model）是浏览器对象模型，`window` 是全局顶级对象，所有全局变量、函数、BOM 属性/方法都是 `window` 的属性，调用时可省略 `window`。

| BOM 核心对象 | 作用                                  | 核心成员/方法                          |
|--------------|---------------------------------------|-----------------------------------|
| `window`     | 全局容器，承载所有 BOM/DOM 核心能力    | 全局变量/函数自动成为其属性；`alert()`/`console.log()` 是其方法 |
| 延时函数     | 延迟执行代码（仅执行一次）            | `setTimeout(回调, 毫秒数)`；`clearTimeout(定时器ID)` |
| location     | 操作 URL 地址，实现跳转、刷新          | `href`（跳转/获取 URL）、`search`（获取?后参数）、`hash`（获取#后哈希值）、`reload(true)`（强制刷新） |
| navigator    | 获取浏览器/设备信息                   | `userAgent`（检测设备/浏览器版本） |
| history      | 管理浏览器历史记录（前进/后退）       | `back()`（后退）、`forward()`（前进）、`go(数字)`（前进/后退N页） |

#### （1）延时函数 vs 间歇函数（关键区别）
| 函数类型   | 执行次数 | 核心语法                          | 适用场景                          |
|------------|----------|-----------------------------------|-----------------------------------|
| 延时函数（setTimeout） | 仅1次    | `let timer = setTimeout(fn, 1000)`；`clearTimeout(timer)` | 延迟执行（如5秒后关闭广告）        |
| 间歇函数（setInterval） | 重复执行 | `let timer = setInterval(fn, 1000)`；`clearInterval(timer)` | 循环执行（如倒计时）              |

#### （2）JS 执行机制（重点详细）
JS 是**单线程**（同一时间只能做一件事），为解决阻塞问题，分为同步任务和异步任务，通过“事件循环”执行：
1. **同步任务**：主线程执行栈直接执行，顺序与代码一致（如 `console.log`、变量声明）。
2. **异步任务**：不阻塞主线程，先放入“任务队列”，类型包括：
   - 普通事件（click、resize）
   - 资源加载（load、error）
   - 定时器（setTimeout/setInterval）
3. **事件循环流程**：
   - 先执行执行栈中所有同步任务。
   - 同步任务执行完毕，读取任务队列中异步任务，进入执行栈执行。
   - 重复上述步骤，形成循环。

- 经典面试题解析：
  ```javascript
  // 题1：输出顺序？1111 → 3333 → 2222（setTimeout是异步，放入任务队列）
  console.log(1111);
  setTimeout(() => console.log(2222), 1000);
  console.log(3333);

  // 题2：输出顺序？1111 → 3333 → 2222（即使延时0ms，异步任务仍需等同步执行完）
  console.log(1111);
  setTimeout(() => console.log(2222), 0);
  console.log(3333);
  ```


### 2. 本地存储（核心重点）
本地存储用于在浏览器中持久化存储数据，页面刷新不丢失，容量约 5M，分两种类型：

| 存储类型       | 生命周期                | 数据共享范围                          | 核心语法（存储/获取/删除）                          |
|----------------|-------------------------|---------------------------------------|-----------------------------------|
| localStorage    | 永久存储（手动删除才消失） | 同一浏览器所有窗口/页面共享            | 存储：`localStorage.setItem(key, value)`<br>获取：`localStorage.getItem(key)`<br>删除：`localStorage.removeItem(key)` |
| sessionStorage  | 关闭浏览器窗口后失效     | 仅当前窗口/页面共享                    | 语法与 localStorage 完全一致        |

#### （1）关键注意事项
- 本地存储**仅支持字符串存储**，无法直接存对象、数组等复杂类型。
- 复杂数据类型存储流程：
  1. 存储时：用 `JSON.stringify(复杂数据)` 转为字符串。
  2. 获取时：用 `JSON.parse(字符串)` 转回原数据类型。
- 示例（存储对象）：
  ```javascript
  const user = { name: '张三', age: 20 };
  // 存储
  localStorage.setItem('user', JSON.stringify(user));
  // 获取
  const getuser = JSON.parse(localStorage.getItem('user'));
  console.log(getuser.name); // 张三
  ```


### 3. 数组方法（案例核心依赖）
文档中综合案例重点使用 `map` 和 `join` 方法优化渲染性能，减少 DOM 操作：

| 方法名 | 作用                                  | 语法/示例                          | 适用场景                          |
|--------|---------------------------------------|-----------------------------------|-----------------------------------|
| map    | 遍历数组，处理数据并返回新数组        | `const newArr = arr.map((item, index) => 处理逻辑)` | 批量处理数据（如案例中生成 tr 标签） |
| join   | 将数组元素转为字符串，用指定分隔符连接 | `const str = arr.join('')`（无分隔符） | 案例中将 tr 数组转为字符串，赋值给 tbody |

- 示例（案例中渲染页面）：
  ```javascript
  const students = [{ stuId: 1001, name: '欧阳霸天' }, { stuId: 1002, name: '令狐霸天' }];
  // 用map生成tr数组，join转为字符串
  const trStr = students.map((stu, index) => `
    <tr>
      <td>${stu.stuId}</td>
      <td>${stu.name}</td>
      <td><a data-index="${index}" href="javascript:">删除</a></td>
    </tr>
  `).join('');
  document.querySelector('tbody').innerHTML = trStr;
  ```


### 4. 综合案例：学生信息表（核心实战）
案例核心：结合本地存储实现“录入-渲染-删除”，页面刷新数据不丢失，核心逻辑分 5 步：

#### （1）核心流程
1. **读取本地存储数据**：
   - 若本地有数据，用 `JSON.parse` 读取；无数据则初始化空数组。
   - 处理 `stuId`：无数据时设为 1，有数据时取最后一条的 `stuId + 1`。
2. **渲染页面**：用 `map` 遍历数组生成 tr 字符串，`join` 后赋值给 tbody。
3. **录入功能**：
   - 阻止表单默认提交，验证表单非空。
   - 收集表单数据，生成学生对象，推入数组。
   - 用 `JSON.stringify` 存储数组到本地，重新渲染，重置表单。
4. **删除功能**：
   - 事件委托给 tbody，点击删除按钮获取索引。
   - 用 `splice(index, 1)` 删除数组对应数据。
   - 更新本地存储，重新渲染。

#### （2）关键难点
- `stuId` 自增：`const newStuId = students.length ? students[students.length - 1].stuId + 1 : 1;`
- 表单验证：遍历带 name 属性的表单，判断值是否为空。
- 减少 DOM 操作：用 `innerHTML` 一次性赋值，替代多次 `appendChild`。


## 四、常见错误与陷阱（高频）
1. **本地存储复杂数据未转换**：
   - 错误：`localStorage.setItem('arr', [1,2,3])`（直接存数组，实际存为 "[object Array]"）。
   - 解决：必须用 `JSON.stringify` 转换后存储。

2. **JS 执行机制异步任务优先级混淆**：
   - 错误：认为 `setTimeout(fn, 0)` 会立即执行（实际需等同步任务完毕）。
   - 解决：记住“同步先执行，异步排队”的核心规则。

3. **学生信息表 `stuId` 重复**：
   - 错误：直接用数组长度作为 `stuId`（删除中间数据后长度变化，导致重复）。
   - 解决：取最后一条数据的 `stuId + 1`，无数据时设为 1。

4. **map 方法忘记返回值**：
   - 错误：`arr.map(item => { item + '1' })`（无 return，新数组全是 undefined）。
   - 解决：箭头函数无大括号直接返回，有大括号需显式写 `return`。


## 五、快速练习（把知识变成肌肉记忆）
### 1. 10 分钟任务（基础回顾）
- 任务 1：用本地存储实现“用户名记忆”：输入用户名，点击保存，刷新页面后自动填充输入框。
- 任务 2：解析 JS 执行机制面试题：
  ```javascript
  console.log(1);
  document.addEventListener('click', () => console.log(2));
  setTimeout(() => console.log(3), 0);
  console.log(4);
  // 输出顺序？1→4→3→点击后输出2
  ```
- 任务 3：用 map 和 join 遍历数组 `[1,2,3]`，生成 `<li>1</li><li>2</li><li>3</li>` 字符串并插入 ul。

### 2. 1 小时任务（综合应用）
- 需求：简化版学生信息表（姓名、年龄）：
  1. 表单录入姓名和年龄，验证非空。
  2. 点击提交，存储到 localStorage，页面实时渲染。
  3. 点击删除按钮，删除对应数据，更新本地存储。
  4. 刷新页面，数据不丢失。


## 六、代码片段（常用模板，拷贝即用）
### 1. 本地存储增删改查模板
```javascript
// 存储（支持复杂数据）
function setStorage(key, data) {
  localStorage.setItem(key, JSON.stringify(data));
}

// 获取
function getStorage(key) {
  const data = localStorage.getItem(key);
  return data ? JSON.parse(data) : null;
}

// 删除
function removeStorage(key) {
  localStorage.removeItem(key);
}

// 示例使用
const userList = [{ name: '张三' }, { name: '李四' }];
setStorage('userList', userList);
console.log(getStorage('userList'));
```

### 2. JS 执行机制面试题解析
```javascript
// 输出顺序：同步1 → 同步2 → 异步1（延时0） → 异步2（延时1000）
console.log('同步1');
setTimeout(() => console.log('异步1'), 0);
console.log('同步2');
setTimeout(() => console.log('异步2'), 1000);
```

### 3. 学生信息表核心代码（简化版）
```javascript
// 1. 读取数据
function getData() {
  const data = localStorage.getItem('students');
  return data ? JSON.parse(data) : [];
}

// 2. 渲染页面
function render() {
  const students = getData();
  const tbody = document.querySelector('tbody');
  // map生成tr，join转为字符串
  const trStr = students.map((stu, idx) => `
    <tr>
      <td>${stu.stuId}</td>
      <td>${stu.name}</td>
      <td>${stu.age}</td>
      <td><a data-idx="${idx}" href="javascript:">删除</a></td>
    </tr>
  `).join('');
  tbody.innerHTML = trStr;
}

// 3. 录入数据
document.querySelector('form').addEventListener('submit', (e) => {
  e.preventDefault();
  const name = document.querySelector('[name="uname"]').value.trim();
  const age = document.querySelector('[name="age"]').value.trim();
  if (!name || !age) return alert('请填写完整信息');
  
  const students = getData();
  // 生成stuId
  const stuId = students.length ? students[students.length - 1].stuId + 1 : 1;
  // 新增数据
  students.push({ stuId, name, age });
  // 存储并渲染
  localStorage.setItem('students', JSON.stringify(students));
  render();
  e.target.reset();
});

// 4. 删除数据（事件委托）
document.querySelector('tbody').addEventListener('click', (e) => {
  if (e.target.tagName === 'A') {
    const idx = e.target.dataset.idx;
    const students = getData();
    students.splice(idx, 1);
    localStorage.setItem('students', JSON.stringify(students));
    render();
  }
});

// 页面加载时渲染
render();
```


## 八、复习计划（建议周期）
### 1. 每周（30 分钟）
- 回顾“核心概念速查”，重点记忆 JS 执行机制、本地存储转换、map/join 用法。
- 完成 1 个“10 分钟任务”，如本地存储用户名记忆、JS 执行机制面试题。

### 2. 每两周（2 小时）
- 完成 1 个“1 小时任务”，如简化版学生信息表，整合本地存储和数组方法。
- 用浏览器 Application 面板查看本地存储数据，验证存储和删除逻辑。

### 3. 每月（半天）
- 独立完成完整学生信息表案例，包含表单验证、stuId 自增、本地存储、删除功能。
- 拓展练习：添加“编辑”功能，点击编辑按钮填充表单，修改后更新本地存储。


## 九、自测题（检验掌握情况）
1. JS 是单线程还是多线程？同步任务和异步任务的执行顺序是什么？事件循环的流程是什么？
2. localStorage 和 sessionStorage 的核心区别（生命周期、数据共享）是什么？
3. 如何存储复杂数据类型到本地存储？需要用到哪些方法？
4. location 对象的 `href`、`search`、`hash` 分别获取 URL 的哪部分？`reload(true)` 的作用是什么？
5. 数组 `map` 和 `join` 方法的作用是什么？案例中为什么用它们来渲染页面？
6. 学生信息表中，`stuId` 如何实现自增？避免重复的核心逻辑是什么？
7. 写出本地存储“存储-获取-删除”一个数组的完整代码。


## 十、复习小贴士
1. **JS 执行机制多练面试题**：通过刷题巩固同步异步、事件循环的理解，这是高频考点。
2. **本地存储避坑**：记住“仅存字符串”的规则，复杂数据必用 JSON 转换，否则会存储为 `[object Object]`。
3. **数组方法优化 DOM 操作**：案例中用 map+join 减少 DOM 操作次数，避免频繁 appendChild 导致回流，实际开发中优先使用。
4. **浏览器工具辅助调试**：用 Application 面板查看 localStorage 数据，Sources 面板打断点调试 JS 执行顺序。
5. **案例多练**：学生信息表是本地存储和数组方法的综合应用，至少独立写 3 遍，熟练掌握核心流程。