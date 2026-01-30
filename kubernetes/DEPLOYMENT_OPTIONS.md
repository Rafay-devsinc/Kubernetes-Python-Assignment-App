# Kubernetes Deployment Options

## Two Deployment Modes

### Option 1: SQLite (Simple) ⚡
**Script**: `./deploy.sh`

- Flask app with SQLite database
- Database stored in each pod
- No external database needed
- Fast and simple

### Option 2: PostgreSQL (Production-Ready) 🐘
**Script**: `./deploy-with-postgres.sh`

- Flask app with PostgreSQL database
- Separate PostgreSQL pod
- Persistent database storage
- Production-ready architecture

---

## Comparison

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| **Setup Complexity** | ⭐ Simple | ⭐⭐ Moderate |
| **Performance** | Good for low traffic | Better for high traffic |
| **Data Persistence** | Per-pod | Centralized |
| **Scaling** | Limited | Excellent |
| **Production Ready** | Development only | Yes |
| **Resource Usage** | Low | Medium |
| **Deployment Time** | ~30 seconds | ~60 seconds |
| **Storage** | 1Gi (logs only) | 6Gi (5Gi DB + 1Gi logs) |
| **Components** | 5 resources | 9 resources |

---

## Option 1: SQLite Deployment

### Architecture
```
minikube
  └── NodePort Service (30001)
       └── Flask Deployment (2 pods)
            ├── Pod 1 (SQLite in pod)
            └── Pod 2 (SQLite in pod)
```

### Components
1. ConfigMap (app config)
2. Secret (connection string)
3. PVC (logs - 1Gi)
4. Deployment (2 Flask replicas)
5. Service (NodePort 30001)

### Deploy
```bash
cd kubernetes
./deploy.sh
```

### Use Cases
- ✅ Development
- ✅ Testing
- ✅ Demos
- ✅ Learning Kubernetes
- ❌ Production
- ❌ High traffic

### Pros
- Fast deployment
- No database management
- Low resource usage
- Simple troubleshooting

### Cons
- Data not shared between pods
- Limited scalability
- Not production-ready
- Data lost if pod restarts

---

## Option 2: PostgreSQL Deployment

### Architecture
```
minikube
  └── NodePort Service (30001)
       └── Flask Deployment (2 pods)
            ├── Pod 1 ──┐
            └── Pod 2 ──┤
                        ├──> ClusterIP Service
                        │         ↓
                        │    PostgreSQL Pod
                        │         ↓
                        └──> PVC (5Gi)
```

### Components
1. **PostgreSQL**:
   - postgres-secret (password)
   - postgres-pvc (5Gi storage)
   - postgres-deployment (1 replica)
   - postgres-service (ClusterIP)

2. **Flask App**:
   - configmap (app config)
   - secret (DB connection)
   - pvc (logs - 1Gi)
   - deployment (2 Flask replicas)
   - service (NodePort 30001)

### Deploy
```bash
cd kubernetes
./deploy-with-postgres.sh
```

### Use Cases
- ✅ Production
- ✅ High traffic
- ✅ Data persistence critical
- ✅ Multiple replicas needed
- ✅ Real-world applications
- ✅ Team collaboration

### Pros
- Production-ready
- Centralized data
- Better performance
- Proper data persistence
- Scalable
- Industry standard

### Cons
- More complex setup
- Higher resource usage
- Requires DB maintenance
- Longer deployment time

---

## Quick Decision Guide

### Choose SQLite if:
- 🎓 Learning Kubernetes
- 🧪 Testing features
- 💻 Development environment
- ⚡ Need quick setup
- 📱 Low traffic expected

### Choose PostgreSQL if:
- 🏢 Production deployment
- 📈 Expecting traffic
- 💾 Data persistence critical
- 👥 Multiple users
- 🔄 Need to scale

---

## Resource Requirements

