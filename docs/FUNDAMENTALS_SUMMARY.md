# React Fundamentals - What You Learned (Session 1 & 2)

## 📊 Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        REACT APP                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Components (UI pieces)                                  │  │
│  │      ↓                                                   │  │
│  │  Props (data flows DOWN)                                 │  │
│  │      ↓                                                   │  │
│  │  useState (component remembers data)                     │  │
│  │      ↓                                                   │  │
│  │  useEffect (side effects: API, localStorage)            │  │
│  │      ↓                                                   │  │
│  │  React Router (multiple pages)                          │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1️⃣ Components & JSX

### What is it?
A **Component** is a reusable piece of UI. Like LEGO blocks for web pages.

### Java Equivalent
```
React Component  =  JPanel class in Swing
                 =  @Component in JSF
```

### Syntax
```tsx
// Function that returns JSX (HTML-like syntax)
function ProductCard() {
  return (
    <div>
      <h1>Product Name</h1>
      <p>Price: $99</p>
    </div>
  )
}
```

### Key Rules
| JSX | HTML | Why? |
|-----|------|------|
| `className` | `class` | `class` is reserved word in JS |
| `onClick` | `onclick` | camelCase in React |
| `<img />` | `<img>` | Must close all tags |
| `{variable}` | - | Embed JavaScript with `{}` |

### Usage
```tsx
// Use component like HTML tag
<ProductCard />
<ProductCard />  // Reuse!
```

---

## 2️⃣ Props (Properties)

### What is it?
**Props** = Data passed from Parent → Child component (ONE WAY only!)

### Java Equivalent
```
Props  =  Constructor parameters
       =  Method arguments
```

### Visual Flow
```
Parent Component
    │
    │  <ProductCard name="Laptop" price={999} />
    │
    ▼
Child Component (receives props)
    │
    │  function ProductCard({ name, price }) {
    │    return <div>{name} - ${price}</div>
    │  }
```

### With TypeScript
```tsx
// Define what props are expected (like Java interface)
interface ProductCardProps {
  name: string      // required
  price: number     // required
  discount?: number // optional (?)
}

function ProductCard({ name, price, discount }: ProductCardProps) {
  return <div>{name}</div>
}
```

### Key Rules
- Props are **READ-ONLY** (never modify!)
- Data flows **DOWN** only (parent → child)
- To send data UP: pass a **function** as prop

```tsx
// Parent
function Parent() {
  const handleDelete = (id: number) => { /* delete logic */ }
  return <Child onDelete={handleDelete} />  // pass function down
}

// Child
function Child({ onDelete }) {
  return <button onClick={() => onDelete(5)}>Delete</button>  // call parent's function
}
```

---

## 3️⃣ useState (Local State)

### What is it?
**useState** = Component's memory. Data that can CHANGE and triggers UI update.

### Java Equivalent
```
useState  =  Class field + PropertyChangeListener
          =  Observable variable that auto-updates UI
```

### Syntax
```tsx
const [value, setValue] = useState(initialValue)
//     ↑        ↑                    ↑
//   current  function to        starting
//   value    update it          value
```

### Example
```tsx
function Counter() {
  const [count, setCount] = useState(0)
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Add
      </button>
    </div>
  )
}
```

### Key Rules

| Do ✅ | Don't ❌ |
|-------|---------|
| `setCount(5)` | `count = 5` |
| `setProducts([...products, new])` | `products.push(new)` |
| Use setter function | Mutate directly |

### Why?
```tsx
// ❌ Direct mutation - React doesn't know it changed!
count = 5  // UI won't update

// ✅ Setter function - React re-renders UI
setCount(5)  // UI updates automatically
```

### Common Patterns
```tsx
// Simple value
const [name, setName] = useState('')

// Array
const [products, setProducts] = useState<Product[]>([])
setProducts([...products, newProduct])  // Add
setProducts(products.filter(p => p.id !== id))  // Delete

// Object
const [user, setUser] = useState({ name: '', age: 0 })
setUser({ ...user, name: 'John' })  // Update one field

// Lazy initialization (expensive computation)
const [data, setData] = useState(() => {
  return JSON.parse(localStorage.getItem('data'))
})
```

---

## 4️⃣ useEffect (Side Effects)

### What is it?
**useEffect** = Do something AFTER render. For side effects like:
- Fetch data from API
- Save to localStorage
- Set up timers
- Subscribe to events

### Java Equivalent
```
useEffect  =  @PostConstruct (run after component created)
           =  componentDidMount / componentDidUpdate in old React
```

### Syntax
```tsx
useEffect(() => {
  // This code runs after render
  
  return () => {
    // Cleanup (optional) - runs before next effect or unmount
  }
}, [dependencies])  // When to run
```

