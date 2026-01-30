# Kubernetes Deployment Guide (Minikube)

This guide will help you deploy the Flask Task Management App on Kubernetes using Minikube.

## Prerequisites

1. **Minikube installed**:
   ```bash
   brew install minikube
   ```

2. **kubectl installed**:
   ```bash
   brew install kubectl
   ```

3. **Docker Desktop running** (for building images)

## Step 1: Start Minikube

```bash
# Start minikube
minikube start

# Verify it's running
minikube status

# Enable minikube dashboard (optional)
minikube dashboard
```

## Step 2: Build Docker Image

Build the Docker image in minikube's Docker environment:

```bash
# Point your terminal to use minikube's Docker daemon
eval $(minikube docker-env)

# Build the image (from project root)
docker build -t flask-app:latest .

# Verify the image
docker images | grep flask-app
```

## Step 3: Deploy to Kubernetes

Apply the Kubernetes manifests in order:

```bash
# 1. Create ConfigMap (application configuration)
kubectl apply -f kubernetes/configmap.yaml

# 2. Create Secret (sensitive data)
kubectl apply -f kubernetes/secret.yaml

# 3. Create PersistentVolumeClaim (for logs)
kubectl apply -f kubernetes/pvc.yaml

# 4. Create Deployment (pods)
kubectl apply -f kubernetes/deployment.yaml

# 5. Create Service (expose the app)
kubectl apply -f kubernetes/service.yaml
```

Or apply all at once:

```bash
kubectl apply -f kubernetes/
```

## Step 4: Verify Deployment

Check if everything is running:

```bash
# Check pods
kubectl get pods

# Check services
kubectl get services

# Check deployments
kubectl get deployments

# Check PVC
kubectl get pvc

# View pod logs
kubectl logs -l app=flask-app

# Describe deployment (for troubleshooting)
kubectl describe deployment flask-app
```

## Step 5: Access the Application

Get the Minikube IP and access the app:

```bash
# Get minikube IP
minikube ip

# Access the app at:
# http://<minikube-ip>:30001/
```

Or use minikube service command:

```bash
# This will automatically open in your browser
minikube service flask-app-service

# Or get the URL
minikube service flask-app-service --url
```

## Application Endpoints

Once deployed, access these URLs:

- **Home**: `http://<minikube-ip>:30001/`
- **Task Management**: `http://<minikube-ip>:30001/assignment`
- **Statistics**: `http://<minikube-ip>:30001/stats`
- **Logs**: `http://<minikube-ip>:30001/logs`

## Architecture Overview

### Components:

1. **Deployment** (`deployment.yaml`):
   - 2 replicas for high availability
   - Resource limits: 256Mi memory, 500m CPU
   - Health checks (liveness and readiness probes)
   - Persistent volume for logs

2. **Service** (`service.yaml`):
   - Type: NodePort (port 30001)
   - Routes traffic to Flask pods

3. **ConfigMap** (`configmap.yaml`):
   - Non-sensitive configuration (APP_NAME, APP_ENV)

4. **Secret** (`secret.yaml`):
   - Sensitive data (DATABASE_URL, SECRET_KEY)

5. **PersistentVolumeClaim** (`pvc.yaml`):
   - 1Gi storage for logs
   - Persists across pod restarts

## Scaling

Scale the deployment up or down:

```bash
# Scale to 3 replicas
kubectl scale deployment flask-app --replicas=3

# Verify
kubectl get pods
```

## Updating the Application

After making code changes:

```bash
# 1. Rebuild the image (with minikube docker-env)
eval $(minikube docker-env)
docker build -t flask-app:latest .

# 2. Restart the deployment
kubectl rollout restart deployment flask-app

# 3. Check rollout status
kubectl rollout status deployment flask-app
```

## Viewing Logs

```bash
# Logs from all pods
kubectl logs -l app=flask-app

# Logs from specific pod
kubectl logs <pod-name>

# Stream logs
kubectl logs -f -l app=flask-app

# Previous pod logs (if crashed)
kubectl logs <pod-name> --previous
```

## Troubleshooting

### Pods not starting:

```bash
# Check pod status
kubectl get pods

# Describe pod for events
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>
```

### Image pull errors:

Make sure you built the image in minikube's Docker environment:

```bash
eval $(minikube docker-env)
docker build -t flask-app:latest .
```

### Service not accessible:

```bash
# Check service
kubectl get svc flask-app-service

# Use minikube tunnel (if needed)
minikube tunnel
```

### PVC issues:

```bash
# Check PVC status
kubectl get pvc

# Check PV
kubectl get pv
```

## Cleanup

Remove all resources:

```bash
# Delete all resources
kubectl delete -f kubernetes/

# Or delete individually
kubectl delete deployment flask-app
kubectl delete service flask-app-service
kubectl delete configmap flask-config
kubectl delete secret flask-secrets
kubectl delete pvc flask-logs-pvc

# Stop minikube
minikube stop

# Delete minikube cluster
minikube delete
```

## Production Considerations

For production deployments, consider:

1. **Use PostgreSQL** instead of SQLite:
   - Deploy PostgreSQL as a StatefulSet
   - Update DATABASE_URL in secret

2. **Ingress** instead of NodePort:
   - Set up Ingress controller
   - Configure domain routing

3. **Resource limits**:
   - Adjust based on actual usage
   - Monitor with metrics

4. **Secrets management**:
   - Use external secret managers (e.g., Vault)
   - Don't commit secrets to Git

5. **Persistent storage**:
   - Use proper storage class
   - Configure backup strategy

6. **Monitoring**:
   - Add Prometheus/Grafana
   - Set up alerts

## Quick Reference

```bash
# Start everything
minikube start
eval $(minikube docker-env)
docker build -t flask-app:latest .
kubectl apply -f kubernetes/
minikube service flask-app-service

# Check status
kubectl get all

# View logs
kubectl logs -l app=flask-app -f

# Clean up
kubectl delete -f kubernetes/
minikube stop
```
