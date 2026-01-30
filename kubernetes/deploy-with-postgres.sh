#!/bin/bash

# Kubernetes Deployment Script with PostgreSQL for Minikube

set -e

echo "🚀 Deploying Flask App + PostgreSQL to Kubernetes (Minikube)"
echo "=============================================================="
echo ""

# Check if minikube is running
if ! minikube status > /dev/null 2>&1; then
    echo "❌ Minikube is not running!"
    echo "Start minikube with: minikube start"
    exit 1
fi

echo "✅ Minikube is running"
echo ""

# Build Docker image in minikube environment
echo "📦 Building Docker image..."
eval $(minikube docker-env)
docker build -t flask-app:latest ..
echo "✅ Docker image built successfully"
echo ""

# Apply Kubernetes manifests
echo "🔧 Applying Kubernetes manifests..."
echo ""

echo "1️⃣  Creating PostgreSQL Secret..."
kubectl apply -f postgres-secret.yaml

echo "2️⃣  Creating PostgreSQL PVC..."
kubectl apply -f postgres-pvc.yaml

echo "3️⃣  Creating PostgreSQL Deployment..."
kubectl apply -f postgres-deployment.yaml

echo "4️⃣  Creating PostgreSQL Service..."
kubectl apply -f postgres-service.yaml

echo "⏳ Waiting for PostgreSQL to be ready..."
kubectl wait --for=condition=ready pod -l app=postgres --timeout=120s
echo "✅ PostgreSQL is ready"
echo ""

echo "5️⃣  Creating Flask ConfigMap..."
kubectl apply -f configmap.yaml

echo "6️⃣  Creating Flask Secret..."
kubectl apply -f secret.yaml

echo "7️⃣  Creating Flask Logs PVC..."
kubectl apply -f pvc.yaml

echo "8️⃣  Creating Flask Deployment..."
kubectl apply -f deployment.yaml

echo "9️⃣  Creating Flask Service..."
kubectl apply -f service.yaml

echo ""
echo "✅ All resources created successfully!"
echo ""

# Wait for Flask deployment to be ready
echo "⏳ Waiting for Flask pods to be ready..."
kubectl wait --for=condition=ready pod -l app=flask-app --timeout=120s

echo ""
echo "✅ Deployment successful!"
echo ""

# Display status
echo "📊 Current Status:"
echo "=================="
kubectl get all
echo ""
kubectl get pvc
echo ""

# Get service URL
echo "🌐 Access your application:"
echo "==========================="
minikube service flask-app-service --url
echo ""
echo "Or open in browser:"
echo "  minikube service flask-app-service"
echo ""

echo "📊 PostgreSQL Info:"
echo "==================="
echo "Database: assignment_db"
echo "User: postgres"
echo "Service: postgres-service:5432"
echo ""
echo "To connect to PostgreSQL:"
echo "  kubectl exec -it <postgres-pod-name> -- psql -U postgres -d assignment_db"
echo ""
