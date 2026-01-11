from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
import hashlib

from app.database import get_db
from app.models.user_model import UserModel
from app.models.user import User, UserCreate, UserUpdate

router = APIRouter()


def hash_password(password: str) -> str:
    """
    Simple password hashing (for learning purposes)
    In production, use bcrypt or passlib

    JAVA EQUIVALENT:
    public String hashPassword(String password) {
        return BCrypt.hashpw(password, BCrypt.gensalt());
    }
    """
    return hashlib.sha256(password.encode()).hexdigest()


@router.get("/users", response_model=List[User])
def get_all_users(db: Session = Depends(get_db)):
    """
    Get all users from database

    JAVA EQUIVALENT:
    @GetMapping("/users")
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }
    """
    return db.query(UserModel).all()


@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a single user by ID

    JAVA EQUIVALENT:
    @GetMapping("/users/{id}")
    public User getUser(@PathVariable Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new NotFoundException("User not found"));
    }
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user


@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user

    JAVA EQUIVALENT:
    @PostMapping("/users")
    public User createUser(@RequestBody UserDTO dto) {
        // Check for duplicate username
        if (userRepository.existsByUsername(dto.getUsername())) {
            throw new BadRequestException("Username already exists");
        }
        // Check for duplicate email
        if (userRepository.existsByEmail(dto.getEmail())) {
            throw new BadRequestException("Email already exists");
        }
        User user = new User();
        BeanUtils.copyProperties(dto, user);
        user.setPasswordHash(BCrypt.hashpw(dto.getPassword(), BCrypt.gensalt()));
        return userRepository.save(user);
    }
    """
    # Check if username already exists
    existing_username = db.query(UserModel).filter(UserModel.username == user.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username '{user.username}' already exists"
        )

    # Check if email already exists
    existing_email = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{user.email}' already exists"
        )

    # Create user with hashed password
    user_data = user.model_dump()
    password = user_data.pop("password")  # Remove plain password

    db_user = UserModel(
        **user_data,
        password_hash=hash_password(password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Update an existing user

    JAVA EQUIVALENT:
    @PutMapping("/users/{id}")
    public User updateUser(@PathVariable Long id, @RequestBody UserDTO dto) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new NotFoundException("User not found"));

        // Check username uniqueness if changed
        if (dto.getUsername() != null && !dto.getUsername().equals(user.getUsername())) {
            if (userRepository.existsByUsername(dto.getUsername())) {
                throw new BadRequestException("Username already exists");
            }
        }

        // Check email uniqueness if changed
        if (dto.getEmail() != null && !dto.getEmail().equals(user.getEmail())) {
            if (userRepository.existsByEmail(dto.getEmail())) {
                throw new BadRequestException("Email already exists");
            }
        }

        BeanUtils.copyProperties(dto, user, getNullPropertyNames(dto));

        if (dto.getPassword() != null) {
            user.setPasswordHash(BCrypt.hashpw(dto.getPassword(), BCrypt.gensalt()));
        }

        return userRepository.save(user);
    }
    """
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    update_data = user_update.model_dump(exclude_unset=True)

    # Check if username is being updated and already exists
    if "username" in update_data and update_data["username"] != db_user.username:
        username_exists = db.query(UserModel).filter(
            UserModel.username == update_data["username"],
            UserModel.id != user_id
        ).first()
        if username_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Username '{update_data['username']}' already exists"
            )

    # Check if email is being updated and already exists
    if "email" in update_data and update_data["email"] != db_user.email:
        email_exists = db.query(UserModel).filter(
            UserModel.email == update_data["email"],
            UserModel.id != user_id
        ).first()
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{update_data['email']}' already exists"
            )

    # Handle password update separately
    if "password" in update_data:
        password = update_data.pop("password")
        update_data["password_hash"] = hash_password(password)

    # Update only provided fields
    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user

    JAVA EQUIVALENT:
    @DeleteMapping("/users/{id}")
    public void deleteUser(@PathVariable Long id) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new NotFoundException("User not found"));
        userRepository.delete(user);
    }
    """
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    db.delete(db_user)
    db.commit()
    return None
