#!/bin/bash
set -e

echo "Starting development container..."

# Change to project root directory
cd /app

# Load environment variables
if [ -f .env.dev ]; then
    echo "Loading environment variables from .env.dev..."
    export $(grep -v '^#' .env.dev | xargs)
fi

# Wait for database to be ready
echo "Waiting for database at ${DEV_DB_HOST:-db_dev}:${DEV_DB_PORT:-5432}..."
while ! nc -z ${DEV_DB_HOST:-db_dev} ${DEV_DB_PORT:-5432}; do
    sleep 1
done
echo "Database is ready!"

# Apply Django migrations (manage.py is in project root)
echo "Applying database migrations..."
python /app/manage.py migrate

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
        # Load all fixtures in a single call so Django disables FK constraint
        # checking across the entire batch, resolving circular dependencies
        # between artwork (main_photo FK) and photo (artwork FK).
        # Order still matters for non-circular FKs:
        #   groups → users → profiles → categories → framing → artwork + photos → address
        call_command(
            'loaddata',
            'account_group.json',
            'account.json',
            'profiles.json',
            'artwork_categories.json',
            'artwork_framing_options.json',
            'artwork.json',
            'photo_cloudinary_local.json',
            'address.json',
        )
        print('All fixtures loaded successfully.')
    except Exception as e:
        print(f'Error loading fixtures: {e}')
        print('Please check your fixture files and paths.')
        os._exit(1) # Exit with an error code
"


# Install Node dependencies at project root
echo "Installing Node dependencies at project root..."
if [ -f /app/package.json ]; then
    cd /app
    npm install
else
    echo "Warning: package.json not found in /app"
fi

# Build Tailwind CSS and JavaScript assets
echo "Building Tailwind CSS and JavaScript..."
cd /app
npm run build || echo "Warning: Tailwind and JS build failed (check package.json)"

# Collect static files into STATIC_ROOT
echo "Collecting static files..."
python /app/manage.py collectstatic --noinput

# Function to handle graceful shutdown
cleanup() {
    echo "Shutting down services..."
    kill $(jobs -p) 2>/dev/null || true
    exit 0
}

trap cleanup SIGTERM SIGINT

# Start Tailwind and JavaScript watcher in background (from project root)
echo "Starting Tailwind and JavaScript in watch mode..."
cd /app
npm run start &
WATCH_PID=$!

# Wait a moment for watchers to start
sleep 2

# Start Django development server
echo "Starting Django development server..."
echo "Access the application at: http://localhost:8000"
echo "Access MailDev at: http://localhost:1080"
echo "Press Ctrl+C to stop all services"

# Run Django server in foreground (this keeps the container running)
python /app/manage.py runserver 0.0.0.0:8000

# This line should never be reached, but just in case
wait