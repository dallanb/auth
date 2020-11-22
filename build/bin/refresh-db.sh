#!/bin/sh

docker exec -it auth bash -c "python manage.py reset_db"
docker exec -it auth bash -c "python manage.py init"