python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python run.py   

# ERP Inventory Manager - Backend API

FastAPI backend for the ERP Inventory Management System with **SQLite database**.

## Features

- **Products API** - Full CRUD operations for product management
- **Customers API** - Full CRUD operations for customer management
- **SQLite Database** - Persistent storage (data survives restart!)
- **Auto-generated API Documentation** - Swagger UI and ReDoc
- **CORS Enabled** - Ready to connect with React frontend
- **Type Safety** - Pydantic models with validation
- **Email Validation** - Built-in email format validation
- **Seed Data** - Sample data auto-created on first run

---

## Tech Stack

| Technology | Purpose | Java Equivalent |
|------------|---------|-----------------|
| **FastAPI** | Web framework | Spring Boot |
| **SQLAlchemy** | ORM | Hibernate/JPA |
| **SQLite** | Database | H2 Database |
| **Pydantic** | Validation | Bean Validation |
| **Uvicorn** | ASGI server | Tomcat |
| **Python 3.10+** | Language | Java |

---

## Project Structure

```
erp-inventory-manager-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app, CORS, DB init
│   ├── database.py             # Database connection & session
│   ├── models/
│   │   ├── __init__.py
│   │   ├── product.py          # Pydantic schemas (API)
│   │   ├── customer.py         # Pydantic schemas (API)
│   │   ├── product_model.py    # SQLAlchemy model (DB)
│   │   └── customer_model.py   # SQLAlchemy model (DB)
│   └── routers/
│       ├── __init__.py
│       ├── products.py         # Products endpoints
│       └── customers.py        # Customers endpoints
├── data/
│   └── erp.db                  # SQLite database file
├── docs/                       # Documentation
├── requirements.txt            # Python dependencies
├── run.py                      # Development server runner
├── .gitignore
└── README.md
```

---

## Installation

### 1. Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- Pydantic (validation)
- SQLAlchemy (ORM)
- Email validator

---

## Running the Server

### Option 1: Using run.py (Recommended)

```bash
python run.py
```

### Option 2: Using uvicorn directly

```bash
uvicorn app.main:app --reload
```

### Expected Output

```
🚀 Starting ERP Inventory Manager API...
✅ Database initialized at: D:\CODE-BASE\erp-inventory-manager-backend\data\erp.db
📦 Seeding products...
✅ Added 4 products
👥 Seeding customers...
✅ Added 3 customers
INFO:     Uvicorn running on http://127.0.0.1:8000
```

The server will start at: **http://127.0.0.1:8000**

---

## API Documentation

Once the server is running, visit:

- **Swagger UI (Interactive)**: http://127.0.0.1:8000/api/docs
- **ReDoc (Alternative)**: http://127.0.0.1:8000/api/redoc

You can test all endpoints directly in the Swagger UI!

---

## API Endpoints

### Root Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API health check |
| GET | `/api/health` | Health status |

### Products API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products` | Get all products |
| GET | `/api/products/{id}` | Get product by ID |
| POST | `/api/products` | Create new product |
| PUT | `/api/products/{id}` | Update product |
| DELETE | `/api/products/{id}` | Delete product |

### Customers API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/customers` | Get all customers |
| GET | `/api/customers/{id}` | Get customer by ID |
| POST | `/api/customers` | Create new customer |
| PUT | `/api/customers/{id}` | Update customer |
| DELETE | `/api/customers/{id}` | Delete customer |

---

## Example Requests

### Get All Products

```bash
curl http://127.0.0.1:8000/api/products
```

### Get Single Product

```bash
curl http://127.0.0.1:8000/api/products/1
```

### Create Product

```bash
curl -X POST http://127.0.0.1:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Webcam",
    "description": "HD webcam",
    "price": 89.99,
    "stock": 25,
    "category": "Accessories"
  }'
```

### Update Product

```bash
curl -X PUT http://127.0.0.1:8000/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "price": 899.99,
    "stock": 45
  }'
```

### Delete Product

```bash
curl -X DELETE http://127.0.0.1:8000/api/products/5
```

---

## Data Models

### Product

```json
{
  "id": 1,
  "name": "Laptop",
  "description": "High-performance laptop",
  "price": 999.99,
  "stock": 50,
  "category": "Electronics"
}
```

**Validation Rules:**
- `name`: 1-100 characters (required)
- `description`: 0-500 characters (optional)
- `price`: Must be positive (required)
- `stock`: Must be non-negative (required)
- `category`: 0-50 characters (optional)

