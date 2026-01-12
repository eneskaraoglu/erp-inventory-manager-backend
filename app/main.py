from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routers import products, customers, users, auth
from app.database import init_db, SessionLocal
from app.models.product_model import ProductModel
from app.models.customer_model import CustomerModel
from app.models.user_model import UserModel
import hashlib


def seed_data():
    """
    Add initial data if database is empty.
    Like Spring's data.sql or CommandLineRunner
    """
    db = SessionLocal()
    try:
        # Check if products exist
        if db.query(ProductModel).count() == 0:
            print("Seeding products...")
            products_data = [
                ProductModel(name="Laptop", description="High-performance laptop", price=999.99, stock=50, category="Electronics"),
                ProductModel(name="Mouse", description="Wireless mouse", price=29.99, stock=100, category="Accessories"),
                ProductModel(name="Keyboard", description="Mechanical keyboard", price=89.99, stock=75, category="Accessories"),
                ProductModel(name="Monitor", description="27-inch 4K monitor", price=449.99, stock=30, category="Electronics"),
            ]
            db.add_all(products_data)
            db.commit()
            print(f"Added {len(products_data)} products")

        # Check if customers exist
        if db.query(CustomerModel).count() == 0:
            print("Seeding customers...")
            customers_data = [
                CustomerModel(name="John Doe", email="john@example.com", phone="+1234567890", address="123 Main St, New York, NY", company="Acme Corp"),
                CustomerModel(name="Jane Smith", email="jane@example.com", phone="+0987654321", address="456 Oak Ave, Los Angeles, CA", company="Tech Solutions"),
                CustomerModel(name="Bob Johnson", email="bob@example.com", phone="+1122334455", address="789 Pine Rd, Chicago, IL", company="Global Industries"),
            ]
            db.add_all(customers_data)
            db.commit()
            print(f"Added {len(customers_data)} customers")

        # Check if users exist
        if db.query(UserModel).count() == 0:
            print("Seeding users...")
            users_data = [
                UserModel(
                    username="admin",
                    email="admin@example.com",
                    password_hash=hashlib.sha256("admin123".encode()).hexdigest(),
                    full_name="Admin User",
                    role="admin",
                    is_active=True
                ),
                UserModel(
                    username="manager",
                    email="manager@example.com",
                    password_hash=hashlib.sha256("manager123".encode()).hexdigest(),
                    full_name="Manager User",
                    role="manager",
                    is_active=True
                ),
                UserModel(
                    username="johndoe",
                    email="john.user@example.com",
                    password_hash=hashlib.sha256("password123".encode()).hexdigest(),
                    full_name="John Doe",
                    role="user",
                    is_active=True
                ),
            ]
            db.add_all(users_data)
            db.commit()
            print(f"Added {len(users_data)} users")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events.
    Like @PostConstruct and @PreDestroy in Spring
    """
    # Startup
    print("Starting ERP Inventory Manager API...")
    init_db()
    seed_data()
    yield
    # Shutdown
    print("Shutting down...")


app = FastAPI(
    title="ERP Inventory Manager API",
    description="Backend API for ERP Inventory Management System",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# CORS middleware - Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default
        "http://localhost:3000",  # Create React App default
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api", tags=["Authentication"])  # Auth first!
app.include_router(products.router, prefix="/api", tags=["Products"])
app.include_router(customers.router, prefix="/api", tags=["Customers"])
app.include_router(users.router, prefix="/api", tags=["Users"])


@app.get("/")
def read_root():
    """Root endpoint - API health check"""
    return {
        "message": "ERP Inventory Manager API",
        "status": "running",
        "database": "SQLite (persistent)",
        "docs": "/api/docs",
        "version": "1.0.0"
    }


@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "database": "connected"}
