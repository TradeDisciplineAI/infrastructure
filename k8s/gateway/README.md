# Kubernetes Gateway API & NGINX Gateway Fabric Infrastructure

This directory contains the Kubernetes Gateway API manifests, TLS certificate configurations, and setup instructions for external HTTP & HTTPS traffic routing on the live Azure AKS cluster (`trading-aks`).

---

## Component Specifications & Pinned Versions

- **Kubernetes Gateway API Specification:** `v1.2.0` (Standard Channel)
- **Gateway Controller:** NGINX Gateway Fabric `v1.6.0` (`ghcr.io/nginx/nginx-gateway-fabric:1.6.0`)
- **Cert-Manager Version:** `v1.16.2` (with `--enable-gateway-api` flag enabled)
- **ACME TLS Provider:** Let's Encrypt Production (`ClusterIssuer` `letsencrypt-prod`)
- **Public Hostname:** `tradingcopilot.duckdns.org` $\rightarrow$ `48.217.133.140`
- **GatewayClass Name:** `nginx` (`gateway.nginx.org/nginx-gateway-controller`)
- **Gateway Namespace:** `gateway-system`
- **Controller Namespace:** `nginx-gateway`
- **Cert-Manager Namespace:** `cert-manager`

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

### 3. Install cert-manager (v1.16.2) with Gateway API Support
```bash
# Install cert-manager release manifest
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.16.2/cert-manager.yaml

# Enable Gateway API feature flag on cert-manager controller
kubectl patch deployment cert-manager -n cert-manager --type=json -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--enable-gateway-api"}]'
```

### 4. Deploy Platform Gateway, TLS Certificates & Routes
```bash
kubectl apply -f namespace.yaml
kubectl apply -f clusterissuer.yaml
kubectl apply -f gateway.yaml
kubectl apply -f certificate.yaml
kubectl apply -f referencegrants.yaml
kubectl apply -f httproutes.yaml
```

---

## Route Topology & Path Mapping

| Protocol | Path Match Prefix | Target Microservice | Namespace | Target Service Port | Service Type |
| :---: | :--- | :--- | :---: | :---: | :---: |
| HTTP/HTTPS | `/auth/*` | `auth-app` | `authentication` | `8000` | `ClusterIP` |
| HTTP/HTTPS | `/dashboard/*`, `/portfolio/*`, `/alerts/*` | `market-service` | `market-service` | `8001` | `ClusterIP` |
| HTTP/HTTPS | `/ai-usage`, `/analyze-news`, `/agent3/*`, `/agent6/*`, `/trade-proposals/*` | `ai-service` | `ai-service` | `8002` | `ClusterIP` |

---

## TLS Certificate & Renewal Management

- **TLS Secret Name:** `tradingcopilot-tls` (managed automatically by cert-manager in `gateway-system`)
- **Challenge Solver:** ACME HTTP-01 via Gateway API
- **Automatic Renewal:** Scheduled automatically 30 days prior to certificate expiration.
