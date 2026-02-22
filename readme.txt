# 📱 Django Server on Termux & Docker

Полноценный веб-сервер на базе Django с поддержкой двух режимов развертывания:
1. **Native Termux** — для запуска на Android-устройствах
2. **Docker Compose** — для развертывания на любых серверах (VPS, локально, cloud)

---

## 📋 Оглавление

- [О проекте](#о-проекте)
- [Архитектура](#архитектура)
- [Требования](#требования)
- [Быстрый старт](#быстрый-старт)
- [Установка на Termux](#установка-на-termux)
- [Установка через Docker](#установка-через-docker)
- [Конфигурация](#конфигурация)
- [Управление сервером](#управление-сервером)
- [Деплой и CI/CD](#деплой-и-cicd)
- [Безопасность](#безопасность)
- [Структура проекта](#структура-проекта)
- [Troubleshooting](#troubleshooting)
- [Лицензия](#лицензия)

---

## 🎯 О проекте

Этот проект предоставляет готовую инфраструктуру для запуска Django-приложений на:
- 📱 **Android-устройствах** через Termux (идеально для тестирования, домашних серверов, IoT)
- 🖥️ **Любых серверах** через Docker Compose (production, VPS, cloud)

**Особенности:**
- ✅ Автоматический деплой через Git
- ✅ Nginx + Gunicorn в production-конфигурации
- ✅ SSH-доступ для удаленного управления
- ✅ Единая кодовая база для обоих режимов
- ✅ Минимальные требования к ресурсам

---

## 🏗 Архитектура

### Termux (Native)
```
┌─────────────────────────────────────────────────────────────────┐
│                         БРАУЗЕР                                 │
│                    (http://IP:8080)                             │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                         NGINX                                   │
│                    (порт 8080, reverse proxy)                   │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                        GUNICORN                                 │
│                    (порт 8000, WSGI)                            │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DJANGO                                   │
│                    + SQLite/PostgreSQL                          │
└─────────────────────────────────────────────────────────────────┘
```

### Docker Compose
```
┌─────────────────────────────────────────────────────────────────┐
│                         БРАУЗЕР                                 │
│                    (http://IP:80)                               │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    NGINX (Container)                            │
│                    (порт 80/443)                                │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   GUNICORN (Container)                          │
│                    (порт 8000)                                  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│               DJANGO + PostgreSQL (Container)                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Требования

### Для Termux
| Компонент | Версия | Примечание |
|-----------|--------|------------|
| Android | 7.0+ | Чем новее, тем лучше |
| Termux | Latest | **Только из F-Droid или GitHub** |
| Python | 3.10+ | Устанавливается через pkg |
| Свободное место | 500 MB+ | Для проекта и зависимостей |

### Для Docker
| Компонент | Версия | Примечание |
|-----------|--------|------------|
| Docker | 20.10+ | Docker Engine или Desktop |
| Docker Compose | 2.0+ | Включен в Docker Desktop |
| RAM | 512 MB+ | Минимум для контейнеров |
| CPU | 1 ядро+ | Рекомендуется 2+ ядра |

---

## 🚀 Быстрый старт

### Termux (5 минут)
```bash
# 1. Клонировать репозиторий
git clone https://github.com/username/repo.git ~/www/myproject
cd ~/www/myproject

# 2. Запустить установку
./scripts/setup_termux.sh

# 3. Запустить сервер
./procman.sh start

# 4. Открыть в браузере
# http://<IP_ТЕЛЕФОНА>:8080
```

### Docker (2 минуты)
```bash
# 1. Клонировать репозиторий
git clone https://github.com/username/repo.git
cd repo

# 2. Запустить контейнеры
docker-compose up -d

# 3. Открыть в браузере
# http://localhost:80
```

---

## 📱 Установка на Termux

### Шаг 1: Установка Termux

⚠️ **ВАЖНО:** Не устанавливайте Termux из Google Play!

| Источник | Ссылка |
|----------|--------|
| **F-Droid** (рекомендуется) | [termux.dev/f-droid](https://f-droid.org/packages/com.termux/) |
| **GitHub Releases** | [github.com/termux/termux-app](https://github.com/termux/termux-app/releases) |

### Шаг 2: Базовая настройка Termux

```bash
# Обновить пакеты
pkg update && pkg upgrade

# Выбрать зеркало (если есть ошибки)
termux-change-repo

# Установить зависимости
pkg install python nginx git openssh clang libjpeg-turbo libwebp zlib

# Дать доступ к хранилищу (опционально)
termux-setup-storage
```

### Шаг 3: Установка проекта

```bash
# Создать папку для проекта
mkdir -p ~/www/myproject
cd ~/www/myproject

# Клонировать репозиторий
git clone https://github.com/username/repo.git .

# Или инициализировать новый проект
git init
```

### Шаг 4: Настройка окружения

```bash
# Создать файл переменных окружения
cp .env.example .env
nano .env

# Отредактировать значения:
# SECRET_KEY=your-secret-key
# DEBUG=False
# ALLOWED_HOSTS=127.0.0.1,localhost,<IP_ТЕЛЕФОНА>
```

### Шаг 5: Установка зависимостей Python

```bash
# Установить зависимости
pip install -r requirements.txt

# Применить миграции
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Собрать статику
python manage.py collectstatic --noinput
```

### Шаг 6: Настройка SSH (для удаленного доступа)

```bash
# Установить пароль
passwd

# Запустить SSH сервер
sshd

# Проверить IP телефона
ifconfig
# Ищите wlan0 -> inet (например, 192.168.1.55)
```

**Подключение с компьютера:**
```bash
ssh -p 8022 u0_a123@192.168.1.55
```

### Шаг 7: Настройка Nginx

```bash
# Отредактировать конфиг
nano $PREFIX/etc/nginx/nginx.conf

# Проверить конфиг
nginx -t
```

### Шаг 8: Первый запуск

```bash
# Запустить сервисы
./procman.sh start

# Проверить статус
./procman.sh status

# Посмотреть логи
tail -f logs/gunicorn_access.log
```

---

## 🐳 Установка через Docker

### Шаг 1: Подготовка

```bash
# Клонировать репозиторий
git clone https://github.com/username/repo.git
cd repo

# Создать файл окружения
cp .env.example .env
nano .env
```

### Шаг 2: Настройка Docker Compose

Отредактируйте `docker-compose.yml` при необходимости:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    environment:
      - DATABASE_URL=postgres://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=${DEBUG}
    depends_on:
      - db

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### Шаг 3: Запуск контейнеров

```bash
# Сборка и запуск
docker-compose up -d --build

# Применить миграции
docker-compose exec web python manage.py migrate

# Создать суперпользователя
docker-compose exec web python manage.py createsuperuser

# Собрать статику
docker-compose exec web python manage.py collectstatic --noinput
```

### Шаг 4: Управление контейнерами

```bash
# Просмотр логов
docker-compose logs -f web
docker-compose logs -f nginx

# Остановка
docker-compose down

# Перезапуск
docker-compose restart

# Обновление
docker-compose pull
docker-compose up -d --build
```

---

## ⚙️ Конфигурация

### Переменные окружения (.env)

```bash
# ─────────────────────────────────────────────────────────────
# Django
# ─────────────────────────────────────────────────────────────
SECRET_KEY=your-super-secret-key-change-in-production
DEBUG=False
ALLOWED_HOSTS=127.0.0.1,localhost,192.168.1.55

# ─────────────────────────────────────────────────────────────
# База данных
# ─────────────────────────────────────────────────────────────
# Для Termux (SQLite)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Для Docker (PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=myproject
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=db
DB_PORT=5432

# ─────────────────────────────────────────────────────────────
# Email (опционально)
# ─────────────────────────────────────────────────────────────
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

# ─────────────────────────────────────────────────────────────
# Termux специфичные
# ─────────────────────────────────────────────────────────────
TERMUX_MODE=True
SSH_PORT=8022
WEB_PORT=8080
```

### Настройки Django (settings.py)

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# База данных
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT', ''),
    }
}

# Статические файлы
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Медиа файлы
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

---

## 🎛 Управление сервером

### Termux Scripts

| Команда | Описание |
|---------|----------|
| `./procman.sh start` | Запустить Gunicorn + Nginx |
| `./procman.sh stop` | Остановить все сервисы |
| `./procman.sh restart` | Перезапустить сервисы |
| `./procman.sh status` | Проверить статус сервисов |
| `./deploy.sh` | Автоматический деплой из Git |
| `./scripts/backup.sh` | Создать бэкап БД и медиа |

### Docker Commands

| Команда | Описание |
|---------|----------|
| `docker-compose up -d` | Запустить контейнеры |
| `docker-compose down` | Остановить контейнеры |
| `docker-compose logs -f` | Просмотр логов |
| `docker-compose exec web bash` | Войти в контейнер web |
| `docker-compose restart web` | Перезапустить web |

---

## 🚀 Деплой и CI/CD

### Автоматический деплой (Termux)

```bash
# Подключиться по SSH и запустить деплой
ssh -p 8022 user@<IP_ТЕЛЕФОНА> 'cd ~/www/myproject && ./deploy.sh'

# Или одной командой с компьютера
./scripts/deploy_remote.sh
```

### Деплой через Git Hook (автоматически)

```bash
# На сервере создать hook
nano .git/hooks/post-receive

# Вставить:
#!/bin/bash
cd ~/www/myproject || exit
git reset --hard HEAD
./deploy.sh

# Сделать исполняемым
chmod +x .git/hooks/post-receive
```

### Docker: Обновление образа

```bash
# Pull новых образов
docker-compose pull

# Пересоздать контейнеры
docker-compose up -d --build

# Применить миграции
docker-compose exec web python manage.py migrate

# Собрать статику
docker-compose exec web python manage.py collectstatic --noinput
```

---

## 🔒 Безопасность

### Рекомендации для Production

| Аспект | Рекомендация |
|--------|--------------|
| **DEBUG** | Всегда `False` в продакшене |
| **SECRET_KEY** | Генерировать уникальный для каждого окружения |
| **ALLOWED_HOSTS** | Указывать конкретные домены/IP |
| **HTTPS** | Использовать Let's Encrypt через Nginx |
| **SSH** | Использовать ключи вместо паролей |
| **Бэкапы** | Регулярно бэкапить БД и медиа |
| **Обновления** | Следить за обновлениями Django и пакетов |

### Генерация SECRET_KEY

```bash
# Python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# OpenSSL
openssl rand -base64 50
```

### Настройка SSH ключей

```bash
# На компьютере сгенерировать ключ
ssh-keygen -t ed25519

# Копировать публичный ключ на сервер
ssh-copy-id -p 8022 user@<IP_ТЕЛЕФОНА>

# Или вручную
cat ~/.ssh/id_ed25519.pub | ssh -p 8022 user@<IP> "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

### Firewall (для Docker/VPS)

```bash
# Разрешить только необходимые порты
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable
```

---

## 📁 Структура проекта

```
myproject/
├── config/                    # Настройки Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── apps/                      # Django приложения
│   ├── blog/
│   ├── shop/
│   └── users/
│
├── static/                    # Исходная статика (разработка)
│   ├── css/
│   ├── js/
│   └── images/
│
├── staticfiles/               # Собранная статика (production)
│   └── ...
│
├── media/                     # Загрузки пользователей
│   └── uploads/
│
├── logs/                      # Логи приложения
│   ├── gunicorn_access.log
│   ├── gunicorn_error.log
│   └── deploy.log
│
├── scripts/                   # Вспомогательные скрипты
│   ├── setup_termux.sh
│   ├── backup.sh
│   └── deploy_remote.sh
│
├── templates/                 # HTML шаблоны
│   ├── base.html
│   └── includes/
│
├── .env                       # Переменные окружения
├── .env.example               # Шаблон переменных
├── .gitignore                 # Игнорируемые файлы
├── requirements.txt           # Python зависимости
├── requirements-dev.txt       # Зависимости для разработки
├── manage.py                  # Утилита Django
│
├── procman.sh                 # Управление процессами (Termux)
├── deploy.sh                  # Скрипт деплоя (Termux)
│
├── docker-compose.yml         # Docker Compose конфигурация
├── Dockerfile                 # Docker образ
├── nginx/
│   └── nginx.conf             # Nginx конфигурация
│
└── README.md                  # Этот файл
```

---

## 🔧 Troubleshooting

### Termux

| Проблема | Решение |
|----------|---------|
| **pkg update ошибка** | `termux-change-repo` — сменить зеркало |
| **Permission denied** | `chmod +x *.sh` — сделать скрипты исполняемыми |
| **Порт занят** | `pkill -f gunicorn` — убить зависшие процессы |
| **Сервер отключается** | Включить "Без ограничений" в настройках батареи Termux |
| **SSH не подключается** | Проверить `sshd` запущен, порт 8022, firewall |
| **Nginx не запускается** | `nginx -t` — проверить конфиг, пути к логам |

### Docker

| Проблема | Решение |
|----------|---------|
| **Контейнер не стартует** | `docker-compose logs web` — посмотреть логи |
| **Migration failed** | `docker-compose down -v` — удалить volumes и начать заново |
| **Static 404** | `docker-compose exec web python manage.py collectstatic` |
| **Database connection** | Проверить переменные окружения в .env |
| **Port already in use** | Изменить порт в docker-compose.yml |

### Общие

```bash
# Проверить что слушает порты
netstat -tlnp | grep 8000
netstat -tlnp | grep 8080

# Проверить процессы
ps aux | grep python
ps aux | grep nginx

# Проверить логи
tail -f logs/gunicorn_error.log
tail -f $PREFIX/var/log/nginx/error.log  # Termux
docker-compose logs -f nginx             # Docker
```

---

## 📊 Сравнение режимов развертывания

| Характеристика | Termux | Docker Compose |
|----------------|--------|----------------|
| **Целевая платформа** | Android | Любая (Linux, macOS, Windows) |
| **Требования к ресурсам** | Минимальные | Средние |
| **Сложность настройки** | Средняя | Низкая |
| **Масштабируемость** | Ограничена | Высокая |
| **База данных** | SQLite (рекомендуется) | PostgreSQL |
| **Порт веб-сервера** | 8080 | 80/443 |
| **Порт SSH** | 8022 | 22 (стандартный) |
| **Автозапуск** | Через .termux/boot.sh | Docker restart policy |
| **Бэкапы** | Ручные/скрипты | Docker volumes |
| **Рекомендуемое использование** | Тестирование, домашний сервер, IoT | Production, VPS, Cloud |

---

## 📝 Лицензия

MIT License — свободное использование, модификация и распространение.

---

## 🤝 Contributing

1. Fork репозиторий
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

---

## 📞 Контакты

- **GitHub:** [github.com/username](https://github.com/username)
- **Email:** your-email@example.com
- **Telegram:** @yourusername

---

## 🙏 Благодарности

- [Termux](https://termux.dev/) — потрясающий терминал для Android
- [Django](https://www.djangoproject.com/) — веб-фреймворк для перфекционистов
- [Gunicorn](https://gunicorn.org/) — WSGI сервер
- [Nginx](https://nginx.org/) — веб-сервер и reverse proxy

---

**Made with ❤️ for Android & Docker enthusiasts**

*Последнее обновление: Февраль 2026*
