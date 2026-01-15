# ERP Inventory Manager - Backend

FastAPI backend for the ERP Inventory Management System.

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Pull and run
docker pull eneskaraoglu/erp-backend:latest
docker run -d -p 8001:8001 -v erp-data:/app/data eneskaraoglu/erp-backend:latest

# Access API docs
open http://localhost:8001/api/docs
```

### Option 2: Local Development

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run server
python run.py
```

## 📁 Project Structure

```
erp-inventory-manager-backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # SQLite connection
│   ├── models/              # Pydantic & SQLAlchemy models
│   │   ├── product.py
│   │   ├── product_model.py
│   │   ├── customer.py
│   │   ├── customer_model.py
│   │   ├── user.py
│   │   └── user_model.py
│   └── routers/             # API endpoints
│       ├── products.py
│       ├── customers.py
│       ├── users.py
│       └── auth.py
├── data/
│   └── erp.db               # SQLite database
├── Dockerfile               # Container build
├── docker-compose.yml       # Docker orchestration
├── requirements.txt         # Python dependencies
└── run.py                   # Development server
```

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | Login, get JWT token |
| GET | `/api/products` | List all products |
| POST | `/api/products` | Create product |
| GET | `/api/products/{id}` | Get product |
| PUT | `/api/products/{id}` | Update product |
| DELETE | `/api/products/{id}` | Delete product |
| GET | `/api/customers` | List all customers |
| GET | `/api/users` | List all users |

Full API documentation: `http://localhost:8001/api/docs`

## 🔐 Authentication

JWT token-based authentication.

**Test Credentials:**
| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Manager | manager | manager123 |
| User | johndoe | password123 |

## 🐳 Docker

See [DOCKER_GUIDE.md](./DOCKER_GUIDE.md) for full deployment instructions.

```bash
# Build
docker build -t eneskaraoglu/erp-backend:latest .

# Push to Docker Hub
docker push eneskaraoglu/erp-backend:latest
```

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Database:** SQLite + SQLAlchemy
- **Auth:** JWT (PyJWT)
- **Validation:** Pydantic
- **Server:** Uvicorn

## 📝 License

MIT
