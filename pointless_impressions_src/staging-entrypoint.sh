#!/bin/sh
set -e

echo "Starting staging container..."

# Load environment variables
if [ -f ".env.staging" ]; then
    export $(grep -v '^#' .env.staging | xargs)
fi

# Wait for Postgres
echo "Waiting for database at $STAGING_DB_HOST:$STAGING_DB_PORT..."
while ! nc -z $STAGING_DB_HOST $STAGING_DB_PORT; do
  sleep 1
done
echo "Database ready."

# Run database migrations
echo "Running Django migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn staging server..."
exec gunicorn pointless_impressions_src.pointless_impressions.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile '-' \
    --error-logfile '-' \
    --log-level info
