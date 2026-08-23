/**
 * Analytics: Metrika + GA load by default; user can opt out via cookie settings.
 * Matches cenzyk brief (same pattern as psychologist sites).
 */
(function (global) {
  var METRIKA_ID = 105346765;
  var GTAG_ID = 'G-MHZ849WZ9M';
  var STORAGE_KEY = 'cz_analytics_consent';

  function readConsent() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (raw === 'denied') return 'denied';
      if (raw === 'granted') return 'granted';
    } catch (e) {}
    return 'granted';
  }

  function writeConsent(value) {
    try {
      localStorage.setItem(STORAGE_KEY, value);
    } catch (e) {}
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

  function loadMetrika() {
    if (global.__czMetrikaLoaded) return;
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

  function applyConsent(value) {
    writeConsent(value);
    if (value === 'denied') {
      clearAnalyticsCookies();
      return;
    }
    loadMetrika();
    loadGtag();
  }

  global.CZAnalytics = {
    getConsent: readConsent,
    setConsent: applyConsent,
    openSettings: function () {
      if (typeof global.CZCookie !== 'undefined' && global.CZCookie.openSettings) {
        global.CZCookie.openSettings();
      }
    },
  };

  applyConsent(readConsent());
})(window);
