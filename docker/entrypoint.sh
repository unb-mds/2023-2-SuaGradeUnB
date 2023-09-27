#!/bin/sh

echo "Migrando banco de dados..."
python3 ./api/manage.py migrate

exec "$@"