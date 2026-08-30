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

  function gaEnabled() {
    var current =
      global.CZAnalytics && global.CZAnalytics.getConsent
        ? global.CZAnalytics.getConsent()
        : 'unset';
    return current !== 'denied';
  }

  function closeBanner() {
    var el = document.getElementById('czCookieNotice');
    if (el) el.classList.remove('open');
  }

  function closeModal() {
    var modal = document.getElementById('czCookieModal');
    if (modal) modal.classList.remove('open');
    document.documentElement.classList.remove('cz-cookie-lock');
  }

  function openSettings() {
    var modal = document.getElementById('czCookieModal');
    if (!modal) return;
    var toggle = modal.querySelector('#czGaToggle');
    if (toggle) toggle.checked = gaEnabled();
    modal.classList.add('open');
    document.documentElement.classList.add('cz-cookie-lock');
  }

  function saveSettings() {
    var modal = document.getElementById('czCookieModal');
    var toggle = modal && modal.querySelector('#czGaToggle');
    var allow = toggle ? toggle.checked : true;
    if (global.CZAnalytics) {
      global.CZAnalytics.setConsent(allow ? 'granted' : 'denied');
    }
    markSeen();
    closeModal();
    closeBanner();
  }

  function acceptAll() {
    if (global.CZAnalytics) {
      global.CZAnalytics.setConsent('granted');
    }
    markSeen();
    closeBanner();
  }

  function mount() {
    if (document.getElementById('czCookieNotice')) return;

    var banner = document.createElement('div');
    banner.id = 'czCookieNotice';
    banner.className = 'cz-cookie';
    banner.innerHTML =
      '<p>Яндекс.Метрика включается сразу (статистика сайта). Google Analytics подключается позже и не обязателен — его можно отключить в настройках. <a href="#" class="js-cz-cookie-settings">Настроить</a> · <a href="/privacy/">Политика</a>.</p>' +
      '<button type="button" class="js-cz-cookie-ok">Понятно</button>';
    document.body.appendChild(banner);

    var modal = document.createElement('div');
    modal.id = 'czCookieModal';
    modal.className = 'cz-cookie-modal';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-labelledby', 'czCookieModalTitle');
    modal.innerHTML =
      '<div class="cz-cookie-modal__backdrop js-cz-cookie-close" tabindex="-1"></div>' +
      '<div class="cz-cookie-modal__panel">' +
      '<h2 id="czCookieModalTitle">Настройки cookie</h2>' +
      '<p class="cz-cookie-modal__lead">Яндекс.Метрика работает всегда — для учёта посещений и улучшения сайта. Её нельзя отключить в этом окне.</p>' +
      '<label class="cz-cookie-modal__row">' +
      '<span><strong>Google Analytics</strong><br /><span class="cz-cookie-modal__hint">Подключается с задержкой, чтобы не тормозить загрузку. Можно выключить.</span></span>' +
      '<input type="checkbox" id="czGaToggle" />' +
      '</label>' +
      '<div class="cz-cookie-modal__actions">' +
      '<button type="button" class="js-cz-cookie-save">Сохранить</button>' +
      '<button type="button" class="cz-cookie-modal__ghost js-cz-cookie-close">Закрыть</button>' +
      '</div>' +
      '<p class="cz-cookie-modal__foot"><a href="/privacy/">Политика обработки ПДн</a></p>' +
      '</div>';
    document.body.appendChild(modal);

    banner.querySelector('.js-cz-cookie-ok').addEventListener('click', acceptAll);
    banner.querySelector('.js-cz-cookie-settings').addEventListener('click', function (e) {
      e.preventDefault();
      openSettings();
    });
    modal.querySelector('.js-cz-cookie-save').addEventListener('click', saveSettings);
    modal.querySelectorAll('.js-cz-cookie-close').forEach(function (el) {
      el.addEventListener('click', closeModal);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && modal.classList.contains('open')) closeModal();
    });

    if (!seen()) banner.classList.add('open');
  }

  global.CZCookie = { openSettings: openSettings };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      setTimeout(mount, 400);
    });
  } else {
    setTimeout(mount, 400);
  }
})(window);
