#!/bin/sh
set -e

echo "Starting staging container..."

# This is a more robust way to wait for the external database
# It uses the STAGING_DB_URL from the environment.
echo "Waiting for database..."
python /app/manage.py shell -c "
import os
import sys
import time
from django.db import connections
from django.db.utils import OperationalError

db_conn = None
db_url = os.environ.get('STAGING_DB_URL')

if not db_url:
    print('STAGING_DB_URL not set. Exiting.')
    sys.exit(1)

retries = 30
while retries > 0:
    try:
        db_conn = connections['default']
        db_conn.cursor()
        print('Database is ready!')
        break
    except OperationalError:
        print('Database unavailable, waiting 1 second...')
        time.sleep(1)
    retries -= 1

if db_conn is None:
    print('Could not connect to database. Exiting.')
    sys.exit(1)
"

# Check if we can connect to the database
echo "Testing database connection..."
python /app/manage.py check --database default || {
    echo "Error: Cannot connect to database. Please check your STAGING_DB_URL or staging database settings."
    exit 1
}
echo "Database connection ready."

# Run database migrations
echo "Running Django migrations..."
python /app/manage.py migrate --noinput || {
    echo "Error: Database migration failed."
    exit 1
}

# Create cache table if needed (for database cache backend)
echo "Creating cache tables if needed..."
python /app/manage.py createcachetable

# Load initial data fixtures (always load to get latest data)
echo "Loading initial data fixtures..."
python /app/manage.py shell -c "
from django.core.management import call_command

print('Loading fixtures to ensure latest data...')
try:
    call_command('loaddata', 'account.json')
    call_command('loaddata', 'account_group.json')
    call_command('loaddata', 'profiles.json')
    call_command('loaddata', 'artwork_categories.json')
    call_command('loaddata', 'artwork_framing_conditions.json')
    call_command('loaddata', 'photo.json')
    call_command('loaddata', 'artwork.json')
    print('All fixtures loaded successfully.')
except Exception as e:
    print(f'Error loading fixtures: {e}')
    # Exit with error if fixtures fail
    exit(1)
"

# Start Gunicorn with improved settings for staging
echo "Starting Gunicorn staging server..."
exec gunicorn pointless_impressions_src.pointless_impressions.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 1 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 120 \
    --keep-alive 5 \
    --access-logfile '-' \
    --error-logfile '-' \
    --log-level info \
    --capture-output \
    --enable-stdio-inheritance
