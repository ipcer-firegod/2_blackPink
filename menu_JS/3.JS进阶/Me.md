- 这阶段的代码敲得比较少，掌握的也很有限。
- 至少吧06-练习中的代码都能自己手敲一遍，理解代码才行。之后需要使用时间完成。
- 现在我已经忘记了2.web APis中第六七天的那些内容，或者说，没有掌握好那些内容。那些东西我可是用了好几天时间在上面的。现在这些甚至还没用多少时间呢。
- 诗歌问题

# d1

## 渲染的两种方法
```js
// 渲染函数
function renderGoods(goods) {
      let str = ''
      goods.forEach(item => {
        const { name, price } = item
        str += `
        <div>
         <h3 class="name">${name}</h3>
         <p class="price">¥${price}</p>
        </div> 
        `
      })
      document.querySelector('.goods-list').innerHTML = str
}

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
```
简短结论
- 两种方法本质上都能把数据渲染到页面：第一种是拼 HTML 字符串并一次性写入 `innerHTML`，第二种是逐条创建 DOM 节点并 `appendChild`。  
- 哪个“更好”取决于场景：初次渲染少量或静态内容用 `innerHTML` 简洁且通常更快；频繁局部更新、需要保留事件处理器、或要避免 XSS/保持节点引用时，用原生 DOM API（或 DocumentFragment / template）更稳健。

### 对比要点（精要）
- 性能：
  - `innerHTML`：一次性解析整个字符串，通常在初次批量渲染时最快（浏览器能优化 HTML 解析）。
  - DOM 创建：每次创建与插入会触发更多的 DOM 操作，若不批量（例如不使用 DocumentFragment）在大列表时更慢。
- 安全（XSS）：
  - `innerHTML`：直接插入字符串，必须对用户/外部数据进行转义或消毒，否则会有 XSS 风险。
  - DOM API：通过 `createElement` + `textContent` 可自然避免注入风险（更安全）。
- 事件监听与节点引用：
  - `innerHTML`：写入会移除并替换已有子节点，已绑定的事件监听器会丢失、已有节点引用无效。
  - DOM API：可以在已有容器上追加或操作现有节点，能保留事件和引用。
- 可维护性与可读性：
  - 字符串拼接：短小场景可读，但复杂模板容易出现转义/缩进问题。
  - DOM API：结构清晰、类型安全，但代码更啰嗦；可配合 `template` 提高可读性。
- 浏览器兼容与解析：
  - 二者都广泛支持；`innerHTML` 对 HTML 片段解析更直接，但对某些元素（如 `table`）插入片段需注意父容器。

### 改进建议与样例（推荐用法）

1) 高效且仍用字符串（初次渲染、数据可信时）
- 用 `map(...).join('')` 代替逐次 `+=`，稍微快且更整洁。
```js
function renderGoods(goods) {
  const html = goods.map(item =>
    `<div><h3 class="name">${item.name}</h3><p class="price">¥${item.price}</p></div>`
  ).join('');
  document.querySelector('.goods-list').innerHTML = html;
}
```
注意：若 `item.name` 来源不可信，请先做 HTML 转义（见下）。

2) DOM API + DocumentFragment（大量节点或需保留事件时）
- 批量构建并一次性插入，兼顾安全与性能。
```js
function renderGoods(goods) {
  const list = document.querySelector('.goods-list');
  list.innerHTML = ''; // 清空（如果想保留部分节点，改用 diff/更新逻辑）
  const frag = document.createDocumentFragment();
  goods.forEach(item => {
    const div = document.createElement('div');
    const h3 = document.createElement('h3');
    h3.className = 'name';
    h3.textContent = item.name; // 安全，自动转义
    const p = document.createElement('p');
    p.className = 'price';
    p.textContent = `¥${item.price}`;
    div.appendChild(h3);
    div.appendChild(p);
    frag.appendChild(div);
  });
  list.appendChild(frag);
}
```

3) 使用 `<template>`（可维护的模板方式）
```html
<template id="goodTpl">
  <div>
    <h3 class="name"></h3>
    <p class="price"></p>
  </div>
</template>
```
```js
function renderGoods(goods) {
  const list = document.querySelector('.goods-list');
  list.innerHTML = '';
  const tpl = document.getElementById('goodTpl');
  const frag = document.createDocumentFragment();
  goods.forEach(item => {
    const node = tpl.content.cloneNode(true);
    node.querySelector('.name').textContent = item.name;
    node.querySelector('.price').textContent = `¥${item.price}`;
    frag.appendChild(node);
  });
  list.appendChild(frag);
}
```

4) 如果必须用 `innerHTML` 且数据不可信，先做转义
```js
function escapeHTML(str) {
  return String(str).replace(/[&<>"']/g, s => ({
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
  })[s]);
}
```
然后在模板中使用 `escapeHTML(item.name)`。

实用建议（何时用哪种）
- 首次渲染少量静态数据：`innerHTML`（map/join）更简洁、足够快。
- 渲染大列表或需要保留事件/引用：使用 DocumentFragment + DOM API 或 `template`。
- 数据来自用户/外部：避免直接插入未经转义的字符串，优先用 `textContent` 或先转义。
- 需要频繁局部更新：考虑差分更新（reuse nodes）、虚拟列表或框架（React/Vue）以避免整段重绘。

### 总结一句话
- 没有绝对“最好”的方法：对于简单、一次性的静态渲染，`innerHTML`（map/join）足够且简洁；对于安全、可维护和频繁更新的场景，使用 `DocumentFragment` + DOM API（或 template）更稳健并更容易扩展。需要我根据你的页面（比如有多少条、是否有交互事件）给出具体推荐并把你的代码改成更合适的实现吗？

## 占位

# d2
## 购物车优化
- 新文件：cart.refactor.js

主要改动与优点
- 使用模块化 IIFE 封装，避免全局污染（仅导出 `window.CartRefactor` 用于调试）。
- 使用 DocumentFragment 批量渲染，减少回流与重绘。
- 用 createElement + textContent 构建 DOM，避免 XSS 风险（比直接拼 innerHTML 更安全）。
- 事件委托 + closest：更健壮地处理删除、增减、复选框等操作。
- 局部更新（增减数量只更新对应行的小计与数量），避免每次都完全重绘，提高性能。
- 提供 `render()` 与 `updateTotals()` 可重用接口（方便未来做局部刷新 / 异步数据更新）。

下一步建议（请选择一项）
- 我可以把 `购物车.html` 中原内联脚本替换为对这个新文件的引用（把旧脚本移除并加上 `<script src="cart.refactor.js"></script>`）。我现在没有直接修改 HTML，你想让我替你替换吗？（我可以直接修改并提交）
- 或者你可以手动在 `购物车.html` 的底部添加一行：
  <script src="./menu_JS/3.JS进阶/d2_JavaScript进阶第二天/07-作业/02-主观题/cart.refactor.js"></script>
  （Windows 路径在 HTML 中用相对 URL 即可）
