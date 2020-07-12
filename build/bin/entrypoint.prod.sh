#!/bin/sh

gunicorn --bind 0.0.0.0:5000 manage:app