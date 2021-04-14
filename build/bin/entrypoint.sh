#!/bin/sh

. ~/.bashrc

pip install -e .

if [ "$DATABASE" = "auth" ]; then
  echo "Waiting for auth..."
  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi


if [ ! -d "migrations/versions" ]; then
  echo "Directory migrations/versions does not exist."
  flask db init --directory=migrations
  sed -i '/import sqlalchemy as sa/a import sqlalchemy_utils' migrations/script.py.mako
  flask db migrate --directory=migrations
  sed -i 's/length=1137/max_length=1137/' migrations/versions/*.py
  flask db upgrade --directory=migrations
  manage init
  manage load
else
  flask db migrate --directory=migrations
  flask db upgrade --directory=migrations
fi


manage run -h 0.0.0.0