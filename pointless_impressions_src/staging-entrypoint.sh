#!/bin/sh
set -e

echo "Starting staging container..."

# Change to Django project directory
cd /app/pointless_impressions_src

# Load environment variables
if [ -f "/app/.env.staging" ]; then
    echo "Loading environment variables from .env.staging..."
    export $(grep -v '^#' /app/.env.staging | xargs)
fi

# Set default database connection variables for staging
DB_HOST=${STAGING_DB_HOST:-${DATABASE_URL:-db_staging}}
DB_PORT=${STAGING_DB_PORT:-5432}

# Wait for database (supports both manual config and DATABASE_URL)
if [ -n "$DATABASE_URL" ]; then
    echo "Using DATABASE_URL for database connection..."
    # Extract host from DATABASE_URL if needed for health check
    DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
    echo "Waiting for database at $DB_HOST..."
    # Simple wait for DATABASE_URL connection
    sleep 5
else
    echo "Waiting for database at $DB_HOST:$DB_PORT..."
    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 1
    done
fi
echo "Database connection ready."

# Check if we can connect to the database
echo "Testing database connection..."
python /app/manage.py check --database default || {
    echo "Error: Cannot connect to database. Please check your DATABASE_URL or staging database settings."
    exit 1
}

# Run database migrations
echo "Running Django migrations..."
python /app/manage.py migrate --noinput || {
    echo "Error: Database migration failed."
    exit 1
}

# Collect static files
echo "Collecting static files..."
python /app/manage.py collectstatic --noinput --clear || {
    echo "Warning: Static file collection failed, continuing..."
}

# Create cache table if needed (for database cache backend)
echo "Creating cache tables if needed..."
python /app/manage.py createcachetable 2>/dev/null || echo "Cache tables already exist or not needed."

# Show deployment info
echo "Staging deployment information:"
echo "- Django settings module: ${DJANGO_SETTINGS_MODULE:-pointless_impressions_src.pointless_impressions.settings.staging}"
echo "- Debug mode: ${DJANGO_DEBUG:-False}"
echo "- Allowed hosts: ${DJANGO_ALLOWED_HOSTS:-not set}"
echo "- Database: $(echo $DATABASE_URL | sed 's/.*@//' | sed 's/\?.*//' || echo 'Local staging database')"

# Start Gunicorn with improved settings for staging
echo "Starting Gunicorn staging server..."
exec gunicorn pointless_impressions_src.pointless_impressions.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 120 \
    --keep-alive 5 \
    --access-logfile '-' \
    --error-logfile '-' \
    --log-level info \
    --capture-output \
    --enable-stdio-inheritance
