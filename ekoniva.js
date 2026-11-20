const showcase = document.querySelector('.ek-showcase');
if (showcase) {
  const panels = [...showcase.querySelectorAll('.ek-panel')];
  const controls = showcase.querySelector('.ek-controls');
  const status = showcase.querySelector('.ek-status');
  let active = Math.floor(panels.length / 2);
  let touchStart = null;

  function show(index) {
    active = (index + panels.length) % panels.length;
    panels.forEach((panel, position) => {
      let offset = (position - active + panels.length) % panels.length;
      if (offset > panels.length / 2) offset -= panels.length;
      panel.style.transform = `translateX(-50%) translateX(${offset * 78}%) translateY(${Math.abs(offset) * 18}px) scale(${1 - Math.abs(offset) * .1})`;
      panel.style.zIndex = panels.length - Math.abs(offset);
      // Explicit focus handling also keeps neighboring panels visible in Safari.
      panel.style.pointerEvents = offset === 0 ? 'auto' : 'none';
      panel.querySelectorAll('a, button, video').forEach(control => { control.tabIndex = offset === 0 ? 0 : -1; });
      panel.setAttribute('aria-hidden', String(offset !== 0));
      if (offset !== 0) panel.querySelector('video')?.pause();
    });
    status.textContent = `${showcase.dataset.status} ${active + 1} / ${panels.length}`;
  }

  // Manual progression keeps the review readable and gives visitors control.
  showcase.classList.add('ek-ready');
  controls.hidden = false;
  show(active);
  controls.addEventListener('click', event => {
    const button = event.target.closest('button[data-direction]');
    if (button) show(active + Number(button.dataset.direction));
  });
  showcase.addEventListener('keydown', event => {
    if (event.target.closest('video, a')) return;
    const directions = { ArrowLeft: -1, ArrowRight: 1 };
    if (event.key in directions) {
      event.preventDefault();
      show(active + directions[event.key]);
    } else if (event.key === 'Home' || event.key === 'End') {
      event.preventDefault();
      show(event.key === 'Home' ? 0 : panels.length - 1);
    }
  });
  showcase.addEventListener('pointerdown', event => {
    if (event.pointerType === 'touch' && !event.target.closest('video, button, a')) {
      touchStart = { x: event.clientX, y: event.clientY };
    }
  }, { passive: true });
  showcase.addEventListener('pointerup', event => {
    if (!touchStart) return;
    const dx = event.clientX - touchStart.x;
    const dy = event.clientY - touchStart.y;
    touchStart = null;
    if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy) * 1.4) {
      show(active + (dx < 0 ? 1 : -1));
    }
  }, { passive: true });
  showcase.addEventListener('pointercancel', () => { touchStart = null; });
  showcase.addEventListener('play', event => {
    for (const video of showcase.querySelectorAll('video')) {
      if (video !== event.target) video.pause();
    }
  }, true);
}
