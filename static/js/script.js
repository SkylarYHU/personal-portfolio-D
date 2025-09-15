document.addEventListener('DOMContentLoaded', function() {
  console.log('JavaScript Loaded'); // 确保 JavaScript 已加载

  // GSAP 鼠标跟随光晕效果
  function initSpotlightEffect() {
    // 只在桌面设备启用
    if (window.innerWidth > 768) {
      // 创建光晕元素
      const spotlight = document.createElement('div');
      spotlight.className = 'spotlight';
      document.body.appendChild(spotlight);

      // 鼠标移动事件
      document.addEventListener('mousemove', (e) => {
        gsap.to(spotlight, {
          x: e.clientX,
          y: e.clientY,
          duration: 0.3,
          ease: "power2.out"
        });
        
        // 显示光晕
        spotlight.classList.add('active');
      });

      // 鼠标离开页面时隐藏光晕
      document.addEventListener('mouseleave', () => {
        spotlight.classList.remove('active');
      });

      // 交互式亮度变化
      document.addEventListener('mouseover', (e) => {
        if (e.target.matches('.portfolio-item, .role-item, .nav-links a, .contact-item')) {
          gsap.to(spotlight, {
            scale: 1.5,
            duration: 0.3,
            ease: "power2.out"
          });
          spotlight.classList.add('spotlight-hover');
        }
      });

      document.addEventListener('mouseout', (e) => {
        if (e.target.matches('.portfolio-item, .role-item, .nav-links a, .contact-item')) {
          gsap.to(spotlight, {
            scale: 1,
            duration: 0.3,
            ease: "power2.out"
          });
          spotlight.classList.remove('spotlight-hover');
        }
      });
    }
  }

  // 初始化光晕效果
  initSpotlightEffect();

  // Initialize ScrollReveal
  const sr = ScrollReveal({
    origin: 'bottom',
    distance: '60px',
    duration: 2000,
    delay: 400,
    // reset: true // 如果希望动画重复播放，取消注释这行
  });

  // Hero section now uses Animate.css fadeInDown animation
  // Removed ScrollReveal animation to avoid conflicts

  // Portfolio section animations
  sr.reveal('.portfolio h2', {
    delay: 200
  });
  
  sr.reveal('.portfolio p', {
    delay: 400
  });

  // Portfolio items with staggered animation
  sr.reveal('.portfolio-item', {
    interval: 200
  });

  // Previous role section
  sr.reveal('.previous-role h2', {
    delay: 200
  });
  
  sr.reveal('.previous-role > p', {
    delay: 400
  });
  
  sr.reveal('.dashed-line', {
    delay: 600
  });

  // Role items with alternating origins
  sr.reveal('.role-item:nth-child(odd)', {
    origin: 'left',
    delay: 200
  });
  
  sr.reveal('.role-item:nth-child(even)', {
    origin: 'right',
    delay: 200
  });

  // Client experience section
  sr.reveal('.client-experience h2', {
    delay: 200
  });
  
  sr.reveal('.client-experience p', {
    delay: 400
  });
  
  sr.reveal('.company-logo li', {
    interval: 100,
    origin: 'bottom',
    distance: '30px'
  });

  // Contact section
  sr.reveal('.contact h2', {
    delay: 200
  });
  
  sr.reveal('.contact p', {
    delay: 400
  });
  
  sr.reveal('.contact-logo li', {
    interval: 100,
    origin: 'bottom',
    distance: '30px'
  });
  
  sr.reveal('.design-detail', {
    delay: 600
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
