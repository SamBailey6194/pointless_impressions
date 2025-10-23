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
    echo "  migrate       Run Django migrations"
    echo "  makemigrations Run Django makemigrations"
    echo "  createsuperuser Create a Django superuser"
    echo "  test          Run Django tests"
    echo "  collectstatic Collect static files"
    echo "  clean         Clean up containers, images, and volumes"
    echo "  status        Show status of all services"
    echo "  help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./dev.sh start        # Start development environment"
    echo "  ./dev.sh logs web     # Show logs for web service only"
    echo "  ./dev.sh shell        # Access Django shell"
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
        docker compose -f docker-compose.dev.yml exec web python manage.py shell
        ;;
    bash)
        print_status "Accessing bash shell..."
        docker compose -f docker-compose.dev.yml exec web bash
        ;;
    migrate)
        print_status "Running migrations..."
        docker compose -f docker-compose.dev.yml exec web python manage.py migrate
        print_success "Migrations completed!"
        ;;
    makemigrations)
        print_status "Creating migrations..."
        docker compose -f docker-compose.dev.yml exec web python manage.py makemigrations
        print_success "Migrations created!"
        ;;
    createsuperuser)
        print_status "Creating superuser..."
        docker compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
        ;;
    test)
        print_status "Running tests..."
        docker compose -f docker-compose.dev.yml exec web python manage.py test
        ;;
    collectstatic)
        print_status "Collecting static files..."
        docker compose -f docker-compose.dev.yml exec web python manage.py collectstatic --noinput
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
    status)
        print_status "Development environment status:"
        docker compose -f docker-compose.dev.yml ps
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac