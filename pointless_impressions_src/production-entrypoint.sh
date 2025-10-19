#!/bin/sh
set -e

echo "Starting production container..."

# Load environment variables
if [ -f ".env.production" ]; then
    export $(grep -v '^#' .env.production | xargs)
fi

# Wait for Postgres
echo "Waiting for database at $PROD_DB_HOST:$PROD_DB_PORT..."
while ! nc -z $PROD_DB_HOST $PROD_DB_PORT; do
  sleep 1
done
echo "Database ready."

# Install Node dependencies (production only)
NODE_DIR="./pointless_impressions_src/theme/static_src"
echo "Installing Node dependencies..."
cd $NODE_DIR
RUN npm install -g npm@11.6.2
npm ci --omit=dev
cd - > /dev/null

# Run migrations
echo "Running Django migrations..."
python manage.py migrate --noinput

# Build Tailwind + JS
echo "Building Tailwind + JS..."
python manage.py tailwind build
cd $NODE_DIR
npm run build:js
cd - > /dev/null

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn server..."
exec gunicorn pointless_impressions_src.pointless_impressions.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 5 \
    --timeout 120 \
    --access-logfile '-' \
    --error-logfile '-' \
    --log-level info