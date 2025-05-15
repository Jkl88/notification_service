# 📨 Сервис уведомлений на FastAPI

Этот проект — простой backend для системы уведомлений. 😎

---

## ⚙️ Что реализовано в этом проекте

- ✅ Регистрация пользователей
- 🔑 Авторизация (JWT access и refresh токены)
- 📩 Создание уведомлений
- 📬 Получение уведомлений с кешированием через Redis
- ❌ Удаление уведомлений
- 🐘 PostgreSQL для хранения данных
- 🐳 Docker-сборка

---

## 🛠 Как всё работает

### Авторизация

JWT-токены:
- `access_token` — для запросов
- `refresh_token` — чтобы получить новый access

Хранятся в `Authorization: Bearer <token>`

### Redis

Для ускорения ответов:
- Когда запрашиваются уведомления, сначала смотрится в Redis
- Если нет — берётся из БД и кешируется

---

## 📬 Основные эндпоинты

### 🔐 Авторизация

**POST /auth/register** — регистрация  
Пример:
```json
{
  "username": "user",
  "password": "123456"
}
```

**POST /auth/login** — вход  
Формат: `application/x-www-form-urlencoded`  
Пример:
```
username=user&password=123456
```

**POST /auth/refresh** — обновление токена  
Требуется `Authorization: Bearer <refresh_token>`

---

### 🔔 Уведомления

**POST /notifications/** — создать уведомление  
Требует авторизацию  
```json
{
  "type": "like",
  "text": "str"
}
```

**GET /notifications/** — получить список  
Параметры:
- `limit`: сколько записей (по умолчанию 10)
- `offset`: откуда начинать (по умолчанию 0)

**DELETE /notifications/{id}** — удалить уведомление  
Только если пользователь — владелец уведомления

---

## ▶️ Как запустить

1. Установить Docker
2. Клонировать проект и перейти:
   ```bash
   git clone https://github.com/your/repo.git
   cd notification_service
   ```
3. Создать `.env`
4. Запустить:
   ```bash
   docker-compose up --build
   ```

---

Спасибо, что заглянули 👋
