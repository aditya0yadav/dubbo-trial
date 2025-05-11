"""Models for the User Management Service."""
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Address:
    street: str
    city: str
    country: str
    postal_code: str


@dataclass
class User:
    id: int
    name: str
    email: str
    active: bool = True
    roles: List[str] = field(default_factory=list)
    address: Optional[Address] = None
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class CreateUserRequest:
    user: User


@dataclass
class CreateUserResponse:
    user: User
    status: str
    created_at: int  # Unix timestamp


@dataclass
class GetUserRequest:
    id: int


@dataclass
class GetUserResponse:
    user: Optional[User] = None
