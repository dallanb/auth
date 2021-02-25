#!/bin/sh

. ~/.bashrc
pip install -e .

if [ "$DATABASE" = "app" ]; then
  echo "Waiting for app..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

while ! nc -z zookeeper 2181; do
  sleep 0.1
done
echo "Kafka started"

manage init
manage load

gunicorn --bind 0.0.0.0:5000 manage:app
