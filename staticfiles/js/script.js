document.addEventListener('DOMContentLoaded', function() {

  // Initialize ScrollReveal
  const sr = ScrollReveal({
    origin: 'bottom',
    distance: '60px',
    duration: 1200,
    delay: 200
    // reset: true // 如果希望动画重复播放，取消注释这行
  });

  // Folder tab functionality removed - using simple content display

  // Hero section now uses Animate.css fadeInDown animation
  // Removed ScrollReveal animation to avoid conflicts

  // Portfolio section animations
  sr.reveal('.portfolio h2', {
    delay: 100
  });
  
  sr.reveal('.portfolio p', {
    delay: 200
  });

  // Portfolio items with staggered animation
  sr.reveal('.portfolio-item', {
    interval: 150
  });

  // Previous role section
  sr.reveal('.previous-role h2', {
    delay: 100
  });
  
  sr.reveal('.previous-role > p', {
    delay: 200
  });
  
  sr.reveal('.dashed-line', {
    delay: 300
  });

  // Role items with alternating origins
  sr.reveal('.role-item:nth-child(odd)', {
    origin: 'left',
    delay: 100
  });
  
  sr.reveal('.role-item:nth-child(even)', {
    origin: 'right',
    delay: 100
  });

  // Client experience section
  sr.reveal('.client-experience h2', {
    delay: 100
  });
  
  sr.reveal('.client-experience p', {
    delay: 200
  });
  
  sr.reveal('.company-logo li', {
    interval: 80,
    origin: 'bottom',
    distance: '30px'
  });

  // Contact section
  sr.reveal('.contact h2', {
    delay: 100
  });
  
  sr.reveal('.contact p', {
    delay: 200
  });
  
  sr.reveal('.contact-logo li', {
    interval: 80,
    origin: 'bottom',
    distance: '30px'
  });
  
  sr.reveal('.design-detail', {
    delay: 300
  });

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
      const link = event.target.closest('a'); // 检查是否点击了链接
      
      if (item && !link) {
        // 只有当点击的不是链接时才处理data-link
        event.preventDefault();
        const dataLink = item.getAttribute('data-link');
        console.log('Clicked portfolio item, data-link:', dataLink); // 调试输出
        if (dataLink) {
          window.open(dataLink, '_blank');
        }
      } else if (link) {
        // 如果点击的是链接，让默认行为继续（跳转到详情页）
        console.log('Clicked on a link, allowing default behavior');
      } else {
        console.log('Clicked area is not a portfolio item');
      }
    });
  } else {
    console.error('Portfolio grid not found.');
  }

  // Accordion functionality for Table of Content
  const accordionItems = document.querySelectorAll('.accordion-item');
  
  console.log('Found accordion items:', accordionItems.length);
  
  accordionItems.forEach((item, index) => {
    const targetId = item.getAttribute('data-target');
    console.log(`Accordion item ${index + 1} target:`, targetId);
    
    // Add click event only for EXPLORE buttons
    const exploreButton = item.querySelector('.learn-more');
    if (exploreButton && targetId) {
      exploreButton.addEventListener('click', function(e) {
        console.log('=== EXPLORE BUTTON CLICKED ===');
        console.log('Target ID:', targetId);
        
        // 阻止默认的链接行为
        e.preventDefault();
        e.stopPropagation();
        
        // 查找目标元素
        const targetElement = document.querySelector(targetId);
        console.log('Target element found:', !!targetElement);
        
        if (targetElement) {
          console.log('Scrolling to target element...');
          
          // 简单直接的滚动方法
          const elementPosition = targetElement.offsetTop;
          const offsetPosition = elementPosition - 80; // 导航栏高度补偿
          
          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
          });
          
          console.log('Scroll command executed');
        } else {
          console.error('Target element not found for:', targetId);
        }
      });
    }
  })
});
