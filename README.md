На основе предоставленной информации, я подготовлю подробное описание и документацию для вашего микросервисного проекта новостной платформы. Вот детализированное содержание документации, охватывающее каждый аспект проекта и объясняющее его работу для вашего потенциального работодателя.

---

## Документация для проекта "Микросервисная новостная платформа"

### 1. Общая информация о проекте

**Название проекта:** Микросервисная новостная платформа

**Цель проекта:** 
Создание платформы, где пользователи могут регистрироваться, публиковать новости, редактировать и удалять их, а также просматривать новости других пользователей. Платформа включает базовые функции социальной сети и имеет инфраструктуру для хранения и обработки данных о пользователях и новостях.

**Описание функциональности:**
Проект представляет собой пет-проект для практики в разработке микросервисной архитектуры. Пользователи могут:
- Зарегистрироваться с подтверждением через электронную почту или SMS.
- Авторизоваться с использованием JWT токенов.
- Создавать, редактировать и удалять свои новости.
- Просматривать ленту новостей с указанием авторства.

---

### 2. Архитектура проекта

Проект разделен на два основных микросервиса, которые взаимодействуют друг с другом через gRPC:

#### 2.1. Микросервис пользователей
- **Фреймворк:** Django Rest Framework (DRF)
- **Функциональность:**
  - Регистрация пользователя с подтверждением через SMS или email.
  - Авторизация через JWT токены.
  - Управление профилем пользователя (смена пароля, подтверждение учетной записи и т.д.).
  - Поддержка уровней доступа (администраторы, сотрудники, пользователи).
  - Отправка уведомлений по email через Celery.
  - Хранение данных в PostgreSQL.

#### 2.2. Микросервис новостей
- **Фреймворк:** FastAPI
- **Функциональность:**
  - Создание, редактирование и удаление новостей.
  - Отображение новостей с привязкой к пользователям, идентифицированным через микросервис пользователей.
  - Получение информации о пользователе через gRPC при создании или изменении новостей.
  - Хранение данных в PostgreSQL (хранится ID пользователя для указания авторства).

#### Взаимодействие между микросервисами
- **gRPC:** 
  - На стороне DRF-сервиса реализован gRPC сервер, предоставляющий информацию о пользователе.
  - FastAPI-сервис содержит gRPC клиент, который обращается к серверу для получения данных о пользователе. Используется для проверки авторизации и получения информации о пользователе, создающем новость.

---

### 3. Используемые технологии и стек

- **Бэкенд:**
  - Django Rest Framework для сервиса пользователей.
  - FastAPI для сервиса новостей.
  - Celery для отправки email-сообщений.
  - JWT для аутентификации.
  
- **Базы данных:**
  - PostgreSQL для каждого микросервиса (отдельные базы данных для пользователей и новостей).

---

### 4. Основные пользовательские сценарии и API

#### 4.1. Пользовательский сценарий
1. **Регистрация:** Пользователь регистрируется с указанием email или номера телефона. Выбранный метод используется для подтверждения личности (отправляется код).
2. **Подтверждение:** Пользователь получает код по SMS или email, который вводит для завершения регистрации.
3. **Авторизация:** После подтверждения личности пользователь может авторизоваться, получив JWT токен.
4. **Создание новости:** Авторизованный пользователь может создать новость, введя текст и, при необходимости, загрузив медиа-файлы. Сервис новостей отправляет JWT токен через gRPC в сервис пользователей для проверки токена и получения ID пользователя.
5. **Отображение новости:** Новости отображаются с указанием авторства на основе данных, полученных от сервиса пользователей.

#### 4.2. API методы

##### Микросервис пользователей (DRF)
- `POST /register`: регистрация пользователя с отправкой кода на подтверждение.
- `POST /confirm`: подтверждение кода для завершения регистрации.
- `POST /login`: авторизация с выдачей JWT токена.
- `POST /reset-password`: сброс пароля.
- **Swagger:** доступен для тестирования всех вышеуказанных эндпоинтов.

##### Микросервис новостей (FastAPI)
- `POST /news`: создание новости.
- `PUT /news/{news_id}`: редактирование новости.
- `DELETE /news/{news_id}`: удаление новости.
- `GET /news`: просмотр всех новостей.
- **Swagger:** отдельный интерфейс для взаимодействия с API новостей.

---

### 5. Аутентификация и авторизация

- **Тип аутентификации:** JWT токены.
- **Подтверждение личности:** через код, отправляемый по email или SMS.
- **Роли пользователей:** Администраторы, сотрудники, обычные пользователи. Роли определяют права доступа к различным действиям в сервисе пользователей.

---

### 6. Логирование и мониторинг

- **Логирование:** 
  - Включено в сервисе пользователей (DRF), записывает действия и ошибки пользователей.
  - В сервисе новостей не реализовано, но планируется для улучшения мониторинга.

---

### 7. Развертывание и переменные окружения

#### Docker и Docker Compose
Проект разворачивается с помощью Docker Compose, где конфигурации для каждого сервиса указаны в едином `docker-compose.yml` файле. Каждому микросервису выделен отдельный контейнер для PostgreSQL, Django и FastAPI.

#### Пример файла переменных окружения
```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=your-database-name
DB_HOST=database-host
DB_USER=database-user
DB_PASS=database-password
REDISHOST=your-redis-host

EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=email-password

SMS_LOGIN=sms-service-login
SMS_PASSWORD=sms-service-password
SMS_SENDER=sms-sender-name
```

---

### Дополнительные сведения

1. **Ограничения и будущие обновления:**
   - В будущем планируется интеграция Redis для кэширования в сервис новостей для оптимизации работы.
   - Планируется добавление логирования и мониторинга в сервис новостей.

2. **Производительность и масштабирование:**
   - Проект разработан с минимальной нагрузкой, однако может быть улучшен для поддержки распределенной архитектуры с использованием брокера сообщений и горизонтального масштабирования через Kubernetes.

--- 

### Заключение
Этот проект был разработан как пет-проект для изучения микросервисной архитектуры. Он представляет собой полноценный пример архитектуры, состоящей из нескольких сервисов, которые могут быть развернуты и масштабированы независимо друг от друга.