#!/bin/sh

. ~/.bashrc

if [ "$DATABASE" = "auth" ]; then
  echo "Waiting for auth..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi


gunicorn --bind 0.0.0.0:5000 manage:app