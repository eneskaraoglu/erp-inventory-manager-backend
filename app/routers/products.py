from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.product_model import ProductModel
from app.models.product import Product, ProductCreate, ProductUpdate

router = APIRouter()


@router.get("/products", response_model=List[Product])
def get_all_products(db: Session = Depends(get_db)):
    """
    Get all products from database
    
    JAVA EQUIVALENT:
    @GetMapping("/products")
    public List<Product> getAllProducts() {
        return productRepository.findAll();
    }
    """
    return db.query(ProductModel).all()


@router.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get a single product by ID
    
    JAVA EQUIVALENT:
    @GetMapping("/products/{id}")
    public Product getProduct(@PathVariable Long id) {
        return productRepository.findById(id)
            .orElseThrow(() -> new NotFoundException("Product not found"));
    }
    """
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    return product


@router.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product
    
    JAVA EQUIVALENT:
    @PostMapping("/products")
    public Product createProduct(@RequestBody ProductDTO dto) {
        Product product = new Product();
        BeanUtils.copyProperties(dto, product);
        return productRepository.save(product);
    }
    """
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)  # Get the generated ID
    return db_product


@router.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    """
    Update an existing product
    
    JAVA EQUIVALENT:
    @PutMapping("/products/{id}")
    public Product updateProduct(@PathVariable Long id, @RequestBody ProductDTO dto) {
        Product product = productRepository.findById(id)
            .orElseThrow(() -> new NotFoundException("Product not found"));
        BeanUtils.copyProperties(dto, product, getNullPropertyNames(dto));
        return productRepository.save(product);
    }
    """
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )

    # Update only provided fields
    update_data = product_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete a product
    
    JAVA EQUIVALENT:
    @DeleteMapping("/products/{id}")
    public void deleteProduct(@PathVariable Long id) {
        Product product = productRepository.findById(id)
            .orElseThrow(() -> new NotFoundException("Product not found"));
        productRepository.delete(product);
    }
    """
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    
    db.delete(db_product)
    db.commit()
    return None
