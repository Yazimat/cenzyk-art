/**
 * Cloudflare Worker: POST /api/lead → Telegram Bot API
 * Secrets: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
 */

const ALLOWED_ORIGINS = new Set([
  'https://илай-металл.рф',
  'https://www.илай-металл.рф',
  'https://xn----7sbbtmhmfag1e.xn--p1ai',
  'https://www.xn----7sbbtmhmfag1e.xn--p1ai',
  'https://cenzyk.art',
  'https://www.cenzyk.art',
  'https://yazimat.github.io',
  'http://127.0.0.1:4173',
  'http://localhost:4173',
  'http://127.0.0.1:8000',
  'http://localhost:8000',
]);

const MAX_LEN = {
  name: 80,
  phone: 40,
  contact: 20,
  address: 200,
  comment: 2000,
  budget: 40,
  lead: 40,
};

/** @type {Map<string, number[]>} */
const rateBuckets = new Map();
const RATE_WINDOW_MS = 10 * 60 * 1000;
const RATE_MAX = 5;

function corsHeaders(origin) {
  const allow = origin && ALLOWED_ORIGINS.has(origin) ? origin : 'null';
  return {
    'Access-Control-Allow-Origin': allow,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
    Vary: 'Origin',
  };
}

function json(body, status, origin) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      ...corsHeaders(origin),
    },
  });
}

function clip(value, max) {
  const s = String(value == null ? '' : value).trim();
  return s.slice(0, max);
}

function clientIp(request) {
  return (
    request.headers.get('CF-Connecting-IP') ||
    request.headers.get('X-Forwarded-For')?.split(',')[0]?.trim() ||
    'unknown'
  );
}

function rateLimit(ip) {
  const now = Date.now();
  let hits = rateBuckets.get(ip) || [];
  hits = hits.filter((t) => now - t < RATE_WINDOW_MS);
  if (hits.length >= RATE_MAX) {
    rateBuckets.set(ip, hits);
    return false;
  }
  hits.push(now);
  rateBuckets.set(ip, hits);
  return true;
}

function buildMessage(data) {
  const lines = [
    'Новая заявка — илай-металл.рф',
    '',
    'Тип: ' + data.lead,
    'Имя: ' + data.name,
    'Телефон: ' + data.phone,
    'Связь: ' + data.contact,
    'Адрес: ' + data.address,
    'Бюджет: ' + data.budget,
    'Комментарий: ' + data.comment,
  ];
  return lines.join('\n');
}

async function sendTelegram(env, text) {
  const token = env.TELEGRAM_BOT_TOKEN;
  const chatId = env.TELEGRAM_CHAT_ID;
  if (!token || !chatId) {
    return { ok: false, error: 'server_misconfigured' };
  }

  const url = 'https://api.telegram.org/bot' + token + '/sendMessage';
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: chatId,
      text: text,
      disable_web_page_preview: true,
    }),
  });

  if (!res.ok) {
    return { ok: false, error: 'telegram_failed' };
  }
  return { ok: true };
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const url = new URL(request.url);

    if (request.method === 'OPTIONS') {
      if (!ALLOWED_ORIGINS.has(origin)) {
        return new Response(null, { status: 403 });
      }
      return new Response(null, { status: 204, headers: corsHeaders(origin) });
    }

    if (request.method !== 'POST' || url.pathname !== '/api/lead') {
      return json({ ok: false, error: 'not_found' }, 404, origin);
    }

    if (origin && !ALLOWED_ORIGINS.has(origin)) {
      return json({ ok: false, error: 'origin_denied' }, 403, origin);
    }

    const ip = clientIp(request);
    if (!rateLimit(ip)) {
      return json({ ok: false, error: 'rate_limited' }, 429, origin);
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return json({ ok: false, error: 'invalid_json' }, 400, origin);
    }

    // Honeypot: bots fill "website"
    if (clip(body.website, 200)) {
      return json({ ok: true }, 200, origin);
    }

    const data = {
      lead: clip(body.lead || body.type || 'site', MAX_LEN.lead) || 'site',
      name: clip(body.name, MAX_LEN.name),
      phone: clip(body.phone, MAX_LEN.phone),
      contact: clip(body.contact, MAX_LEN.contact) || '—',
      address: clip(body.address, MAX_LEN.address) || '—',
      comment: clip(body.comment, MAX_LEN.comment) || '—',
      budget: clip(body.budget, MAX_LEN.budget) || '—',
    };

    if (!data.name || data.name.length < 2) {
      return json({ ok: false, error: 'name_required' }, 400, origin);
    }
    if (!data.phone || data.phone.length < 5) {
      return json({ ok: false, error: 'phone_required' }, 400, origin);
    }

    const tg = await sendTelegram(env, buildMessage(data));
    if (!tg.ok) {
      return json({ ok: false, error: tg.error }, 502, origin);
    }

    return json({ ok: true }, 200, origin);
  },
};
