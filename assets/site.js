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
