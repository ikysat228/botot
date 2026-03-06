# GPT Telegram Bot for Replit

## Опис
Цей бот працює з Telegram та OpenAI (GitHub Models). Підходить для хостингу на Replit та деплою на GitHub.

## Запуск на Replit
1. Додайте файли gpt.py та requirements.txt у репозиторій.
2. У Replit додайте змінні середовища:
   - `TELEGRAM_TOKEN` — токен вашого Telegram-бота
   - `GITHUB_TOKEN` — токен для доступу до GitHub Models (або OpenAI)
3. Встановіть залежності:
   - В Replit це робиться автоматично, або виконайте:  
     `pip install -r requirements.txt`
4. Запустіть файл gpt.py:
   - В Replit натисніть Run, або в терміналі:  
     `python gpt.py`

## Важливо
- Не зберігайте токени у відкритому коді!
- Для деплою на GitHub додайте ці файли у репозиторій та пуште у потрібну гілку.
