#!/bin/bash
set -e

mongo <<EOF
use $MONGO_USER_DB
db.createUser({
    user: '$MONGO_USER',
    pwd: '$MONGO_PWD',
    roles: [
        {
            role: '$MONGO_USER_ROLE',
            db: '$MONGO_USER_DB'
        }
    ]
})
EOF