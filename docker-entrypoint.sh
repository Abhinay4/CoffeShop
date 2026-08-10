#!/bin/sh
set -e

echo "Waiting for the database..."
python <<'PY'
import os
import sys
import time

import psycopg2

url = os.environ.get("DATABASE_URL")
for _ in range(30):
    try:
        psycopg2.connect(url).close()
        break
    except psycopg2.OperationalError:
        time.sleep(1)
else:
    sys.exit("Database never became available")
PY
echo "Database is up."

echo "Running database migrations..."
flask db upgrade

exec "$@"
