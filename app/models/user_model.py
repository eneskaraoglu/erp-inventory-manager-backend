from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class UserModel(Base):
    """
    User database model (SQLAlchemy ORM)

    JAVA EQUIVALENT:
    @Entity
    @Table(name = "users")
    public class User {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;

        @Column(nullable = false, unique = true, length = 50)
        private String username;

        @Column(nullable = false, unique = true, length = 100)
        private String email;

        @Column(nullable = false, length = 255)
        private String passwordHash;

        @Column(length = 100)
        private String fullName;

        @Column(nullable = false)
        private Boolean isActive = true;

        @Column(nullable = false, length = 20)
        private String role = "user";

        @Column(nullable = false, updatable = false)
        @CreationTimestamp
        private LocalDateTime createdAt;
    }
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)  # Stores hashed password
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(String(20), default="user", nullable=False)  # user, admin, manager
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
