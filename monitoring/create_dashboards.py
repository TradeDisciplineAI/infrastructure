import json, os

os.makedirs('infrastructure/monitoring/dashboards', exist_ok=True)

# 1. PLATFORM OVERVIEW DASHBOARD
dashboard_overview = {
    "title": "Trading Discipline AI — Platform Overview",
    "uid": "trading-platform-overview",
    "tags": ["trading-platform", "overview"],
    "timezone": "browser",
    "schemaVersion": 39,
    "refresh": "10s",
    "panels": [
        {
            "id": 1,
            "title": "Cluster CPU Utilization",
            "type": "gauge",
            "gridPos": {"h": 6, "w": 4, "x": 0, "y": 0},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "percent", "min": 0, "max": 100, "thresholds": {"mode": "absolute", "steps": [{"color": "green", "value": None}, {"color": "yellow", "value": 70}, {"color": "red", "value": 85}]}}},
            "targets": [{"expr": '(sum(rate(container_cpu_usage_seconds_total{container!=""}[5m])) / sum(kube_node_status_allocatable{resource="cpu"})) * 100', "legendFormat": "CPU %"}]
        },
        {
            "id": 2,
            "title": "Cluster Memory Utilization",
            "type": "gauge",
            "gridPos": {"h": 6, "w": 4, "x": 4, "y": 0},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "percent", "min": 0, "max": 100, "thresholds": {"mode": "absolute", "steps": [{"color": "green", "value": None}, {"color": "yellow", "value": 75}, {"color": "red", "value": 90}]}}},
            "targets": [{"expr": '(sum(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / sum(node_memory_MemTotal_bytes)) * 100', "legendFormat": "Memory %"}]
        },
        {
            "id": 3,
            "title": "Ready Pods",
            "type": "stat",
            "gridPos": {"h": 6, "w": 4, "x": 8, "y": 0},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"color": {"mode": "thresholds"}, "thresholds": {"mode": "absolute", "steps": [{"color": "green", "value": None}]}}},
            "targets": [{"expr": 'sum(kube_pod_status_ready{condition="true"})', "legendFormat": "Ready Pods"}]
        },
        {
            "id": 4,
            "title": "Deployment Availability",
            "type": "stat",
            "gridPos": {"h": 6, "w": 4, "x": 12, "y": 0},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "percent", "min": 0, "max": 100, "thresholds": {"mode": "absolute", "steps": [{"color": "red", "value": None}, {"color": "yellow", "value": 90}, {"color": "green", "value": 99}]}}},
            "targets": [{"expr": 'sum(kube_deployment_status_replicas_available) / sum(kube_deployment_spec_replicas) * 100', "legendFormat": "Available %"}]
        },
        {
            "id": 5,
            "title": "Pod Restart Count (1h)",
            "type": "stat",
            "gridPos": {"h": 6, "w": 4, "x": 16, "y": 0},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"thresholds": {"mode": "absolute", "steps": [{"color": "green", "value": None}, {"color": "yellow", "value": 1}, {"color": "red", "value": 5}]}}},
            "targets": [{"expr": 'sum(increase(kube_pod_container_status_restarts_total[1h]))', "legendFormat": "Restarts"}]
        },
        {
            "id": 6,
            "title": "Total HTTP Requests / sec",
            "type": "timeseries",
            "gridPos": {"h": 6, "w": 4, "x": 20, "y": 0},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "reqps"}},
            "targets": [{"expr": 'sum(rate(http_requests_total[5m]))', "legendFormat": "req/s"}]
        },
        {
            "id": 7,
            "title": "HTTP 4xx Error Rate",
            "type": "timeseries",
            "gridPos": {"h": 8, "w": 8, "x": 0, "y": 6},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "percent"}},
            "targets": [{"expr": '(sum(rate(http_requests_total{status=~"4.."}[5m])) / sum(rate(http_requests_total[5m]))) * 100 or vector(0)', "legendFormat": "4xx Rate %"}]
        },
        {
            "id": 8,
            "title": "HTTP 5xx Error Rate",
            "type": "timeseries",
            "gridPos": {"h": 8, "w": 8, "x": 8, "y": 6},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "percent"}},
            "targets": [{"expr": '(sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))) * 100 or vector(0)', "legendFormat": "5xx Rate %"}]
        },
        {
            "id": 9,
            "title": "HTTP p95 Latency",
            "type": "timeseries",
            "gridPos": {"h": 8, "w": 8, "x": 16, "y": 6},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "s"}},
            "targets": [{"expr": 'histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))', "legendFormat": "p95 Latency"}]
        },
        {
            "id": 10,
            "title": "Auth Service Request Rate",
            "type": "timeseries",
            "gridPos": {"h": 7, "w": 8, "x": 0, "y": 14},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "reqps"}},
            "targets": [{"expr": 'sum(rate(http_requests_total{namespace="authentication"}[5m])) by (handler)', "legendFormat": "{{handler}}"}]
        },
        {
            "id": 11,
            "title": "Market Service Request Rate",
            "type": "timeseries",
            "gridPos": {"h": 7, "w": 8, "x": 8, "y": 14},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "reqps"}},
            "targets": [{"expr": 'sum(rate(http_requests_total{namespace="market-service"}[5m])) by (handler)', "legendFormat": "{{handler}}"}]
        },
        {
            "id": 12,
            "title": "AI Service Request Rate",
            "type": "timeseries",
            "gridPos": {"h": 7, "w": 8, "x": 16, "y": 14},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "reqps"}},
            "targets": [{"expr": 'sum(rate(http_requests_total{namespace="ai-service"}[5m])) by (handler)', "legendFormat": "{{handler}}"}]
        }
    ]
}

