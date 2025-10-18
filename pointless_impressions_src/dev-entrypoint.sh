#!/bin/sh
set -e

echo "Starting development container..."

# Load environment variables
if [ -f ".env.dev" ]; then
    export $(grep -v '^#' .env.dev | xargs)
fi

# Wait for Postgres
echo "Waiting for database at $DEV_DB_HOST:$DEV_DB_PORT..."
while ! nc -z $DEV_DB_HOST $DEV_DB_PORT; do
  sleep 1
done

# Install Node dependencies (for Tailwind Plugins, Jest, Cypress)
NODE_DIR="./pointless_impressions_src/theme/static_src"
if [ ! -d "$NODE_DIR/node_modules" ]; then
  echo "Installing Node dependencies..."
  cd $NODE_DIR
  RUN npm install -g npm@11.6.2
  npm install
  cd - > /dev/null
else
  echo "Node dependencies already installed."
fi

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Install Tailwind
echo "Installing Tailwind..."
python manage.py tailwind install

# Start Tailwind in watch mode
echo "Starting Tailwind"
python manage.py tailwind start &

# Start Django dev server
echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000
