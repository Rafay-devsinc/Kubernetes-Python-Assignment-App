# Docker Hub Setup Complete ✅

## Image Information

**Docker Hub Repository**: `rafaydevsinc/assignment_app`  
**Access**: Public (anyone can pull)  
**Tags**: 
- `latest` - Latest version
- `v1.0` - Version 1.0

## Image Details

```bash
Repository: rafaydevsinc/assignment_app
Tags: latest, v1.0
Size: ~500MB
Digest: sha256:4e95416efb5465efd474f23aa34912083ed77647df28aa2ecaaf61d31981bef4
```

## Pull the Image

Anyone can pull your public image:

```bash
# Pull latest
docker pull rafaydevsinc/assignment_app:latest

# Pull specific version
docker pull rafaydevsinc/assignment_app:v1.0

# Run directly
docker run -p 5001:5001 rafaydevsinc/assignment_app:latest
```

## Where It's Used

### 1. Docker Compose ✅
File: `docker-compose.yml`

```yaml
services:
  flask-app:
    image: rafaydevsinc/assignment_app:latest
```

**Start**: `docker-compose up -d`

### 2. Kubernetes ✅
File: `kubernetes/deployment.yaml`

```yaml
containers:
- name: flask-app
  image: rafaydevsinc/assignment_app:latest
  imagePullPolicy: Always
```

**Deploy**: `cd kubernetes && ./deploy.sh`

## Updated Files

### Kubernetes Deployment
- ✅ `kubernetes/deployment.yaml` - Updated to use Docker Hub image
- ✅ `kubernetes/deploy.sh` - No longer builds locally
- ✅ `kubernetes/deploy-with-postgres.sh` - No longer builds locally

### Docker Compose
- ✅ `docker-compose.yml` - Uses Docker Hub image
- ✅ `DOCKER_COMPOSE.md` - Complete documentation

## Deployment Options

### Option 1: Docker Compose (Simple)

```bash
# Start with PostgreSQL
docker-compose up -d

# Access
http://localhost:5001
```

**Use Case**: Local development, testing, quick demos

### Option 2: Kubernetes (Production)

```bash
# Start Minikube
minikube start

# Deploy with PostgreSQL
cd kubernetes
./deploy-with-postgres.sh

# Access
minikube service flask-app-service
```

**Use Case**: Production, learning Kubernetes, scalable deployments

## Update Workflow

When you make code changes:

### 1. Build New Image

```bash
# Build and tag
docker build -t rafaydevsinc/assignment_app:latest -t rafaydevsinc/assignment_app:v1.1 .
```

### 2. Push to Docker Hub

```bash
# Login (if needed)
docker login -u rafaydevsinc

# Push
docker push rafaydevsinc/assignment_app:latest
docker push rafaydevsinc/assignment_app:v1.1
```

### 3. Update Deployments

**Docker Compose**:
```bash
docker-compose pull
docker-compose up -d --force-recreate
```

**Kubernetes**:
```bash
kubectl rollout restart deployment flask-app
# Or redeploy
kubectl delete -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/deployment.yaml
```

## Version Management

### Current Tags
- `latest` - Always points to newest version
- `v1.0` - Stable version 1.0

### Create New Version

```bash
# Build with new version
docker build -t rafaydevsinc/assignment_app:v1.1 .

# Tag as latest
docker tag rafaydevsinc/assignment_app:v1.1 rafaydevsinc/assignment_app:latest

# Push both
docker push rafaydevsinc/assignment_app:v1.1
docker push rafaydevsinc/assignment_app:latest
```

### Use Specific Version in Kubernetes

Edit `kubernetes/deployment.yaml`:
```yaml
image: rafaydevsinc/assignment_app:v1.0  # Pin to specific version
```

## Docker Hub Commands

```bash
# Login
docker login -u rafaydevsinc

# List local images
docker images rafaydevsinc/assignment_app

# Remove local image
docker rmi rafaydevsinc/assignment_app:latest

# Pull fresh copy
docker pull rafaydevsinc/assignment_app:latest

# Inspect image
docker inspect rafaydevsinc/assignment_app:latest

# View image history
docker history rafaydevsinc/assignment_app:latest
```

## Image Layers

Your image includes:
1. **Base**: Python 3.12-slim
2. **System packages**: gcc, postgresql-client
3. **Python dependencies**: Flask, SQLAlchemy, psycopg2, etc.
4. **Application code**: app.py, templates, static files
5. **Configuration**: .env file

## Security Notes

### Public Repository
- ✅ Anyone can pull your image
- ✅ Good for open-source projects
- ⚠️ Don't include secrets in the image
- ⚠️ Secrets should be passed via environment variables

### Secrets Management

**Docker Compose** (use environment variables):
```yaml
services:
  flask-app:
    environment:
      SECRET_KEY: ${SECRET_KEY}
```

**Kubernetes** (use secrets):
```yaml
env:
- name: SECRET_KEY
  valueFrom:
    secretKeyRef:
      name: flask-secrets
      key: SECRET_KEY
```

## CI/CD Integration

### Example GitHub Actions

```yaml
name: Build and Push

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Login to Docker Hub
        uses: docker/login-action@v1
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v2
        with:
          push: true
          tags: |
            rafaydevsinc/assignment_app:latest
            rafaydevsinc/assignment_app:${{ github.sha }}
```

## Verification

### Test Image Locally

```bash
# Pull and run
docker pull rafaydevsinc/assignment_app:latest
docker run -p 5001:5001 \
  -e DATABASE_URL=sqlite:///assignment.db \
  rafaydevsinc/assignment_app:latest

# Access
http://localhost:5001
```

### Test in Docker Compose

```bash
docker-compose up -d
docker-compose ps
docker-compose logs -f
```

### Test in Kubernetes

```bash
cd kubernetes
./deploy-with-postgres.sh
kubectl get pods
kubectl logs -l app=flask-app
```

## Troubleshooting

### Image pull failed

```bash
# Check image exists
docker pull rafaydevsinc/assignment_app:latest

# Check Kubernetes events
kubectl describe pod <pod-name>
```

### Image not updating

```bash
# Force pull in Kubernetes
kubectl rollout restart deployment flask-app

# Force recreate in Docker Compose
docker-compose pull
docker-compose up -d --force-recreate
```

### Wrong image version

```bash
# Check running image
docker inspect <container-id> | grep Image

# In Kubernetes
kubectl describe pod <pod-name> | grep Image
```

## Quick Reference

```bash
# Build
docker build -t rafaydevsinc/assignment_app:latest .

# Push
docker push rafaydevsinc/assignment_app:latest

# Pull
docker pull rafaydevsinc/assignment_app:latest

# Run
docker run -p 5001:5001 rafaydevsinc/assignment_app:latest

# Docker Compose
docker-compose up -d

# Kubernetes
kubectl apply -f kubernetes/
```

## Links

- **Docker Hub**: https://hub.docker.com/r/rafaydevsinc/assignment_app
- **Image**: `docker pull rafaydevsinc/assignment_app:latest`
- **Repository**: Public (anyone can pull)

---

✅ Your image is on Docker Hub and ready to use!

Both Docker Compose and Kubernetes are configured to pull from Docker Hub.
