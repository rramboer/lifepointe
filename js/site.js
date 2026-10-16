/* Lifepointe — progressive enhancement only; every page works without JS. */
(function () {
  'use strict';

  /* Mobile navigation: the Menu button opens and closes the menu. Escape closes it and returns
     to the button. A tap outside it closes it too, and so does choosing one of its links
     (which may only jump within the page). */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    var setOpen = function (open) {
      nav.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    };
    toggle.addEventListener('click', function () {
      setOpen(!nav.classList.contains('is-open'));
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open') &&
          (nav.contains(document.activeElement) || toggle === document.activeElement)) {
        setOpen(false);
        toggle.focus();
      }
    });
    document.addEventListener('click', function (e) {
      if (nav.classList.contains('is-open') && !nav.contains(e.target) && !toggle.contains(e.target)) setOpen(false);
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setOpen(false);
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
    var groups = '.grid-2, .grid-3, .grid-4, .quote-columns, .steps, .card-stack, .team-grid, .product-grid, .reach-grid, .doctor';
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

  /* Phones: slide the bottom action bar (Call, Request an appointment) away while the closing
     call-to-action band or the contact page's appointment section is on screen, since they
     show the same two actions. */
  var bar = document.querySelector('.action-bar');
  var sameActions = document.querySelectorAll('.cta-band, #appointment');
  if (bar && sameActions.length && 'IntersectionObserver' in window) {
    var onScreen = [];
    var barWatch = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var at = onScreen.indexOf(e.target);
        if (e.isIntersecting && at === -1) onScreen.push(e.target);
        if (!e.isIntersecting && at !== -1) onScreen.splice(at, 1);
      });
      bar.classList.toggle('is-away', onScreen.length > 0);
    }, { rootMargin: '0px 0px -12% 0px' });
    sameActions.forEach(function (el) { barWatch.observe(el); });
  }

  /* Office hours, in the office's own time zone, so a visitor elsewhere still sees Clarkston's
     day and time. Each hours table row has data-days (0 = Sunday) and data-hours
     ("07:30-11:30 14:30-18:00", empty when closed). This marks today's row, and fills the
     [data-open-status] line above the table: "Open now · until 11:30am" or "Closed now · opens
     Monday at 7:30am". It goes by the regular hours, as Google's listing does. */
  var DAY_NAMES = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  function officeNow() {
    try {
      var parts = {};
      new Intl.DateTimeFormat('en-US', { timeZone: 'America/Detroit', weekday: 'short', hour: 'numeric', minute: 'numeric', hourCycle: 'h23' })
        .formatToParts(new Date()).forEach(function (part) { parts[part.type] = part.value; });
      var day = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(parts.weekday);
      if (day === -1) throw new Error('weekday');
      return { day: day, minutes: (Number(parts.hour) % 24) * 60 + Number(parts.minute) };
    } catch (err) {
      var local = new Date();
      return { day: local.getDay(), minutes: local.getHours() * 60 + local.getMinutes() };
    }
  }
  function clock(minutes) {
    var h = Math.floor(minutes / 60), m = minutes % 60;
    return (h % 12 || 12) + (m ? ':' + (m < 10 ? '0' : '') + m : '') + (h < 12 ? 'am' : 'pm');
  }
  var now = officeNow();
  var week = [[], [], [], [], [], [], []];
  var rows = document.querySelectorAll('.hours-table [data-days]');
  rows.forEach(function (row) {
    var days = row.getAttribute('data-days').split(',').map(Number);
    var sessions = (row.getAttribute('data-hours') || '').split(' ').filter(Boolean).map(function (span) {
      var t = span.split('-').map(function (hhmm) { var x = hhmm.split(':'); return Number(x[0]) * 60 + Number(x[1]); });
      return { open: t[0], close: t[1] };
    });
    days.forEach(function (d) { week[d] = sessions; });
    if (days.indexOf(now.day) !== -1) {
      row.classList.add('is-today');
      row.setAttribute('aria-current', 'date');
      var th = row.querySelector('th');
      if (th) th.insertAdjacentHTML('beforeend', ' <span class="visually-hidden">(today)</span>');
    }
  });
  var status = null, open = false;
  if (rows.length) {
    week[now.day].forEach(function (s) {
      if (now.minutes >= s.open && now.minutes < s.close) { open = true; status = 'Open now · until ' + clock(s.close); }
    });
    for (var ahead = 0; status === null && ahead < 7; ahead++) {
      var d = (now.day + ahead) % 7;
      var next = week[d].filter(function (s) { return ahead > 0 || s.open > now.minutes; })[0];
      if (next) {
        var when = ahead === 0 ? 'today' : ahead === 1 ? 'tomorrow' : DAY_NAMES[d];
        status = 'Closed now · opens ' + when + ' at ' + clock(next.open);
      }
    }
  }
  if (status) {
    document.querySelectorAll('[data-open-status]').forEach(function (el) {
      el.textContent = status;
      el.classList.toggle('is-open', open);
      el.hidden = false;
    });
  }

  /* "Copy email address" (contact page): shown only where the browser can copy. The button
     reads "Copied" for a moment, and the status line after it tells screen readers. */
  if (navigator.clipboard && window.isSecureContext) {
    document.querySelectorAll('[data-copy]').forEach(function (button) {
      var label = button.textContent;
      var said = button.nextElementSibling && button.nextElementSibling.getAttribute('role') === 'status'
        ? button.nextElementSibling : null;
      button.hidden = false;
      button.addEventListener('click', function () {
        navigator.clipboard.writeText(button.getAttribute('data-copy')).then(function () {
          button.textContent = 'Copied';
          if (said) said.textContent = 'Email address copied';
          window.setTimeout(function () {
            button.textContent = label;
            if (said) said.textContent = '';
          }, 2500);
        }, function () { /* the address is on the screen to copy by hand */ });
      });
    });
  }

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
