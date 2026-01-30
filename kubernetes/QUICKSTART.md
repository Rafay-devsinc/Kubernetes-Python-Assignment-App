# Kubernetes Quick Start (Minikube)

## 🚀 Deploy in 3 Commands

```bash
# 1. Start minikube
minikube start

# 2. Deploy the app
cd kubernetes
./deploy.sh

# 3. Open in browser
minikube service flask-app-service
```

## 📋 Files Overview

| File | Purpose |
|------|---------|
| `deployment.yaml` | Defines pods (2 replicas) with health checks |
| `service.yaml` | Exposes app on NodePort 30001 |
| `configmap.yaml` | Non-sensitive config (APP_NAME, APP_ENV) |
| `secret.yaml` | Sensitive data (DATABASE_URL, SECRET_KEY) |
| `pvc.yaml` | Persistent storage for logs (1Gi) |
| `deploy.sh` | Automated deployment script |
| `README.md` | Comprehensive deployment guide |

## 🔧 Common Commands

### Deploy
```bash
# Using script
./deploy.sh

# Manual
kubectl apply -f kubernetes/
```

### Check Status
```bash
kubectl get all
kubectl get pods
kubectl logs -l app=flask-app
```

### Access App
```bash
# Get URL
minikube service flask-app-service --url

# Open browser
minikube service flask-app-service
```

### Scale
```bash
kubectl scale deployment flask-app --replicas=3
```

### Update Code
```bash
eval $(minikube docker-env)
docker build -t flask-app:latest .
kubectl rollout restart deployment flask-app
```

### Clean Up
```bash
kubectl delete -f kubernetes/
minikube stop
```

## 📊 Architecture

```
                    ┌─────────────────┐
                    │  Minikube Node  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  NodePort Svc   │
                    │   Port: 30001   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   Deployment    │
                    │   (2 replicas)  │
                    └────────┬────────┘
                             │
            ┌────────────────┴────────────────┐
            │                                  │
      ┌─────▼─────┐                     ┌─────▼─────┐
      │  Pod #1   │                     │  Pod #2   │
      │ flask-app │                     │ flask-app │
      └─────┬─────┘                     └─────┬─────┘
            │                                  │
            └──────────┬──────────────────────┘
                       │
                ┌──────▼──────┐
                │ PVC (Logs)  │
                │    1Gi      │
                └─────────────┘
```

## 🎯 What Each Component Does

- **Deployment**: Manages 2 Flask pods with auto-restart
- **Service**: Load balances traffic across pods
- **ConfigMap**: Stores APP_NAME and APP_ENV
- **Secret**: Stores DATABASE_URL and SECRET_KEY
- **PVC**: Persistent storage for application logs

## 🔍 Troubleshooting

### Pods stuck in pending
```bash
kubectl describe pod <pod-name>
```

### Image not found
```bash
eval $(minikube docker-env)
docker build -t flask-app:latest .
```

### Service not accessible
```bash
minikube service list
minikube tunnel  # if needed
```

### View detailed logs
```bash
kubectl logs -l app=flask-app --all-containers=true
```

## 🌐 Application URLs

Once deployed, access via `minikube service flask-app-service --url`:

- `/` - Home page
- `/assignment` - Task management
- `/stats` - Statistics dashboard
- `/logs` - Application logs

## 📝 Notes

- Default: 2 replicas for HA
- SQLite database (portable)
- Logs persist across restarts
- Health checks configured
- Resource limits set
