#!/bin/sh
set -e

echo "Starting production container..."

# Change to the project directory
cd /app/pointless_impressions_src

# Load environment variables from the app root
if [ -f "/app/.env.production" ]; then
    echo "Loading environment variables from /app/.env.production"
    export $(grep -v '^#' /app/.env.production | xargs)
fi

# Set Django settings module
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-pointless_impressions_src.pointless_impressions.settings.production}"

# Wait for services (database and cache)
echo "Waiting for services to be ready..."

# Handle both DATABASE_URL (course database) and manual database config
if [ -n "$DATABASE_URL" ]; then
    echo "Using course DATABASE_URL for database connection"
    # Extract host and port from DATABASE_URL for connection test
    DB_HOST=$(echo $DATABASE_URL | sed 's/.*@//' | sed 's/:.*//')
    DB_PORT=$(echo $DATABASE_URL | sed 's/.*://' | sed 's/\/.*//')
    echo "Testing connection to $DB_HOST:$DB_PORT..."
else
    echo "Using manual database configuration"
    DB_HOST="${PROD_DB_HOST:-db_prod}"
    DB_PORT="${PROD_DB_PORT:-5432}"
    echo "Testing connection to $DB_HOST:$DB_PORT..."
fi

# Wait for database with timeout
timeout=60
while ! nc -z $DB_HOST $DB_PORT; do
    timeout=$((timeout - 1))
    if [ $timeout -le 0 ]; then
        echo "Error: Database connection timeout"
        exit 1
    fi
    sleep 1
done
echo "Database connection successful."

# Check if we can connect to the database
echo "Testing database connection..."
python manage.py check --database default || {
    echo "Error: Cannot connect to database. Please check your DATABASE_URL or production database settings."
    exit 1
}

# Run database migrations
echo "Running Django migrations..."
python manage.py migrate --noinput || {
    echo "Error: Database migration failed."
    exit 1
}

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear || {
    echo "Warning: Static file collection failed, continuing..."
}

# Create cache table if needed (for database cache backend)
echo "Creating cache tables if needed..."
python manage.py createcachetable 2>/dev/null || echo "Cache tables already exist or not needed."

# Show deployment info
echo "Production deployment information:"
echo "- Django settings module: ${DJANGO_SETTINGS_MODULE}"
echo "- Debug mode: ${DJANGO_DEBUG:-False}"
echo "- Allowed hosts: ${DJANGO_ALLOWED_HOSTS:-not set}"
echo "- Database: $(echo $DATABASE_URL | sed 's/.*@//' | sed 's/\?.*//' || echo 'Local production database')"

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