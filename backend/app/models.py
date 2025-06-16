# backend/app/models.py

from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
    func
)
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column

# The Declarative Base is a factory function that constructs a base class for
# declarative class definitions. All of our models will inherit from this class.
Base = declarative_base()

class User(Base):
    """
    SQLAlchemy model for the 'users' table.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # This creates the one-to-many relationship.
    # The 'back_populates' argument tells SQLAlchemy to link this relationship
    # with the 'author' relationship on the Recipe model.
    recipes: Mapped[list["Recipe"]] = relationship(
        "Recipe", back_populates="author", cascade="all, delete-orphan"
    )


class Recipe(Base):
    """
    SQLAlchemy model for the 'recipes' table.
    """
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # This column holds the foreign key to the 'users' table.
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    # This creates the many-to-one relationship from Recipe to User.
    # 'back_populates' links it back to the 'recipes' relationship on the User model.
    author: Mapped["User"] = relationship("User", back_populates="recipes")