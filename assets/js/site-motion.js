(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var hero = document.querySelector('.hero, .land-hero, .chooser-box');
  if (hero) {
    hero.style.opacity = '0';
    hero.style.transform = 'translateY(14px)';
    requestAnimationFrame(function () {
      hero.style.transition = 'opacity .55s ease, transform .55s ease';
      hero.style.opacity = '1';
      hero.style.transform = 'none';
    });
  }

  var revealEls = document.querySelectorAll('.service, .proof article, .steps li, .meeting-card, .price-card');
  if (!('IntersectionObserver' in window) || !revealEls.length) return;

  revealEls.forEach(function (el) {
    el.style.opacity = '0';
    el.style.transform = 'translateY(12px)';
    el.style.transition = 'opacity .45s ease, transform .45s ease';
  });

  var io2 = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'none';
        io2.unobserve(entry.target);
      });
    },
    { threshold: 0.14 }
  );

  revealEls.forEach(function (el) {
    io2.observe(el);
  });
})();
