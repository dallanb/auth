#!/bin/sh

. ~/.bashrc

if [ "$DATABASE" = "auth" ]; then
  echo "Waiting for auth..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

if [ ! -d "migrations/dev/versions" ]; then
  echo "Directory migrations/dev/versions does not exist."
  flask db init --directory=migrations/dev
  sed -i '/import sqlalchemy as sa/a import sqlalchemy_utils' migrations/dev/script.py.mako
  flask db migrate --directory=migrations/dev
fi

flask db upgrade --directory=migrations/dev


manage run -h 0.0.0.0