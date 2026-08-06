# Shared Infrastructure Repository

Production-grade shared infrastructure services using Docker Compose.

This repository manages shared backend infrastructure components independently from domain microservices.

---

## 🚀 Services Overview

- **PostgreSQL 16 Alpine**: Isolated database engine exposed on host port `5434` (`5432` internally) for pytest suites.
- **Redis 7 Alpine**: Shared cache and message broker exposed on host port `6379`.
- **Jenkins (Custom Image)**: Core CI/CD automation server configured with pre-installed plugins and docker-out-of-docker (DooD) support.

---

## 🛠️ Quick Start

### 1. Prerequisites
- Docker (version 24.0+)
- Docker Compose (version 2.20+)

### 2. Environment Configuration
Copy the template environment file and set secure password credentials:

```bash
cp .env.example .env
```

---

## 📖 Operational Commands

### Start Infrastructure
Start all containers in detached mode:

```bash
docker compose up -d
```

To build and start only the Jenkins container:

```bash
docker compose up -d --build jenkins
```

### Stop Infrastructure
Gracefully stop the running containers:

```bash
docker compose down
```

### Inspect Container Logs
View and follow container logs:

```bash
# Follow logs for all services
docker compose logs -f

# Follow logs for Jenkins container only
docker compose logs -f jenkins
```

### Connect to Database via `psql`
Execute an interactive `psql` shell inside the running database container:

```bash
docker compose exec test_db psql -U postgres -d trading_test_db
```

Or connect from the host machine using external port `5434`:

```bash
psql -h localhost -p 5434 -U postgres -d trading_test_db
```

### Reset Data Volumes (Wipe Data)
To completely remove persistent data volumes and reset all services:

> [!CAUTION]
> This command permanently deletes all data in the `shared_postgres_data`, `shared_redis_data`, and `shared_jenkins_data` volumes.

```bash
docker compose down -v
```

---

## 🏗️ Jenkins CI Infrastructure

### Purpose & Architecture Overview
The shared Jenkins server functions as the central automation orchestrator for all microservices in the platform (e.g., `authentication-service` and `market-service`).

Key architectural decisions & reproducibility practices:
- **Docker-out-of-Docker (DooD)**: Jenkins mounts the host machine's Docker daemon socket (`/var/run/docker.sock`). This allows Jenkins to execute sibling docker builds, runs, and image pushes without the overhead of nested virtualization.
- **Custom Image**: Built from the custom `jenkins/Dockerfile` (derived from `jenkins/jenkins:2.568.2-lts-jdk21`).
  - **Pinned Base Image**: The base image version is pinned to `2.568.2-lts-jdk21` to guarantee deterministic builds, preventing unexpected updates to the runtime platform.
  - **Docker CLI**: It pre-installs `docker-ce-cli` for running Docker commands directly in pipeline stages.
- **Pinned Plugins**: Every plugin in `jenkins/plugins.txt` is version-pinned (e.g., `git:5.10.1`) to ensure that builds remain fully reproducible and immune to regressions from upstream updates.

### Docker Socket Group ID Configuration
To communicate with the host's Docker daemon via `/var/run/docker.sock`, the container process must run with permissions allowing it to read and write to the socket.
- **DOCKER_SOCKET_GID**: Configured in `.env`, this is mapped to the container via the `group_add` property to grant the `jenkins` user access to the socket.
- **Windows Docker Desktop**: Set `DOCKER_SOCKET_GID=0` (root group). Windows maps the socket as owned by `root`.
- **Linux Hosts**: Linux users should set this to the GID of the host's `docker` group. To determine the correct GID, run:
  ```bash
  getent group docker | cut -d: -f3
  ```
  And specify the returned GID (commonly `998` or `999`) in `.env`.

### Persistent Storage
Jenkins configurations, credentials, build workspaces, and job history are persistently saved in the named Docker volume `jenkins_data` (mapped to `/var/jenkins_home`). These survive container recreation.

### Accessing the Web UI
The Jenkins Web UI is exposed at:
[http://localhost:8080](http://localhost:8080)

### Initial Administrator Password
During first boot, Jenkins generates an initial admin password. Retrieve it using:
```bash
docker compose exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```
Alternatively, check the container logs:
```bash
docker compose logs jenkins
```

### Future Role in the Platform
In the future, each microservice will define its own `Jenkinsfile` pipeline. Jenkins will load these pipelines, pull/build service Docker containers using the mounted socket, run unit/integration tests against PostgreSQL and Redis, capture test and warnings results, and automate deployments.

---

## 🔒 Security Best Practices

1. **Secrets Management**: Never commit `.env` files containing actual production passwords to Git.
2. **Access Control**: Keep host ports restricted to localhost or protected internal networks.