### Dependency Array Controls WHEN it Runs

| Dependency | When it runs | Use case |
|------------|--------------|----------|
| `[]` | Once on mount | Fetch initial data |
| `[products]` | When `products` changes | Save to localStorage |
| No array | Every render | Rarely used |

### Examples
```tsx
// Run ONCE when component mounts
useEffect(() => {
  console.log('Component mounted!')
}, [])

// Run when 'products' changes
useEffect(() => {
  localStorage.setItem('products', JSON.stringify(products))
}, [products])

// Cleanup example (timer)
useEffect(() => {
  const timer = setInterval(() => console.log('tick'), 1000)
  
  return () => clearInterval(timer)  // Cleanup!
}, [])
```

### Visual Timeline
```
Component Mount
      │
      ▼
   Render
      │
      ▼
   useEffect runs ← (after render)
      │
      ▼
State changes (setProducts)
      │
      ▼
   Re-render
      │
      ▼
   useEffect runs again (if dependency changed)
```

---

## 5️⃣ React Router (Pages/Navigation)

### What is it?
**React Router** = Multiple pages in a Single Page Application (SPA)

### Java Equivalent
```
React Router  =  web.xml servlet mapping
              =  @RequestMapping in Spring
              =  FacesServlet URL patterns
```

### Core Concepts

| Concept | Purpose | Java Equivalent |
|---------|---------|-----------------|
| `<BrowserRouter>` | Enable routing | Application context |
| `<Routes>` | Container for routes | - |
| `<Route>` | URL → Component mapping | @RequestMapping |
| `<Link>` | Navigation (no reload) | - |
| `useParams()` | Get URL params | @PathVariable |
| `useNavigate()` | Redirect in code | response.sendRedirect() |

### Setup
```tsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/products">Products</Link>
      </nav>
      
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/products" element={<Products />} />
        <Route path="/products/:id" element={<ProductDetail />} />
      </Routes>
    </BrowserRouter>
  )
}
```

### URL Parameters
```tsx
// Route definition
<Route path="/products/:id" element={<ProductDetail />} />

// In ProductDetail component
function ProductDetail() {
  const { id } = useParams()  // URL: /products/123 → id = "123"
  
  // Find product
  const product = products.find(p => p.id === Number(id))
}
```

### Programmatic Navigation
```tsx
function AddProduct() {
  const navigate = useNavigate()
  
  const handleSubmit = () => {
    // Save product...
    navigate('/products')  // Redirect after save
  }
}
```

### Link vs a href
```tsx
// ❌ Full page reload (slow)
<a href="/products">Products</a>

// ✅ Client-side navigation (fast, keeps state)
<Link to="/products">Products</Link>
```

---

## 🔗 How They All Connect

```
App.tsx (ROOT)
│
├── BrowserRouter (enables routing)
│   │
│   └── Routes
│       │
│       ├── Route "/" → Dashboard
│       │                 │
│       │                 └── receives products (props)
│       │
│       ├── Route "/products" → ProductsPage
│       │                         │
│       │                         ├── useState (searchTerm)
│       │                         ├── receives products (props)
│       │                         └── renders ProductCard (component)
│       │
│       └── Route "/products/:id" → ProductDetailPage
│                                     │
│                                     ├── useParams (get id)
│                                     ├── useNavigate (redirect)
│                                     └── receives products (props)
│
├── useState (products array)
│
└── useEffect (save to localStorage)
```

---

## 📝 Quick Reference Card

```
COMPONENT
─────────
function Name() { return <div>...</div> }

PROPS
─────
<Child name="X" />              // Pass
function Child({ name }) {}     // Receive

STATE
─────
const [val, setVal] = useState(initial)
setVal(newValue)                // Update

EFFECT
──────
useEffect(() => { }, [])        // Once
useEffect(() => { }, [dep])     // When dep changes

ROUTER
──────
<Link to="/path">               // Navigate
<Route path="/x/:id" />         // Define route
const { id } = useParams()      // Get param
const nav = useNavigate()       // Redirect
nav('/path')
```

---

## ✅ You Can Now Build

With these 5 concepts, you can build:

- ✅ Multi-page applications
- ✅ Lists with add/delete
- ✅ Search/filter functionality
- ✅ Detail pages with URL parameters
- ✅ Data persistence (localStorage)
- ✅ Navigation between pages

---

## ➡️ Next Concepts to Learn

1. **useContext** - Share state globally (no prop drilling)
2. **useReducer** - Complex state logic
3. **Custom Hooks** - Reusable logic
4. **API Integration** - Connect to backend
5. **React Query** - Smart data fetching

---

**You've built a solid foundation! 🎉**
