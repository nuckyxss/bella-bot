# Telegram Bot Webhook

Ten projekt implementuje webhook dla bota Telegram, który wykorzystuje model AI poprzez OpenRouter do generowania odpowiedzi.

## Wymagania

- Python 3.7+
- Token dla bota Telegram (uzyskany przez BotFather)
- Klucz API OpenRouter

## Instalacja i uruchomienie lokalne

1. Zainstaluj wymagane zależności:

```bash
pip install -r requirements.txt
```

2. Uzupełnij plik `.env` swoimi kluczami API:

```
TELEGRAM_BOT_TOKEN=twój_token_bota_telegram
OPENROUTER_API_KEY=twój_klucz_api_openrouter
```

3. Uruchom lokalnie serwer webhook:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

# Instrukcja wdrożenia na Render.com (krok po kroku)

## 1. Wrzucenie projektu na GitHub

1. Utwórz nowe konto na GitHub (https://github.com/signup) jeśli go jeszcze nie masz
2. Po zalogowaniu, kliknij przycisk "+" w prawym górnym rogu i wybierz "New repository"
3. Nadaj nazwę repozytorium (np. "telegram-bot")
4. Ustaw repozytorium jako publiczne (Public)
5. Kliknij "Create repository"
6. Postępuj zgodnie z instrukcjami, aby przesłać swój kod do GitHub:

```bash
git init
git add .
git commit -m "Pierwszy commit"
git branch -M main
git remote add origin https://github.com/TWOJA_NAZWA_UŻYTKOWNIKA/telegram-bot.git
git push -u origin main
```

## 2. Połączenie z Render.com

1. Utwórz darmowe konto na Render.com (https://render.com)
2. Po zalogowaniu, kliknij przycisk "New +" i wybierz "Web Service"
3. Połącz swoje konto GitHub z Render (kliknij "Connect GitHub")
4. Wybierz utworzone wcześniej repozytorium
5. Skonfiguruj usługę:
   - Nazwa: "telegram-bot" (lub dowolna inna)
   - Region: Wybierz najbliższy region
   - Branch: main
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port 10000`
   - Plan: Free

## 3. Dodanie zmiennych środowiskowych

1. Po utworzeniu usługi, przejdź do panelu zarządzania
2. Kliknij zakładkę "Environment"
3. Dodaj następujące zmienne środowiskowe:
   - Klucz: `TELEGRAM_BOT_TOKEN`, Wartość: twój token bota Telegram
   - Klucz: `OPENROUTER_API_KEY`, Wartość: twój klucz API OpenRouter
4. Kliknij "Save Changes"
5. Poczekaj, aż usługa zostanie ponownie uruchomiona z nowymi zmiennymi

## 4. Ustawienie webhooka w Telegramie

1. Po pomyślnym wdrożeniu, Render przydzieli twojej aplikacji adres URL w formacie:
   `https://twoja-aplikacja.onrender.com`
2. Aby ustawić webhook Telegram, otwórz przeglądarkę i wklej poniższy link (zastępując zmienne swoimi wartościami):

```
https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url=https://twoja-aplikacja.onrender.com/webhook
```

Przykład:
```
https://api.telegram.org/bot123456789:ABCdefGhIJklmNoPQRstUVwxYZ/setWebhook?url=https://telegram-bot-xyzw.onrender.com/webhook
```

3. Powinieneś otrzymać odpowiedź JSON potwierdzającą poprawne ustawienie webhooka

## 5. Konfiguracja UptimeRobot (aby bot działał 24/7)

Render może wyłączać darmowe aplikacje po okresie nieaktywności. Aby temu zapobiec:

1. Utwórz darmowe konto na UptimeRobot (https://uptimerobot.com/signup)
2. Po zalogowaniu kliknij "+ Add New Monitor"
3. Skonfiguruj monitor:
   - Monitor Type: HTTP(s)
   - Friendly Name: "Telegram Bot Ping"
   - URL: `https://twoja-aplikacja.onrender.com/ping`
   - Monitoring Interval: Every 5 minutes
4. Kliknij "Create Monitor"

Ten monitor będzie "budzić" twoją aplikację co 5 minut, zapobiegając jej uśpieniu przez Render.

## Sprawdzenie statusu webhooka

Aby sprawdzić, czy webhook został poprawnie ustawiony:

```
https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getWebhookInfo
```

## Usunięcie webhooka

Aby usunąć webhook:

```
https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook
```
