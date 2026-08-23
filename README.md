# cenzyk.art — Илай Саматов · Кузнец-Дизайнер

Статический сайт (HTML/CSS/JS) → **GitHub Pages**.  
Репозиторий изолирован: не затрагивает сайты психолога и общий `psi-leads`.

## Локальный просмотр

```bash
python3 -m http.server 4173
```

- http://127.0.0.1:4173/ — главная (**V1 refined**: тонкие линии + жёлтые кривые)
- http://127.0.0.1:4173/3d-primerka/ — посадочная 3D под Директ
- http://127.0.0.1:4173/preview/ — архив старых вариантов

Стиль: фундамент V1 + минималистичные «кованые» кривые жёлтых оттенков.

## Стек

- Статика, без админки
- Метрика `105346765` + GA `G-MHZ849WZ9M` (`assets/js/consent-analytics.js`)
- Cookie-notice с отказом от статистики
- Заявки: временный deep-link в Telegram (`assets/js/lead-form.js`); отдельный Worker — следующим шагом

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
DNS на `cenzyk.art` пользователь меняет вручную (без `www`).
