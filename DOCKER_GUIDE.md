# Docker Deployment Guide 🐳

## Quick Start

### Prerequisites
- Docker Desktop installed and running

---

## Option 1: Run Backend Only

```bash
cd D:\CODE-BASE\erp-inventory-manager-backend
docker-compose up -d --build
```

Access:
- API: http://localhost:8001
- Docs: http://localhost:8001/api/docs

---

## Option 2: Run Full Stack (Backend + Frontend)

```bash
cd D:\CODE-BASE\erp-inventory-manager-backend
docker-compose -f docker-compose.full.yml up -d --build
```

Access:
- Frontend: http://localhost
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/api/docs

---

## Common Commands

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build

# Check status
docker-compose ps

# Enter container shell
docker exec -it erp-backend /bin/sh
```

---

## File Structure

```
erp-inventory-manager-backend/
├── Dockerfile              # Backend container
├── docker-compose.yml      # Backend only
├── docker-compose.full.yml # Full stack
├── .dockerignore          # Excluded files
└── app/                   # Application code

erp-inventory-manager/
├── Dockerfile             # Frontend container (multi-stage)
├── docker-compose.yml     # Frontend only
├── nginx.conf            # Nginx configuration
└── src/                  # React code
```

---

## Test Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Manager | manager | manager123 |
| User | johndoe | password123 |

---

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8001
netstat -ano | findstr :8001

# Kill process
taskkill /PID <PID> /F
```

### Reset Database
```bash
docker-compose down -v
docker-compose up -d --build
```
