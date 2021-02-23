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

if [ "$MONGO_DATABASE" = "app" ]; then
  echo "Waiting for app..."

  while ! nc -z $MONGO_HOST $MONGO_PORT; do
    sleep 0.1
  done

  echo "MongoDB started"
fi


if [ ! -d "migrations/versions" ]; then
  echo "Directory migrations/versions does not exist."
  flask db init --directory=migrations
  sed -i '/import sqlalchemy as sa/a import sqlalchemy_utils' migrations/script.py.mako
fi

flask db migrate --directory=migrations
flask db upgrade --directory=migrations


manage run -h 0.0.0.0