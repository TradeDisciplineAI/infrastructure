# Shared Infrastructure Repository

Production-grade shared infrastructure services using Docker Compose.

This repository manages shared backend infrastructure components independently from domain microservices.

---

## 🚀 Services Overview

- **PostgreSQL 16 Alpine**: Shared database engine exposed on host port `5433` (`5432` internally).

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
Start the PostgreSQL container in detached mode:

```bash
docker compose up -d
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

# Follow logs for PostgreSQL database container only
docker compose logs -f db
```

### Connect to Database via `psql`
Execute an interactive `psql` shell inside the running database container:

```bash
docker compose exec db psql -U postgres -d trading_db
```

Or connect from the host machine using external port `5433`:

```bash
psql -h localhost -p 5433 -U postgres -d trading_db
```

### Reset Database Volume (Wipe Data)
To completely remove persistent data volumes and reset the database:

> [!CAUTION]
> This command permanently deletes all data in the `shared_postgres_data` volume.

```bash
docker compose down -v
```

---

## 🔒 Security Best Practices

1. **Secrets Management**: Never commit `.env` files containing actual production passwords to Git.
2. **Access Control**: Keep host port `5433` restricted to localhost or protected internal networks.
