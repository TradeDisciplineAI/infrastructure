# Kubernetes Gateway API & NGINX Gateway Fabric Infrastructure

This directory contains the Kubernetes Gateway API manifests and setup instructions for external traffic routing on the live Azure AKS cluster (`trading-aks`).

---

## Component Specifications & Pinned Versions

- **Kubernetes Gateway API Specification:** `v1.2.0` (Standard Channel)
- **Gateway Controller:** NGINX Gateway Fabric `v1.6.0`
- **GatewayClass Name:** `nginx` (`gateway.nginx.org/nginx-gateway-controller`)
- **Gateway Namespace:** `gateway-system`
- **Controller Namespace:** `nginx-gateway`

---

## Reproducible Cluster Installation Steps

### 1. Install Standard Kubernetes Gateway API CRDs (v1.2.0)
```bash
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.2.0/standard-install.yaml
```

### 2. Install NGINX Gateway Fabric Controller (v1.6.0)
```bash
# Install NGINX Gateway Fabric CRDs
kubectl apply -f https://raw.githubusercontent.com/nginx/nginx-gateway-fabric/v1.6.0/deploy/crds.yaml

# Install NGINX Gateway Fabric Controller Deployment & GatewayClass 'nginx'
kubectl apply -f https://raw.githubusercontent.com/nginx/nginx-gateway-fabric/v1.6.0/deploy/default/deploy.yaml
```

### 3. Deploy Platform Gateway & Routes
```bash
kubectl apply -f namespace.yaml
kubectl apply -f gateway.yaml
kubectl apply -f referencegrants.yaml
kubectl apply -f httproutes.yaml
```

---

## Route Topology & Path Mapping

| Path Match Prefix | Target Microservice | Namespace | Target Service Port | Service Type |
| :--- | :--- | :---: | :---: | :---: |
| `/auth/*` | `auth-app` | `authentication` | `8000` | `ClusterIP` |
| `/dashboard/*`, `/portfolio/*`, `/alerts/*` | `market-service` | `market-service` | `8001` | `ClusterIP` |
| `/ai-usage`, `/analyze-news`, `/agent3/*`, `/agent6/*`, `/trade-proposals/*` | `ai-service` | `ai-service` | `8002` | `ClusterIP` |

---

## Cross-Namespace Authorization (`ReferenceGrant`)

Each target namespace (`authentication`, `market-service`, `ai-service`) contains a `ReferenceGrant` allowing `HTTPRoute` objects in namespace `gateway-system` to bind to `Service` endpoints.
