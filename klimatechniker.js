// Native controls remain usable without JavaScript. Posters load without video data.
const films = [...document.querySelectorAll('.kt-player video')];
for (const film of films) {
  const start = film.parentElement.querySelector('.kt-start');
  if (start) {
    start.hidden = false;
    start.addEventListener('click', async () => {
      start.disabled = true;
      try {
        await film.play();
        start.hidden = true;
        film.focus();
      } catch {
        // Keep the user-initiated control available if loading was interrupted.
        start.hidden = false;
      } finally {
        start.disabled = false;
      }
    });
  }
  film.addEventListener('play', () => {
    if (start) start.hidden = true;
    for (const other of films) if (other !== film) other.pause();
  });
}

const stageList = document.querySelector('.kt-stages');
if (stageList) {
  const stages = [...stageList.querySelectorAll('.kt-stage')];
  const links = [...document.querySelectorAll('.kt-stage-nav a')];
  let activeStage = -1;
  let framePending = false;

  function updateTimeline() {
    framePending = false;
    const rail = stageList.getBoundingClientRect();
    const readingLine = window.innerHeight * 0.38;
    const progress = Math.max(0, Math.min(1, (readingLine - rail.top) / rail.height));
    let current = 0;

    for (const [index, stage] of stages.entries()) {
      if (stage.getBoundingClientRect().top <= readingLine) current = index;
    }

    stageList.style.setProperty('--rail-progress', String(progress));
    if (current === activeStage) return;

    if (activeStage >= 0) {
      stages[activeStage].classList.remove('is-current');
      links[activeStage].removeAttribute('aria-current');
    }
    stages[current].classList.add('is-current');
    links[current].setAttribute('aria-current', 'step');
    activeStage = current;
  }

  function scheduleTimelineUpdate() {
    if (framePending) return;
    framePending = true;
    requestAnimationFrame(updateTimeline);
  }

  window.addEventListener('scroll', scheduleTimelineUpdate, { passive: true });
  window.addEventListener('resize', scheduleTimelineUpdate);
  window.addEventListener('load', scheduleTimelineUpdate, { once: true });
  scheduleTimelineUpdate();
}
