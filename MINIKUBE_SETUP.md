# Minikube Setup Complete ✅

## Installation Summary

**Status**: ✅ Successfully installed and running

### Components Installed:
- ✅ **Minikube**: v1.37.0
- ✅ **kubectl**: v1.35.0  
- ✅ **Docker Desktop**: Running
- ✅ **Kubernetes**: v1.34.0

### Configuration:
- **Driver**: Docker (containerized)
- **CPUs**: 2
- **Memory**: 4000MB
- **Container Name**: minikube

## Verify Installation

```bash
# Check Minikube status
minikube status

# Check Kubernetes nodes
kubectl get nodes

# Check Minikube Docker container
docker ps --filter "name=minikube"

# Get Minikube IP
minikube ip
```

## Current Status

```
minikube
├── type: Control Plane
├── host: Running ✅
├── kubelet: Running ✅
├── apiserver: Running ✅
└── kubeconfig: Configured ✅
```

## Quick Commands

### Start/Stop
```bash
# Start Minikube
minikube start

# Stop Minikube
minikube stop

# Delete cluster
minikube delete

# Restart
minikube delete && minikube start --driver=docker
```

### Access
```bash
# Get Minikube IP
minikube ip

# SSH into Minikube
minikube ssh

# Open dashboard
minikube dashboard
```

### Docker Integration
```bash
# Use Minikube's Docker daemon
eval $(minikube docker-env)

# Build images for Minikube
docker build -t myapp:latest .

# List images in Minikube
docker images

# Return to host Docker daemon
eval $(minikube docker-env -u)
```

### Service Access
```bash
# List services
minikube service list

# Get service URL
minikube service <service-name> --url

# Open service in browser
minikube service <service-name>

# Create tunnel (for LoadBalancer services)
minikube tunnel
```

## Deploy Your Flask App

Now that Minikube is running, deploy your app:

```bash
# Navigate to kubernetes directory
cd kubernetes

# Run deployment script
./deploy.sh

# Or deploy manually
kubectl apply -f kubernetes/

# Access the app
minikube service flask-app-service
```

## Troubleshooting

### Minikube not starting
```bash
# Check Docker is running
docker ps

# Delete and recreate
minikube delete
minikube start --driver=docker
```

### Can't connect to cluster
```bash
# Update kubeconfig
minikube update-context

# Check kubectl context
kubectl config current-context
```

### Resource issues
```bash
# Start with more resources
minikube start --driver=docker --cpus=4 --memory=8192
```

### Clean slate
```bash
# Remove everything and start fresh
minikube delete
docker system prune -a
minikube start --driver=docker
```

## Addons

Enable useful Minikube addons:

```bash
# View available addons
minikube addons list

# Enable dashboard
minikube addons enable dashboard

# Enable metrics-server
minikube addons enable metrics-server

# Enable ingress
minikube addons enable ingress
```

## Configuration

```bash
# Set default driver
minikube config set driver docker

# Set default CPUs
minikube config set cpus 4

# Set default memory
minikube config set memory 8192

# Disable update notifications
minikube config set WantUpdateNotification false
```

## Next Steps

1. **Deploy your Flask app**:
   ```bash
   cd kubernetes
   ./deploy.sh
   ```

2. **Access the application**:
   ```bash
   minikube service flask-app-service
   ```

3. **View logs**:
   ```bash
   kubectl logs -l app=flask-app -f
   ```

4. **Scale deployment**:
   ```bash
   kubectl scale deployment flask-app --replicas=3
   ```

## Useful Links

- Minikube Dashboard: `minikube dashboard`
- Your Flask App: `http://192.168.49.2:30001/` (after deployment)
- Kubernetes Dashboard: `http://127.0.0.1:xxxxx/` (from dashboard command)

## System Information

```
Host OS: macOS 15.7.2
Docker Version: Docker Desktop (latest)
Minikube Driver: Docker (containerized)
Kubernetes Version: v1.34.0
Storage Class: standard (default)
Network: bridge CNI
```

---

✅ **Your Minikube environment is ready to use!**

Run `cd kubernetes && ./deploy.sh` to deploy your Flask Task Management App.
