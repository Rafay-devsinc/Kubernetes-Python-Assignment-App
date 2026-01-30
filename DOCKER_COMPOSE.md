# Docker Compose Setup

## Overview

This project includes a `docker-compose.yml` that runs the Flask Task Management App with PostgreSQL database.

## Quick Start

```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down
```

Access the app at: **http://localhost:5001**

## Architecture

```
docker-compose
├── postgres (PostgreSQL 14)
│   ├── Port: 5432
│   ├── Database: assignment_db
│   └── Volume: postgres_data
│
└── flask-app (Task Management App)
    ├── Port: 5001
    ├── Image: rafaydevsinc/assignment_app:latest
    └── Volumes: logs, app_data
```

## Services

### 1. PostgreSQL Database

**Image**: `postgres:14-alpine`  
**Container Name**: `assignment_postgres`  
**Port**: `5432:5432`

**Environment Variables**:
- `POSTGRES_DB`: assignment_db
- `POSTGRES_USER`: postgres
- `POSTGRES_PASSWORD`: postgres

**Health Check**: `pg_isready -U postgres` every 10s

### 2. Flask Application

**Image**: `rafaydevsinc/assignment_app:latest` (from Docker Hub)  
**Container Name**: `assignment_flask_app`  
**Port**: `5001:5001`

**Environment Variables**:
- `APP_NAME`: Task Management App
- `APP_ENV`: production
- `DATABASE_URL`: postgresql://postgres:postgres@postgres:5432/assignment_db
- `SECRET_KEY`: your-secret-key-change-in-production

**Dependencies**: Waits for PostgreSQL to be healthy before starting

## Commands

### Start Services

```bash
# Start in foreground
docker-compose up

# Start in background (detached)
docker-compose up -d

# Start specific service
docker-compose up flask-app
docker-compose up postgres
```

### View Logs

```bash
# All services
docker-compose logs

# Follow logs
docker-compose logs -f

# Specific service
docker-compose logs flask-app
docker-compose logs postgres

# Last 100 lines
docker-compose logs --tail=100
```

### Stop Services

```bash
# Stop containers (keeps data)
docker-compose stop

# Stop and remove containers (keeps data)
docker-compose down

# Stop and remove everything including volumes (deletes data!)
docker-compose down -v
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart flask-app
docker-compose restart postgres
```

### View Status

```bash
# List running containers
docker-compose ps

# View resource usage
docker-compose top
```

### Execute Commands

```bash
# Access Flask container shell
docker-compose exec flask-app /bin/sh

# Access PostgreSQL
docker-compose exec postgres psql -U postgres -d assignment_db

# Run SQL query
docker-compose exec postgres psql -U postgres -d assignment_db -c "SELECT * FROM tasks;"
```

## Volumes

### postgres_data
- Stores PostgreSQL database files
- Persists across container restarts
- Located in Docker's volume directory

### app_data
- Application data
- Persists across container restarts

### ./logs (bind mount)
- Application logs
- Mapped to `./logs` directory on host
- Accessible directly from host system

## Networking

**Network**: `app-network` (bridge driver)

Services communicate using container names:
- Flask connects to PostgreSQL via `postgres:5432`
- Both services are isolated in the same network

## Configuration

### Change Database Password

Edit `docker-compose.yml`:

```yaml
services:
  postgres:
    environment:
      POSTGRES_PASSWORD: your-secure-password
  
  flask-app:
    environment:
      DATABASE_URL: "postgresql://postgres:your-secure-password@postgres:5432/assignment_db"
```

### Change Port

Edit `docker-compose.yml`:

```yaml
services:
  flask-app:
    ports:
      - "8080:5001"  # Access on port 8080
```

### Use Different Database

```yaml
services:
  postgres:
    environment:
      POSTGRES_DB: my_custom_db
  
  flask-app:
    environment:
      DATABASE_URL: "postgresql://postgres:postgres@postgres:5432/my_custom_db"
```

## Development Workflow

### 1. Start Services

```bash
docker-compose up -d
```

### 2. Check Status

```bash
docker-compose ps
docker-compose logs -f
```

### 3. Access Application

Open http://localhost:5001 in your browser

### 4. Make Changes

After updating code and pushing to Docker Hub:

```bash
# Pull latest image
docker-compose pull

# Recreate containers
docker-compose up -d --force-recreate
```

### 5. View Database

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U postgres -d assignment_db

# List tables
\dt

# View tasks
SELECT * FROM tasks;

# Exit
\q
```

## Troubleshooting

### Services won't start

```bash
# Check logs
docker-compose logs

# Check if ports are available
lsof -i :5001
lsof -i :5432

# Remove old containers
docker-compose down
docker-compose up -d
```

### Database connection failed

```bash
# Check PostgreSQL is healthy
docker-compose ps

# Check PostgreSQL logs
docker-compose logs postgres

# Restart services
docker-compose restart
```

### Can't access the app

```bash
# Check if container is running
docker-compose ps

# Check Flask logs
docker-compose logs flask-app

# Verify port mapping
docker-compose port flask-app 5001
```

### Reset everything

```bash
# Stop and remove everything
docker-compose down -v

# Start fresh
docker-compose up -d
```

## Production Considerations

For production deployments, consider:

1. **Use secrets** instead of plain text passwords
2. **Use environment files** (`.env`)
3. **Configure resource limits**
4. **Set up proper logging**
5. **Use reverse proxy** (nginx)
6. **Enable SSL/TLS**
7. **Regular backups**
8. **Health checks and monitoring**

### Example with Resource Limits

```yaml
services:
  flask-app:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

### Example with Environment File

Create `.env` file:
```bash
POSTGRES_PASSWORD=secure_password
SECRET_KEY=your_secret_key
```

Update `docker-compose.yml`:
```yaml
services:
  postgres:
    env_file:
      - .env
```

## Data Management

### Backup Database

```bash
# Create backup
docker-compose exec postgres pg_dump -U postgres assignment_db > backup.sql

# Or using docker
docker exec assignment_postgres pg_dump -U postgres assignment_db > backup.sql
```

### Restore Database

```bash
# Restore from backup
cat backup.sql | docker-compose exec -T postgres psql -U postgres -d assignment_db
```

### View Volumes

```bash
# List volumes
docker volume ls | grep docker-python-assignment-app

# Inspect volume
docker volume inspect docker-python-assignment-app_postgres_data
```

## Comparison: Docker Compose vs Kubernetes

| Feature | Docker Compose | Kubernetes |
|---------|----------------|------------|
| **Complexity** | Simple | Advanced |
| **Use Case** | Development, Single Host | Production, Multi-Host |
| **Scaling** | Manual | Automatic |
| **High Availability** | No | Yes |
| **Load Balancing** | Basic | Advanced |
| **Self-Healing** | No | Yes |
| **Best For** | Dev/Test | Production |

## Quick Reference

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Logs
docker-compose logs -f

# Shell access
docker-compose exec flask-app sh
docker-compose exec postgres psql -U postgres -d assignment_db

# Restart
docker-compose restart

# Pull updates
docker-compose pull
docker-compose up -d --force-recreate

# Clean up
docker-compose down -v
```

## Links

- **Application**: http://localhost:5001
- **Task Management**: http://localhost:5001/assignment
- **Statistics**: http://localhost:5001/stats
- **Logs**: http://localhost:5001/logs
- **PostgreSQL**: localhost:5432

---

✅ Your Docker Compose setup is ready to use!

Run `docker-compose up -d` to start the application.
