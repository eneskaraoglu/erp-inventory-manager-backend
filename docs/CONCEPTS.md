# Full-Stack Concepts - Quick Reference

---

# Part 1: React Frontend

## Java ↔ React Comparison

| Java/Swing | React | Notes |
|------------|-------|-------|
| JPanel class | Function Component | Reusable UI units |
| Constructor params | Props | Data from parent |
| Class fields | useState | Mutable state |
| PropertyChangeListener | useState setter | Triggers re-render |
| componentDidMount | useEffect(() => {}, []) | Runs on mount |
| ActionListener | onClick, onChange | Event handlers |
| for loop + add() | .map() + JSX | Rendering lists |
| Servlet URL mapping | React Router | URL → Component |
| Command Pattern | useReducer | Action-based state |
| Component reference | useRef | DOM access |
| Bean Validation | Zod | Form validation |
| HttpClient | fetch() | API calls |

---

## Hook Rules 📜

1. **Only call hooks at top level** - Never in conditions/loops
2. **Only call hooks in React functions** - Components or custom hooks

---

## useState Patterns

```tsx
// Basic
const [count, setCount] = useState(0)
setCount(5)
setCount(c => c + 1)

// Object
const [user, setUser] = useState({ name: '', age: 0 })
setUser({ ...user, name: 'John' })

// Array
const [items, setItems] = useState([])
setItems([...items, newItem])
setItems(items.filter(i => i.id !== id))
```

---

## useEffect Patterns

```tsx
// Run once on mount
useEffect(() => {
  fetchData()
}, [])

// Run on dependency change
useEffect(() => {
  console.log('value changed')
}, [value])

// Cleanup
useEffect(() => {
  const timer = setInterval(() => {}, 1000)
  return () => clearInterval(timer)
}, [])
```

---

## API Integration Patterns

### Basic Fetch
```tsx
const [data, setData] = useState([])
const [loading, setLoading] = useState(true)
const [error, setError] = useState(null)

useEffect(() => {
  const fetchData = async () => {
    try {
      setLoading(true)
      const response = await fetch('http://localhost:8000/api/products')
      const json = await response.json()
      setData(json)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }
  fetchData()
}, [])
```

### POST Request
```tsx
const createProduct = async (product) => {
  const response = await fetch('http://localhost:8000/api/products', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(product)
  })
  return response.json()
}
```

### API Service Pattern
```tsx
// services/api.ts
export const productApi = {
  getAll: () => fetchApi<Product[]>('/products'),
  getById: (id) => fetchApi<Product>(`/products/${id}`),
  create: (data) => fetchApi<Product>('/products', { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => fetchApi<Product>(`/products/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id) => fetchApi<void>(`/products/${id}`, { method: 'DELETE' }),
}
```

---

## Loading & Error States

```tsx
function ProductsPage() {
  const { products, loading, error } = useProducts()

  if (loading) {
    return <div className="animate-spin">Loading...</div>
  }

  if (error) {
    return <div className="text-red-500">{error}</div>
  }

  return <div>{products.map(p => ...)}</div>
}
```

---

## useReducer Pattern

```tsx
type Action =
  | { type: 'ADD_ITEM'; payload: Item }
  | { type: 'REMOVE_ITEM'; payload: { id: number } }
  | { type: 'CLEAR' }

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'ADD_ITEM':
      return { ...state, items: [...state.items, action.payload] }
    case 'CLEAR':
      return { items: [], total: 0 }
    default:
      return state
  }
}

const [state, dispatch] = useReducer(reducer, initialState)
dispatch({ type: 'ADD_ITEM', payload: newItem })
```

---

## useRef Pattern

```tsx
// DOM Reference
const inputRef = useRef<HTMLInputElement>(null)
<input ref={inputRef} />
inputRef.current?.focus()

// Persist value (no re-render)
const renderCount = useRef(0)
renderCount.current += 1
```

---

## Zod Validation

```tsx
import { z } from 'zod'

const schema = z.object({
  name: z.string().min(1, 'Required').max(100),
  email: z.string().email('Invalid email'),
  price: z.string().refine(v => Number(v) > 0, 'Must be positive'),
})

