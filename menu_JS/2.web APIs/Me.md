
# d1
- 看练习中的两个例子即可


# d2

## 1
### 为什么 `.tab-nav a:nth-child(${i + 1})` 不行

### 正确的选择器
- 使用 `.tab-nav li:nth-child(${i + 1}) a`：这会先选第 (i+1) 个 li，再从该 li 中选取 a（符合你的结构）。
- 也可以写成 `.tab-nav ul li:nth-child(${i + 1}) > a`（更明确，使用子选择器）。

### 额外建议（更健壮的实现）
1. 查找当前带 active 的元素：用 `.tab-nav a.active` 会更直接（不需要先定位 li 再找 a）。
2. 在 DOM 查询时加空值检查，防止 querySelector 返回 null 导致报错。
3. 可把选择器缓存，或直接使用 nodes 列表切换 class（效率更高、更清晰）。

推荐的 toggle 实现（示例）：
```js
function toggle() {
  const prevA = document.querySelector('.tab-nav a.active');
  const prevContent = document.querySelector('.tab-content .item.active');
  const targetA = document.querySelector(`.tab-nav li:nth-child(${i + 1}) a`);
  const targetContent = document.querySelector(`.tab-content .item:nth-child(${i + 1})`);

  if (prevA) prevA.classList.remove('active');
  if (prevContent) prevContent.classList.remove('active');

  if (targetA) targetA.classList.add('active');
  if (targetContent) targetContent.classList.add('active');
}
```

更进一步的重构（使用 NodeList，避免多次 querySelector）：
```js
const tabs = Array.from(document.querySelectorAll('.tab-nav li'));
const panels = Array.from(document.querySelectorAll('.tab-content .item'));

function activate(index) {
  tabs.forEach((li, idx) => {
    const a = li.querySelector('a');
    if (a) a.classList.toggle('active', idx === index);
  });
  panels.forEach((panel, idx) => {
    panel.classList.toggle('active', idx === index);
  });
}
```
然后在事件中调用 `activate(index)`。

### 小结
- 原因：因为 nth-child 是相对于父元素的位置，`.tab-nav a:nth-child(...)` 试图对 a 在其父元素（li）中的位置计数，但每个 a 都是其 li 的第 1 个子元素，所以不会得到期望的按序匹配。
- 解决：先选 li 的第 n 个，再选 li 里的 a：`.tab-nav li:nth-child(${i + 1}) a`；或使用更清晰的 `.tab-nav a.active` 来寻找当前激活项，并添加空值检查与更稳健的切换逻辑。





## 2
### a.active 是什么选择器，选择的是什么？
- 语法构成：`a.active` = 元素类型选择器（a） + 类选择器（.active）。  
  它会匹配所有标签名为 `<a>` 且 class 列表中包含 `active` 的元素。例如：<a class="active">或<a class="foo active bar">都会被匹配。

- 在复合选择器 `.tab-nav a.active` 中：
  - `.tab-nav` 是父级选择器（或祖先选择器）。
  - 空格是后代组合符（descendant combinator）。
  - `a.active` 是目标元素选择器（只匹配带 active 类的 a）。
  整体意思：在 `.tab-nav` 的任意后代中，选择那些标签名是 a 且含有 class "active" 的元素。

### 和相近选择器的区别
- `.tab-nav .active`：匹配 `.tab-nav` 的后代中任何带 `.active` 类的元素（不限标签），不局限于 a 元素。
- `.tab-nav a .active`（注意空格）：匹配位于 a 元素内部的、带 `.active` 类的后代元素（即 `.active` 在 a 的子孙中），与 `a.active` 含义不同。
- `a.active`（无前缀）：匹配整个文档中所有带 `active` 类的 a 元素（不限定在 `.tab-nav` 内）。
- `.tab-nav > a.active`：只匹配 `.tab-nav` 的直接子元素中为 a 并带 active 类的元素（你的结构中 a 在 li 内，所以通常不会匹配）。

### 在你当前 HTML（示例）里的行为
你的 HTML 片段：
<ul>
  <li><a class="active" href="...">精选</a></li>
  <li><a href="...">美食</a></li>
  ...
</ul>