### SQLite Deployment
```yaml
Flask Pods (2x):
  CPU: 100m request, 500m limit
  Memory: 128Mi request, 256Mi limit

Total:
  CPU: 200m-1000m
  Memory: 256Mi-512Mi
  Storage: 1Gi
```

### PostgreSQL Deployment
```yaml
Flask Pods (2x):
  CPU: 100m request, 500m limit
  Memory: 128Mi request, 256Mi limit

PostgreSQL (1x):
  CPU: 250m request, 500m limit
  Memory: 256Mi request, 512Mi limit

Total:
  CPU: 450m-1500m
  Memory: 512Mi-1024Mi
  Storage: 6Gi (5Gi DB + 1Gi logs)
```

---

## Migration Between Options

### SQLite → PostgreSQL

```bash
# 1. Delete SQLite deployment
kubectl delete -f deployment.yaml
kubectl delete -f service.yaml
kubectl delete -f secret.yaml

# 2. Deploy PostgreSQL
./deploy-with-postgres.sh
```

### PostgreSQL → SQLite

```bash
# 1. Backup data (if needed)
kubectl exec <postgres-pod> -- pg_dump -U postgres assignment_db > backup.sql

# 2. Delete PostgreSQL
kubectl delete -f postgres-service.yaml
kubectl delete -f postgres-deployment.yaml
kubectl delete -f postgres-pvc.yaml
kubectl delete -f postgres-secret.yaml

# 3. Update Flask secret for SQLite
# Edit secret.yaml to use sqlite:///assignment.db

# 4. Redeploy Flask
kubectl apply -f secret.yaml
kubectl rollout restart deployment flask-app
```

---

## File Structure

```
kubernetes/
├── SQLite (5 files)
│   ├── configmap.yaml
│   ├── secret.yaml          # Uses sqlite://
│   ├── pvc.yaml
│   ├── deployment.yaml
│   └── service.yaml
│
├── PostgreSQL (4 additional files)
│   ├── postgres-deployment.yaml
│   ├── postgres-service.yaml
│   ├── postgres-pvc.yaml
│   └── postgres-secret.yaml
│
├── Deployment Scripts
│   ├── deploy.sh                    # SQLite
│   └── deploy-with-postgres.sh      # PostgreSQL
│
└── Documentation
    ├── README.md
    ├── QUICKSTART.md
    ├── POSTGRES.md
    └── DEPLOYMENT_OPTIONS.md (this file)
```

---

## Testing Both Options

### Test SQLite
```bash
# Deploy
./deploy.sh

# Test
minikube service flask-app-service
# Create some tasks

# Check data (in pod)
kubectl exec -it <flask-pod> -- ls -la assignment.db
```

### Test PostgreSQL
```bash
# Switch to PostgreSQL
kubectl delete -f deployment.yaml service.yaml secret.yaml
./deploy-with-postgres.sh

# Test
minikube service flask-app-service
# Create some tasks

# Check data (in PostgreSQL)
kubectl exec -it <postgres-pod> -- psql -U postgres -d assignment_db -c "SELECT * FROM tasks;"
```

---

## Recommended Setup

**For this assignment**: Start with **SQLite** to understand Kubernetes basics, then upgrade to **PostgreSQL** to learn database integration.

**For production**: Always use **PostgreSQL** or managed database services.

---

## Commands Cheat Sheet

### SQLite Deployment
```bash
cd kubernetes
./deploy.sh                           # Deploy
minikube service flask-app-service    # Access
kubectl logs -l app=flask-app         # Logs
kubectl delete -f .                   # Clean up
```

### PostgreSQL Deployment
```bash
cd kubernetes
./deploy-with-postgres.sh             # Deploy
minikube service flask-app-service    # Access
kubectl logs -l app=flask-app         # Flask logs
kubectl logs -l app=postgres          # DB logs
kubectl exec -it <postgres-pod> -- psql -U postgres -d assignment_db  # DB access
kubectl delete -f .                   # Clean up
```

---

✅ Both deployment options are ready to use!

Choose based on your needs and learning goals.
