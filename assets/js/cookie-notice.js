(function (global) {
  var NOTICE_KEY = 'cz_cookie_notice_seen';

  function seen() {
    try {
      return localStorage.getItem(NOTICE_KEY) === '1';
    } catch (e) {
      return false;
    }
  }

  function markSeen() {
    try {
      localStorage.setItem(NOTICE_KEY, '1');
    } catch (e) {}
  }

  function consentLabel() {
    var current =
      global.CZAnalytics && global.CZAnalytics.getConsent
        ? global.CZAnalytics.getConsent()
        : 'unset';
    if (current === 'granted') return 'ВКЛ';
    if (current === 'denied') return 'ВЫКЛ';
    return 'не задано';
  }

  function openSettings() {
    var next = window.confirm(
      'Сбор статистики (Яндекс.Метрика / Google Analytics) сейчас: ' +
        consentLabel() +
        '.\n\nOK — включить статистику\nОтмена — только необходимые cookie'
    );
    if (global.CZAnalytics) {
      global.CZAnalytics.setConsent(next ? 'granted' : 'denied');
    }
    markSeen();
    var el = document.getElementById('czCookieNotice');
    if (el) el.classList.remove('open');
  }

  function acceptAnalytics() {
    if (global.CZAnalytics) {
      global.CZAnalytics.setConsent('granted');
    }
    markSeen();
    var el = document.getElementById('czCookieNotice');
    if (el) el.classList.remove('open');
  }

  function mount() {
    if (document.getElementById('czCookieNotice')) return;
    var el = document.createElement('div');
    el.id = 'czCookieNotice';
    el.className = 'cz-cookie';
    el.innerHTML =
      '<p>Используем необходимые cookie для работы сайта. Статистику (Метрика / GA) включаем только с вашего согласия. <a href="#" class="js-cz-cookie-settings">Настроить</a> · <a href="/privacy/">Политика</a>.</p>' +
      '<button type="button" class="js-cz-cookie-ok">Принять статистику</button>';
    document.body.appendChild(el);
    el.querySelector('.js-cz-cookie-ok').addEventListener('click', acceptAnalytics);
    el.querySelector('.js-cz-cookie-settings').addEventListener('click', function (e) {
      e.preventDefault();
      openSettings();
    });
    var consent =
      global.CZAnalytics && global.CZAnalytics.getConsent
        ? global.CZAnalytics.getConsent()
        : 'unset';
    if (!seen() || consent === 'unset') el.classList.add('open');
  }

  global.CZCookie = { openSettings: openSettings };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      setTimeout(mount, 800);
    });
  } else {
    setTimeout(mount, 800);
  }
})(window);
