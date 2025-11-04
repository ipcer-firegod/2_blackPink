
// 简单的进度记录功能
document.addEventListener('DOMContentLoaded', function () {
  // 从localStorage读取进度
  const completed = localStorage.getItem('completedChapters') || '[]';
  const completedChapters = JSON.parse(completed);

  // 更新进度显示
  const progressElement = document.getElementById('main-progress');
  const completedElement = document.getElementById('completed-chapters');
  const percentageElement = document.getElementById('progress-percentage');

  // 动态计算总章节数，避免新增模块导致超过 100% 的问题
  const totalChapters = document.querySelectorAll('.chapter-card').length || 1;
  const percentage = (completedChapters.length / totalChapters) * 100;
  progressElement.style.width = Math.min(percentage, 100) + '%';
  completedElement.textContent = completedChapters.length + ' / ' + totalChapters;
  percentageElement.textContent = Math.round(Math.min(percentage, 100)) + '%';

  // 为章节添加完成标记功能
  const chapterCards = document.querySelectorAll('.chapter-card');
  chapterCards.forEach((card, index) => {
    // 检查当前章节是否已完成
    if (completedChapters.includes(index + 1)) {
      card.style.border = '2px solid #667eea';
      card.style.backgroundColor = '#f8f9ff';
    }

    // 添加点击标记完成/取消完成
    card.addEventListener('click', function (e) {
      // 只有点击卡片本身（不是链接）才触发
      if (!e.target.closest('.btn')) {
        const chapterNum = index + 1;
        const chapterIndex = completedChapters.indexOf(chapterNum);

        if (chapterIndex === -1) {
          // 标记为完成
          completedChapters.push(chapterNum);
          card.style.border = '2px solid #667eea';
          card.style.backgroundColor = '#f8f9ff';
        } else {
          // 取消完成标记
          completedChapters.splice(chapterIndex, 1);
          card.style.border = 'none';
          card.style.backgroundColor = 'white';
        }

        // 保存进度
        localStorage.setItem('completedChapters', JSON.stringify(completedChapters));

        // 更新进度显示（实时使用当前页面的章节总数）
        const total = document.querySelectorAll('.chapter-card').length || 1;
        const newPercentage = (completedChapters.length / total) * 100;
        progressElement.style.width = Math.min(newPercentage, 100) + '%';
        completedElement.textContent = completedChapters.length;
        percentageElement.textContent = Math.round(Math.min(newPercentage, 100)) + '%';
      }
    });
  });
});
