/**
 * Goal clicks → Yandex Metrika reachGoal + GA4 events.
 */
(function (global) {
  var METRIKA_ID = 112001575;
  var queue = [];
  var flushTimer = null;

  function consentOk() {
    if (!global.CZAnalytics || !global.CZAnalytics.getConsent) return true;
    return global.CZAnalytics.getConsent() !== 'denied';
  }

  function flushQueue() {
    if (!consentOk()) {
      queue = [];
      return;
    }
    if (typeof global.ym !== 'function') return;
    while (queue.length) {
      var item = queue.shift();
      try {
        global.ym(METRIKA_ID, 'reachGoal', item.goal);
      } catch (e) {}
    }
  }

  function scheduleFlush() {
    flushQueue();
    if (!queue.length) return;
    if (flushTimer) return;
    var tries = 0;
    flushTimer = setInterval(function () {
      tries += 1;
      flushQueue();
      if (!queue.length || tries > 40) {
        clearInterval(flushTimer);
        flushTimer = null;
      }
    }, 250);
  }

  function reach(goalId, gaName, params) {
    if (!consentOk() || !goalId) return;

    if (typeof global.ym === 'function') {
      try {
        global.ym(METRIKA_ID, 'reachGoal', goalId);
      } catch (e) {
        queue.push({ goal: goalId });
        scheduleFlush();
      }
    } else {
      queue.push({ goal: goalId });
      scheduleFlush();
    }

    try {
      if (typeof global.gtag === 'function') {
        global.gtag('event', gaName || goalId, params || {});
      }
    } catch (e2) {}
  }

  function closestLink(el) {
    while (el && el !== document && el.nodeType === 1) {
      if (el.tagName === 'A' && el.getAttribute('href')) return el;
      el = el.parentElement;
    }
    return null;
  }

  function classify(href, link) {
    var h = (href || '').trim();
    var low = h.toLowerCase();
    if (!h || low.indexOf('javascript:') === 0) return null;

    if (low.indexOf('tel:') === 0) {
      return { goal: 'click_phone', ga: 'click_phone', params: {} };
    }

    if (/t\.me\/cenzykt_g\b/i.test(h) || /telegram\.me\/cenzykt_g\b/i.test(h)) {
      return {
        goal: 'click_tg_channel',
        ga: 'click_messenger',
        params: { messenger: 'telegram_channel' },
      };
    }

    if (/t\.me\/cenzyk\b/i.test(h) || /telegram\.me\/cenzyk\b/i.test(h)) {
      return {
        goal: 'click_telegram',
        ga: 'click_messenger',
        params: { messenger: 'telegram' },
      };
    }

    if (/max\.ru\//i.test(h)) {
      return {
        goal: 'click_max',
        ga: 'click_messenger',
        params: { messenger: 'max' },
      };
    }

    if (/#meeting\b/i.test(h)) {
      var label = ((link && (link.getAttribute('aria-label') || link.textContent)) || '')
        .replace(/\s+/g, ' ')
        .trim()
        .slice(0, 80);
      return {
        goal: 'cta_meeting',
        ga: 'cta_meeting',
        params: { label: label || 'meeting' },
      };
    }

    return null;
  }

  function onClick(e) {
    var link = closestLink(e.target);
    if (!link) return;
    var hit = classify(link.getAttribute('href') || '', link);
    if (!hit) return;
    reach(hit.goal, hit.ga, hit.params);
  }

  function fireThankYou() {
    var path = (location.pathname || '').toLowerCase();
    if (path.indexOf('/thanks') === -1) return;
    // URL-цель Метрики ловит path; JS — запасной сигнал
    reach('thank_you', 'thank_you', { page_path: location.pathname });
  }

  document.addEventListener('click', onClick, true);

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fireThankYou);
  } else {
    fireThankYou();
  }

  global.CZGoals = { reach: reach };
})(window);
