#!/bin/bash
set -e
echo "Starting development container..."

# Load environment variables
if [ -f .env.dev ]; then
    export $(grep -v '^#' .env.dev | xargs)
fi

# Wait for database to be ready
echo "Waiting for database at ${DEV_DB_HOST}:${DEV_DB_PORT}..."
while ! nc -z $DEV_DB_HOST $DEV_DB_PORT; do
  sleep 1
done

# Initialize hash files
REQ_HASH_FILE=/tmp/requirements.hash
PKG_HASH_FILE=/tmp/package.hash

touch $REQ_HASH_FILE $PKG_HASH_FILE

if [ -f requirements.txt ]; then
    md5sum requirements.txt | awk '{print $1}' > $REQ_HASH_FILE
fi

NODE_DIR=./pointless_impressions_src/theme/static_src
if [ -f "$NODE_DIR/package.json" ]; then
    md5sum "$NODE_DIR/package.json" | awk '{print $1}' > $PKG_HASH_FILE
fi

# Apply Django migrations
echo "Applying database migrations..."
python manage.py migrate || true

# Install Tailwind dependencies and build
echo "Installing Tailwind and Node..."
cd $NODE_DIR
npm install
cd -

# Start Tailwind watcher in background
echo "Starting Tailwind in watch mode..."
python manage.py tailwind start &

# Start Django dev server in background
echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000 &

# Watch requirements.txt and package.json for changes
echo "Watching requirements.txt and package.json for changes..."
while inotifywait -e close_write requirements.txt ./pointless_impressions_src/theme/static_src/package.json; do
    echo "Change detected!"

    # Update Python dependencies if requirements.txt changed
    if [ -f requirements.txt ]; then
        echo "Installing Python dependencies..."
        pip install -r requirements.txt
    fi

    # Update Node dependencies if package.json changed
    NODE_DIR=./pointless_impressions_src/theme/static_src
    if [ -f "$NODE_DIR/package.json" ]; then
        echo "Installing Node dependencies..."
        cd $NODE_DIR
        npm install
        cd -
    fi
done
