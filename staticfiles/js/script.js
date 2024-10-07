document.addEventListener('DOMContentLoaded', function() {
  console.log('JavaScript Loaded'); // 确保 JavaScript 已加载

  // 菜单按钮的切换逻辑
  const toggleButton = document.querySelector('.toggle');
  const navLinks = document.querySelector('.nav-links');

  if (toggleButton && navLinks) {
    console.log('Toggle button and navigation links found.');
    toggleButton.addEventListener('click', function() {
      navLinks.classList.toggle('show');
    });
  } else {
    console.error('Toggle button or navigation links not found.');
  }

  // 项目项的点击事件逻辑
  const portfolioGrid = document.querySelector('.portfolio-grid');
  
  if (portfolioGrid) {
    console.log('Portfolio grid found.');
    portfolioGrid.addEventListener('click', function(event) {
      console.log('Portfolio grid clicked'); // 调试信息
      const item = event.target.closest('.portfolio-item');
      if (item) {
        event.preventDefault();
        const link = item.getAttribute('data-link');
        console.log('Clicked portfolio item, link:', link); // 调试输出
        if (link) {
          window.open(link, '_blank');
        }
      } else {
        console.log('Clicked area is not a portfolio item');
      }
    });
  } else {
    console.error('Portfolio grid not found.');
  }
});
