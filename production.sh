#!/bin/bash

# production.sh - Helper script for production environment operations
# Usage: ./production.sh [command]

# ANSI color codes for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.production.yml"
ENV_FILE=".env.production"
PROJECT_NAME="pointless_impressions_production"

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
                print_message $YELLOW "Please edit $ENV_FILE with your production configuration"
            fi
        fi
        exit 1
    fi
}

# Function to show help
show_help() {
    print_message $CYAN "🚀 Pointless Impressions Production Environment Helper"
    echo
    print_message $YELLOW "Usage: ./production.sh [command]"
    echo
    print_message $BLUE "Available commands:"
    echo "  start       - Start production services"
    echo "  stop        - Stop production services"
    echo "  restart     - Restart production services"
    echo "  build       - Build production images"
    echo "  rebuild     - Rebuild images and start services"
    echo "  logs        - Show production logs"
    echo "  shell       - Open shell in production Django container"
    echo "  migrate     - Run Django migrations in production"
    echo "  test        - Run Django tests in production"
    echo "  backup      - Create database backup"
    echo "  clean       - Remove production containers and volumes"
    echo "  status      - Show status of production services"
    echo "  urls        - Show production service URLs"
    echo "  health      - Check service health"
    echo "  help        - Show this help message"
    echo
    print_message $MAGENTA "Examples:"
    echo "  ./production.sh start"
    echo "  ./production.sh logs web_prod"
    echo "  ./production.sh shell"
    echo "  ./production.sh migrate"
    echo "  ./production.sh backup"
    echo
    print_message $RED "⚠️  WARNING: This is the PRODUCTION environment!"
    print_message $RED "   Use with caution. All changes affect live users."
}

# Function to start production services
start_services() {
    print_message $RED "⚠️  WARNING: Starting PRODUCTION services!"
    read -p "Are you sure you want to start production? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_message $YELLOW "Production start cancelled."
        exit 0
    fi
    
    print_message $GREEN "🚀 Starting production services..."
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" up -d
    
    if [ $? -eq 0 ]; then
        print_message $GREEN "✅ Production services started successfully!"
        show_urls
    else
        print_message $RED "❌ Failed to start production services"
        exit 1
    fi
}

# Function to stop production services
stop_services() {
    print_message $YELLOW "🛑 Stopping production services..."
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" down
    
    if [ $? -eq 0 ]; then
        print_message $GREEN "✅ Production services stopped successfully!"
    else
        print_message $RED "❌ Failed to stop production services"
        exit 1
    fi
}

# Function to restart production services
restart_services() {
    print_message $RED "⚠️  WARNING: Restarting PRODUCTION services!"
    read -p "Are you sure you want to restart production? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_message $YELLOW "Production restart cancelled."
        exit 0
    fi
    
    print_message $YELLOW "🔄 Restarting production services..."
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" restart
    
    if [ $? -eq 0 ]; then
        print_message $GREEN "✅ Production services restarted successfully!"
        show_urls
    else
        print_message $RED "❌ Failed to restart production services"
        exit 1
    fi
}

# Function to build production images
build_images() {
    print_message $BLUE "🔨 Building production images..."
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" build --no-cache
    
    if [ $? -eq 0 ]; then
        print_message $GREEN "✅ Production images built successfully!"
    else
        print_message $RED "❌ Failed to build production images"
        exit 1
    fi
}

# Function to rebuild and start
rebuild_and_start() {
    print_message $RED "⚠️  WARNING: Rebuilding and starting PRODUCTION!"
    read -p "Are you sure you want to rebuild production? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_message $YELLOW "Production rebuild cancelled."
        exit 0
    fi
    
    print_message $BLUE "🔨 Rebuilding production images and starting services..."
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" up -d --build --force-recreate
    
    if [ $? -eq 0 ]; then
        print_message $GREEN "✅ Production services rebuilt and started successfully!"
        show_urls
    else
        print_message $RED "❌ Failed to rebuild and start production services"
        exit 1
    fi
}

# Function to show logs
show_logs() {
    local service=$1
    if [ -z "$service" ]; then
        print_message $BLUE "📋 Showing logs for all production services..."
        docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" logs -f
    else
        print_message $BLUE "📋 Showing logs for $service..."
        docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" logs -f "$service"
    fi
}

