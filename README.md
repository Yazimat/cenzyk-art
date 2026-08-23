# илай-металл.рф — Илай Саматов · изделия из металла

Статический сайт (HTML/CSS/JS) → **GitHub Pages**.  
Основной домен: **`илай-металл.рф`**.  
`cenzyk.art` → редирект на `илай-металл.рф` (настраивается у регистратора).

Репозиторий изолирован: не затрагивает сайты психолога и общий `psi-leads`.

## Локальный просмотр

```bash
python3 -m http.server 4173
```

- http://127.0.0.1:4173/ — главная
- http://127.0.0.1:4173/3d-primerka/ — посадочная 3D под Директ
- http://127.0.0.1:4173/preview/ — архив старых вариантов

## Стек

- Статика, без админки
- Метрика `105346765` + GA `G-MHZ849WZ9M` (`assets/js/consent-analytics.js`)
- Cookie-notice с отказом от статистики
- Заявки → Telegram через Cloudflare Worker (`workers/lead-telegram/`, см. [docs/TELEGRAM-LEADS.md](docs/TELEGRAM-LEADS.md))

## Ключевые пути

| Путь | Назначение |
|------|------------|
| `preview/` | Варианты главной (noindex) |
| `3d-primerka/` | Посадка Директ |
| `balkony/` `zabory/` `lestnicy/` `mebel/` | Услуги |
| `docs/BRAND-BRIEF.md` | Бриф |
| `docs/telegram-*.txt` | Выгрузка канала |

## Деплой

Push в `main` → Actions **Deploy to GitHub Pages**.  
Custom domain в GitHub: `илай-металл.рф`.

### DNS `илай-металл.рф` (Reg.ru)

- 4× A `@` → `185.199.108.153` / `.109.153` / `.110.153` / `.111.153`
- 4× AAAA `@` (опционально) → GitHub IPv6
- CNAME `www` → `yazimat.github.io.`

### Редирект `cenzyk.art` → `илай-металл.рф`

GitHub Pages принимает **один** custom domain. Редирект старого домена — у регистратора:

1. Reg.ru → домен `cenzyk.art` → **Перенаправление** / **URL-forwarding**
2. Куда: `https://илай-металл.рф/` (лучше с сохранением пути, если есть опция)
3. Убери A/AAAA на GitHub у `cenzyk.art`, если они ещё стоят — иначе конфликт с forwarding

В репозитории есть запасной JS (`assets/js/domain-redirect.js`) на случай, если старый хост всё же откроет этот сайт.

## Заявки в Telegram

Пока сайт на GitHub Pages, формы шлют JSON на **Cloudflare Worker**, тот пишет боту в личку. VPS не нужен.

1. Создать бота и взять `chat_id` — шаги в [docs/TELEGRAM-LEADS.md](docs/TELEGRAM-LEADS.md)
2. Задеплоить Worker:

```bash
cd workers/lead-telegram
npm install
npx wrangler login
npx wrangler secret put TELEGRAM_BOT_TOKEN
npx wrangler secret put TELEGRAM_CHAT_ID
npx wrangler deploy
```

3. Вставить URL из деплоя в `LEAD_API_URL` в [`assets/js/lead-form.js`](assets/js/lead-form.js) и запушить сайт.

Пока `LEAD_API_URL` пустой — работает запасной deep-link в `t.me/Cenzyk`.  
На VPS позже: тот же `POST /api/lead`, меняется только `LEAD_API_URL`.
