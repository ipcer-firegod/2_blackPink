(function () {
  'use strict';

  // 模块化购物车实现（独立文件）
  // - 使用 DocumentFragment 批量渲染，减少回流
  // - 事件委托 + closest 查找，容错性强
  // - 所有 DOM 更新通过 updateTotals 统一处理
  // - 避免直接 innerHTML 插入未转义的数据

  const dataArr = [
    { id: 1, icon: 'http://autumnfish.cn/static/火龙果.png', isChecked: true, num: 2, price: 6 },
    { id: 2, icon: 'http://autumnfish.cn/static/荔枝.png', isChecked: false, num: 7, price: 20 },
    { id: 3, icon: 'http://autumnfish.cn/static/榴莲.png', isChecked: false, num: 3, price: 40 },
    { id: 4, icon: 'http://autumnfish.cn/static/鸭梨.png', isChecked: true, num: 10, price: 3 },
    { id: 5, icon: 'http://autumnfish.cn/static/樱桃.png', isChecked: false, num: 20, price: 34 }
  ];

  // 缓存选择器
  const tbody = document.querySelector('.tbody');
  const checkAll = document.querySelector('.check-all input');
  const priceBox = document.querySelector('.price-box .price');
  const payBtn = document.querySelector('.pay');
  const emptyEl = document.querySelector('.empty');

  function formatPrice(n) {
    return Number(n).toFixed(2);
  }

  // 渲染一行（createElement 方式，更安全）
  function createRow(item, index) {
    const tr = document.createElement('div');
    tr.className = 'tr';
    tr.dataset.id = index; // 使用 index 与原始实现兼容

    const tdChecked = document.createElement('div');
    tdChecked.className = 'td';
    const input = document.createElement('input');
    input.type = 'checkbox';
    input.checked = !!item.isChecked;
    tdChecked.appendChild(input);

    const tdImg = document.createElement('div');
    tdImg.className = 'td';
    const img = document.createElement('img');
    img.src = item.icon;
    img.alt = item.name || '';
    tdImg.appendChild(img);

    const tdPrice = document.createElement('div');
    tdPrice.className = 'td';
    tdPrice.textContent = String(item.price);

    const tdNum = document.createElement('div');
    tdNum.className = 'td';
    const numBox = document.createElement('div');
    numBox.className = 'my-input-number';
    const btnDec = document.createElement('button');
    btnDec.className = 'decrease';
    btnDec.textContent = '-';
    const spanNum = document.createElement('span');
    spanNum.className = 'my-input';
    spanNum.textContent = String(item.num);
    const btnInc = document.createElement('button');
    btnInc.className = 'increase';
    btnInc.textContent = '+';
    numBox.appendChild(btnDec);
    numBox.appendChild(spanNum);
    numBox.appendChild(btnInc);
    tdNum.appendChild(numBox);

    const tdSub = document.createElement('div');
    tdSub.className = 'td';
    tdSub.textContent = String(item.price * item.num);

    const tdOp = document.createElement('div');
    tdOp.className = 'td';
    const delBtn = document.createElement('button');
    delBtn.className = 'button del';
    delBtn.textContent = '删除';
    tdOp.appendChild(delBtn);

    tr.appendChild(tdChecked);
    tr.appendChild(tdImg);
    tr.appendChild(tdPrice);
    tr.appendChild(tdNum);
    tr.appendChild(tdSub);
    tr.appendChild(tdOp);

    return tr;
  }

  function render() {
    // 清空并重建
    tbody.innerHTML = '';
    const frag = document.createDocumentFragment();
    dataArr.forEach((item, idx) => frag.appendChild(createRow(item, idx)));
    tbody.appendChild(frag);

    // 更新 totals
    updateTotals();

    // 空车判断
    emptyEl.style.display = dataArr.length === 0 ? 'block' : 'none';
  }

  function updateTotals() {
    const checked = dataArr.filter(it => it.isChecked);
    const totalPrice = checked.reduce((s, it) => s + it.price * it.num, 0);
    const totalNum = checked.reduce((s, it) => s + it.num, 0);
    priceBox.textContent = formatPrice(totalPrice);
    payBtn.textContent = `结算(${totalNum})`;

    // 全选状态
    if (checkAll) checkAll.checked = dataArr.length > 0 && dataArr.every(it => it.isChecked === true);
  }

  // 工具：根据点击元素找到 tr 的 index（dataset.id），返回 -1 表示找不到
  function findRowIndexFromEventTarget(target) {
    const tr = target.closest && target.closest('.tr');
    if (!tr) return -1;
    const id = tr.dataset.id;
    return id == null ? -1 : Number(id);
  }

  // 事件委托处理 tbody 内所有交互
  function onTbodyClick(e) {
    const target = e.target;
    // 删除
    if (target.classList && target.classList.contains('del')) {
      const idx = findRowIndexFromEventTarget(target);
      if (idx >= 0) {
        dataArr.splice(idx, 1);
        render();
      }
      return;
    }

    // checkbox 点击
    if (target.tagName === 'INPUT' && target.type === 'checkbox') {
      const idx = findRowIndexFromEventTarget(target);
      if (idx >= 0) {
        dataArr[idx].isChecked = target.checked;
        updateTotals();
      }
      return;
    }

    // increase / decrease
    if (target.classList && (target.classList.contains('increase') || target.classList.contains('decrease'))) {
      const idx = findRowIndexFromEventTarget(target);
      if (idx < 0) return;
      if (target.classList.contains('increase')) {
        dataArr[idx].num++;
      } else {
        dataArr[idx].num = Math.max(1, dataArr[idx].num - 1);
      }
      // 局部更新：只更新该行的数量与小计，避免完全重绘
      const tr = tbody.children[idx];
      if (tr) {
        const spanNum = tr.querySelector('.my-input');
        const subTd = tr.children[4]; // 第五列是小计（和createRow顺序一致）
        if (spanNum) spanNum.textContent = String(dataArr[idx].num);
        if (subTd) subTd.textContent = String(dataArr[idx].price * dataArr[idx].num);
      }
      updateTotals();
      return;
    }
  }

  // 全选切换
  function onCheckAllClick(e) {
    const checked = e.target.checked;
    dataArr.forEach(it => it.isChecked = checked);
    // 局部更新所有行的 checkbox
    Array.from(tbody.children).forEach((tr, idx) => {
      const cb = tr.querySelector('input[type="checkbox"]');
      if (cb) cb.checked = checked;
    });
    updateTotals();
  }

  function bind() {
    tbody.addEventListener('click', onTbodyClick);
    if (checkAll) checkAll.addEventListener('click', onCheckAllClick);
  }

  // DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      render();
      bind();
    });
  } else {
    render();
    bind();
  }

  // 导出用于调试（非必须）
  window.CartRefactor = {
    dataArr,
    render,
    updateTotals
  };
})();
