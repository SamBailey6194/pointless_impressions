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

# --- NEW: Load all fixture data ---
# This populates the database with users, profiles, groups, and art.
echo "Loading initial data fixtures..."
# (Make sure your fixture files are in the 'fixtures' dir of each app)
python /app/manage.py loaddata account.json
echo "Loaded the accounts fixture."
python /app/manage.py loaddata account_group.json
echo "Loaded the account groups fixture."
python /app/manage.py loaddata profiles.json
echo "Loaded the profiles fixture."
python /app/manage.py loaddata artwork_categories.json
echo "Loaded the artwork categories fixture."
python /app/manage.py loaddata artwork_framing_conditions.json
echo "Loaded the artwork framing conditions fixture."
python /app/manage.py loaddata photo.json
echo "Loaded the photos fixture."
python /app/manage.py loaddata artwork.json
echo "Loaded the artwork fixture."
echo "All fixtures loaded successfully."

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