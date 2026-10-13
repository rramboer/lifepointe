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

  /* Scroll effects: the header's shadow once the page has scrolled, and the spine rail.

     The rail's green fill is a function of the scroll position, worked out from a few stops
     (layoutRails): it reaches each vertebra just as that section's eyebrow reaches a reading
     line 55% of the way down the window, and the whole rail at the bottom of the page. On a
     page whose first sections open above the reading line, the fill starts at the first
     vertebra instead of halfway down, and catches up as you scroll. Vertebrae too close to
     the bottom to ever reach the reading line share the last stretch of scrolling, so every
     one lights. Between stops the fill moves evenly, with a point at its leading edge. */
  var header = document.querySelector('.site-header');
  var rails = Array.prototype.slice.call(document.querySelectorAll('.rail-wrap')).map(function (el) {
    var head = document.createElement('span');
    head.className = 'rail-head';
    head.setAttribute('aria-hidden', 'true');
    el.appendChild(head);
    return { el: el, head: head, nodes: Array.prototype.slice.call(el.querySelectorAll('.vertebra')) };
  });

  function layoutRails() {
    var reading = window.innerHeight * 0.55;
    var maxScroll = Math.max(document.documentElement.scrollHeight - window.innerHeight, 0);
    rails.forEach(function (rail) {
      var top = rail.el.getBoundingClientRect().top + window.scrollY;
      var height = rail.el.offsetHeight || 1;
      /* Each vertebra's place on the rail, 0 (top) to 1 (bottom) */
      rail.marks = rail.nodes.map(function (node) {
        var box = node.getBoundingClientRect();
        return (box.top + box.height / 2 + window.scrollY - top) / height;
      });
      /* [scroll position, fill] pairs, in scroll order */
      var stops = [];
      var startFill = Math.min(Math.max((reading - top) / height, 0), rail.marks.length ? rail.marks[0] : 1);
      if (top - reading > 0) stops.push([0, 0], [top - reading, 0]);
      else stops.push([0, startFill]);
      rail.marks.concat([1]).forEach(function (mark) {
        if (mark > startFill) stops.push([top + mark * height - reading, mark]);
      });
      /* Vertebrae already above the reading line when the page opens light one by one over
         the first stretch of scrolling, each after a further 15% of the window */
      var gap = window.innerHeight * 0.15;
      for (var j = 1; j < stops.length; j++) {
        if (stops[j][1] > stops[j - 1][1]) stops[j][0] = Math.max(stops[j][0], stops[j - 1][0] + gap);
      }
      /* Stops past the end of the scroll share the last stretch, the final one at the bottom */
      var late = stops.findIndex(function (stop) { return stop[0] >= maxScroll; });
      if (late !== -1) {
        var from = late > 0 ? stops[late - 1][0] : 0, count = stops.length - late;
        for (var i = late; i < stops.length; i++) stops[i][0] = from + (maxScroll - from) * (i - late + 1) / count;
      }
      rail.stops = stops;
      rail.whole = maxScroll === 0;
    });
  }

  function fillAt(rail, scroll) {
    if (rail.whole) return 1;
    var stops = rail.stops;
    if (scroll <= stops[0][0]) return stops[0][1];
    for (var i = 1; i < stops.length; i++) {
      var a = stops[i - 1], b = stops[i];
      if (scroll <= b[0]) return b[0] === a[0] ? b[1] : a[1] + (b[1] - a[1]) * (scroll - a[0]) / (b[0] - a[0]);
    }
    return 1;
  }

  var ticking = false;
  function onScroll() {
    ticking = false;
    if (header) header.classList.toggle('is-scrolled', window.scrollY > 4);
    rails.forEach(function (rail) {
      var fill = fillAt(rail, window.scrollY);
      rail.el.style.setProperty('--rail-fill', fill.toFixed(4));
      rail.head.classList.toggle('is-moving', fill > 0 && fill < 1);
      rail.nodes.forEach(function (node, i) {
        node.classList.toggle('is-lit', fill >= rail.marks[i] - 0.0005);
      });
    });
  }
  function requestScroll() {
    if (!ticking) { ticking = true; window.requestAnimationFrame(onScroll); }
  }
  function relayout() { layoutRails(); requestScroll(); }
  window.addEventListener('scroll', requestScroll, { passive: true });
  window.addEventListener('resize', relayout);
  window.addEventListener('load', relayout);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(relayout);
  layoutRails();
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