- `.tab-nav a.active` 会匹配第一个 `<a class="active">`（“精选”）——因为它是 `.tab-nav` 的后代并且是带 active 类的 a。
- `.tab-nav a:nth-child(2)` 不会匹配“美食”的 a，因为 nth-child 是相对于父元素的位置（a 在 li 中通常是 li 的第一个子节点），这与之前问题的原因一致。

### 在 JavaScript 中的常见用法
- 取出当前激活的 a（第一个匹配项）：
  const activeA = document.querySelector('.tab-nav a.active');

- 如果可能没有匹配项，先判空：
  const activeA = document.querySelector('.tab-nav a.active');
  if (activeA) activeA.classList.remove('active');

- 如果页面上可能有多个带 active 的 a（不推荐），可用：
  const activeAs = document.querySelectorAll('.tab-nav a.active'); // NodeList

- 更稳健的切换代码（示例）：
  const prev = document.querySelector('.tab-nav a.active');
  if (prev) prev.classList.remove('active');
  const target = document.querySelector(`.tab-nav li:nth-child(${i + 1}) a`);
  if (target) target.classList.add('active');

### 小贴士
- 对于“哪个元素带 active”这种用法，`.tab-nav a.active` 是直接又语义明确的选择器；写 CSS 规则时也会常用 `.tab-nav a.active { ... }` 来专门样式化当前激活项。
- 为了更稳定与可维护，事件处理里推荐缓存节点列表（querySelectorAll）并使用索引去切换，而不是频繁用复杂选择器查询 DOM。

## 作业


```javascript

// 手风琴
  // 获取元素
  const box = document.querySelectorAll('li');// lis = [li, li, li, li, li]
  // 分析：
  // 1、鼠标进入显示图片，
  // 鼠标进入li，让当前li变成800，其他的li变成100
  for (let i = 0; i < box.length; i++) {
    box[i].addEventListener('mouseenter', function () {
      for (let j = 0; j < box.length; j++) {// 事件触发执行，为了让所有li变成240宽的
        box[j].style.width = '100px';
      }
      this.style.width = '800px'
    })

    box[i].addEventListener('mouseleave', function () {
      // 让所有的li变成240
      for (let j = 0; j < box.length; j++) {// 事件触发执行，为了让所有li变成240宽的
        box[j].style.width = '240px';
      }
    })
  }


// 2.
    const agree = document.querySelector('#agree')
    const registerBtn = document.querySelector('#registerBtn')
    // 2. 给按钮注册点击事件
    agree.addEventListener('click', function () {
      // 2.1 如果复选框选中，按钮就启用，如果复选框不选中，按钮就禁用
      // 2.2 注意， 复选框选中是true， 按钮启用 disable 是false，是相反的要小心哦
      registerBtn.disabled = !this.checked
    })


// 3
    // 1. 获取元素 按钮
    const btn = document.querySelector('#btn')
    // 2. 给按钮注册点击事件
    btn.addEventListener('click', function () {
      // 3. 点击之后，禁用按钮，同时开启倒计时
      this.disabled = true
      // 控制显示数字的
      let i = 5
      btn.innerHTML = `${i}秒之后重新获取`
      let timer = setInterval(function () {
        i--
        // 在定时器里面不能用this，this执行的window
        btn.innerHTML = `${i}秒之后重新获取`

        // 4. 如果时间为0，则清除定时器，并且更改文字
        if (i < 0) {
          clearInterval(timer)

          btn.innerHTML = '获取验证码'
          btn.disabled = false
        }
      }, 1000)

    })


// 4
    // 1. 获取元素  label 和 input 
    const label = document.querySelector('label')
    const input = document.querySelector('input')
    // 2. 给label 注册事件， 可以切换类实现图片的切换
    // 声明一个变量来控制
    let flag = true
    label.addEventListener('click', function () {
        // classList.toggle 是切换类名，如果有就删除，没有就添加
        this.classList.toggle('active')
        // 3. 因为要修改input的 type属性 text和password，可以使用一个变量来控制  flag ， 如果为true 就切换为text ，如果为false就修改为 password
        if (flag) {
            input.type = 'text'
        } else {
            input.type = 'password'
        }
        flag = !flag
    })

```