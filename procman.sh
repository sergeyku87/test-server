#!/data/data/com.termux/files/usr/bin/bash

# --- Конфигурация ---
PROJECT_DIR="$HOME/www/test-server"
PIDFILE_GUNICORN="$PROJECT_DIR/gunicorn.pid"
PIDFILE_NGINX="$PROJECT_DIR/nginx.pid"
LOG_DIR="$PROJECT_DIR/logs"

# Создаем папку для логов
mkdir -p $LOG_DIR

start() {
    echo "Запуск сервисов..."
    
    # 1. Запуск Gunicorn
    # Проверяем, запущен ли уже процесс по PID файлу
    if [ -f $PIDFILE_GUNICORN ] && kill -0 $(cat $PIDFILE_GUNICORN) 2>/dev/null; then
        echo "Gunicorn уже запущен"
    else
        echo "Запуск Gunicorn..."
        # Используем системный gunicorn напрямую
        gunicorn \
            --bind 127.0.0.1:8000 \
            --workers 2 \
            --threads 2 \
            --pid $PIDFILE_GUNICORN \
            --daemon \
            --access-logfile $LOG_DIR/gunicorn_access.log \
            --error-logfile $LOG_DIR/gunicorn_error.log \
            --chdir $PROJECT_DIR \
            config.wsgi:application
    fi

    # 2. Запуск Nginx
    if [ -f $PIDFILE_NGINX ] && kill -0 $(cat $PIDFILE_NGINX) 2>/dev/null; then
        echo "Nginx уже запущен"
    else
        echo "Запуск Nginx..."
        # Запускаем nginx с явным указанием конфига
        nginx -c $PREFIX/etc/nginx/nginx.conf
        
        # Сохраняем PID мастер-процесса nginx
        pgrep -f "nginx: master" > $PIDFILE_NGINX
    fi
    
    echo "Сервисы запущены."
}

stop() {
    echo "Остановка сервисов..."
    
    # Остановка Nginx
    if [ -f $PIDFILE_NGINX ]; then
        kill $(cat $PIDFILE_NGINX) 2>/dev/null
        rm -f $PIDFILE_NGINX
        echo "Nginx остановлен"
    else
        pkill -f "nginx: master"
        echo "Nginx остановлен (через pkill)"
    fi
    
    # Остановка Gunicorn
    if [ -f $PIDFILE_GUNICORN ]; then
        kill $(cat $PIDFILE_GUNICORN) 2>/dev/null
        rm -f $PIDFILE_GUNICORN
        echo "Gunicorn остановлен"
    else
        pkill -f "gunicorn"
        echo "Gunicorn остановлен (через pkill)"
    fi
    
    echo "Сервисы остановлены."
}

restart() {
    echo "Перезапуск сервисов..."
    stop
    sleep 2
    start
}

status() {
    echo "--- Статус сервисов ---"
    if pgrep -f "gunicorn" > /dev/null; then
        echo "Gunicorn: [RUNNING] (PID: $(pgrep -f 'gunicorn' | head -1))"
    else
        echo "Gunicorn: [STOPPED]"
    fi
    
    if pgrep -f "nginx: master" > /dev/null; then
        echo "Nginx: [RUNNING] (PID: $(pgrep -f 'nginx: master' | head -1))"
    else
        echo "Nginx: [STOPPED]"
    fi
}

# Обработка аргументов командной строки
case "$1" in
    start) start ;;
    stop) stop ;;
    restart) restart ;;
    status) status ;;
    *) 
        echo "Использование: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
