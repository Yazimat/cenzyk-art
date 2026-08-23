# Заявки в Telegram (Cloudflare Worker)

Сайт на GitHub Pages остаётся статикой. Worker принимает `POST /api/lead` и шлёт сообщение ботом в ваш Telegram. Позже на VPS меняется только URL в `assets/js/lead-form.js`.

## 1. Создать бота

1. Откройте [@BotFather](https://t.me/BotFather) → `/newbot`
2. Имя и username на ваш вкус (например `IlaiMetalLeadsBot`)
3. Сохраните **token** вида `123456:ABC...` — никому не отправляйте и не коммитьте в git

## 2. Узнать chat_id

1. Напишите боту любое сообщение (например «привет»)
2. В браузере откройте (подставьте token):

```
https://api.telegram.org/bot<TOKEN>/getUpdates
```

3. В JSON найдите `"chat":{"id": 123456789` — это ваш **chat_id** (число, может быть отрицательным для группы)

Заявки будут приходить **в этот чат** (личка с ботом или группа, куда добавлен бот).

## 3. Cloudflare + деплой Worker

```bash
cd workers/lead-telegram
npm install
npx wrangler login
npx wrangler secret put TELEGRAM_BOT_TOKEN
# вставьте token
npx wrangler secret put TELEGRAM_CHAT_ID
# вставьте chat_id
npx wrangler deploy
```

В конце деплоя будет URL вида:

```
https://lead-telegram.<ваш-subdomain>.workers.dev
```

## 4. Подключить сайт

В [`assets/js/lead-form.js`](../assets/js/lead-form.js) задайте:

```js
var LEAD_API_URL = 'https://lead-telegram.<ваш-subdomain>.workers.dev/api/lead';
```

Закоммитьте и задеплойте Pages (push в `main`).

## 5. Проверка

1. Откройте сайт → форма 3D-примерки → отправьте тестовую заявку
2. В Telegram должно прийти сообщение от бота
3. Браузер уйдёт на `/thanks/`

Если `LEAD_API_URL` пустой или Worker недоступен — сработает запасной deep-link в `t.me/Cenzyk`.

## Перенос на VPS позже

Тот же контракт: `POST` JSON на `/api/lead`, ответ `{ "ok": true }`.  
На VPS поднимите тот же код (Node/nginx) и смените `LEAD_API_URL` на `https://илай-металл.рф/api/lead`.
