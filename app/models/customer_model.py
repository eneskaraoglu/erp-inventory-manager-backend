# ============================================
# CUSTOMER DATABASE MODEL (SQLAlchemy)
# Like @Entity class in JPA/Hibernate
# ============================================

from sqlalchemy import Column, Integer, String
from app.database import Base


class CustomerModel(Base):
    """
    SQLAlchemy Model - Maps to database table
    
    JAVA EQUIVALENT:
    @Entity
    @Table(name = "customers")
    public class Customer {
        @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;
        
        @Column(nullable = false, length = 100)
        private String name;
        
        @Column(nullable = false, unique = true)
        private String email;
        
        @Column(length = 20)
        private String phone;
        
        @Column(length = 200)
        private String address;
        
        @Column(length = 100)
        private String company;
    }
    """
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20), nullable=True)
    address = Column(String(200), nullable=True)
    company = Column(String(100), nullable=True)