# 2. KUBERNETES INFRASTRUCTURE DASHBOARD
dashboard_k8s = {
    "title": "Trading Discipline AI — Kubernetes Infrastructure",
    "uid": "trading-k8s-infrastructure",
    "tags": ["trading-platform", "kubernetes"],
    "timezone": "browser",
    "schemaVersion": 39,
    "refresh": "10s",
    "templating": {
        "list": [
            {
                "name": "namespace",
                "label": "Namespace",
                "type": "query",
                "datasource": {"type": "prometheus", "uid": "prometheus"},
                "query": "label_values(kube_pod_info, namespace)",
                "refresh": 1,
                "includeAll": True,
                "multi": True,
                "current": {"text": "All", "value": "$__all"}
            },
            {
                "name": "pod",
                "label": "Pod",
                "type": "query",
                "datasource": {"type": "prometheus", "uid": "prometheus"},
                "query": "label_values(kube_pod_info{namespace=~\"$namespace\"}, pod)",
                "refresh": 1,
                "includeAll": True,
                "multi": True,
                "current": {"text": "All", "value": "$__all"}
            }
        ]
    },
    "panels": [
        {
            "id": 1,
            "title": "Node CPU Utilization",
            "type": "timeseries",
            "gridPos": {"h": 7, "w": 12, "x": 0, "y": 0},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "percent"}},
            "targets": [{"expr": '100 - (avg by (node) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)', "legendFormat": "{{node}}"}]
        },
        {
            "id": 2,
            "title": "Node Memory Utilization",
            "type": "timeseries",
            "gridPos": {"h": 7, "w": 12, "x": 12, "y": 0},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "percent"}},
            "targets": [{"expr": '((node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes) * 100', "legendFormat": "Memory %"}]
        },
        {
            "id": 3,
            "title": "Pod CPU Usage",
            "type": "timeseries",
            "gridPos": {"h": 7, "w": 12, "x": 0, "y": 7},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "short"}},
            "targets": [{"expr": 'sum(rate(container_cpu_usage_seconds_total{namespace=~"$namespace", pod=~"$pod", container!=""}[5m])) by (pod)', "legendFormat": "{{pod}}"}]
        },
        {
            "id": 4,
            "title": "Pod Memory Usage (Working Set)",
            "type": "timeseries",
            "gridPos": {"h": 7, "w": 12, "x": 12, "y": 7},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "bytes"}},
            "targets": [{"expr": 'sum(container_memory_working_set_bytes{namespace=~"$namespace", pod=~"$pod", container!=""}) by (pod)', "legendFormat": "{{pod}}"}]
        },
        {
            "id": 5,
            "title": "Pod Restarts (1h)",
            "type": "timeseries",
            "gridPos": {"h": 7, "w": 8, "x": 0, "y": 14},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "short"}},
            "targets": [{"expr": 'sum(increase(kube_pod_container_status_restarts_total{namespace=~"$namespace", pod=~"$pod"}[1h])) by (pod)', "legendFormat": "{{pod}}"}]
        },
        {
            "id": 6,
            "title": "Deployment Desired Replicas",
            "type": "stat",
            "gridPos": {"h": 7, "w": 8, "x": 8, "y": 14},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "short"}},
            "targets": [{"expr": 'sum(kube_deployment_spec_replicas{namespace=~"$namespace"}) by (deployment)', "legendFormat": "{{deployment}}"}]
        },
        {
            "id": 7,
            "title": "Deployment Available Replicas",
            "type": "stat",
            "gridPos": {"h": 7, "w": 8, "x": 16, "y": 14},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "short"}},
            "targets": [{"expr": 'sum(kube_deployment_status_replicas_available{namespace=~"$namespace"}) by (deployment)', "legendFormat": "{{deployment}}"}]
        },
        {
            "id": 8,
            "title": "Deployment Unavailable Replicas",
            "type": "stat",
            "gridPos": {"h": 7, "w": 12, "x": 0, "y": 21},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "short"}},
            "targets": [{"expr": 'sum(kube_deployment_status_replicas_unavailable{namespace=~"$namespace"}) by (deployment) or vector(0)', "legendFormat": "{{deployment}}"}]
        },
        {
            "id": 9,
            "title": "Container CPU Throttling Rate",
            "type": "timeseries",
            "gridPos": {"h": 7, "w": 12, "x": 12, "y": 21},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "cps"}},
            "targets": [{"expr": 'sum(rate(container_cpu_cfs_throttled_periods_total{namespace=~"$namespace", pod=~"$pod"}[5m])) by (pod) or vector(0)', "legendFormat": "{{pod}}"}]
        }
    ]
}

