# Решение проблемы RECAPTCHA_CHECK при авторизации

**Дата:** 2025-11-14
**Ошибка:** `RPCError 403: RECAPTCHA_CHECK_signup__6LdcRsEqAAAAAHUaNCc1GUe47g5jKlOzbJJiyIZt`

---

## Причина проблемы

Telegram заблокировал попытки получения SMS-кода из-за обнаружения автоматизации или подозрительной активности:
- Множественные попытки авторизации
- Подозрительный IP адрес
- Защита от ботов

**ВАЖНО:** Это НЕ связано с device fingerprints! Это ограничение Telegram API.

---

## ❌ Что НЕ работает

- Telegram API не поддерживает автоматическое прохождение CAPTCHA
- Telethon не может обойти эту защиту
- Нельзя решить программно

---

## ✅ Решения (в порядке эффективности)

### 1. Авторизация через Telegram Desktop (РЕКОМЕНДУЕТСЯ)

Этот метод работает лучше всего, так как вы пройдете CAPTCHA через официальное приложение:

**Шаги:**

1. **Скачайте Telegram Desktop**
   - Официальный сайт: https://desktop.telegram.org/

2. **Авторизуйтесь с вашим номером**
   - Введите номер телефона
   - Пройдите CAPTCHA (если требуется)
   - Введите SMS-код
   - Войдите в аккаунт

3. **Скопируйте session файл**

   **На macOS:**
   ```bash
   # Telegram Desktop session файлы:
   ~/Library/Application Support/Telegram Desktop/tdata/

   # Найдите файлы с именем вашего аккаунта и скопируйте в:
   app_data/sessions/
   ```

   **На Linux:**
   ```bash
   ~/.local/share/TelegramDesktop/tdata/
   ```

   **На Windows:**
   ```
   %APPDATA%\Telegram Desktop\tdata\
   ```

4. **Укажите путь к session при добавлении аккаунта**
   - В программе при добавлении аккаунта укажите путь к скопированному session файлу

### 2. Использовать Telethon для первичной авторизации с retry

Попробуйте авторизоваться через официальный скрипт Telethon с паузами:

```python
# scripts/manual_authorize.py
import asyncio
from telethon import TelegramClient

async def authorize():
    # Ваши API credentials
    api_id = "YOUR_API_ID"
    api_hash = "YOUR_API_HASH"
    phone = "+7XXXXXXXXXX"

    client = TelegramClient(f"app_data/sessions/session_{phone}", api_id, api_hash)

    await client.start(phone=phone)
    print("✅ Авторизация успешна!")
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(authorize())
```

Запустите:
```bash
venv/bin/python scripts/manual_authorize.py
```

### 3. Подождать 2-24 часа

- Telegram может снять блокировку автоматически
- НЕ делайте повторные попытки!
- После перерыва попробуйте снова

### 4. Сменить IP адрес

**Варианты:**
- Перезагрузите роутер для получения нового IP
- Используйте качественный VPN (платный, не Datacenter IP):
  - ExpressVPN
  - NordVPN
  - Private Internet Access
- Используйте мобильный интернет (4G/5G вместо Wi-Fi)
- Попробуйте с другой сети (дом → работа → кафе)

### 5. Использовать прокси с хорошей репутацией

Если вы используете прокси, убедитесь что:
- Это не Datacenter IP
- Это не публичный прокси
- IP не в blacklist Telegram

**Проверить IP:**
```bash
curl https://ipinfo.io
# Убедитесь что "org" не содержит "Datacenter", "VPS", "Hosting"
```

### 6. Авторизация через web.telegram.org

1. Откройте https://web.telegram.org/
2. Введите номер телефона
3. Пройдите CAPTCHA
4. После успешной авторизации попробуйте снова через программу

---

## Что делать СЕЙЧАС

### Шаг 1: Не добавляйте новые аккаунты
- Подождите минимум 2-6 часов
- Используйте уже работающие аккаунты

### Шаг 2: Используйте рабочие аккаунты
У вас есть 2 авторизованных аккаунта:
```
+79879531873 - ONLINE ✅
+79874410793 - ONLINE ✅
```

### Шаг 3: Для новых аккаунтов
- Попробуйте Вариант 1 (Telegram Desktop) - САМЫЙ НАДЕЖНЫЙ
- Или дождитесь снятия блокировки (2-24 часа)
- Не делайте повторные попытки!

---

## Проверка IP адреса

Проверьте ваш текущий IP:
```bash
# Проверить IP и его репутацию
curl https://ipinfo.io

# Проверить не в blacklist ли
curl https://blackbox.ipinfo.app/lookup/$(curl -s https://api.ipify.org)
```

Если показывает "Datacenter", "Hosting", "VPS" - это плохо для Telegram.

---

## Дополнительные рекомендации

### Безопасная стратегия добавления аккаунтов:

1. **Не добавляйте много аккаунтов сразу**
   - Максимум 1-2 аккаунта в день
   - Делайте паузы между попытками (минимум 1 час)

2. **Используйте разные IP для разных аккаунтов**
   - Каждый аккаунт = свой прокси
   - Или добавляйте из разных сетей

3. **Авторизуйтесь через официальные приложения сначала**
   - Telegram Desktop
   - Telegram Web
   - Потом импортируйте session

4. **Не используйте виртуальные номера**
   - Telegram блокирует сервисы типа sms-activate
   - Используйте реальные SIM-карты

---

## Техническая информация

**Код ошибки:** 403 RECAPTCHA_CHECK_signup
**Место возникновения:** `app/gui/widgets/account_widget.py:269`
**Метод:** `client.send_code_request(phone_number)`

**Лог ошибки:**
```
2025-11-14 21:29:21 - Async authorization error: RPCError 403:
RECAPTCHA_CHECK_signup__6LdcRsEqAAAAAHUaNCc1GUe47g5jKlOzbJJiyIZt
(caused by SendCodeRequest)
```

---

## FAQ

**Q: Можно ли обойти CAPTCHA программно?**
A: Нет. Telegram API не поддерживает это. Только ручное прохождение.

**Q: Поможет ли смена device fingerprint?**
A: Нет. Проблема не в fingerprint, а в IP/rate limiting.

**Q: Сколько ждать?**
A: От 2 до 24 часов. В крайнем случае - до 7 дней.

**Q: Можно ли использовать 2captcha/anticaptcha?**
A: Нет. CAPTCHA проверяется на стороне Telegram, API не предоставляет доступа.

**Q: Что если блокировка не снимется?**
A: Используйте Вариант 1 (Telegram Desktop) - он всегда работает.

---

## Полезные ссылки

- Telegram Desktop: https://desktop.telegram.org/
- Telethon документация: https://docs.telethon.dev/
- Проверка IP: https://ipinfo.io/
- Telegram Web: https://web.telegram.org/

---

**Статус:** Проблема идентифицирована. Ждите или используйте Telegram Desktop для авторизации.
