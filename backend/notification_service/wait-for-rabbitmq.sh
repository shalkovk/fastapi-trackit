#!/bin/bash

set -e

host="${RABBITMQ_HOST:-rabbitmq}"
port="${RABBITMQ_PORT:-5672}"

echo "[*] Ожидание RabbitMQ на ${host}:${port}..."

while ! nc -z "$host" "$port"; do
  sleep 1
done

echo "[*] RabbitMQ доступен. Запускаем сервис..."
exec "$@"