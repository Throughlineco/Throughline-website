// Shared header behavior: the "Who we help" menu opens on click/tap and keyboard
// (hover is handled in CSS), and closes on Escape or a click outside.
(function () {
  var triggers = document.querySelectorAll('.nav-trigger');
  function close(t) { t.setAttribute('aria-expanded', 'false'); }
  triggers.forEach(function (t) {
    t.addEventListener('click', function (e) {
      e.stopPropagation();
      t.setAttribute('aria-expanded', String(t.getAttribute('aria-expanded') !== 'true'));
    });
  });
  document.addEventListener('click', function (e) {
    triggers.forEach(function (t) { if (!t.parentNode.contains(e.target)) close(t); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') triggers.forEach(function (t) { if (t.getAttribute('aria-expanded') === 'true') { close(t); t.focus(); } });
  });
}());

// Selected work: the hovered project's cover follows the cursor, like the portrait above it.
(function () {
  var list = document.querySelector('.work-index'), cover = document.querySelector('.work-cover');
  if (!list || !cover || !matchMedia('(pointer: fine) and (hover: hover)').matches || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var img = cover.querySelector('img'), x = 0, y = 0, cx = 0, cy = 0, raf = 0, on = false;
  function loop() {
    cx += (x - cx) * 0.18; cy += (y - cy) * 0.18;
    cover.style.transform = 'translate3d(' + (cx + 28) + 'px,' + (cy - 110) + 'px,0)';
    raf = on ? requestAnimationFrame(loop) : 0;
  }
  window.addEventListener('mousemove', function (ev) { x = ev.clientX; y = ev.clientY; }, { passive: true });
  list.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('mouseenter', function () {
      if (!a.dataset.cover) { on = false; cover.classList.remove('on'); return; }
      if (!raf) { cx = x; cy = y; }
      img.src = a.dataset.cover; on = true; cover.classList.add('on');
      if (!raf) raf = requestAnimationFrame(loop);
    });
  });
  list.addEventListener('mouseleave', function () { on = false; cover.classList.remove('on'); });
}());
