#!/bin/bash

set -e

if [ "$MIGRATE" == true ]; then
	echo "Running migrations...."
	python manage.py makemigrations
	python manage.py migrate
fi

exec "$@"