#!/bin/bash

# staging.sh - Helper script for staging environment operations
# Usage: ./staging.sh [command]

# ANSI color codes for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.staging.yml"
ENV_FILE=".env.staging"
PROJECT_NAME="pointless_impressions_staging"

# Function to print colored messages
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check prerequisites
check_prerequisites() {
    if ! command -v docker &> /dev/null; then
        print_message $RED "❌ Docker is not installed or not in PATH"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        print_message $RED "❌ Docker Compose is not installed or not in PATH"
        exit 1
    fi

    if [ ! -f "$COMPOSE_FILE" ]; then
        print_message $RED "❌ $COMPOSE_FILE not found"
        exit 1
    fi

    if [ ! -f "$ENV_FILE" ]; then
        print_message $YELLOW "⚠️  $ENV_FILE not found"
        if [ -f "$ENV_FILE.example" ]; then
            print_message $YELLOW "Please copy $ENV_FILE.example to $ENV_FILE and configure it"
            read -p "Copy example file now? (y/n): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                cp "$ENV_FILE.example" "$ENV_FILE"
                print_message $GREEN "✅ Copied $ENV_FILE.example to $ENV_FILE"
                print_message $YELLOW "Please edit $ENV_FILE with your staging configuration"
            fi
        fi
        exit 1
    fi
}

# Function to show help
show_help() {
    print_message $CYAN "🚀 Pointless Impressions Staging Environment Helper"
    echo
    print_message $YELLOW "Usage: ./staging.sh [command]"
    echo
    print_message $BLUE "Available commands:"
    echo "  start       - Start staging services"
    echo "  stop        - Stop staging services"
    echo "  restart     - Restart staging services"
    echo "  build       - Build staging images"
    echo "  rebuild     - Rebuild images and start services"
    echo "  logs        - Show staging logs"
    echo "  shell       - Open shell in staging Django container"
    echo "  migrate     - Run Django migrations in staging"
    echo "  test        - Run Django tests in staging"
    echo "  clean       - Remove staging containers and volumes"
    echo "  status      - Show status of staging services"
    echo "  urls        - Show staging service URLs"
    echo "  help        - Show this help message"
    echo
    print_message $MAGENTA "Examples:"
    echo "  ./staging.sh start"
    echo "  ./staging.sh logs web_staging"
    echo "  ./staging.sh shell"
    echo "  ./staging.sh migrate"
}

# Function to start staging services
start_services() {
    print_message $GREEN "🚀 Starting staging services..."
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" up -d
    
    if [ $? -eq 0 ]; then
        print_message $GREEN "✅ Staging services started successfully!"
        show_urls
    else
        print_message $RED "❌ Failed to start staging services"
        exit 1
    fi
}

# Function to stop staging services
stop_services() {
    print_message $YELLOW "🛑 Stopping staging services..."
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" down
    
    if [ $? -eq 0 ]; then
        print_message $GREEN "✅ Staging services stopped successfully!"
    else
        print_message $RED "❌ Failed to stop staging services"
        exit 1
    fi
}

# Function to restart staging services
restart_services() {
    print_message $YELLOW "🔄 Restarting staging services..."
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" restart
    
    if [ $? -eq 0 ]; then
        print_message $GREEN "✅ Staging services restarted successfully!"
        show_urls
    else
        print_message $RED "❌ Failed to restart staging services"
        exit 1
    fi
}

# Function to build staging images
build_images() {
    print_message $BLUE "🔨 Building staging images..."
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" build --no-cache
    
    if [ $? -eq 0 ]; then
        print_message $GREEN "✅ Staging images built successfully!"
    else
        print_message $RED "❌ Failed to build staging images"
        exit 1
    fi
}

# Function to rebuild and start
rebuild_and_start() {
    print_message $BLUE "🔨 Rebuilding staging images and starting services..."
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" up -d --build --force-recreate
    
    if [ $? -eq 0 ]; then
        print_message $GREEN "✅ Staging services rebuilt and started successfully!"
        show_urls
    else
        print_message $RED "❌ Failed to rebuild and start staging services"
        exit 1
    fi
}

# Function to show logs
show_logs() {
    local service=$1
    if [ -z "$service" ]; then
        print_message $BLUE "📋 Showing logs for all staging services..."
        docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" logs -f
    else
        print_message $BLUE "📋 Showing logs for $service..."
        docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" logs -f "$service"
    fi
}

# Function to open shell
open_shell() {
    print_message $BLUE "🐚 Opening shell in staging Django container..."
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" exec web_staging /bin/bash
}

# Function to run migrations
run_migrations() {
    print_message $BLUE "🗃️  Running Django migrations in staging..."
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" exec web_staging python /app/manage.py migrate
    
    if [ $? -eq 0 ]; then
        print_message $GREEN "✅ Migrations completed successfully!"
    else
        print_message $RED "❌ Failed to run migrations"
        exit 1
    fi
}

# Function to run tests
run_tests() {
    print_message $BLUE "🧪 Running Django tests in staging..."
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" exec web_staging python /app/manage.py test
    
    if [ $? -eq 0 ]; then
        print_message $GREEN "✅ Tests completed successfully!"
    else
        print_message $RED "❌ Some tests failed"
        exit 1
    fi
}

# Function to clean up
clean_up() {
    print_message $YELLOW "🧹 Cleaning up staging containers and volumes..."
    read -p "This will remove all staging containers and volumes. Are you sure? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" down -v --remove-orphans
        docker system prune -f
        print_message $GREEN "✅ Cleanup completed!"
    else
        print_message $YELLOW "Cleanup cancelled."
    fi
}

# Function to show status
show_status() {
    print_message $BLUE "📊 Staging services status:"
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" ps
}

# Function to show URLs
show_urls() {
    print_message $CYAN "🌐 Staging service URLs:"
    echo "  📱 Django App:     http://localhost:8001"
    echo "  🗄️  PostgreSQL:     localhost:5434"
    echo "  📦 Redis:          localhost:6380"
    echo
    print_message $YELLOW "Note: These URLs are for local access to staging services"
}

# Main script logic
case ${1:-help} in
    "start")
        check_prerequisites
        start_services
        ;;
    "stop")
        check_prerequisites
        stop_services
        ;;
    "restart")
        check_prerequisites
        restart_services
        ;;
    "build")
        check_prerequisites
        build_images
        ;;
    "rebuild")
        check_prerequisites
        rebuild_and_start
        ;;
    "logs")
        check_prerequisites
        show_logs $2
        ;;
    "shell")
        check_prerequisites
        open_shell
        ;;
    "migrate")
        check_prerequisites
        run_migrations
        ;;
    "test")
        check_prerequisites
        run_tests
        ;;
    "clean")
        check_prerequisites
        clean_up
        ;;
    "status")
        check_prerequisites
        show_status
        ;;
    "urls")
        show_urls
        ;;
    "help"|*)
        show_help
        ;;
esac