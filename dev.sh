#!/bin/bash

# Development helper script for Pointless Impressions
# This script provides easy commands for common development tasks

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker and Docker Compose are installed
check_requirements() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! command -v docker compose &> /dev/null && ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
}

# Create .env.dev if it doesn't exist
setup_env() {
    if [ ! -f .env.dev ]; then
        print_warning ".env.dev not found. Creating from example..."
        cp .env.dev.example .env.dev
        print_success ".env.dev created. Please review and update the values."
    fi
}

# Show usage information
show_help() {
    echo "Development Helper Script for Pointless Impressions"
    echo ""
    echo "Usage: ./dev.sh [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start         Start all development services"
    echo "  stop          Stop all development services"
    echo "  restart       Restart all development services"
    echo "  build         Build the development containers"
    echo "  logs          Show logs from all services"
    echo "  shell         Access Django shell in the web container"
    echo "  bash          Access bash shell in the web container"
    echo "  db            Access PostgreSQL database shell"
    echo "  migrate       Run Django migrations"
    echo "  makemigrations Run Django makemigrations"
    echo "  createsuperuser Create a Django superuser"
    echo "  flush         Flush the database (DANGER: deletes all data)"
    echo "  test          Run all Django TestCase tests"
    echo "  test [app]    Run Django TestCase tests (optionally specify app name)"
    echo "  behave        Run all Behave tests"
    echo "  cypress:reset Reset Cypress test database ready for tests"
    echo "  cypress       Run Cypress E2E tests (with test database)"
    echo "  cypress-open  Open Cypress UI (with test database)"
    echo "  jest          Run Jest tests"
    echo "  collectstatic Collect static files"
    echo "  clean         Clean up containers, images, and volumes"
    echo "  loadfixtures  Load initial data fixtures into the database"
    echo "  status        Show status of all services"
    echo "  help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./dev.sh start            # Start development environment"
    echo "  ./dev.sh logs web         # Show logs for web service only"
    echo "  ./dev.sh shell            # Access Django shell"
    echo "  ./dev.sh cypress          # Run Cypress E2E tests"
    echo "  ./dev.sh test             # Run all Django tests"
    echo "  ./dev.sh test artwork     # Run tests for artwork app only"
    echo "  ./dev.sh behave           # Run all Behave tests"
}

