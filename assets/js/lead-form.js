(function () {
  /**
   * After `wrangler deploy` paste the Worker URL here, e.g.:
   * 'https://lead-telegram.<subdomain>.workers.dev/api/lead'
   * Leave empty to use Telegram deep-link fallback only.
   * On VPS later: 'https://илай-металл.рф/api/lead'
   */
  var LEAD_API_URL = '';

  var TG_FALLBACK = 'https://t.me/Cenzyk';

  function thanksUrl(form) {
    try {
      return new URL('thanks/', form.baseURI || location.href).href;
    } catch (e) {
      return 'thanks/';
    }
  }

  function toTelegramText(form) {
    var data = new FormData(form);
    return [
      'Заявка с илай-металл.рф',
      'Тип: ' + (form.getAttribute('data-lead') || 'site'),
      'Имя: ' + (data.get('name') || ''),
      'Телефон: ' + (data.get('phone') || ''),
      'Связь: ' + (data.get('contact') || ''),
      'Адрес: ' + (data.get('address') || ''),
      'Бюджет: ' + (data.get('budget') || ''),
      'Комментарий: ' + (data.get('comment') || ''),
    ].join('\n');
  }

  function openTelegramFallback(form) {
    var text = encodeURIComponent(toTelegramText(form));
    window.open(TG_FALLBACK + '?text=' + text, '_blank', 'noopener');
  }

  function ensureStatusEl(form) {
    var el = form.querySelector('[data-lead-status]');
    if (el) return el;
    el = document.createElement('p');
    el.className = 'tiny dark';
    el.setAttribute('data-lead-status', '');
    el.setAttribute('role', 'status');
    el.hidden = true;
    var btn = form.querySelector('button[type="submit"]');
    if (btn && btn.parentNode) {
      btn.parentNode.insertBefore(el, btn.nextSibling);
    } else {
      form.appendChild(el);
    }
    return el;
  }

  function setStatus(form, message, isError) {
    var el = ensureStatusEl(form);
    if (!message) {
      el.hidden = true;
      el.textContent = '';
      return;
    }
    el.hidden = false;
    el.textContent = message;
    el.style.color = isError ? '#b33' : '';
  }

  function payloadFromForm(form) {
    var data = new FormData(form);
    return {
      lead: form.getAttribute('data-lead') || 'site',
      name: String(data.get('name') || '').trim(),
      phone: String(data.get('phone') || '').trim(),
      contact: String(data.get('contact') || '').trim(),
      address: String(data.get('address') || '').trim(),
      comment: String(data.get('comment') || '').trim(),
      budget: String(data.get('budget') || '').trim(),
      website: String(data.get('website') || '').trim(),
    };
  }

  function setBusy(form, busy) {
    var btn = form.querySelector('button[type="submit"]');
    if (!btn) return;
    if (busy) {
      btn.disabled = true;
      btn.dataset.label = btn.textContent;
      btn.textContent = 'Отправка…';
    } else {
      btn.disabled = false;
      if (btn.dataset.label) btn.textContent = btn.dataset.label;
    }
  }

  async function submitToApi(form) {
    var res = await fetch(LEAD_API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(payloadFromForm(form)),
    });
    var body = null;
    try {
      body = await res.json();
    } catch (e) {
      body = null;
    }
    if (!res.ok || !body || !body.ok) {
      var err = (body && body.error) || 'send_failed';
      throw new Error(err);
    }
  }

  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form.matches || !form.matches('form[data-lead]')) return;
    e.preventDefault();

    setStatus(form, '', false);

    if (!LEAD_API_URL) {
      openTelegramFallback(form);
      location.href = thanksUrl(form);
      return;
    }

    setBusy(form, true);
    submitToApi(form)
      .then(function () {
        location.href = thanksUrl(form);
      })
      .catch(function () {
        setBusy(form, false);
        setStatus(
          form,
          'Не удалось отправить автоматически. Откроется Telegram — нажмите «Отправить» там.',
          true
        );
        openTelegramFallback(form);
      });
  });
})();
