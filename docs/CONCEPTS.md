# Full-Stack Concepts - Quick Reference

---

# Part 1: React Frontend

## Java ↔ React Comparison

| Java/Swing | React | Notes |
|------------|-------|-------|
| JPanel class | Function Component | Both are reusable UI units |
| Constructor params | Props | Data passed from parent |
| Class fields | useState | Mutable component data |
| PropertyChangeListener | useState setter | Triggers UI update |
| componentDidMount | useEffect(() => {}, []) | Runs once on mount |
| componentDidUpdate | useEffect(() => {}, [deps]) | Runs when deps change |
| ActionListener | onClick, onChange | Event handlers |
| for loop + add() | .map() + JSX | Rendering lists |
| if/else for visibility | Conditional rendering | `{show && <Component />}` |
| Servlet URL mapping | React Router | URL → Component |
| Command Pattern | useReducer | Action-based state changes |
| Component reference | useRef | DOM access |
| Bean Validation | Zod | Form validation |
| HttpClient | fetch() | API calls |

---

## Hook Rules 📜

1. **Only call hooks at top level**
   ```tsx
   // ❌ WRONG
   if (condition) {
     const [state, setState] = useState()
   }
   
   // ✅ CORRECT
   const [state, setState] = useState()
   if (condition) { /* use state */ }
   ```

2. **Only call hooks in React functions**
   ```tsx
   // ❌ WRONG - regular function
   function helper() {
     const [state, setState] = useState()
   }
   
   // ✅ CORRECT - React component
   function MyComponent() {
     const [state, setState] = useState()
   }
   ```

---

## useState Patterns

### Basic
```tsx
const [count, setCount] = useState(0)
setCount(5)           // Set to 5
setCount(c => c + 1)  // Increment (use prev value)
```

### With Object
```tsx
const [user, setUser] = useState({ name: '', age: 0 })
setUser({ ...user, name: 'John' })  // Spread to keep other fields
```

### With Array
```tsx
const [items, setItems] = useState([])
setItems([...items, newItem])       // Add item
setItems(items.filter(i => i.id !== id))  // Remove item
```

---

## useEffect Patterns

### Run Once (on mount)
```tsx
useEffect(() => {
  fetchData()
}, [])  // Empty array = only on mount
```

### Run on Dependency Change
```tsx
useEffect(() => {
  console.log('products changed')
}, [products])  // Runs when products changes
```

### Cleanup
```tsx
useEffect(() => {
  const timer = setInterval(() => {}, 1000)
  return () => clearInterval(timer)  // Cleanup
}, [])
```

---

## API Integration Patterns ✨ NEW

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

### DELETE Request
```tsx
const deleteProduct = async (id) => {
  await fetch(`http://localhost:8000/api/products/${id}`, {
    method: 'DELETE'
  })
}
```

---

## Loading & Error States ✨ NEW

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

## useReducer Patterns

### When to Use
- Multiple related state values
- Complex state logic
- Many actions on same state

### Basic Pattern
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

## useRef Patterns

### DOM Reference
```tsx
const inputRef = useRef<HTMLInputElement>(null)

<input ref={inputRef} />

inputRef.current?.focus()
```

### Persist Value (no re-render)
```tsx
const renderCount = useRef(0)
renderCount.current += 1  // Doesn't cause re-render!
```

---

## Zod Validation Patterns

```tsx
import { z } from 'zod'

const schema = z.object({
  name: z.string().min(1, 'Required').max(100),
  email: z.string().email('Invalid email'),
  price: z.string().refine(v => Number(v) > 0, 'Must be positive'),
})

// Validate
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
| `ResponseEntity` | Return value | Auto JSON |
| `@Service` | Function | Business logic |
| `throw Exception` | `raise HTTPException` | Error handling |

---

## Database: Java ↔ Python

| Java/Spring | Python/FastAPI | Notes |
|-------------|----------------|-------|
| H2 Database | SQLite | Embedded DB |
| Hibernate/JPA | SQLAlchemy | ORM |
| `@Entity` | `class Model(Base)` | DB table |
| `@Id @GeneratedValue` | `Column(primary_key=True)` | Auto ID |
| `@Column` | `Column()` | Table column |
| `JpaRepository` | `db.query()` | DB operations |
| `@Autowired` | `Depends(get_db)` | Inject session |
| `@Transactional` | `db.commit()` | Save changes |
| `data.sql` | `seed_data()` | Initial data |

---

## SQLAlchemy Model Pattern

```python
# Like @Entity in JPA
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
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, length = 100)
    private String name;
    
    @Column(nullable = false)
    private Double price;
    
    @Column
    private Integer stock = 0;
}
```

---

## Repository Pattern

```python
# Python/FastAPI
@router.get("/products")
def get_all(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()

@router.get("/products/{id}")
def get_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Not found")
    return product

@router.post("/products")
def create(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
```

**Java Equivalent:**
```java
@GetMapping("/products")
public List<Product> getAll() {
    return repository.findAll();
}

@GetMapping("/products/{id}")
public Product getById(@PathVariable Long id) {
    return repository.findById(id)
        .orElseThrow(() -> new NotFoundException("Not found"));
}

@PostMapping("/products")
public Product create(@RequestBody ProductDTO dto) {
    Product product = new Product();
    BeanUtils.copyProperties(dto, product);
    return repository.save(product);
}
```

---

## Pydantic vs Bean Validation

```python
# Python/Pydantic
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
```

```java
// Java/Bean Validation
public class ProductDTO {
    @NotBlank @Size(min=1, max=100)
    private String name;
    
    @NotNull @Positive
    private Double price;
    
    @NotNull @PositiveOrZero
    private Integer stock;
}
```

---

## Database Session (Dependency Injection)

```python
# Python - Like @Autowired EntityManager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Usage
@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()
```

```java
// Java Equivalent
@Autowired
private EntityManager entityManager;

// Or with Spring Data
@Autowired
private ProductRepository repository;
```

---

## Common Mistakes ❌

### React
| Mistake | Fix |
|---------|-----|
| `class="..."` | `className="..."` |
| Forgetting key | `key={item.id}` |
| Mutating state directly | Use setter with spread |
| Not handling loading/error | Add states |

### FastAPI
| Mistake | Fix |
|---------|-----|
| Forgetting `db.commit()` | Always commit after changes |
| Not refreshing after insert | `db.refresh(item)` |
| Wrong status code | Use `status.HTTP_201_CREATED` |
| Missing CORS | Add CORSMiddleware |

---

## Full-Stack Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│  React Component                                            │
│  const { data } = await fetch('/api/products')              │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP Request
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  FastAPI Router                                             │
│  @router.get("/products")                                   │
│  def get_products(db: Session = Depends(get_db)):          │
└─────────────────────────┬───────────────────────────────────┘
                          │ SQLAlchemy Query
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  SQLite Database                                            │
│  SELECT * FROM products                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Reference URLs

| Service | URL |
|---------|-----|
| React Frontend | http://localhost:5173 |
| FastAPI Backend | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/api/docs |
| Database File | `data/erp.db` |
