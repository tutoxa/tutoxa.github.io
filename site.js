const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');

function closeMenu() {
  menuButton?.setAttribute('aria-expanded', 'false');
  navigation?.classList.remove('open');
}

menuButton?.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('open', open);
});
navigation?.addEventListener('click', event => {
  if (event.target.closest('a')) closeMenu();
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuButton?.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    menuButton.focus();
  }
});

function initHeroDots() {
  const layer = document.querySelector('.intro-dots');
  if (!layer) return;

  const canvas = layer.querySelector('canvas');
  const context = canvas.getContext('2d');
  if (!context || !('IntersectionObserver' in window) || !('ResizeObserver' in window)) return;

  const hero = layer.closest('.intro');
  const canAnimate = matchMedia('(hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference)');
  const spacing = 16;
  const radius = 108;
  let visible = false;
  let width = 0;
  let height = 0;
  let pointer = null;
  let center = null;
  let opacity = 0;
  let frame = 0;

  function clear() {
    cancelAnimationFrame(frame);
    frame = 0;
    pointer = null;
    center = null;
    opacity = 0;
    context.clearRect(0, 0, width, height);
  }

  function schedule() {
    if (!frame && visible && canAnimate.matches && !document.hidden) {
      frame = requestAnimationFrame(draw);
    }
  }

  function draw() {
    frame = 0;
    context.clearRect(0, 0, width, height);
    const targetOpacity = pointer ? 1 : 0;
    opacity += (targetOpacity - opacity) * .24;
    if (Math.abs(targetOpacity - opacity) < .01) opacity = targetOpacity;
    if (!center || opacity === 0) return;

    if (pointer) {
      center.x += (pointer.x - center.x) * .25;
      center.y += (pointer.y - center.y) * .25;
    }

    // The CSS pattern supplies the idle dots. Paint only the nearby highlights.
    const firstX = Math.max(0, Math.floor((center.x - radius) / spacing)) * spacing + spacing / 2;
    const firstY = Math.max(0, Math.floor((center.y - radius) / spacing)) * spacing + spacing / 2;
    for (let y = firstY; y < Math.min(height, center.y + radius); y += spacing) {
      for (let x = firstX; x < Math.min(width, center.x + radius); x += spacing) {
        const distance = Math.hypot(x - center.x, y - center.y);
        if (distance >= radius) continue;
        const strength = (1 - distance / radius) ** 2 * opacity;
        context.fillStyle = `rgba(24, 24, 24, ${strength * .33})`;
        context.beginPath();
        context.arc(x, y, .75 + strength * .95, 0, Math.PI * 2);
        context.fill();
      }
    }

    const moving = pointer && Math.hypot(pointer.x - center.x, pointer.y - center.y) > .35;
    if (moving || opacity !== targetOpacity) schedule();
  }

  new ResizeObserver(() => {
    width = layer.clientWidth;
    height = layer.clientHeight;
    const ratio = Math.max(1, Math.min(devicePixelRatio || 1, 1.5));
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    clear();
  }).observe(layer);

  new IntersectionObserver(([entry]) => {
    visible = entry.isIntersecting;
    if (!visible) clear();
  }).observe(hero);

  hero.addEventListener('pointermove', event => {
    if (!visible || !canAnimate.matches || event.pointerType === 'touch') return;
    const rect = layer.getBoundingClientRect();
    pointer = { x: event.clientX - rect.left, y: event.clientY - rect.top };
    if (!center || opacity === 0) center = { ...pointer };
    schedule();
  }, { passive: true });
  hero.addEventListener('pointerleave', () => {
    pointer = null;
    schedule();
  }, { passive: true });
  canAnimate.addEventListener('change', clear);
  document.addEventListener('visibilitychange', clear);
}

initHeroDots();
