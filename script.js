/* Terra Altera — interakcje strony */
(function () {
  'use strict';

  var navToggle = document.getElementById('navToggle');
  var mainNav = document.getElementById('mainNav');
  var navLinks = document.querySelectorAll('.nav-link');

  // --- Menu mobilne (hamburger) ---
  if (navToggle && mainNav) {
    navToggle.addEventListener('click', function () {
      var isOpen = mainNav.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    navLinks.forEach(function (link) {
      link.addEventListener('click', function () {
        mainNav.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // --- Podświetlanie aktywnej sekcji w menu podczas przewijania ---
  var sections = Array.prototype.slice.call(document.querySelectorAll('main section[id]'));

  if (sections.length && 'IntersectionObserver' in window) {
    var linkById = {};
    navLinks.forEach(function (link) {
      var id = link.getAttribute('href').replace('#', '');
      linkById[id] = link;
    });

    var ratios = {};

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        ratios[entry.target.id] = entry.isIntersecting ? entry.intersectionRatio : 0;
      });

      var bestId = null;
      var bestRatio = 0;
      Object.keys(ratios).forEach(function (id) {
        if (ratios[id] > bestRatio) {
          bestRatio = ratios[id];
          bestId = id;
        }
      });

      if (bestId) {
        navLinks.forEach(function (l) { l.classList.remove('active'); });
        linkById[bestId].classList.add('active');
      }
    }, {
      rootMargin: '-45% 0px -50% 0px',
      threshold: [0, 0.25, 0.5, 0.75, 1]
    });

    sections.forEach(function (section) { observer.observe(section); });
  }
})();