### Customer

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "address": "123 Main St, New York, NY",
  "company": "Acme Corp"
}
```

**Validation Rules:**
- `name`: 1-100 characters (required)
- `email`: Valid email format, unique (required)
- `phone`: 0-20 characters (optional)
- `address`: 0-200 characters (optional)
- `company`: 0-100 characters (optional)

---

## Database

### SQLite (Persistent Storage)

The database file is stored at: `data/erp.db`

**Features:**
- ✅ Data persists across server restarts
- ✅ Automatic table creation on startup
- ✅ Seed data on first run
- ✅ Similar to H2 in Java/Spring

### Seed Data (Auto-Created)

**Products (4 items):**
| ID | Name | Price | Stock | Category |
|----|------|-------|-------|----------|
| 1 | Laptop | $999.99 | 50 | Electronics |
| 2 | Mouse | $29.99 | 100 | Accessories |
| 3 | Keyboard | $89.99 | 75 | Accessories |
| 4 | Monitor | $449.99 | 30 | Electronics |

**Customers (3 items):**
| ID | Name | Email | Company |
|----|------|-------|---------|
| 1 | John Doe | john@example.com | Acme Corp |
| 2 | Jane Smith | jane@example.com | Tech Solutions |
| 3 | Bob Johnson | bob@example.com | Global Industries |

### Reset Database

To start fresh, delete the database file:

```bash
# Windows
del data\erp.db

# Mac/Linux
rm data/erp.db
```

Then restart the server - new database will be created with seed data.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend                          │
│                  (localhost:5173)                           │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP (fetch)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend                           │
│                  (localhost:8000)                           │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Routers   │→ │  Pydantic   │→ │    SQLAlchemy       │ │
│  │ (Endpoints) │  │  (Schemas)  │  │    (Models)         │ │
│  └─────────────┘  └─────────────┘  └──────────┬──────────┘ │
└────────────────────────────────────────────────┼────────────┘
                                                 │ SQL
                                                 ▼
                                    ┌─────────────────────────┐
                                    │   SQLite Database       │
                                    │   (data/erp.db)         │
                                    │   - products table      │
                                    │   - customers table     │
                                    └─────────────────────────┘
```

---

## CORS Configuration

The API accepts requests from:
- `http://localhost:5173` (Vite - React dev server)
- `http://localhost:3000` (Create React App)
- `http://127.0.0.1:5173`
- `http://127.0.0.1:3000`

To add more origins, edit `app/main.py`:

```python
allow_origins=[
    "http://localhost:5173",
    "http://your-custom-origin.com",
]
```

---

## Connecting with React Frontend

### Using fetch

```javascript
// Fetch all products
const response = await fetch('http://127.0.0.1:8000/api/products');
const products = await response.json();

// Create product
const response = await fetch('http://127.0.0.1:8000/api/products', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'New Product',
    price: 99.99,
    stock: 100
  })
});
```

### Using React Query (recommended)

```javascript
const { data: products } = useQuery({
  queryKey: ['products'],
  queryFn: () => fetch('http://127.0.0.1:8000/api/products').then(r => r.json())
});
```

---

## Troubleshooting

### Server won't start

```bash
# Check if port 8000 is already in use
netstat -ano | findstr :8000

# Kill the process using port 8000
taskkill /PID <process_id> /F
```

### Import errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### CORS errors in React

Make sure your React dev server origin is listed in `app/main.py` CORS configuration.

### Database errors

```bash
# Delete and recreate database
del data\erp.db
python run.py
```

---

## Java Comparison

| Concept | Java/Spring | Python/FastAPI |
|---------|-------------|----------------|
| Entity | `@Entity` | `class Model(Base)` |
| Repository | `JpaRepository` | `db.query(Model)` |
| DTO | `ProductDTO` | Pydantic `BaseModel` |
| Validation | `@Valid` | Automatic with Pydantic |
| Injection | `@Autowired` | `Depends(get_db)` |
| Database | H2 / MySQL | SQLite / PostgreSQL |
| ORM | Hibernate | SQLAlchemy |

---

## Learning Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org
- **Pydantic Docs**: https://docs.pydantic.dev
- **SQLite**: https://sqlite.org

---

## License

This is a learning project for understanding FastAPI, SQLAlchemy, and React integration.

---

**Happy coding! 🚀**
