const button=document.querySelector('.menu-toggle');const nav=document.querySelector('#navigation');button?.addEventListener('click',()=>{const open=button.getAttribute('aria-expanded')!=='true';button.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open)});nav?.addEventListener('click',e=>{if(e.target.closest('a')){nav.classList.remove('open');button.setAttribute('aria-expanded','false')}});

// Animate small content groups once as they enter the viewport.
// The page remains fully visible before JavaScript runs and during fast scrolling.
if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const revealObserver = new IntersectionObserver((entries, observer) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add('editorial-enter');
      observer.unobserve(entry.target);
    }
  }, { threshold: 0.12 });

  const revealTargets = document.querySelectorAll([
    '.ed-feature-caption',
    '.ed-project',
    '.ed-about-copy',
    '.ed-capability-grid',
    '.kt-stage-heading',
    '.kt-profile-pair',
    '.kt-photo-grid figure',
    '.kt-video',
    '.kt-next-title',
    '.case-text',
    '.case-cover',
  ].join(', '));

  for (const target of revealTargets) {
    if (target.getBoundingClientRect().top >= window.innerHeight) {
      revealObserver.observe(target);
    }
  }
}
