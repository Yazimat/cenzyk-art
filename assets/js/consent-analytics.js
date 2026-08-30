/**
 * Analytics:
 * - Default: Metrika immediately; GA delayed (perf)
 * - Cookie modal "Статистика" can disable both
 */
(function (global) {
  var METRIKA_ID = 112001575;
  var GTAG_ID = 'G-93Z1C124BV';
  var STORAGE_KEY = 'cz_ga_consent';
  var LEGACY_KEY = 'cz_analytics_consent';
  var GA_DELAY_MS = 2500;

  function readConsent() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (raw === 'denied' || raw === 'granted') return raw;
      var legacy = localStorage.getItem(LEGACY_KEY);
      if (legacy === 'denied') return 'denied';
      if (legacy === 'granted') return 'granted';
    } catch (e) {}
    return 'unset';
  }

  function writeConsent(value) {
    try {
      localStorage.setItem(STORAGE_KEY, value);
    } catch (e) {}
  }

  function loadMetrika() {
    if (global.__czMetrikaLoaded) return;
    if (readConsent() === 'denied') return;
    global.__czMetrikaLoaded = true;
    (function (m, e, t, r, i, k, a) {
      m[i] =
        m[i] ||
        function () {
          (m[i].a = m[i].a || []).push(arguments);
        };
      m[i].l = 1 * new Date();
      k = e.createElement(t);
      a = e.getElementsByTagName(t)[0];
      k.async = 1;
      k.src = r;
      a.parentNode.insertBefore(k, a);
    })(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js?id=' + METRIKA_ID, 'ym');
    global.ym(METRIKA_ID, 'init', {
      clickmap: true,
      trackLinks: true,
      accurateTrackBounce: true,
      webvisor: true,
    });
  }

  function loadGtag() {
    if (global.__czGtagLoaded) return;
    global.__czGtagLoaded = true;
    global.dataLayer = global.dataLayer || [];
    global.gtag =
      global.gtag ||
      function () {
        global.dataLayer.push(arguments);
      };
    global.gtag('js', new Date());
    global.gtag('config', GTAG_ID, { anonymize_ip: true });
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GTAG_ID;
    document.head.appendChild(s);
  }

  function clearAnalyticsCookies() {
    var cookies = document.cookie ? document.cookie.split(';') : [];
    cookies.forEach(function (part) {
      var name = part.split('=')[0].trim();
      if (!name) return;
      if (/^(_ym|_ga|_gid|_gat|ymex|yabs-sid)/.test(name)) {
        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;';
      }
    });
  }

  function scheduleGtag() {
    if (global.__czGtagScheduled || global.__czGtagLoaded) return;
    if (readConsent() === 'denied') return;
    global.__czGtagScheduled = true;
    var run = function () {
      if (readConsent() === 'denied') return;
      loadGtag();
    };
    if (typeof global.requestIdleCallback === 'function') {
      global.requestIdleCallback(run, { timeout: GA_DELAY_MS });
    } else {
      setTimeout(run, GA_DELAY_MS);
    }
  }

  function applyConsent(value) {
    if (value !== 'granted' && value !== 'denied') return;
    writeConsent(value);
    if (value === 'denied') {
      clearAnalyticsCookies();
      return;
    }
    loadMetrika();
    scheduleGtag();
  }

  global.CZAnalytics = {
    metrikaId: METRIKA_ID,
    gtagId: GTAG_ID,
    getConsent: readConsent,
    setConsent: applyConsent,
    openSettings: function () {
      if (typeof global.CZCookie !== 'undefined' && global.CZCookie.openSettings) {
        global.CZCookie.openSettings();
      }
    },
  };

  // Default: stats on until user chooses «Только необходимые»
  if (readConsent() !== 'denied') {
    loadMetrika();
    scheduleGtag();
  }
})(window);
