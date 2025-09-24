// Mouse Follow Effect
document.addEventListener('DOMContentLoaded', function() {
  // Check if device supports mouse (not touch-only)
  const hasMouseSupport = window.matchMedia('(pointer: fine)').matches;
  
  if (!hasMouseSupport) {
    return; // Exit on touch-only devices
  }

  // Create cursor follow element
  const cursorFollow = document.createElement('div');
  cursorFollow.className = 'cursor-follow';
  document.body.appendChild(cursorFollow);

  let mouseX = 0;
  let mouseY = 0;
  let cursorX = 0;
  let cursorY = 0;

  // Update mouse position
  document.addEventListener('mousemove', function(e) {
    mouseX = e.clientX;
    mouseY = e.clientY;
  });

  // Smooth animation loop
  function animateCursor() {
    // Smooth following effect
    cursorX += (mouseX - cursorX) * 0.1;
    cursorY += (mouseY - cursorY) * 0.1;
    
    cursorFollow.style.left = cursorX + 'px';
    cursorFollow.style.top = cursorY + 'px';
    
    requestAnimationFrame(animateCursor);
  }
  
  animateCursor();

  // Add active state on click
  document.addEventListener('mousedown', function() {
    cursorFollow.classList.add('active');
  });

  document.addEventListener('mouseup', function() {
    cursorFollow.classList.remove('active');
  });

  // Hide cursor when leaving window
  document.addEventListener('mouseleave', function() {
    cursorFollow.style.opacity = '0';
  });

  document.addEventListener('mouseenter', function() {
    cursorFollow.style.opacity = '0.8';
  });

  // Special effects for interactive elements
  const interactiveElements = document.querySelectorAll('a, button, .clickable, .learn-more');
  
  interactiveElements.forEach(element => {
    element.addEventListener('mouseenter', function() {
      cursorFollow.classList.add('active');
    });
    
    element.addEventListener('mouseleave', function() {
      cursorFollow.classList.remove('active');
    });
  });
});