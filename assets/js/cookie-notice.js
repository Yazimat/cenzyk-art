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

  function openSettings() {
    var current =
      global.CZAnalytics && global.CZAnalytics.getConsent
        ? global.CZAnalytics.getConsent()
        : 'granted';
    var next = window.confirm(
      'Сбор статистики (Яндекс.Метрика / Google Analytics) сейчас: ' +
        (current === 'denied' ? 'ВЫКЛ' : 'ВКЛ') +
        '.\n\nOK — включить статистику\nОтмена — только необходимые cookie'
    );
    if (global.CZAnalytics) {
      global.CZAnalytics.setConsent(next ? 'granted' : 'denied');
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
      '<p>Мы используем cookie: необходимые — для работы сайта; статистику можно <a href="#" class="js-cz-cookie-settings">настроить</a>. Подробнее — в <a href="/privacy/">политике</a>.</p>' +
      '<button type="button" class="js-cz-cookie-ok">Ок</button>';
    document.body.appendChild(el);
    el.querySelector('.js-cz-cookie-ok').addEventListener('click', function () {
      markSeen();
      el.classList.remove('open');
    });
    el.querySelector('.js-cz-cookie-settings').addEventListener('click', function (e) {
      e.preventDefault();
      openSettings();
    });
    if (!seen()) el.classList.add('open');
  }

  global.CZCookie = { openSettings: openSettings };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      setTimeout(mount, 1200);
    });
  } else {
    setTimeout(mount, 1200);
  }
})(window);
