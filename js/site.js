/* Lifepointe prototype — progressive enhancement only; every page works without JS. */
(function () {
  'use strict';

  /* Mobile navigation */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open') &&
          (nav.contains(document.activeElement) || toggle === document.activeElement)) {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  /* Spine rail: light each vertebra as its section reaches the viewport.
     Nodes stay lit — the rail reads as progress down the spine. */
  var nodes = document.querySelectorAll('.vertebra');
  if ('IntersectionObserver' in window && nodes.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-lit');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -45% 0px' });
    nodes.forEach(function (n) { io.observe(n); });
  } else {
    nodes.forEach(function (n) { n.classList.add('is-lit'); });
  }

  /* Highlight today's row in the office-hours table */
  var day = new Date().getDay(); /* 0 = Sunday */
  document.querySelectorAll('.hours-table [data-days]').forEach(function (row) {
    if (row.getAttribute('data-days').split(',').indexOf(String(day)) !== -1) {
      row.classList.add('is-today');
      row.setAttribute('aria-current', 'date');
      var th = row.querySelector('th');
      if (th) th.insertAdjacentHTML('beforeend', ' <span class="visually-hidden">(today)</span>');
    }
  });

  /* Footer year */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
