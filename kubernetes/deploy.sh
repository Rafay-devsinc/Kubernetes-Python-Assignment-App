#!/bin/bash

# Kubernetes Deployment Script for Minikube

set -e

echo "🚀 Deploying Flask App to Kubernetes (Minikube)"
echo "================================================"
echo ""

# Check if minikube is running
if ! minikube status > /dev/null 2>&1; then
    echo "❌ Minikube is not running!"
    echo "Start minikube with: minikube start"
    exit 1
fi

echo "✅ Minikube is running"
echo ""

# Using Docker Hub image (no local build needed)
echo "📦 Using image from Docker Hub: rafaydevsinc/assignment_app:latest"
echo ""

# Apply Kubernetes manifests
echo "🔧 Applying Kubernetes manifests..."
echo ""

echo "1️⃣  Creating ConfigMap..."
kubectl apply -f configmap.yaml

echo "2️⃣  Creating Secret..."
kubectl apply -f secret.yaml

echo "3️⃣  Creating PersistentVolumeClaim..."
kubectl apply -f pvc.yaml

echo "4️⃣  Creating Deployment..."
kubectl apply -f deployment.yaml

echo "5️⃣  Creating Service..."
kubectl apply -f service.yaml

echo ""
echo "✅ All resources created successfully!"
echo ""

# Wait for deployment to be ready
echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=flask-app --timeout=120s

echo ""
echo "✅ Deployment successful!"
echo ""

# Display status
echo "📊 Current Status:"
echo "=================="
kubectl get all
echo ""

# Get service URL
echo "🌐 Access your application:"
echo "==========================="
minikube service flask-app-service --url
echo ""
echo "Or open in browser:"
echo "  minikube service flask-app-service"
echo ""
