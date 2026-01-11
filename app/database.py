# ============================================
# DATABASE CONFIGURATION
# Like Spring's DataSource configuration
# ============================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SQLite database file path - data persists here!
DATABASE_PATH = os.path.join(BASE_DIR, "data", "erp.db")

# Database URL (like jdbc:h2:file:./data/erp in Java)
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Create engine (like DataSource in Spring)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Session factory (like EntityManagerFactory)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models (like @MappedSuperclass)
Base = declarative_base()


def get_db():
    """
    Dependency that provides database session.
    
    JAVA EQUIVALENT:
    @Autowired
    private EntityManager entityManager;
    
    Or in Spring:
    @Transactional
    public void someMethod() { ... }
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Create all tables if they don't exist.
    Like Hibernate's hbm2ddl.auto=update
    """
    # Import models so SQLAlchemy knows about them
    from app.models import product_model, customer_model, user_model

    # Create tables
    Base.metadata.create_all(bind=engine)
    print(f"Database initialized at: {DATABASE_PATH}")