# Function to open shell
open_shell() {
    print_message $BLUE "🐚 Opening shell in production Django container..."
    print_message $RED "⚠️  WARNING: You are accessing the PRODUCTION environment!"
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" exec web_prod /bin/bash
}

# Function to run migrations
run_migrations() {
    print_message $RED "⚠️  WARNING: Running migrations in PRODUCTION!"
    read -p "Are you sure you want to run migrations in production? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_message $YELLOW "Production migrations cancelled."
        exit 0
    fi
    
    print_message $BLUE "🗃️  Running Django migrations in production..."
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" exec web_prod python /app/manage.py migrate
    
    if [ $? -eq 0 ]; then
        print_message $GREEN "✅ Migrations completed successfully!"
    else
        print_message $RED "❌ Failed to run migrations"
        exit 1
    fi
}

# Function to run tests
run_tests() {
    print_message $BLUE "🧪 Running Django tests in production..."
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" exec web_prod python /app/manage.py test
    
    if [ $? -eq 0 ]; then
        print_message $GREEN "✅ Tests completed successfully!"
    else
        print_message $RED "❌ Some tests failed"
        exit 1
    fi
}

# Function to create backup
create_backup() {
    local backup_file="backup_prod_$(date +%Y%m%d_%H%M%S).sql"
    print_message $BLUE "💾 Creating database backup: $backup_file"
    
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" exec db_prod pg_dump -U prod_user -d prod_db > "$backup_file"
    
    if [ $? -eq 0 ]; then
        print_message $GREEN "✅ Database backup created: $backup_file"
    else
        print_message $RED "❌ Failed to create backup"
        exit 1
    fi
}

# Function to clean up
clean_up() {
    print_message $RED "⚠️  WARNING: This will DELETE all production data!"
    print_message $YELLOW "🧹 This will remove all production containers and volumes..."
    read -p "Are you ABSOLUTELY SURE you want to delete production data? (type 'DELETE' to confirm): " -r
    echo
    if [[ $REPLY == "DELETE" ]]; then
        docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" down -v --remove-orphans
        docker system prune -f
        print_message $GREEN "✅ Production cleanup completed!"
    else
        print_message $YELLOW "Cleanup cancelled. Production data is safe."
    fi
}

# Function to show status
show_status() {
    print_message $BLUE "📊 Production services status:"
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" ps
}

# Function to check health
check_health() {
    print_message $BLUE "🏥 Checking production service health:"
    
    # Check if containers are running
    if ! docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" ps --services --filter "status=running" | grep -q web_prod; then
        print_message $RED "❌ Production web service is not running"
        return 1
    fi
    
    # Check database connection
    if docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" exec -T db_prod pg_isready -U prod_user -d prod_db > /dev/null 2>&1; then
        print_message $GREEN "✅ Database is healthy"
    else
        print_message $RED "❌ Database is not responding"
    fi
    
    # Check Redis connection
    if docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" exec -T redis_prod redis-cli ping > /dev/null 2>&1; then
        print_message $GREEN "✅ Redis is healthy"
    else
        print_message $RED "❌ Redis is not responding"
    fi
    
    # Check web service
    if curl -f http://localhost:8002/health/ > /dev/null 2>&1; then
        print_message $GREEN "✅ Web service is healthy"
    else
        print_message $RED "❌ Web service health check failed"
    fi
}

# Function to show URLs
show_urls() {
    print_message $CYAN "🌐 Production service URLs:"
    echo "  📱 Django App:     http://localhost:8002"
    echo "  🗄️  PostgreSQL:     localhost:5435"
    echo "  📦 Redis:          localhost:6381"
    echo
    print_message $RED "⚠️  These URLs are for local access to production services"
    print_message $YELLOW "   In actual deployment, use your domain/Heroku URL"
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
    "backup")
        check_prerequisites
        create_backup
        ;;
    "clean")
        check_prerequisites
        clean_up
        ;;
    "status")
        check_prerequisites
        show_status
        ;;
    "health")
        check_prerequisites
        check_health
        ;;
    "urls")
        show_urls
        ;;
    "help"|*)
        show_help
        ;;
esac