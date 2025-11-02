document.addEventListener('DOMContentLoaded', function () {
  const toggle = document.querySelector('.side-toggle');
  const side = document.getElementById('side-nav');
  if (toggle && side) {
    toggle.addEventListener('click', function () {
      const isOpen = side.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(isOpen));
      toggle.setAttribute('aria-label', isOpen ? '关闭导航' : '打开导航');
    });
  }

  // handle collapsing the JS sublist on small screens
  document.querySelectorAll('.has-children').forEach(function (li) {
    const parentBtn = li.querySelector('.side-parent');
    const sub = li.querySelector('.side-sublist');
    if (parentBtn && sub) {
      // on small screens start collapsed
      if (window.matchMedia && window.matchMedia('(max-width: 900px)').matches) {
        sub.classList.add('collapsed');
        parentBtn.setAttribute('aria-expanded', 'false');
      }
      parentBtn.addEventListener('click', function () {
        const collapsed = sub.classList.toggle('collapsed');
        parentBtn.setAttribute('aria-expanded', String(!collapsed));
      });
    }
  });

  // Close sidebar if user clicks outside on mobile
  document.addEventListener('click', function (e) {
    const sideIsOpen = side && side.classList.contains('open');
    if (!sideIsOpen) return;
    const clickInside = e.target.closest && (e.target.closest('#side-nav') || e.target.closest('.side-toggle'));
    if (!clickInside) {
      side.classList.remove('open');
      if (toggle) toggle.setAttribute('aria-expanded', 'false');
    }
  });

  // Collapse entire sidebar into a single button and pop out on click
  const collapseBtn = document.querySelector('.side-collapse');
  function isPopupOpen() { return document.body.classList.contains('side-popup-open'); }
  function isCollapsed() { return document.body.classList.contains('nav-collapsed'); }
  if (collapseBtn && side) {
    let overlayEl = null;
    function createOverlay() {
      if (overlayEl) return overlayEl;
      overlayEl = document.createElement('div');
      overlayEl.className = 'side-overlay';
      overlayEl.addEventListener('click', function () {
        // clicking overlay closes popup and returns to collapsed state
        closePopup();
      });
      return overlayEl;
    }

    function openPopup() {
      document.body.classList.remove('nav-collapsed');
      document.body.classList.add('side-popup-open');
      side.classList.add('open');
      collapseBtn.setAttribute('aria-label', '关闭侧栏弹窗');
      collapseBtn.setAttribute('aria-expanded', 'true');
      const ov = createOverlay();
      document.body.appendChild(ov);
    }

    function closePopup() {
      document.body.classList.remove('side-popup-open');
      document.body.classList.add('nav-collapsed');
      side.classList.remove('open');
      collapseBtn.setAttribute('aria-label', '折叠/展开侧栏');
      collapseBtn.setAttribute('aria-expanded', 'false');
      if (overlayEl && overlayEl.parentNode) overlayEl.parentNode.removeChild(overlayEl);
    }

    collapseBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      // If popup currently open -> close popup and keep collapsed
      if (isPopupOpen()) {
        closePopup();
        return;
      }

      // If currently collapsed (button-only) -> open popup
      if (isCollapsed()) {
        openPopup();
        return;
      }

  // Otherwise (normal visible sidebar) -> collapse into button-only
  document.body.classList.add('nav-collapsed');
  side.classList.remove('open');
  collapseBtn.setAttribute('aria-label', '展开侧栏');
  collapseBtn.setAttribute('aria-expanded', 'false');
    });

    // Close popup when clicking outside while popup is open (safety)
    document.addEventListener('click', function (e) {
      if (!isPopupOpen()) return;
      const clickInside = e.target.closest && (e.target.closest('#side-nav') || e.target.closest('.side-collapse'));
      if (!clickInside) {
        closePopup();
      }
    });
  }
});