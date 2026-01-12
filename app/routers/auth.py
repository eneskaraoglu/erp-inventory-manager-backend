# ============================================
# AUTH ROUTER - JWT Authentication
# Like Spring Security's AuthenticationController
# ============================================

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
import hashlib
import jwt

from app.database import get_db
from app.models.user_model import UserModel

router = APIRouter()

# ============================================
# CONFIGURATION
# In production, use environment variables!
# ============================================

SECRET_KEY = "your-secret-key-change-in-production"  # Like application.properties
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

security = HTTPBearer()


# ============================================
# SCHEMAS (DTOs in Java)
# ============================================

class LoginRequest(BaseModel):
    """Login credentials"""
    username: str
    password: str


class LoginResponse(BaseModel):
    """Login response with token"""
    access_token: str
    token_type: str = "bearer"
    user: dict  # User info (without password)


class TokenPayload(BaseModel):
    """JWT token payload"""
    sub: str  # subject (user_id)
    username: str
    role: str
    exp: datetime


# ============================================
# HELPER FUNCTIONS
# ============================================

def hash_password(password: str) -> str:
    """Hash password with SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def create_access_token(user: UserModel) -> str:
    """
    Create JWT token for user
    
    JAVA EQUIVALENT:
    public String createToken(User user) {
        return Jwts.builder()
            .setSubject(String.valueOf(user.getId()))
            .claim("username", user.getUsername())
            .claim("role", user.getRole())
            .setExpiration(new Date(System.currentTimeMillis() + EXPIRATION))
            .signWith(SignatureAlgorithm.HS256, SECRET_KEY)
            .compact();
    }
    """
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {
        "sub": str(user.id),      # User ID as subject
        "username": user.username,
        "role": user.role,
        "exp": expire
    }
    
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
    """
    Verify and decode JWT token
    
    JAVA EQUIVALENT:
    public Claims verifyToken(String token) {
        return Jwts.parser()
            .setSigningKey(SECRET_KEY)
            .parseClaimsJws(token)
            .getBody();
    }
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


# ============================================
# DEPENDENCY - Get Current User from Token
# Like @AuthenticationPrincipal in Spring
# ============================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> UserModel:
    """
    Extract user from JWT token
    
    JAVA EQUIVALENT:
    public User getCurrentUser(@AuthenticationPrincipal UserDetails userDetails) {
        return userRepository.findByUsername(userDetails.getUsername())
            .orElseThrow(() -> new UnauthorizedException("User not found"));
    }
    """
    token = credentials.credentials
    payload = verify_token(token)
    
    user_id = int(payload["sub"])
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive"
        )
    
    return user


# ============================================
# ENDPOINTS
# ============================================

@router.post("/auth/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token
    
    JAVA EQUIVALENT:
    @PostMapping("/auth/login")
    public ResponseEntity<LoginResponse> login(@RequestBody LoginRequest request) {
        User user = userRepository.findByUsername(request.getUsername())
            .orElseThrow(() -> new UnauthorizedException("Invalid credentials"));
        
        if (!passwordEncoder.matches(request.getPassword(), user.getPasswordHash())) {
            throw new UnauthorizedException("Invalid credentials");
        }
        
        String token = jwtService.createToken(user);
        return ResponseEntity.ok(new LoginResponse(token, user));
    }
    """
    # Find user by username
    user = db.query(UserModel).filter(
        UserModel.username == request.username
    ).first()
    
    # Check if user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Verify password
    password_hash = hash_password(request.password)
    if user.password_hash != password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive"
        )
    
    # Create JWT token
    token = create_access_token(user)
    
    # Return token and user info
    return LoginResponse(
        access_token=token,
        user={
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active
        }
    )


@router.get("/auth/me")
def get_me(current_user: UserModel = Depends(get_current_user)):
    """
    Get current authenticated user
    
    JAVA EQUIVALENT:
    @GetMapping("/auth/me")
    public User getMe(@AuthenticationPrincipal User user) {
        return user;
    }
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "is_active": current_user.is_active
    }


@router.post("/auth/logout")
def logout():
    """
    Logout - client-side just removes token
    
    Note: JWT is stateless, so we can't invalidate server-side
    In production, you might use a token blacklist with Redis
    """
    return {"message": "Logged out successfully"}