# 3. APPLICATION SERVICES DASHBOARD
dashboard_app = {
    "title": "Trading Discipline AI — Application Services",
    "uid": "trading-app-services",
    "tags": ["trading-platform", "application"],
    "timezone": "browser",
    "schemaVersion": 39,
    "refresh": "10s",
    "templating": {
        "list": [
            {
                "name": "namespace",
                "label": "Namespace",
                "type": "query",
                "datasource": {"type": "prometheus", "uid": "prometheus"},
                "query": "label_values(http_requests_total, namespace)",
                "refresh": 1,
                "includeAll": True,
                "multi": True,
                "current": {"text": "All", "value": "$__all"}
            },
            {
                "name": "service",
                "label": "Service",
                "type": "query",
                "datasource": {"type": "prometheus", "uid": "prometheus"},
                "query": "label_values(http_requests_total{namespace=~\"$namespace\"}, job)",
                "refresh": 1,
                "includeAll": True,
                "multi": True,
                "current": {"text": "All", "value": "$__all"}
            }
        ]
    },
    "panels": [
        {
            "id": 1,
            "title": "HTTP Requests / sec",
            "type": "timeseries",
            "gridPos": {"h": 7, "w": 12, "x": 0, "y": 0},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "reqps"}},
            "targets": [{"expr": 'sum(rate(http_requests_total{namespace=~"$namespace", job=~"$service"}[5m])) by (job, handler)', "legendFormat": "{{job}} - {{handler}}"}]
        },
        {
            "id": 2,
            "title": "HTTP Request Latency (p50, p95, p99)",
            "type": "timeseries",
            "gridPos": {"h": 7, "w": 12, "x": 12, "y": 0},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "s"}},
            "targets": [
                {"expr": 'histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket{namespace=~"$namespace", job=~"$service"}[5m])) by (le))', "legendFormat": "p50"},
                {"expr": 'histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{namespace=~"$namespace", job=~"$service"}[5m])) by (le))', "legendFormat": "p95"},
                {"expr": 'histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{namespace=~"$namespace", job=~"$service"}[5m])) by (le))', "legendFormat": "p99"}
            ]
        },
        {
            "id": 3,
            "title": "4xx Client Error Rate %",
            "type": "timeseries",
            "gridPos": {"h": 7, "w": 12, "x": 0, "y": 7},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "percent"}},
            "targets": [{"expr": '(sum(rate(http_requests_total{namespace=~"$namespace", job=~"$service", status=~"4.."}[5m])) / sum(rate(http_requests_total{namespace=~"$namespace", job=~"$service"}[5m]))) * 100 or vector(0)', "legendFormat": "4xx Rate %"}]
        },
        {
            "id": 4,
            "title": "5xx Server Error Rate %",
            "type": "timeseries",
            "gridPos": {"h": 7, "w": 12, "x": 12, "y": 7},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "percent"}},
            "targets": [{"expr": '(sum(rate(http_requests_total{namespace=~"$namespace", job=~"$service", status=~"5.."}[5m])) / sum(rate(http_requests_total{namespace=~"$namespace", job=~"$service"}[5m]))) * 100 or vector(0)', "legendFormat": "5xx Rate %"}]
        },
        {
            "id": 5,
            "title": "Process CPU Usage",
            "type": "timeseries",
            "gridPos": {"h": 7, "w": 12, "x": 0, "y": 14},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "short"}},
            "targets": [{"expr": 'sum(rate(process_cpu_seconds_total{namespace=~"$namespace", job=~"$service"}[5m])) by (pod)', "legendFormat": "{{pod}}"}]
        },
        {
            "id": 6,
            "title": "Process Resident Memory (RSS)",
            "type": "timeseries",
            "gridPos": {"h": 7, "w": 12, "x": 12, "y": 14},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "bytes"}},
            "targets": [{"expr": 'sum(process_resident_memory_bytes{namespace=~"$namespace", job=~"$service"}) by (pod)', "legendFormat": "{{pod}}"}]
        },
        {
            "id": 7,
            "title": "Active / Ready Pod Replicas",
            "type": "stat",
            "gridPos": {"h": 6, "w": 12, "x": 0, "y": 21},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "short"}},
            "targets": [{"expr": 'sum(kube_pod_status_ready{condition="true", namespace=~"$namespace"}) by (namespace, pod)', "legendFormat": "{{namespace}} / {{pod}}"}]
        },
        {
            "id": 8,
            "title": "Container Restart Count (1h)",
            "type": "stat",
            "gridPos": {"h": 6, "w": 12, "x": 12, "y": 21},
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {"defaults": {"unit": "short"}},
            "targets": [{"expr": 'sum(increase(kube_pod_container_status_restarts_total{namespace=~"$namespace"}[1h])) by (namespace, pod)', "legendFormat": "{{namespace}} / {{pod}}"}]
        }
    ]
}

