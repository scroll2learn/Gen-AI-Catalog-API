#!/bin/bash
set -x

DB_NAME=${SAMPLE_DB:-sample_db}


python /usr/src/app/scripts/wait_for_db.py
python /usr/src/app/scripts/create_db.py

TABLE_COUNT=$(PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';")

if [ "$TABLE_COUNT" -eq "0" ]; then
    echo "$DB_NAME database is empty. Importing SQL dump..."
    PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $DB_NAME -f /etc/sample_db/sample_db.sql
    echo "$DB_NAME database import complete."
else
    echo "$DB_NAME database already populated. Skipping import."
fi


alembic upgrade head

uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8011

tail -f /dev/null
