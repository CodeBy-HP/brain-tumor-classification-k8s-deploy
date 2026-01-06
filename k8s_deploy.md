# 🚀 Brain Tumor Detection – EKS Deployment Guide

This guide documents the minimal, consistent steps to deploy the Brain Tumor FastAPI application on AWS EKS.

---

## Phase 1 – Prerequisites

### 1. Fix AWS CLI Conflicts

Ensure you are using the official AWS CLI (MSI version).

```powershell
Get-Command aws
pip uninstall awscli
aws --version
```

### 2. Install kubectl

```powershell
Invoke-WebRequest -Uri "https://dl.k8s.io/release/v1.28.2/bin/windows/amd64/kubectl.exe" -OutFile "kubectl.exe"
Move-Item .\kubectl.exe C:\Windows\System32
kubectl version --client
```

### 3. Install eksctl

```powershell
Invoke-WebRequest -Uri "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_Windows_amd64.zip" -OutFile "eksctl.zip"
Expand-Archive .\eksctl.zip .
Move-Item .\eksctl.exe C:\Windows\System32\eksctl.exe
eksctl version
```

---

## Phase 2 – Create EKS Cluster

```powershell
eksctl create cluster `
  --name brain-tumor-cluster `
  --region us-east-1 `
  --version 1.27 `
  --nodegroup-name brain-tumor-nodes `
  --node-type m7i-flex.large `
  --nodes 1 `
  --nodes-min 1 `
  --nodes-max 1 `
  --managed `
  --node-volume-size 30
```

**Note**: 
- PowerShell uses backticks (`` ` ``) for line continuation, not backslashes
- `--version 1.27` specifies a supported Kubernetes version (supported versions: 1.23-1.27)

Configure kubectl:

```powershell
aws eks --region us-east-1 update-kubeconfig --name brain-tumor-cluster
kubectl get nodes
```

---

## Phase 3 – Kubernetes Manifests

Create `deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: brain-tumor-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: brain-tumor-app
  template:
    metadata:
      labels:
        app: brain-tumor-app
    spec:
      containers:
      - name: brain-tumor-app
        image: <YOUR_ECR_REGISTRY>/<YOUR_ECR_REPOSITORY>:latest
        ports:
        - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: brain-tumor-service
spec:
  type: LoadBalancer
  selector:
    app: brain-tumor-app
  ports:
  - port: 8000
    targetPort: 8000
```

Deploy:

```powershell
kubectl apply -f deployment.yaml
kubectl get pods -w
kubectl get svc brain-tumor-service
```

---

## Phase 4 – Security Group

Go to **EC2 Console** → **Security Groups**, find the security group attached to your EKS nodes, and add an inbound rule:
- Type: HTTP (or Custom TCP)
- Port: **80** (LoadBalancer external port)
- Source: 0.0.0.0/0 (or restrict to your IP)

**Note**: The LoadBalancer routes external port 80 → internal container port 8000

---

## Phase 5 – Test Application

Get the LoadBalancer URL:

```powershell
kubectl get svc brain-tumor-service
```

Access your application:
```
http://<EXTERNAL-IP>
```

Or with explicit port:
```
http://<EXTERNAL-IP>:80
```

---

## Phase 6 – Cleanup

```powershell
kubectl delete deployment brain-tumor-app
kubectl delete service brain-tumor-service
eksctl delete cluster --name brain-tumor-cluster --region us-east-1
```

---

## Cost Awareness

| Resource          | Approx Cost  |
| ----------------- | ------------ |
| EKS Control Plane | ~$72/month   |
| t3.medium Node    | ~$0.046/hour |
| LoadBalancer      | ~$0.025/hour |
