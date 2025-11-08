#!/bin/sh
set -e

echo "Starting production container..."

# This uses the DATABASE_URL from the environment (e.g., Heroku Config Vars)
echo "Waiting for database..."
python /app/manage.py shell -c "
import os
import sys
import time
from django.db import connections
from django.db.utils import OperationalError

db_conn = None
db_url = os.environ.get('PRODUCTION_DB_URL')

if not db_url:
    print('FATAL: PRODUCTION_DB_URL not set. Exiting.')
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
    print('FATAL: Could not connect to database. Exiting.')
    sys.exit(1)
"

# Check if we can connect to the database
echo "Testing database connection..."
python /app/manage.py check --database default || {
    echo "Error: Cannot connect to database. Please check your PRODUCTION_DB_URL or production database settings."
    exit 1
}

# Run database migrations
echo "Running Django migrations..."
python /app/manage.py migrate --noinput || {
    echo "Error: Database migration failed."
    exit 1
}

# Create cache table if needed (for database cache backend)
echo "Creating cache tables if needed..."
python /app/manage.py createcachetable

# Load initial data fixtures if database is empty
echo "Checking if database is populated..."
python /app/manage.py shell -c "
from django.contrib.auth import get_user_model
from django.core.management import call_command
import os

User = get_user_model()

if User.objects.filter(username='superuser').exists():
    print('Database already populated. Skipping fixture loading.')
else:
    print('Database is empty. Loading fixtures...')
    try:
        call_command('loaddata', 'account.json')
        print('Loaded account.json')
        call_command('loaddata', 'account_group.json')
        print('Loaded account_group.json')
        call_command('loaddata', 'profiles.json')
        print('Loaded profiles.json')
        call_command('loaddata', 'artwork_categories.json')
        print('Loaded artwork_categories.json')
        call_command('loaddata', 'artwork_framing_conditions.json')
        print('Loaded artwork_framing_conditions.json')
        call_command('loaddata', 'photo.json')
        print('Loaded photo.json')
        call_command('loaddata', 'artwork.json')
        print('Loaded artwork.json')
        print('All fixtures loaded successfully.')
    except Exception as e:
        print(f'Error loading fixtures: {e}')
        print('Please check your fixture files and paths.')
        os._exit(1) # Exit with an error code
"

# Start Gunicorn with production settings
echo "Starting Gunicorn production server..."
exec gunicorn pointless_impressions_src.pointless_impressions.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --worker-class gthread \
    --threads 2 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --preload \
    --timeout 120 \
    --keep-alive 5 \
    --access-logfile '-' \
    --error-logfile '-' \
    --log-level info \
    --capture-output \
    --enable-stdio-inheritance