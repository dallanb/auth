#!/bin/bash

ssh -i /home/dallanbhatti/.ssh/github super_dallan@mega <<EOF
  docker exec auth_db pg_dump -c -U "$1" auth > auth.sql
EOF
rsync -chavzP --stats --remove-source-files super_dallan@mega:/home/super_dallan/auth.sql "$HUNCHO_DIR"/services/auth/auth.sql

docker exec -i auth_db psql -U "$1" auth <"$HUNCHO_DIR"/services/auth/auth.sql
