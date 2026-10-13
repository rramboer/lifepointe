/* Lifepointe — progressive enhancement only; every page works without JS. */
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

  /* Scroll effects, measured once per frame: the header's shadow once the page has scrolled,
     and the spine rail, which fills green down to a reading line 55% of the way down the
     window, with a point at the fill's leading edge, and lights each vertebra the fill has
     passed. At the bottom of the page the whole rail is lit, so short pages and the last
     section are never left half filled. */
  var header = document.querySelector('.site-header');
  var rails = Array.prototype.slice.call(document.querySelectorAll('.rail-wrap'));
  rails.forEach(function (rail) {
    var head = document.createElement('span');
    head.className = 'rail-head';
    head.setAttribute('aria-hidden', 'true');
    rail.appendChild(head);
  });
  var ticking = false;
  function onScroll() {
    ticking = false;
    var doc = document.documentElement;
    if (header) header.classList.toggle('is-scrolled', window.scrollY > 4);
    var line = window.innerHeight * 0.55;
    var atBottom = window.scrollY + window.innerHeight >= doc.scrollHeight - 2;
    rails.forEach(function (rail) {
      var box = rail.getBoundingClientRect();
      var fill = atBottom ? 1 : Math.min(Math.max((line - box.top) / box.height, 0), 1);
      rail.style.setProperty('--rail-fill', fill.toFixed(4));
      rail.querySelector('.rail-head').classList.toggle('is-moving', fill > 0 && fill < 1);
      rail.querySelectorAll('.vertebra').forEach(function (node) {
        node.classList.toggle('is-lit', atBottom || node.getBoundingClientRect().top < line);
      });
    });
  }
  function requestScroll() {
    if (!ticking) { ticking = true; window.requestAnimationFrame(onScroll); }
  }
  window.addEventListener('scroll', requestScroll, { passive: true });
  window.addEventListener('resize', requestScroll);
  onScroll();
  /* Nodes lit from here on pop as the fill reaches them (css .rail-ready) */
  window.requestAnimationFrame(function () { document.documentElement.classList.add('rail-ready'); });

  /* Scroll reveal: what starts below the window fades up the first time it scrolls into view.
     Each section's blocks are revealed one by one, and the cards, columns, quotes, and steps
     in a grid one by one. Things that arrive together follow each other by 70ms. Nothing is
     hidden under prefers-reduced-motion or without IntersectionObserver. */
  var calm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if ('IntersectionObserver' in window && !calm) {
    var groups = '.grid-2, .grid-3, .grid-4, .quote-columns, .steps, .card-stack';
    var targets = [];
    document.querySelectorAll('main .section:not(.hero) .wrap').forEach(function (wrap) {
      Array.prototype.forEach.call(wrap.children, function (child) {
        if (child.matches(groups)) Array.prototype.push.apply(targets, child.children);
        else targets.push(child);
      });
    });
    var reveal = new IntersectionObserver(function (entries) {
      var arriving = entries.filter(function (e) { return e.isIntersecting; });
      arriving.forEach(function (entry, i) {
        var el = entry.target;
        reveal.unobserve(el);
        el.style.setProperty('--reveal-delay', Math.min(i * 0.07, 0.35) + 's');
        el.classList.add('is-revealed');
        /* Done: hand the element back its own transitions (a card's hover lift) */
        window.setTimeout(function () {
          el.classList.remove('reveal', 'is-revealed');
          el.style.removeProperty('--reveal-delay');
        }, 1000 + i * 70);
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    targets.forEach(function (el) {
      if (el.getBoundingClientRect().top > window.innerHeight) {
        el.classList.add('reveal');
        reveal.observe(el);
      }
    });
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

  /* Years since the practice opened (home page photo chip, data-since="YYYY-MM"). The build
     writes the same number; this keeps it right if the site isn't rebuilt for a while. */
  document.querySelectorAll('[data-since]').forEach(function (el) {
    var since = el.getAttribute('data-since').split('-'), now = new Date();
    var years = now.getFullYear() - Number(since[0]) - (now.getMonth() + 1 < Number(since[1]) ? 1 : 0);
    if (years > 0) el.textContent = years;
  });

  /* Footer year */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