const result = schema.safeParse(data)
if (result.success) {
  console.log(result.data)
}
```

---

# Part 2: FastAPI Backend

## Java ↔ Python Comparison

| Java/Spring | Python/FastAPI | Notes |
|-------------|----------------|-------|
| `@RestController` | `APIRouter` | Group endpoints |
| `@GetMapping` | `@router.get()` | HTTP GET |
| `@PostMapping` | `@router.post()` | HTTP POST |
| `@PathVariable` | Path parameter | `/products/{id}` |
| `@RequestBody` | Pydantic model | Auto-validated |
| `@Valid` | Automatic | Pydantic validates |
| `throw Exception` | `raise HTTPException` | Error handling |

---

## Database: Java ↔ Python

| Java/Spring | Python/FastAPI | Notes |
|-------------|----------------|-------|
| H2 Database | SQLite | Embedded DB |
| Hibernate/JPA | SQLAlchemy | ORM |
| `@Entity` | `class Model(Base)` | DB table |
| `@Id @GeneratedValue` | `Column(primary_key=True)` | Auto ID |
| `JpaRepository` | `db.query()` | DB operations |
| `@Autowired` | `Depends(get_db)` | Inject session |
| `@Transactional` | `db.commit()` | Save changes |

---

## SQLAlchemy Model

```python
class ProductModel(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
```

**Java Equivalent:**
```java
@Entity
@Table(name = "products")
public class Product {
    @Id @GeneratedValue
    private Long id;
    
    @Column(nullable = false)
    private String name;
    
    private Double price;
    private Integer stock = 0;
}
```

---

## Repository Pattern

```python
@router.get("/products")
def get_all(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()

@router.post("/products")
def create(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
```

---

## Password Hashing

```python
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Create user with hashed password
db_user = UserModel(
    username=user.username,
    password_hash=hash_password(user.password)
)
```

---

## JWT Authentication ✨

### Token Creation
```python
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"

def create_token(user_id: int, username: str, role: str) -> str:
    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

### Token Validation
```python
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")
```

### Java ↔ Python Auth Comparison
| Java/Spring | Python/FastAPI |
|-------------|----------------|
| JwtFilter | Depends(get_current_user) |
| JwtService | jwt.encode() / jwt.decode() |
| BCryptPasswordEncoder | hashlib.sha256 |
| SecurityContextHolder | Return from dependency |
| @PreAuthorize | Manual role check |

---

## Pydantic Validation

```python
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
```

---

# Part 3: Full-Stack Flow

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│  React Component                                                │
│  const { data } = await fetch('/api/products')                  │
└─────────────────────────────┬───────────────────────────────────┘
                              │ HTTP Request + JWT Token
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  FastAPI Router                                                 │
│  @router.get("/products")                                       │
│  def get_products(db: Session = Depends(get_db)):              │
└─────────────────────────────┬───────────────────────────────────┘
                              │ SQLAlchemy Query
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  SQLite Database                                                │
│  SELECT * FROM products                                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Module Structure Pattern

### Backend (FastAPI)
```
models/
├── user.py          # Pydantic schema (API validation)
└── user_model.py    # SQLAlchemy model (database)

routers/
├── users.py         # CRUD endpoints
└── auth.py          # Authentication endpoints
```

### Frontend (React)
```
types/
└── index.ts         # TypeScript types

services/
└── api.ts           # API calls

stores/
└── authStore.ts     # Zustand auth state

pages/
├── LoginPage.tsx    # Login form
└── User/
    ├── UsersPage.tsx
    └── UsersGridPage.tsx  # AG Grid version
```

---

## Authentication Flow

```
Login → Token → Store → API Calls → Validate
  │       │       │         │          │
  │       │       │         │          └── Backend verifies
  │       │       │         └── Authorization header
  │       │       └── Zustand persist → localStorage
  │       └── Backend returns JWT
  └── POST /auth/login
```

---

## AG Grid Patterns ✨

### Basic Setup (v35+)
```tsx
import { AgGridReact } from 'ag-grid-react'
import { AllCommunityModule, ModuleRegistry } from 'ag-grid-community'
import type { ColDef } from 'ag-grid-community'

ModuleRegistry.registerModules([AllCommunityModule])

const columnDefs: ColDef[] = [
  { field: 'name', headerName: 'Name', flex: 1 },
  { field: 'price', valueFormatter: p => `$${p.value}` },
]

<div style={{ height: 500 }}>
  <AgGridReact
    rowData={data}
    columnDefs={columnDefs}
    pagination={true}
  />
</div>
```

### Conditional Cell Styling
```tsx
{
  field: 'stock',
  cellStyle: (params) => {
    if (params.value <= 0) return { color: 'red' }
    if (params.value < 10) return { color: 'orange' }
    return { color: 'green' }
  }
}
```

### Custom Cell Renderer
```tsx
function ActionRenderer(props: ICellRendererParams<Product>) {
  return (
    <button onClick={() => handleEdit(props.data)}>Edit</button>
  )
}

{ cellRenderer: ActionRenderer }
```

---

## Quick Reference URLs

| Service | URL |
|---------|-----|
| React Frontend | http://localhost:5173 |
| FastAPI Backend | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/api/docs |
| Database File | `data/erp.db` |

---

## Common Mistakes ❌

### React
| Mistake | Fix |
|---------|-----|
| `class="..."` | `className="..."` |
| Forgetting key | `key={item.id}` |
| Mutating state | Use setter with spread |
| Not handling loading | Add loading state |

### FastAPI
| Mistake | Fix |
|---------|-----|
| Forgetting `db.commit()` | Always commit |
| Not refreshing after insert | `db.refresh(item)` |
| Wrong status code | Use `status.HTTP_201_CREATED` |
| Missing CORS | Add CORSMiddleware |

### AG Grid
| Mistake | Fix |
|---------|-----|
| Missing module registration | `ModuleRegistry.registerModules([AllCommunityModule])` |
| Wrong import | Use `import type { ColDef }` |
| No height on container | Add `style={{ height: 500 }}` |
