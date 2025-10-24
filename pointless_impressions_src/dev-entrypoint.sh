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

# Create superuser if it doesn't exist (for development convenience)
echo "Checking for superuser..."
python /app/manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
" 2>/dev/null || echo "Note: Superuser creation skipped"

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