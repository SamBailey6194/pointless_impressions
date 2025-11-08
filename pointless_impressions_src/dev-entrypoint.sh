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
        call_command('loaddata', 'account.json')
        print('Loaded account.json')
        call_command('loaddata', 'account_group.json')
        print('Loaded account_group.json')
        call_command('loaddata', 'profiles.json')
        print('Loaded profiles.json')
        call_command('loaddata', 'artwork_categories.json')
        print('Loaded artwork_categories.json')
        call_command('loaddata', 'artwork_framing_options.json')
        print('Loaded artwork_framing_options.json')
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