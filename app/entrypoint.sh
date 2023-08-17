#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    # если база еще не запущена
    echo "БД еще не запущена..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "Все гуд..."
fi
# Удаляем все старые данные
python manage.py flush --no-input
# Выполняем миграции
python manage.py migrate

exec "$@"