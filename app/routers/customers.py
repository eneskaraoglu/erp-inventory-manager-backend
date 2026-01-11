from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.customer_model import CustomerModel
from app.models.customer import Customer, CustomerCreate, CustomerUpdate

router = APIRouter()


@router.get("/customers", response_model=List[Customer])
def get_all_customers(db: Session = Depends(get_db)):
    """
    Get all customers from database
    
    JAVA EQUIVALENT:
    @GetMapping("/customers")
    public List<Customer> getAllCustomers() {
        return customerRepository.findAll();
    }
    """
    return db.query(CustomerModel).all()


@router.get("/customers/{customer_id}", response_model=Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Get a single customer by ID
    
    JAVA EQUIVALENT:
    @GetMapping("/customers/{id}")
    public Customer getCustomer(@PathVariable Long id) {
        return customerRepository.findById(id)
            .orElseThrow(() -> new NotFoundException("Customer not found"));
    }
    """
    customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with id {customer_id} not found"
        )
    return customer


@router.post("/customers", response_model=Customer, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """
    Create a new customer
    
    JAVA EQUIVALENT:
    @PostMapping("/customers")
    public Customer createCustomer(@RequestBody CustomerDTO dto) {
        // Check for duplicate email
        if (customerRepository.existsByEmail(dto.getEmail())) {
            throw new BadRequestException("Email already exists");
        }
        Customer customer = new Customer();
        BeanUtils.copyProperties(dto, customer);
        return customerRepository.save(customer);
    }
    """
    # Check if email already exists
    existing = db.query(CustomerModel).filter(CustomerModel.email == customer.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Customer with email {customer.email} already exists"
        )

    db_customer = CustomerModel(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


@router.put("/customers/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer_update: CustomerUpdate, db: Session = Depends(get_db)):
    """
    Update an existing customer
    
    JAVA EQUIVALENT:
    @PutMapping("/customers/{id}")
    public Customer updateCustomer(@PathVariable Long id, @RequestBody CustomerDTO dto) {
        Customer customer = customerRepository.findById(id)
            .orElseThrow(() -> new NotFoundException("Customer not found"));
        // Check email uniqueness if changed
        if (dto.getEmail() != null && !dto.getEmail().equals(customer.getEmail())) {
            if (customerRepository.existsByEmail(dto.getEmail())) {
                throw new BadRequestException("Email already exists");
            }
        }
        BeanUtils.copyProperties(dto, customer, getNullPropertyNames(dto));
        return customerRepository.save(customer);
    }
    """
    db_customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
    
    if not db_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with id {customer_id} not found"
        )

    # Check if email is being updated and already exists
    update_data = customer_update.model_dump(exclude_unset=True)
    if "email" in update_data and update_data["email"] != db_customer.email:
        email_exists = db.query(CustomerModel).filter(
            CustomerModel.email == update_data["email"],
            CustomerModel.id != customer_id
        ).first()
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Customer with email {update_data['email']} already exists"
            )

    # Update only provided fields
    for field, value in update_data.items():
        setattr(db_customer, field, value)
    
    db.commit()
    db.refresh(db_customer)
    return db_customer


@router.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Delete a customer
    
    JAVA EQUIVALENT:
    @DeleteMapping("/customers/{id}")
    public void deleteCustomer(@PathVariable Long id) {
        Customer customer = customerRepository.findById(id)
            .orElseThrow(() -> new NotFoundException("Customer not found"));
        customerRepository.delete(customer);
    }
    """
    db_customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
    
    if not db_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with id {customer_id} not found"
        )
    
    db.delete(db_customer)
    db.commit()
    return None
