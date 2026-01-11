# Backend Setup Session - FastAPI
**Date:** January 10, 2026 (Initial) | January 11, 2026 (SQLite Migration)
**Duration:** ~1 hour (Initial) + ~30 min (Migration)
**Technology:** Python + FastAPI + SQLAlchemy + SQLite

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
- [x] **Migrate to SQLite database** ✨ NEW

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

---

## Project Structure

```
erp-inventory-manager-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app, CORS, routes, DB init
│   ├── database.py                # ✨ NEW - Database connection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── product.py             # Pydantic schemas (validation)
│   │   ├── customer.py            # Pydantic schemas (validation)
│   │   ├── product_model.py       # ✨ NEW - SQLAlchemy model
│   │   └── customer_model.py      # ✨ NEW - SQLAlchemy model
│   └── routers/
│       ├── __init__.py
│       ├── products.py            # Products CRUD (uses DB)
│       └── customers.py           # Customers CRUD (uses DB)
├── data/                          # ✨ NEW - Database folder
│   └── erp.db                     # ✨ SQLite database file
├── docs/
│   ├── BACKEND_SESSION.md         # This file
│   ├── CONCEPTS.md
│   └── FUNDAMENTALS_SUMMARY.md
├── requirements.txt               # Python dependencies (+ sqlalchemy)
├── run.py                         # Dev server runner
├── .gitignore
├── README.md
└── QUICK_START.md
```

---

## Database Migration (SQLite) ✨ NEW

### Why SQLite?

| Feature | In-Memory (Before) | SQLite (After) |
|---------|-------------------|----------------|
| Data persistence | ❌ Lost on restart | ✅ Saved to file |
| Real database | ❌ Just Python lists | ✅ SQL database |
| Production-like | ❌ Not realistic | ✅ Same patterns |
| Java equivalent | - | H2 Database |

### Java ↔ Python Comparison

| Concept | Java/Spring | Python/FastAPI |
|---------|-------------|----------------|
| Database | H2 / MySQL | SQLite / PostgreSQL |
| ORM | JPA/Hibernate | SQLAlchemy |
| Entity | `@Entity class` | `class Model(Base)` |
| Repository | `JpaRepository` | `db.query(Model)` |
| Transaction | `@Transactional` | `db.commit()` |
| Session | `EntityManager` | `Session` |
| DI | `@Autowired` | `Depends(get_db)` |
| Seed data | `data.sql` | `seed_data()` |

### Database Configuration

```python
# database.py - Like application.properties in Spring

# SQLite file path (like jdbc:h2:file:./data/erp)
DATABASE_URL = "sqlite:///data/erp.db"

# Create engine (like DataSource)
engine = create_engine(DATABASE_URL)

# Session factory (like EntityManagerFactory)
SessionLocal = sessionmaker(bind=engine)

# Base class for models (like @MappedSuperclass)
Base = declarative_base()
```

### Entity Model Example

```python
# Python/SQLAlchemy
class ProductModel(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    category = Column(String(50), nullable=True)
```

```java
// Java/JPA Equivalent
@Entity
@Table(name = "products")
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, length = 100)
    private String name;
    
    @Column(length = 500)
    private String description;
    
    @Column(nullable = false)
    private Double price;
    
    @Column(nullable = false)
    private Integer stock = 0;
    
    @Column(length = 50)
    private String category;
}
```

### Repository Pattern

```python
# Python/FastAPI - In router
@router.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()

@router.post("/products")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
```

```java
// Java/Spring Equivalent
@GetMapping("/products")
public List<Product> getAllProducts() {
    return productRepository.findAll();
}

@PostMapping("/products")
public Product createProduct(@RequestBody ProductDTO dto) {
    Product product = new Product();
    BeanUtils.copyProperties(dto, product);
    return productRepository.save(product);
}
```

---

## APIs Built

### Products API ✅

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| GET | `/api/products` | Get all products | 200 |
| GET | `/api/products/{id}` | Get single product | 200 / 404 |
| POST | `/api/products` | Create new product | 201 |
| PUT | `/api/products/{id}` | Update product | 200 / 404 |
| DELETE | `/api/products/{id}` | Delete product | 204 / 404 |

### Customers API ✅

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| GET | `/api/customers` | Get all customers | 200 |
| GET | `/api/customers/{id}` | Get single customer | 200 / 404 |
| POST | `/api/customers` | Create new customer | 201 / 400 |
| PUT | `/api/customers/{id}` | Update customer | 200 / 404 / 400 |
| DELETE | `/api/customers/{id}` | Delete customer | 204 / 404 |

---

## Data Models

### Pydantic Schemas (API Validation)

```python
# For API request/response validation
class Product(BaseModel):
    id: int
    name: str           # 1-100 chars, required
    description: str    # 0-500 chars, optional
    price: float        # Must be positive
    stock: int          # Must be >= 0
    category: str       # 0-50 chars, optional

class Customer(BaseModel):
    id: int
    name: str           # 1-100 chars, required
    email: EmailStr     # Valid email format
    phone: str          # 0-20 chars, optional
    address: str        # 0-200 chars, optional
    company: str        # 0-100 chars, optional
```