# Main script logic
case "${1:-help}" in
    start)
        check_requirements
        setup_env
        print_status "Starting development environment..."
        docker compose -f docker-compose.dev.yml up --build -d
        print_success "Development environment started!"
        print_status "Web application: http://localhost:8000"
        print_status "MailDev interface: http://localhost:1080"
        print_status "Database: localhost:5433"
        print_status "Redis: localhost:6379"
        ;;
    stop)
        print_status "Stopping development environment..."
        docker compose -f docker-compose.dev.yml down
        print_success "Development environment stopped!"
        ;;
    restart)
        print_status "Restarting development environment..."
        docker compose -f docker-compose.dev.yml kill
        docker compose -f docker-compose.dev.yml down
        docker compose -f docker-compose.dev.yml up --build -d
        print_success "Development environment restarted!"
        ;;
    build)
        print_status "Building development containers..."
        docker compose -f docker-compose.dev.yml build --no-cache
        print_success "Development containers built!"
        ;;
    logs)
        if [ -n "$2" ]; then
            docker compose -f docker-compose.dev.yml logs -f "$2"
        else
            docker compose -f docker-compose.dev.yml logs -f
        fi
        ;;
    shell)
        print_status "Accessing Django shell..."
        docker compose -f docker-compose.dev.yml exec web python /app/manage.py shell
        ;;
    bash)
        print_status "Accessing bash shell..."
        docker compose -f docker-compose.dev.yml exec web bash
        ;;
    db)
        DB_SERVICE_NAME="db_dev"
        DB_USER="dev_user" # Using the user defined in your compose file
        DB_NAME="dev_db" # Using the database defined in your compose file
        print_status "Accessing PostgreSQL shell (psql) for service: ${DB_SERVICE_NAME}..."
        
        # Check if the 'db_dev' service container is running
        if ! docker compose -f docker-compose.dev.yml ps -q ${DB_SERVICE_NAME} | grep -q .; then
            print_error "The '${DB_SERVICE_NAME}' service is not running. Please run './dev.sh start' first."
            exit 1
        fi

        # Run psql directly in the 'db_dev' container using the configured user
        docker compose -f docker-compose.dev.yml exec ${DB_SERVICE_NAME} psql -U ${DB_USER} -d ${DB_NAME}
        ;;
    migrate)
        print_status "Running migrations..."
        docker compose -f docker-compose.dev.yml exec web python /app/manage.py migrate
        print_success "Migrations completed!"
        ;;
    makemigrations)
        print_status "Creating migrations..."
        docker compose -f docker-compose.dev.yml exec web python /app/manage.py makemigrations
        print_success "Migrations created!"
        ;;
    flush)
        print_warning "This will delete all data in the database. Are you sure? (y/N)"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            docker compose -f docker-compose.dev.yml exec web python /app/manage.py flush --noinput
            print_success "Database flushed!"
        else
            print_status "Flush operation cancelled."
        fi
        ;;
    createsuperuser)
        print_status "Creating superuser..."
        docker compose -f docker-compose.dev.yml exec web python /app/manage.py createsuperuser
        ;;
    test)
        if [ -n "$2" ]; then
            print_status "Running tests for $2 app..."
            docker compose -f docker-compose.dev.yml exec web python /app/manage.py test "$2"
        else
            print_status "Running all tests..."
            docker compose -f docker-compose.dev.yml exec web python /app/manage.py test
        fi
        ;;
    behave)
        print_status "Running all Behave tests with test settings..."
        docker compose -f docker-compose.dev.yml exec web bash -c "export DJANGO_SETTINGS_MODULE=pointless_impressions_src.pointless_impressions.settings.test && python /app/manage.py behave"
        ;;
    cypress:reset)
        print_status "Resetting Cypress test database..."
        docker compose -f docker-compose.dev.yml exec web bash -c "export ENV=test && export DJANGO_SETTINGS_MODULE=pointless_impressions_src.pointless_impressions.settings.test && python /app/manage.py flush --noinput && python /app/manage.py migrate --noinput && python /app/manage.py create_test_artworks"
        print_success "Cypress test database reset completed!"
        ;;
    cypress)
        print_status "Running Cypress E2E tests with test settings..."
        print_status "Stopping dev server..."
        docker compose -f docker-compose.dev.yml stop web 2>/dev/null || true
        docker ps -a | grep "pointless_impressions-web-run" | awk '{print $1}' | xargs -r docker rm -f 2>/dev/null || true
        sleep 1
        print_status "Setting up test database..."
        docker compose -f docker-compose.dev.yml run -T --rm web bash -c "export ENV=test && export DJANGO_SETTINGS_MODULE=pointless_impressions_src.pointless_impressions.settings.test && python /app/manage.py migrate --noinput"
        print_status "Creating test data..."
        docker compose -f docker-compose.dev.yml run -T --rm web bash -c "export ENV=test && export DJANGO_SETTINGS_MODULE=pointless_impressions_src.pointless_impressions.settings.test && python /app/manage.py create_test_artworks"
        print_status "Starting test server..."
        docker compose -f docker-compose.dev.yml run -d -p 8001:8000 web bash -c "export ENV=test && export DJANGO_SETTINGS_MODULE=pointless_impressions_src.pointless_impressions.settings.test && python /app/manage.py runserver 0.0.0.0:8000"
        sleep 3
        print_status "Running Cypress tests..."
        NODE_ENV=development npx cypress run "${@:2}"
        print_success "Cypress tests completed!"
        print_status "Restarting dev server..."
        ./dev.sh restart
        print_status "Loading fixtures back to dev database..."
        ./dev.sh loadfixtures
        print_success "Cypress tests completed!"
        ;;
    cypress-open)
        print_status "Opening Cypress with test database..."
        print_status "Stopping dev server..."
        docker compose -f docker-compose.dev.yml stop web 2>/dev/null || true
        docker ps -a | grep "pointless_impressions-web-run" | awk '{print $1}' | xargs -r docker rm -f 2>/dev/null || true
        sleep 1
        print_status "Setting up test database..."
        docker compose -f docker-compose.dev.yml run -T --rm web bash -c "export ENV=test && export DJANGO_SETTINGS_MODULE=pointless_impressions_src.pointless_impressions.settings.test && python /app/manage.py migrate --noinput"
        print_status "Creating test data..."
        docker compose -f docker-compose.dev.yml run -T --rm web bash -c "export ENV=test && export DJANGO_SETTINGS_MODULE=pointless_impressions_src.pointless_impressions.settings.test && python /app/manage.py create_test_artworks"
        print_status "Starting test server..."
        docker compose -f docker-compose.dev.yml run -d -p 8001:8000 web bash -c "export ENV=test && export DJANGO_SETTINGS_MODULE=pointless_impressions_src.pointless_impressions.settings.test && python /app/manage.py runserver 0.0.0.0:8000"
        sleep 3
        print_status "Opening Cypress UI..."
        NODE_ENV=development npx cypress open
        print_status "Restarting dev server..."
        docker ps | grep "pointless_impressions-web-run" | awk '{print $1}' | xargs -r docker kill 2>/dev/null || true
        docker compose -f docker-compose.dev.yml up -d web
        print_status "Loading Photo and Artwork fixtures back to dev database..."
        docker compose -f docker-compose.dev.yml exec web python /app/manage.py loaddata photo.json artwork.json
        print_status "Added Photo and Artwork fixtures back to dev database."
        print_success "Cypress UI completed!"
        ;;
    jest)
        print_status "Running Jest tests..."
        docker compose -f docker-compose.dev.yml exec web bash -c "cd /app/pointless_impressions_src/theme/static_src && npm install && npm run test"
        ;;
    collectstatic)
        print_status "Collecting static files..."
        docker compose -f docker-compose.dev.yml exec web python /app/manage.py collectstatic --noinput
        print_success "Static files collected!"
        ;;
    clean)
        print_warning "This will remove all containers, images, and volumes. Are you sure? (y/N)"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            docker compose -f docker-compose.dev.yml down -v --remove-orphans
            docker system prune -af --volumes
            print_success "Development environment cleaned!"
        else
            print_status "Clean operation cancelled."
        fi
        ;;
    loadfixtures)
        print_status "Flushing existing data..."
        docker compose -f docker-compose.dev.yml exec web python /app/manage.py flush --noinput
        print_status "Loading initial data fixtures into the database..."
        docker compose -f docker-compose.dev.yml exec web python /app/manage.py loaddata account_group.json account.json profiles.json address.json artwork_categories.json artwork_framing_options.json photo_cloudinary_local.json artwork.json
        print_success "Fixtures loaded successfully!"
        ;;
    status)
        print_status "Development environment status:"
        docker compose -f docker-compose.dev.yml ps
        ;;
    help--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac