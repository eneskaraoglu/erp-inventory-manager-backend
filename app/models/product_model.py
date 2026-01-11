# ============================================
# PRODUCT DATABASE MODEL (SQLAlchemy)
# Like @Entity class in JPA/Hibernate
# ============================================

from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class ProductModel(Base):
    """
    SQLAlchemy Model - Maps to database table
    
    JAVA EQUIVALENT:
    @Entity
    @Table(name = "products")
    public class Product {
        @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;
        
        @Column(nullable = false, length = 100)
        private String name;
        
        @Column(length = 500)
        private String description;
        
        @Column(nullable = false)
        private Double price;
        
        @Column(nullable = false)
        private Integer stock;
        
        @Column(length = 50)
        private String category;
    }
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    category = Column(String(50), nullable=True)
