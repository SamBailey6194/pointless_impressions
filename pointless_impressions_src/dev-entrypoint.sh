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

# --- Python dependencies watcher ---
REQ_HASH_FILE="/tmp/requirements.hash"
if [ -f requirements.txt ]; then
    REQ_HASH=$(md5sum requirements.txt | awk '{print $1}')
    echo "$REQ_HASH" > "$REQ_HASH_FILE"
    uv pip install -r requirements.txt
fi

# --- Node dependencies watcher ---
NODE_DIR="./pointless_impressions_src/theme/static_src"
PKG_HASH_FILE="/tmp/package.hash"
if [ -f "$NODE_DIR/package.json" ]; then
    PKG_HASH=$(md5sum "$NODE_DIR/package.json" | awk '{print $1}')
    echo "$PKG_HASH" > "$PKG_HASH_FILE"
    [ ! -d "$NODE_DIR/node_modules" ]; then
    echo "Installing Node dependencies..."
    cd $NODE_DIR
    npm install
    cd - > /dev/null
fi

# --- Start background watcher for dev ---
(
while true; do
    # Watch Python requirements
    if [ -f requirements.txt ]; then
        NEW_REQ_HASH=$(md5sum requirements.txt | awk '{print $1}')
        OLD_REQ_HASH=$(cat "$REQ_HASH_FILE")
        if [ "$NEW_REQ_HASH" != "$OLD_REQ_HASH" ]; then
            echo "requirements.txt changed. Installing Python dependencies..."
            uv pip install -r requirements.txt
            echo "$NEW_REQ_HASH" > "$REQ_HASH_FILE"
        fi
    fi

    # Watch Node package.json
    if [ -f "$NODE_DIR/package.json" ]; then
        NEW_PKG_HASH=$(md5sum "$NODE_DIR/package.json" | awk '{print $1}')
        OLD_PKG_HASH=$(cat "$PKG_HASH_FILE")
        if [ "$NEW_PKG_HASH" != "$OLD_PKG_HASH" ]; then
            echo "package.json changed. Installing Node dependencies..."
            cd $NODE_DIR
            npm install
            cd - > /dev/null
            echo "$NEW_PKG_HASH" > "$PKG_HASH_FILE"
        fi
    fi

    sleep 5
done
) &

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
