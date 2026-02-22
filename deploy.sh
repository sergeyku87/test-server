#!/data/data/com.termux/files/usr/bin/bash

# --- Конфигурация ---
PROJECT_DIR="$HOME/www/test-server"
PYTHON="python"        # Системный python
PIP="pip"              # Системный pip
MANAGE="$PROJECT_DIR/manage.py"
LOG_FILE="$PROJECT_DIR/deploy.log"

# --- Функции ---
log() {
    echo "[$(date +'%F %T')] $1" | tee -a $LOG_FILE
}

# --- Начало ---
cd $PROJECT_DIR
log "=== Начало деплоя ==="

# 1. Проверка изменений в Git
log "Проверка обновлений Git..."
git fetch origin

# Получаем текущий коммит и коммит в репозитории
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse @{u})

if [ "$LOCAL" != "$REMOTE" ]; then
    log "Обнаружены изменения. Начинаем обновление..."
    
    # 2. Pull изменений
    git pull origin main || git pull origin master
    if [ $? -ne 0 ]; then
        log "ОШИБКА: Не удалось сделать git pull"
        exit 1
    fi

    # 3. Обновление зависимостей
    if [ -f "requirements.txt" ]; then
        log "Установка зависимостей..."
        $PIP install --upgrade pip
        $PIP install -r requirements.txt
    else
        log "requirements.txt не найден, пропускаем установку зависимостей"
    fi

    # 4. Миграции БД
    log "Выполнение миграций..."
    $PYTHON $MANAGE migrate --noinput

    # 5. Сборка статики
    log "Сборка статических файлов..."
    $PYTHON $MANAGE collectstatic --noinput

    # 6. Перезапуск сервисов
    log "Перезапуск Gunicorn и Nginx..."
    ./procman.sh restart
    
    log "Деплой успешно завершен!"
else
    log "Изменений не обнаружено. Версия актуальна."
fi

log "=== Конец деплоя ==="
