from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# SQLite Database Configuration
DATABASE_URL = "sqlite:///./test.db"

# Creating an engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Base class for declarative models
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String) 

    # Relationship with PortfolioModel
    portfolios = relationship("PortfolioModel", back_populates="user", cascade="all, delete-orphan")

# Portfolio model
class PortfolioModel(Base):
    __tablename__ = "portfolio"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    scheme_code = Column(Integer, nullable=False)
    scheme_name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)

    # Relationship back to User
    user = relationship("User", back_populates="portfolios")

# Create a new session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create the database and the tables."""
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
