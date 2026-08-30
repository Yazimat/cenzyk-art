/**
 * Goal clicks → Yandex Metrika reachGoal + GA4 events.
 * Requires CZAnalytics / ym / gtag after consent-analytics.js.
 */
(function (global) {
  var METRIKA_ID = 112001575;

  function consentOk() {
    if (!global.CZAnalytics || !global.CZAnalytics.getConsent) return true;
    return global.CZAnalytics.getConsent() !== 'denied';
  }

  function reach(goalId, gaName, params) {
    if (!consentOk() || !goalId) return;
    try {
      if (typeof global.ym === 'function') {
        global.ym(METRIKA_ID, 'reachGoal', goalId);
      }
    } catch (e) {}
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

    if (/t\.me\/cenzykt_g/i.test(h) || /telegram\.me\/cenzykt_g/i.test(h)) {
      return {
        goal: 'click_tg_channel',
        ga: 'click_messenger',
        params: { messenger: 'telegram_channel' },
      };
    }

    if (/t\.me\/cenzyk(\?|$|\/|#)/i.test(h) || /telegram\.me\/cenzyk(\?|$|\/|#)/i.test(h)) {
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

    // CTA → #meeting (discuss / contact / connect)
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
