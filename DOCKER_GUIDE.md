# Docker Deployment Guide 🐳

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Any Server (any IP)                                            │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Docker Network (erp-network)                            │   │
│  │                                                         │   │
│  │  ┌─────────────────┐      ┌─────────────────┐          │   │
│  │  │   Frontend      │ ───▶ │    Backend      │          │   │
│  │  │   (Nginx)       │ proxy│    (FastAPI)    │          │   │
│  │  │   Port 3000     │ /api │    Port 8001    │          │   │
│  │  └─────────────────┘      └─────────────────┘          │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Start (Any Machine)

### 1. Install Docker

**Ubuntu:**
```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
newgrp docker
```

**Windows/Mac:** Download [Docker Desktop](https://www.docker.com/products/docker-desktop)

### 2. Create docker-compose.yml

```bash
mkdir ~/erp-app
cd ~/erp-app
nano docker-compose.yml
```

Paste this content:

```yaml
version: '3.8'

services:
  backend:
    image: eneskaraoglu/erp-backend:latest
    container_name: erp-backend
    ports:
      - "8001:8001"
    volumes:
      - backend_data:/app/data
    restart: unless-stopped
    networks:
      - erp-network

  frontend:
    image: eneskaraoglu/erp-frontend:latest
    container_name: erp-frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    restart: unless-stopped
    networks:
      - erp-network

volumes:
  backend_data:
    name: erp-backend-data

networks:
  erp-network:
    driver: bridge
```

### 3. Run

```bash
docker-compose pull
docker-compose up -d
```

### 4. Access

| Service | URL |
|---------|-----|
| Frontend | http://SERVER_IP:3000 |
| Backend API | http://SERVER_IP:8001 |
| API Docs | http://SERVER_IP:8001/api/docs |

---

## Common Commands

| Action | Command |
|--------|---------|
| Start | `docker-compose up -d` |
| Stop | `docker-compose down` |
| Restart | `docker-compose restart` |
| View logs | `docker-compose logs -f` |
| Update images | `docker-compose pull && docker-compose up -d` |
| Reset database | `docker-compose down -v && docker-compose up -d` |
| Check status | `docker-compose ps` |

---

## Test Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Manager | manager | manager123 |
| User | johndoe | password123 |

---

## For Developers: Build & Push

### Prerequisites
```bash
docker login
# Enter Docker Hub username and password
```

### Build Backend
```bash
cd D:\CODE-BASE\erp-inventory-manager-backend
docker build -t eneskaraoglu/erp-backend:latest .
docker push eneskaraoglu/erp-backend:latest
```

### Build Frontend
```bash
cd D:\CODE-BASE\erp-inventory-manager
docker build -t eneskaraoglu/erp-frontend:latest .
docker push eneskaraoglu/erp-frontend:latest
```

---

## How Nginx Proxy Works

The frontend uses Nginx to proxy API requests to the backend. This makes the app **portable** - works on any machine without rebuilding!

```
Browser Request                    What Happens
─────────────────                  ────────────
GET /api/products       →          Nginx proxies to backend:8001/api/products
GET /login              →          Nginx serves React app (index.html)
GET /static/js/app.js   →          Nginx serves static file
```

**nginx.conf:**
```nginx
location /api {
    proxy_pass http://backend:8001/api;
}

location / {
    try_files $uri $uri/ /index.html;
}
```

---

## Troubleshooting

### Port Already in Use
```bash
# Find process
sudo lsof -i :3000
sudo lsof -i :8001

# Kill process
sudo kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "3001:80"  # Use 3001 instead of 3000
```

### Permission Denied
```bash
sudo chmod 666 /var/run/docker.sock
# Or
sudo usermod -aG docker $USER
newgrp docker
```

### Container Won't Start
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Restart from scratch
docker-compose down -v
docker-compose pull
docker-compose up -d
```

### Can't Access from Other Computers
```bash
# Check firewall (Ubuntu)
sudo ufw allow 3000
sudo ufw allow 8001

# Check if containers are running
docker-compose ps
```

---

## File Structure

```
erp-inventory-manager-backend/
├── Dockerfile              # Backend container
├── docker-compose.yml      # Backend only
├── docker-compose.prod.yml # Production (both services)
├── .dockerignore           # Excluded files
├── DOCKER_GUIDE.md         # This file
├── app/                    # FastAPI code
└── data/                   # SQLite database

erp-inventory-manager/
├── Dockerfile              # Frontend multi-stage build
├── docker-compose.yml      # Frontend only
├── nginx.conf              # Nginx with API proxy
├── .dockerignore           # Excluded files
└── src/                    # React code
```

---

## Docker Hub Images

| Image | Description |
|-------|-------------|
| `eneskaraoglu/erp-backend:latest` | FastAPI + SQLite |
| `eneskaraoglu/erp-frontend:latest` | React + Nginx |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Jan 2026 | Initial Docker setup |
| 1.1.0 | Jan 2026 | Added Nginx proxy (portable deployment) |
