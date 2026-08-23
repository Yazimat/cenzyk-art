# lead-telegram (Cloudflare Worker)

Принимает `POST /api/lead` с сайта и шлёт заявку в Telegram.

Полная инструкция: [docs/TELEGRAM-LEADS.md](../../docs/TELEGRAM-LEADS.md)

```bash
npm install
npx wrangler secret put TELEGRAM_BOT_TOKEN
npx wrangler secret put TELEGRAM_CHAT_ID
npx wrangler deploy
```
