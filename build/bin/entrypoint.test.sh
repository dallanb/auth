#!/bin/sh

. ~/.bashrc

if [ "$DATABASE" = "auth" ]; then
  echo "Waiting for auth..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

if [ ! -d "migrations/test/versions" ]; then
  echo "Directory migrations/test/versions does not exist."
  flask db init --directory=migrations/test
  sed -i '/import sqlalchemy as sa/a import sqlalchemy_utils' migrations/test/script.py.mako
  flask db migrate --directory=migrations/test
fi

flask db upgrade --directory=migrations/test


manage run -h 0.0.0.0