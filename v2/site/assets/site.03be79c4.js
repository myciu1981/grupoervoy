/* GRUPO ERVOY: menu na telefonie, filtry kalendarza targów, wyszukiwarka słownika. Bez bibliotek. */
(function () {
  'use strict';

  // menu
  var head = document.querySelector('.site-head');
  var btn = head && head.querySelector('.menu-btn');
  if (btn) {
    btn.addEventListener('click', function () {
      var open = head.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // kalendarz targów
  var filters = document.querySelector('[data-fairs-filters]');
  if (filters) {
    filters.hidden = false;
    var rows = Array.prototype.slice.call(document.querySelectorAll('.fairs tbody tr'));
    var countEl = document.querySelector('[data-count]');
    var forms = JSON.parse(countEl.getAttribute('data-forms'));
    var emptyEl = document.querySelector('[data-empty]');
    var lang = document.documentElement.lang.slice(0, 2);
    var state = { cat: '', city: '' };
    var params = new URLSearchParams(location.search);
    if (params.get('branza')) state.cat = params.get('branza');
    if (params.get('miasto')) state.city = params.get('miasto');

    function plural(n) {
      if (lang === 'pl') {
        if (n === 1) return forms[0];
        var m10 = n % 10, m100 = n % 100;
        return (m10 >= 2 && m10 <= 4 && (m100 < 12 || m100 > 14)) ? forms[1] : forms[2];
      }
      return n === 1 ? forms[0] : forms[1];
    }

    function apply() {
      var n = 0;
      rows.forEach(function (tr) {
        var okCat = !state.cat || (' ' + tr.getAttribute('data-cats') + ' ').indexOf(' ' + state.cat + ' ') >= 0;
        var okCity = !state.city || tr.getAttribute('data-city') === state.city;
        tr.hidden = !(okCat && okCity);
        if (!tr.hidden) n++;
      });
      filters.querySelectorAll('.chip').forEach(function (c) {
        c.setAttribute('aria-pressed', state[c.getAttribute('data-f')] === c.getAttribute('data-v') ? 'true' : 'false');
      });
      countEl.textContent = n ? plural(n).replace('{n}', n) : '';
      emptyEl.hidden = n !== 0;
    }

    filters.addEventListener('click', function (e) {
      var c = e.target.closest('.chip');
      if (!c) return;
      state[c.getAttribute('data-f')] = c.getAttribute('data-v');
      apply();
    });
    apply();
  }

  // słownik
  var search = document.querySelector('[data-gl-search]');
  if (search) {
    search.hidden = false;
    var input = search.querySelector('input');
    var groups = Array.prototype.slice.call(document.querySelectorAll('[data-gl-group]'));
    var glEmpty = document.querySelector('[data-gl-empty]');
    var norm = function (s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); };
    input.addEventListener('input', function () {
      var q = norm(input.value.trim());
      var total = 0;
      groups.forEach(function (g) {
        var shown = 0;
        g.querySelectorAll('.gl-entry').forEach(function (e) {
          var hit = !q || norm(e.getAttribute('data-gl-text')).indexOf(q) >= 0;
          e.hidden = !hit;
          if (hit) shown++;
        });
        g.hidden = shown === 0;
        total += shown;
      });
      glEmpty.hidden = total !== 0;
    });
  }
})();
