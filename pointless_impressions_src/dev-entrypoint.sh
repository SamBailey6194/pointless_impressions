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

# Install Tailwind dependencies
NODE_DIR=/app/pointless_impressions_src/theme/static_src
echo "Installing Tailwind and Node dependencies..."
if [ -f "$NODE_DIR/package.json" ]; then
    cd $NODE_DIR
    npm install
    cd /app
else
    echo "Warning: package.json not found in $NODE_DIR"
fi

# Install Tailwind CSS
echo "Installing Tailwind CSS..."
python /app/manage.py tailwind install

# Function to handle graceful shutdown
cleanup() {
    echo "Shutting down services..."
    kill $(jobs -p) 2>/dev/null || true
    exit 0
}
trap cleanup SIGTERM SIGINT

# Change to Django project directory for Tailwind commands
cd /app/pointless_impressions_src

# Start Tailwind watcher in background
echo "Starting Tailwind in watch mode..."
python /app/manage.py tailwind start &
TAILWIND_PID=$!

# Wait a moment for Tailwind to start
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
