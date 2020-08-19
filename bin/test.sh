#!/bin/sh

. ~/.bashrc
manage delete_db
manage flush_cache
manage init
python -m py.test