### SQLAlchemy Models (Database)

```python
# For database table mapping
class ProductModel(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    # ... other columns

class CustomerModel(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    # ... other columns
```

---

## Database Features

### Auto Table Creation
```python
# Like Hibernate's hbm2ddl.auto=update
Base.metadata.create_all(bind=engine)
```

### Seed Data (Initial Data)
```python
# Like Spring's data.sql or CommandLineRunner
def seed_data():
    if db.query(ProductModel).count() == 0:
        products = [
            ProductModel(name="Laptop", price=999.99, ...),
            ProductModel(name="Mouse", price=29.99, ...),
        ]
        db.add_all(products)
        db.commit()
```

### Startup Lifecycle
```python
# Like @PostConstruct in Spring
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()      # Create tables
    seed_data()    # Add initial data
    yield
    # Shutdown
```

---

## Commands Reference

```bash
# Install dependencies (including SQLAlchemy)
pip install -r requirements.txt

# Or install SQLAlchemy separately
pip install sqlalchemy

# Start development server
python run.py

# Database file location
data/erp.db
```

**Server URL:** http://127.0.0.1:8000
**API Docs:** http://127.0.0.1:8000/api/docs

---

## Server Startup Output

```
🚀 Starting ERP Inventory Manager API...
✅ Database initialized at: D:\CODE-BASE\erp-inventory-manager-backend\data\erp.db
📦 Seeding products...
✅ Added 4 products
👥 Seeding customers...
✅ Added 3 customers
INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## Sample Data (Seeded Automatically)

### Products (4 items)
| ID | Name | Price | Stock | Category |
|----|------|-------|-------|----------|
| 1 | Laptop | $999.99 | 50 | Electronics |
| 2 | Mouse | $29.99 | 100 | Accessories |
| 3 | Keyboard | $89.99 | 75 | Accessories |
| 4 | Monitor | $449.99 | 30 | Electronics |

### Customers (3 items)
| ID | Name | Email | Company |
|----|------|-------|---------|
| 1 | John Doe | john@example.com | Acme Corp |
| 2 | Jane Smith | jane@example.com | Tech Solutions |
| 3 | Bob Johnson | bob@example.com | Global Industries |

---

## Testing the API

### Via Swagger UI (Recommended)
1. Start server: `python run.py`
2. Open: http://127.0.0.1:8000/api/docs
3. Click any endpoint
4. Click "Try it out"
5. Fill in data
6. Click "Execute"

### Via curl

```bash
# Get all products
curl http://127.0.0.1:8000/api/products

# Create product
curl -X POST http://127.0.0.1:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Webcam","price":89.99,"stock":25,"category":"Accessories"}'

# Update product
curl -X PUT http://127.0.0.1:8000/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{"price":899.99}'

# Delete product
curl -X DELETE http://127.0.0.1:8000/api/products/5
```

### Test Data Persistence
1. Add a new product via API
2. Stop the server (Ctrl+C)
3. Start the server again
4. **Your data is still there!** ✅

---

## Files Created/Modified

### Initial Setup (Jan 10)
```
✨ NEW FILES:
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── product.py
│   │   └── customer.py
│   └── routers/
│       ├── __init__.py
│       ├── products.py
│       └── customers.py
├── requirements.txt
├── run.py
└── docs/BACKEND_SESSION.md
```

### SQLite Migration (Jan 11)
```
✨ NEW FILES:
├── app/
│   ├── database.py              # DB connection & session
│   └── models/
│       ├── product_model.py     # SQLAlchemy Product
│       └── customer_model.py    # SQLAlchemy Customer
└── data/
    └── erp.db                   # SQLite database file

📝 MODIFIED FILES:
├── app/
│   ├── main.py                  # Added lifespan, init_db, seed_data
│   ├── models/__init__.py       # Export new models
│   └── routers/
│       ├── products.py          # Use db session
│       └── customers.py         # Use db session
└── requirements.txt             # Added sqlalchemy
```

---

## Architecture Diagram

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

## Summary

### What We Built

| Feature | Status | Description |
|---------|--------|-------------|
| REST API | ✅ | 10 endpoints (CRUD) |
| Validation | ✅ | Pydantic schemas |
| Database | ✅ | SQLite + SQLAlchemy |
| Persistence | ✅ | Data survives restart |
| CORS | ✅ | React can connect |
| Auto Docs | ✅ | Swagger UI |
| Seed Data | ✅ | Initial products/customers |

### Key Learnings

1. **Pydantic** = API validation (like Bean Validation)
2. **SQLAlchemy** = ORM (like Hibernate)
3. **SQLite** = Embedded database (like H2)
4. **Depends()** = Dependency injection (like @Autowired)
5. **lifespan** = Startup/shutdown events (like @PostConstruct)

---

## Total Learning Progress

```
React Frontend:        [████████░░] 60% (Phase 1-2 Complete, API Connected)
Python Backend:        [████████░░] 70% (API + Database Complete)
Full-Stack:            [███████░░░] 65%
```

**Backend is now production-ready with persistent storage!** 🚀
