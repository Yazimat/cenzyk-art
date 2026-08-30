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

  function statsEnabled() {
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
    var toggle = modal.querySelector('#czStatsToggle');
    if (toggle) toggle.checked = statsEnabled();
    modal.classList.add('open');
    document.documentElement.classList.add('cz-cookie-lock');
  }

  function applyStats(allow) {
    if (global.CZAnalytics) {
      global.CZAnalytics.setConsent(allow ? 'granted' : 'denied');
    }
    markSeen();
    closeModal();
    closeBanner();
  }

  function saveSettings() {
    var modal = document.getElementById('czCookieModal');
    var toggle = modal && modal.querySelector('#czStatsToggle');
    applyStats(toggle ? toggle.checked : true);
  }

  function onlyNecessary() {
    var modal = document.getElementById('czCookieModal');
    var toggle = modal && modal.querySelector('#czStatsToggle');
    if (toggle) toggle.checked = false;
    applyStats(false);
  }

  function acceptBanner() {
    applyStats(true);
  }

  function mount() {
    if (document.getElementById('czCookieNotice')) return;

    var banner = document.createElement('div');
    banner.id = 'czCookieNotice';
    banner.className = 'cz-cookie';
    banner.innerHTML =
      '<p>Мы используем cookie: необходимые — для работы сайта; сбор статистики можно <a href="#" class="js-cz-cookie-settings">настроить</a>. Подробнее — в <a href="/privacy/">политике конфиденциальности</a>.</p>' +
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
      '<p class="cz-cookie-modal__lead">Выберите, что разрешить. Подробнее — в <a href="/privacy/">политике конфиденциальности</a>.</p>' +
      '<div class="cz-cookie-modal__row cz-cookie-modal__row--locked">' +
      '<span><strong>Необходимые</strong><br /><span class="cz-cookie-modal__hint">Нужны для работы сайта. Отключить нельзя.</span></span>' +
      '<input type="checkbox" checked disabled aria-label="Необходимые cookie" />' +
      '</div>' +
      '<label class="cz-cookie-modal__row">' +
      '<span><strong>Статистика посещений</strong><br /><span class="cz-cookie-modal__hint">Помогает понимать, как пользуются сайтом (Яндекс.Метрика и Google Analytics). Можно отключить.</span></span>' +
      '<input type="checkbox" id="czStatsToggle" />' +
      '</label>' +
      '<div class="cz-cookie-modal__actions">' +
      '<button type="button" class="cz-cookie-modal__ghost js-cz-cookie-necessary">Только необходимые</button>' +
      '<button type="button" class="js-cz-cookie-save">Сохранить</button>' +
      '</div>' +
      '</div>';
    document.body.appendChild(modal);

    banner.querySelector('.js-cz-cookie-ok').addEventListener('click', acceptBanner);
    banner.querySelector('.js-cz-cookie-settings').addEventListener('click', function (e) {
      e.preventDefault();
      openSettings();
    });
    modal.querySelector('.js-cz-cookie-save').addEventListener('click', saveSettings);
    modal.querySelector('.js-cz-cookie-necessary').addEventListener('click', onlyNecessary);
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
