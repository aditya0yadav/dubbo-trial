"""Pydantic models for the User Management Service."""
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class Address(BaseModel):
    """Address model that can be serialized to Protobuf."""
    street: str
    city: str
    country: str
    postal_code: str = Field(alias="postal_code")
    
    class Config:
        populate_by_name = True


class User(BaseModel):
    """User model that can be serialized to Protobuf."""
    id: int
    name: str
    email: str
    active: bool = True
    roles: List[str] = []
    address: Optional[Address] = None
    metadata: Dict[str, str] = {}
    
    class Config:
        populate_by_name = True


class CreateUserRequest(BaseModel):
    """Request model for creating a user."""
    user: User
    
    class Config:
        populate_by_name = True


class CreateUserResponse(BaseModel):
    """Response model for user creation."""
    user: User
    status: str
    created_at: int  # Unix timestamp
    
    class Config:
        populate_by_name = True


class GetUserRequest(BaseModel):
    """Request model for getting a user."""
    id: int
    
    class Config:
        populate_by_name = True


class GetUserResponse(BaseModel):
    """Response model for user retrieval."""
    user: Optional[User] = None
    
    class Config:
        populate_by_name = True