# SAVE JSON FILES
with open('infrastructure/monitoring/dashboards/platform_overview.json', 'w') as f:
    json.dump(dashboard_overview, f, indent=2)

with open('infrastructure/monitoring/dashboards/k8s_infrastructure.json', 'w') as f:
    json.dump(dashboard_k8s, f, indent=2)

with open('infrastructure/monitoring/dashboards/app_services.json', 'w') as f:
    json.dump(dashboard_app, f, indent=2)

print("Saved 3 dashboard JSON files successfully!")

# CREATE CONFIGMAP YAMLs
def make_cm_yaml(cm_name, json_filename, json_data):
    json_str = json.dumps(json_data)
    yaml_content = f"""apiVersion: v1
kind: ConfigMap
metadata:
  name: {cm_name}
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
    app.kubernetes.io/part-of: trading-platform
    app.kubernetes.io/component: monitoring
data:
  {json_filename}: |
    {json_str}
"""
    return yaml_content

with open('infrastructure/monitoring/dashboards/cm-platform-overview.yaml', 'w') as f:
    f.write(make_cm_yaml('grafana-dashboard-platform-overview', 'platform_overview.json', dashboard_overview))

with open('infrastructure/monitoring/dashboards/cm-k8s-infrastructure.yaml', 'w') as f:
    f.write(make_cm_yaml('grafana-dashboard-k8s-infrastructure', 'k8s_infrastructure.json', dashboard_k8s))

with open('infrastructure/monitoring/dashboards/cm-app-services.yaml', 'w') as f:
    f.write(make_cm_yaml('grafana-dashboard-app-services', 'app_services.json', dashboard_app))

print("Created 3 ConfigMap YAML files successfully!")
