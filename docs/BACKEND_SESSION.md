# Backend Setup Session - FastAPI
**Date:** January 10, 2026 (Initial) | January 11-12, 2026 (Enhancements)
**Duration:** ~3 hours total
**Technology:** Python + FastAPI + SQLAlchemy + SQLite + JWT

---

## Session Goals - ✅ All Completed!

- [x] Choose backend technology (Python + FastAPI)
- [x] Set up FastAPI project structure
- [x] Create Product and Customer data models
- [x] Build complete CRUD APIs for Products
- [x] Build complete CRUD APIs for Customers
- [x] Enable CORS for React frontend
- [x] Test all endpoints
- [x] Generate auto documentation
- [x] **Migrate to SQLite database** ✨
- [x] **Add User module with password hashing** ✨
- [x] **Add JWT Authentication** ✨

---

## Why FastAPI?

Coming from **Java** background, wanted to learn **Python** for:
- AI/ML opportunities
- Data science capabilities
- Scripting & automation
- Modern web development

**FastAPI** chosen because:
- Modern Python web framework
- Type hints (similar to Java's type system)
- Automatic validation (like Bean Validation)
- Dependency injection (like Spring)
- Auto-generated docs (Swagger UI)
- Fast and async support

---

## Tech Stack

| Technology | Version | Purpose | Java Equivalent |
|------------|---------|---------|-----------------|
| Python | 3.10.11 | Programming language | Java |
| FastAPI | 0.115.5 | Web framework | Spring Boot |
| Uvicorn | 0.32.1 | ASGI server | Tomcat |
| Pydantic | 2.10.3 | Data validation | Bean Validation |
| SQLAlchemy | 2.0.36 | ORM | Hibernate/JPA |
| SQLite | Built-in | Database | H2 Database |
| PyJWT | 2.x | JWT tokens | jjwt / Spring Security |

---

## Project Structure

```
erp-inventory-manager-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app, CORS, routes, DB init
│   ├── database.py                # Database connection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── product.py             # Pydantic schemas (validation)
│   │   ├── customer.py            # Pydantic schemas
│   │   ├── user.py                # ✨ User Pydantic schemas
│   │   ├── product_model.py       # SQLAlchemy model
│   │   ├── customer_model.py      # SQLAlchemy model
│   │   └── user_model.py          # ✨ User SQLAlchemy model
│   └── routers/
│       ├── __init__.py
│       ├── products.py            # Products CRUD
│       ├── customers.py           # Customers CRUD
│       ├── users.py               # ✨ Users CRUD
│       └── auth.py                # ✨ JWT Authentication
├── data/
│   └── erp.db                     # SQLite database file
├── docs/
│   ├── BACKEND_SESSION.md         # This file
│   ├── CONCEPTS.md
│   └── FUNDAMENTALS_SUMMARY.md
├── requirements.txt               # Python dependencies
├── run.py                         # Dev server runner
├── .gitignore
├── README.md
└── QUICK_START.md
```

---

## APIs Built

### Products API ✅

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/products` | Get all products | Required |
| GET | `/api/products/{id}` | Get single product | Required |
| POST | `/api/products` | Create new product | Required |
| PUT | `/api/products/{id}` | Update product | Required |
| DELETE | `/api/products/{id}` | Delete product | Required |

### Customers API ✅

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/customers` | Get all customers | Required |
| GET | `/api/customers/{id}` | Get single customer | Required |
| POST | `/api/customers` | Create new customer | Required |
| PUT | `/api/customers/{id}` | Update customer | Required |
| DELETE | `/api/customers/{id}` | Delete customer | Required |

### Users API ✅

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/users` | Get all users | Admin/Manager |
| GET | `/api/users/{id}` | Get single user | Admin/Manager |
| POST | `/api/users` | Create new user | Admin |
| PUT | `/api/users/{id}` | Update user | Admin |
| DELETE | `/api/users/{id}` | Delete user | Admin |

### Auth API ✅

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/login` | Login, get JWT token | Public |
| GET | `/api/auth/me` | Get current user info | Required |

---

## Authentication (JWT) ✨

### Flow
```
1. POST /auth/login { username, password }
2. Backend validates credentials
3. Returns { access_token, user }
4. Frontend stores token in localStorage
5. All requests include: Authorization: Bearer <token>
6. Backend validates token on each request
```

### Java ↔ Python Auth Comparison

| Concept | Java/Spring | Python/FastAPI |
|---------|-------------|----------------|
| Auth Filter | OncePerRequestFilter | Depends() |
| Token Creation | JwtService | jwt.encode() |
| Token Validation | JwtFilter | jwt.decode() |
| Password Hash | BCryptPasswordEncoder | hashlib.sha256 |
| User Details | UserDetailsService | get_current_user() |
| Security Config | SecurityFilterChain | Manual in route |

### Sample Users (Seeded)

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | admin |
| manager | manager123 | manager |
| johndoe | password123 | user |

---

## Database Models

### User Model (with Password Hashing)

```python
class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(64), nullable=False)  # SHA256
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default="user")  # admin, manager, user
    created_at = Column(DateTime, default=datetime.utcnow)
```

### Password Hashing

```python
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed
```

---

## Java ↔ Python Comparison

### Entity/Model

```python
# Python/SQLAlchemy
class ProductModel(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
```

```java
// Java/JPA Equivalent
@Entity
@Table(name = "products")
public class Product {
    @Id @GeneratedValue
    private Long id;
    
    @Column(nullable = false)
    private String name;
    
    private Double price;
}
```

### Repository Pattern

```python
# Python/FastAPI
@router.get("/products")
def get_all(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()
```

```java
// Java/Spring
@GetMapping("/products")
public List<Product> getAll() {
    return repository.findAll();
}
```

### Dependency Injection

```python
# Python - Depends()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def endpoint(db: Session = Depends(get_db)):
    ...
```

```java
// Java - @Autowired
@Autowired
private ProductRepository repository;
```

---

## Commands Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Start development server
python run.py

# Server runs at
http://127.0.0.1:8000

# API Documentation
http://127.0.0.1:8000/api/docs

# Database file
data/erp.db
```

---

## Server Startup Output

```
🚀 Starting ERP Inventory Manager API...
✅ Database initialized at: data/erp.db
📦 Seeding products... ✅ Added 4 products
👥 Seeding customers... ✅ Added 3 customers
👤 Seeding users... ✅ Added 3 users
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend                          │
│                  (localhost:5173)                           │
│   - Login Page → Auth Store (Zustand)                      │
│   - Protected Routes                                        │
│   - AG Grid Tables                                          │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP + JWT Token
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend                           │
│                  (localhost:8000)                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Routers   │→ │  Pydantic   │→ │    SQLAlchemy       │ │
│  │ - products  │  │  (Schemas)  │  │    (Models)         │ │
│  │ - customers │  │             │  │                     │ │
│  │ - users     │  └─────────────┘  └──────────┬──────────┘ │
│  │ - auth      │                              │            │
│  └─────────────┘                              │            │
└───────────────────────────────────────────────┼────────────┘
                                                │ SQL
                                                ▼
                                   ┌─────────────────────────┐
                                   │   SQLite Database       │
                                   │   (data/erp.db)         │
                                   │   - products            │
                                   │   - customers           │
                                   │   - users               │
                                   └─────────────────────────┘
```

---

## Summary

### What We Built

| Feature | Status | Description |
|---------|--------|-------------|
| Products API | ✅ | Full CRUD (5 endpoints) |
| Customers API | ✅ | Full CRUD (5 endpoints) |
| Users API | ✅ | Full CRUD (5 endpoints) |
| Auth API | ✅ | Login + JWT (2 endpoints) |
| Database | ✅ | SQLite + SQLAlchemy |
| Password Hashing | ✅ | SHA256 |
| JWT Auth | ✅ | Token-based auth |
| Role-based Access | ✅ | admin/manager/user |
| CORS | ✅ | React can connect |
| Auto Docs | ✅ | Swagger UI |
| Seed Data | ✅ | Initial data on startup |

### Total Endpoints: 17

| Module | Endpoints |
|--------|-----------|
| Products | 5 |
| Customers | 5 |
| Users | 5 |
| Auth | 2 |

---

## Frontend Integration

The React frontend connects to this backend with:

| Frontend | Backend |
|----------|---------|
| React Query | Products API |
| Context API | Customers API |
| Context API | Users API |
| Zustand (authStore) | Auth API |
| AG Grid | All APIs |

---

## Total Learning Progress

```
React Frontend:        [██████████] 100% ✅
Python Backend:        [██████████] 100% ✅
Full-Stack:            [██████████] 100% ✅
```

**Full-stack ERP system complete!** 🚀

---

## Quick Links

- Frontend Docs: `erp-inventory-manager/docs/`
- Backend Docs: `erp-inventory-manager-backend/docs/`
- API Docs: http://localhost:8000/api/docs
