class CircularText {
  constructor(element, options = {}) {
    this.element = element;
    this.text = options.text || element.dataset.text || 'DIGITAL*MARKETING*';
    this.spinDuration = options.spinDuration || 20;
    this.onHover = options.onHover || 'speedUp';
    this.className = options.className || '';
    
    this.init();
  }

  init() {
    this.element.classList.add('circular-text');
    if (this.className) {
      this.element.classList.add(this.className);
    }
    this.createLetters();
    this.bindEvents();
  }

  createLetters() {
    const letters = Array.from(this.text);
    this.element.innerHTML = '';
    
    // 根据屏幕尺寸调整半径
    let radius = 56; // 默认半径
    if (window.innerWidth <= 480) {
      radius = 35; // 手机端
    } else if (window.innerWidth <= 768) {
      radius = 45; // 平板端
    }
    
    // 计算字符权重，为不同字符分配不同的角度空间
    const getCharWeight = (char) => {
      if (char === '*') return 1.4; // 星号占用更多空间
      if (char === ' ') return 0.6; // 空格占用较少空间
      // 窄字母
      if (/[IiltjJ1]/.test(char)) return 0.7;
      // 中等宽度字母
      if (/[ABCDEFGHKLMNOPQRSTUVXYZabcdefghknopqrsuvxyz]/.test(char)) return 1.0;
      // 宽字母
      if (/[MWmw]/.test(char)) return 1.3;
      return 1.0; // 其他字符
    };
    
    // 计算总权重
    const totalWeight = letters.reduce((sum, letter) => sum + getCharWeight(letter), 0);
    
    let currentAngle = -Math.PI / 2; // 从顶部开始
    
    letters.forEach((letter, i) => {
      const span = document.createElement('span');
      const charWeight = getCharWeight(letter);
      const angleStep = (2 * Math.PI * charWeight) / totalWeight;
      
      // 计算每个字母的位置
      const x = Math.cos(currentAngle) * radius;
      const y = Math.sin(currentAngle) * radius;
      
      // 计算旋转角度（字符朝向圆心外侧）
      const rotationDeg = (currentAngle * 180 / Math.PI) + 90;
      
      span.textContent = letter;
      span.style.transform = `translate(${x}px, ${y}px) rotate(${rotationDeg}deg)`;
      span.style.transformOrigin = '0 0';
      
      this.element.appendChild(span);
      
      // 移动到下一个字符的角度位置
      currentAngle += angleStep;
    });
  }

  bindEvents() {
    this.element.addEventListener('mouseenter', () => this.handleHoverStart());
    this.element.addEventListener('mouseleave', () => this.handleHoverEnd());
  }

  handleHoverStart() {
    if (!this.onHover) return;

    switch (this.onHover) {
      case 'slowDown':
        this.element.style.animationDuration = `${this.spinDuration * 2}s`;
        break;
      case 'speedUp':
        this.element.style.animationDuration = `${this.spinDuration / 4}s`;
        break;
      case 'pause':
        this.element.style.animationPlayState = 'paused';
        break;
      case 'goBonkers':
        this.element.style.animationDuration = `${this.spinDuration / 20}s`;
        this.element.style.transform = 'scale(0.8)';
        break;
      default:
        break;
    }
  }

  handleHoverEnd() {
    this.element.style.animationDuration = `${this.spinDuration}s`;
    this.element.style.animationPlayState = 'running';
    this.element.style.transform = 'scale(1)';
  }
}

// 自动初始化所有带有 circular-text 类的元素
document.addEventListener('DOMContentLoaded', function() {
  const circularTextElements = document.querySelectorAll('.circular-text-container');
  
  circularTextElements.forEach(element => {
    new CircularText(element, {
      text: element.dataset.text,
      spinDuration: parseInt(element.dataset.spinDuration) || 20,
      onHover: element.dataset.onHover || 'speedUp',
      className: element.dataset.className || ''
    });
  });
});

// 导出类以供其他地方使用
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CircularText;
}