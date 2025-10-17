# Coolify Demo App

A full-stack demo application showcasing Docker Compose deployment with PostgreSQL, Redis, FastAPI backend, and static frontend.

## Architecture

```
┌─────────────┐
│   Nginx     │  Port 80 (Static files + Reverse Proxy)
│  (Frontend) │
└──────┬──────┘
       │
       ├── / → Static HTML/JS/CSS
       └── /api → Backend API
              │
              ▼
       ┌──────────────┐
       │   FastAPI    │  Port 8000 (Internal)
       │   (Backend)  │
       └──┬────────┬──┘
          │        │
          │        │
    ┌─────▼─┐  ┌──▼─────┐
    │Postgres│  │ Redis  │
    │  DB    │  │ Cache  │
    └────────┘  └────────┘
```

## Features

- **FastAPI Backend**: RESTful API with automatic OpenAPI documentation
- **PostgreSQL**: Persistent message storage
- **Redis**: Caching and real-time statistics
- **Nginx**: Static file serving and reverse proxy
- **Health Checks**: All services include health monitoring
- **Responsive UI**: Modern, gradient-styled interface

## API Endpoints

- `GET /` - API info
- `GET /health` - Health check (Redis + PostgreSQL status)
- `POST /messages` - Create a message
- `GET /messages` - List all messages
- `GET /stats` - Get statistics (Redis + PostgreSQL counts)
- `GET /docs` - OpenAPI documentation (Swagger UI)
- `GET /redoc` - ReDoc documentation

## Local Development

### Prerequisites
- Docker
- Docker Compose

### Start the application

```bash
cd /Volumes/Storage/lab/coolify-demo-app
docker-compose up -d
```

### Access the application

- **Frontend**: http://localhost
- **API Documentation**: http://localhost/docs
- **Health Check**: http://localhost/api/health

### View logs

```bash
docker-compose logs -f
```

### Stop the application

```bash
docker-compose down
```

### Clean up (remove volumes)

```bash
docker-compose down -v
```

## Deploy to Coolify

This application is designed to be deployed to Coolify using Docker Compose:

1. Push to a Git repository
2. In Coolify, create a new service from Docker Compose
3. Point to this repository
4. Coolify will automatically deploy all services

## Environment Variables

All environment variables are pre-configured in `docker-compose.yml`:

- `POSTGRES_DB=demo`
- `POSTGRES_USER=demo`
- `POSTGRES_PASSWORD=demo123`
- `REDIS_HOST=redis`
- `REDIS_PORT=6379`

For production, change the PostgreSQL password!

## Testing

### Test the API directly

```bash
# Health check
curl http://localhost/api/health

# Create a message
curl -X POST http://localhost/api/messages \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello from Coolify!"}'

# Get messages
curl http://localhost/api/messages

# Get statistics
curl http://localhost/api/stats
```

## Tech Stack

- **Backend**: Python 3.11, FastAPI, Uvicorn
- **Databases**: PostgreSQL 16, Redis 7
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Web Server**: Nginx (Alpine)
- **Orchestration**: Docker Compose

## License

MIT
