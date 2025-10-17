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

This application is production-ready for Coolify deployment:

### Automatic Deployment

1. **Fork or clone this repository**
2. **In Coolify UI**:
   - Create new Application → Public Git Repository
   - Repository: `https://github.com/ammohq/coolify-demo-app.git`
   - Branch: `main`
   - Build Pack: `dockercompose`
   - Add domain (e.g., `demo.yourdomain.com`)
   - Click "Deploy"

3. **Via Coolify MCP** (programmatic):
   ```python
   # Using the Coolify MCP server
   create_application_public_git(
       name="coolify-demo-app",
       git_repository="https://github.com/ammohq/coolify-demo-app.git",
       git_branch="main",
       build_pack="dockercompose",
       instant_deploy=True
   )
   ```

### Coolify-Specific Configuration

The `docker-compose.yaml` file is optimized for Coolify:

- ✅ No custom networks (Coolify manages networking)
- ✅ No port mappings (Traefik handles routing)
- ✅ Backend has `traefik.enable=false` (internal only)
- ✅ Only nginx is publicly exposed
- ✅ Health checks configured for all services

### Important Notes

- **Backend is internal**: The FastAPI backend is NOT exposed to the internet. Only nginx handles external traffic and proxies to the backend.
- **SSL/TLS**: Coolify + Traefik automatically handles HTTPS certificates
- **Domain required**: You must configure a domain in Coolify for the application to be accessible

## Environment Variables

All environment variables are pre-configured in `docker-compose.yaml`:

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
