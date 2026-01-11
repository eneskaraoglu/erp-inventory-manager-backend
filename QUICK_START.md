# Quick Start Guide

## Start the Server

```bash
# Install dependencies (first time only)
pip install -r requirements.txt

# Run server
python run.py
```

**Expected Output:**
```
🚀 Starting ERP Inventory Manager API...
✅ Database initialized at: .../data/erp.db
📦 Seeding products...
✅ Added 4 products
👥 Seeding customers...
✅ Added 3 customers
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Server runs at: **http://127.0.0.1:8000**

---

## View API Documentation

Open in browser: **http://127.0.0.1:8000/api/docs**

Here you can:
- See all endpoints
- Test them interactively
- View request/response schemas
- No Postman needed!

---

## Test Endpoints

```bash
# Get all products
curl http://127.0.0.1:8000/api/products

# Get all customers
curl http://127.0.0.1:8000/api/customers

# Create a product
curl -X POST http://127.0.0.1:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Webcam","price":89.99,"stock":25,"category":"Accessories"}'

# Delete a product
curl -X DELETE http://127.0.0.1:8000/api/products/5
```

---

## Data Persistence ✨

**Your data is saved to SQLite database!**

- Database file: `data/erp.db`
- Data survives server restart
- Like H2 database in Java

### Test It:
1. Add a product via API
2. Stop server (Ctrl+C)
3. Start server again
4. Your data is still there! ✅

### Reset Database:
```bash
del data\erp.db    # Windows
rm data/erp.db     # Mac/Linux
python run.py      # Fresh start with seed data
```

---

## File Structure Overview

```
app/
├── main.py              # Main app, CORS, DB init
├── database.py          # SQLite connection
├── models/
│   ├── product.py       # Pydantic schema (API)
│   ├── customer.py      # Pydantic schema (API)
│   ├── product_model.py # SQLAlchemy model (DB)
│   └── customer_model.py# SQLAlchemy model (DB)
└── routers/
    ├── products.py      # /api/products endpoints
    └── customers.py     # /api/customers endpoints
data/
└── erp.db               # SQLite database file
```

---

## Key Concepts (For Java Developers)

| FastAPI | Java Spring | Purpose |
|---------|-------------|---------|
| `@app.get()` | `@GetMapping` | HTTP GET endpoint |
| `@app.post()` | `@PostMapping` | HTTP POST endpoint |
| `Pydantic BaseModel` | DTO class | API validation |
| `SQLAlchemy Model` | `@Entity` | Database table |
| `Depends(get_db)` | `@Autowired` | Dependency injection |
| `db.query()` | `repository.findAll()` | Database query |
| SQLite | H2 Database | Embedded database |

---

## Python + FastAPI vs Java + Spring

### Java Spring
```java
@Entity
public class Product {
    @Id @GeneratedValue
    private Long id;
    private String name;
}

@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {}

@RestController
public class ProductController {
    @Autowired
    private ProductRepository repo;
    
    @GetMapping("/products")
    public List<Product> getAll() {
        return repo.findAll();
    }
}
```

### FastAPI (Equivalent)
```python
class ProductModel(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)

@router.get("/products")
def get_all(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()
```

**Much shorter! FastAPI handles:**
- JSON serialization/deserialization
- Validation (automatically)
- Documentation generation
- Type checking

---

## What You've Built

1. **Full REST API** with CRUD operations
2. **SQLite database** with persistent storage
3. **Type-safe** endpoints with Pydantic
4. **Auto-validated** requests
5. **CORS enabled** for React frontend
6. **Interactive docs** (Swagger UI)
7. **Seed data** auto-created on startup

---

## Connect to React Frontend

Your React app (localhost:5173) can now call:

```javascript
// Get all products
const response = await fetch('http://127.0.0.1:8000/api/products');
const products = await response.json();

// Create product
await fetch('http://127.0.0.1:8000/api/products', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'Test', price: 99.99, stock: 10 })
});
```

---

**Backend is ready with persistent database! 🚀**
