# PostgreSQL Deployment on Kubernetes

## Overview

This setup includes a full PostgreSQL database deployment alongside your Flask application in Kubernetes.

## Architecture

```
Flask App Pods (2 replicas)
        ↓
    ClusterIP Service
        ↓
PostgreSQL Pod (1 replica)
        ↓
PersistentVolume (5Gi)
```

## Files

| File | Purpose |
|------|---------|
| `postgres-deployment.yaml` | PostgreSQL pod definition |
| `postgres-service.yaml` | ClusterIP service for database |
| `postgres-pvc.yaml` | Persistent storage (5Gi) |
| `postgres-secret.yaml` | Database password |
| `deploy-with-postgres.sh` | Automated deployment script |

## Quick Deploy

```bash
# Deploy everything (PostgreSQL + Flask)
cd kubernetes
./deploy-with-postgres.sh
```

## Manual Deployment

Deploy in this specific order:

```bash
# 1. PostgreSQL resources
kubectl apply -f postgres-secret.yaml
kubectl apply -f postgres-pvc.yaml
kubectl apply -f postgres-deployment.yaml
kubectl apply -f postgres-service.yaml

# Wait for PostgreSQL to be ready
kubectl wait --for=condition=ready pod -l app=postgres --timeout=120s

# 2. Flask application
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f pvc.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

## Configuration

### Database Settings

- **Database Name**: `assignment_db`
- **User**: `postgres`
- **Password**: `postgres` (stored in `postgres-secret.yaml`)
- **Port**: `5432`
- **Service Name**: `postgres-service`

### Connection String

Flask apps connect using:
```
postgresql://postgres:postgres@postgres-service:5432/assignment_db
```

This is automatically configured in `secret.yaml`.

### Storage

- **Volume Size**: 5Gi
- **Storage Class**: standard (minikube default)
- **Access Mode**: ReadWriteOnce
- **Mount Path**: `/var/lib/postgresql/data`

## Verify PostgreSQL

```bash
# Check PostgreSQL pod
kubectl get pods -l app=postgres

# Check PostgreSQL service
kubectl get svc postgres-service

# Check PVC
kubectl get pvc postgres-pvc

# View PostgreSQL logs
kubectl logs -l app=postgres

# Check if PostgreSQL is ready
kubectl exec -it <postgres-pod-name> -- pg_isready -U postgres
```

## Access PostgreSQL

### From within cluster (Flask pods)

Flask automatically connects using the service name:
```
postgres-service:5432
```

### From kubectl

```bash
# Get pod name
kubectl get pods -l app=postgres

# Connect to PostgreSQL CLI
kubectl exec -it <postgres-pod-name> -- psql -U postgres -d assignment_db

# Run SQL commands directly
kubectl exec -it <postgres-pod-name> -- psql -U postgres -d assignment_db -c "SELECT * FROM tasks;"
```

### Port forwarding (from local machine)

```bash
# Forward PostgreSQL port to localhost
kubectl port-forward service/postgres-service 5432:5432

# Then connect from your machine
psql -h localhost -U postgres -d assignment_db
# or
python3 app.py  # With DATABASE_URL pointing to localhost
```

## Database Operations

### Check Tables

```bash
kubectl exec -it <postgres-pod-name> -- psql -U postgres -d assignment_db -c "\dt"
```

### View Tasks

```bash
kubectl exec -it <postgres-pod-name> -- psql -U postgres -d assignment_db -c "SELECT * FROM tasks;"
```

### Backup Database

```bash
# Create backup
kubectl exec <postgres-pod-name> -- pg_dump -U postgres assignment_db > backup.sql

# Restore backup
cat backup.sql | kubectl exec -i <postgres-pod-name> -- psql -U postgres -d assignment_db
```

### Reset Database

```bash
# Drop and recreate database
kubectl exec -it <postgres-pod-name> -- psql -U postgres -c "DROP DATABASE assignment_db;"
kubectl exec -it <postgres-pod-name> -- psql -U postgres -c "CREATE DATABASE assignment_db;"

# Restart Flask pods to reinitialize tables
kubectl rollout restart deployment flask-app
```

## Monitoring

### Check Health

```bash
# PostgreSQL health check
kubectl exec <postgres-pod-name> -- pg_isready -U postgres

# View resource usage
kubectl top pod -l app=postgres
```

### View Logs

```bash
# Real-time logs
kubectl logs -f -l app=postgres

# Last 100 lines
kubectl logs -l app=postgres --tail=100
```

## Scaling Considerations

### Current Setup (Single Replica)

- 1 PostgreSQL pod
- Good for development/testing
- Data persists via PVC

### Production Considerations

For production, consider:

1. **High Availability**:
   - Use StatefulSet instead of Deployment
   - Set up PostgreSQL replication
   - Use multiple replicas

2. **Backup Strategy**:
   - Regular automated backups
   - Point-in-time recovery
   - Off-cluster backup storage

3. **Security**:
   - Strong passwords
   - Network policies
   - Encrypted connections (SSL/TLS)

4. **Monitoring**:
   - Database metrics
   - Query performance
   - Connection pooling

5. **Resources**:
   - Adjust CPU/Memory based on load
   - Use appropriate storage class
   - Consider using cloud-managed databases

## Troubleshooting

### Pod not starting

```bash
# Check events
kubectl describe pod <postgres-pod-name>

# Check logs
kubectl logs <postgres-pod-name>

# Check PVC
kubectl describe pvc postgres-pvc
```

### Connection refused

```bash
# Verify service
kubectl get svc postgres-service

# Check if pod is ready
kubectl get pods -l app=postgres

# Test connection from Flask pod
kubectl exec -it <flask-pod-name> -- nc -zv postgres-service 5432
```

### Data not persisting

```bash
# Check PVC is bound
kubectl get pvc postgres-pvc

# Verify volume mount
kubectl describe pod <postgres-pod-name> | grep -A 5 Mounts
```

### Password issues

```bash
# Check secret
kubectl get secret postgres-secret -o yaml

# Update password
kubectl delete secret postgres-secret
kubectl apply -f postgres-secret.yaml
kubectl rollout restart deployment postgres
```

## Clean Up

```bash
# Delete PostgreSQL resources
kubectl delete -f postgres-service.yaml
kubectl delete -f postgres-deployment.yaml
kubectl delete -f postgres-pvc.yaml
kubectl delete -f postgres-secret.yaml

# Delete everything including Flask
kubectl delete -f kubernetes/
```

⚠️ **Warning**: Deleting the PVC will permanently delete all database data!

## Resource Specifications

### PostgreSQL Pod

```yaml
Resources:
  Requests:
    CPU: 250m
    Memory: 256Mi
  Limits:
    CPU: 500m
    Memory: 512Mi

Health Checks:
  Liveness: pg_isready (every 10s)
  Readiness: pg_isready (every 5s)
```

## Environment Variables

Set in `postgres-deployment.yaml`:

- `POSTGRES_DB`: Database name
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: From postgres-secret
- `PGDATA`: Data directory path

## Next Steps

1. **Deploy**: `./deploy-with-postgres.sh`
2. **Access app**: `minikube service flask-app-service`
3. **Create tasks**: App will auto-create tables
4. **Verify data**: Check PostgreSQL for stored tasks

Your Flask app now uses a real PostgreSQL database in Kubernetes! 🎉
