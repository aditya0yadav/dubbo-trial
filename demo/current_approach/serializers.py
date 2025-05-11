"""Manual serialization for the User Management Service."""
import json
from typing import Dict, Any

from .models import Address, User, CreateUserRequest, CreateUserResponse, GetUserRequest, GetUserResponse


# Manual serialization functions
def serialize_address(address: Address) -> Dict[str, Any]:
    """Manually serialize Address to dictionary."""
    if not address:
        return None
    return {
        "street": address.street,
        "city": address.city,
        "country": address.country,
        "postal_code": address.postal_code,
    }


def deserialize_address(data: Dict[str, Any]) -> Address:
    """Manually deserialize dictionary to Address."""
    if not data:
        return None
    return Address(
        street=data.get("street", ""),
        city=data.get("city", ""),
        country=data.get("country", ""),
        postal_code=data.get("postal_code", ""),
    )


def serialize_user(user: User) -> Dict[str, Any]:
    """Manually serialize User to dictionary."""
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "active": user.active,
        "roles": user.roles,
        "address": serialize_address(user.address),
        "metadata": user.metadata,
    }


def deserialize_user(data: Dict[str, Any]) -> User:
    """Manually deserialize dictionary to User."""
    return User(
        id=data.get("id", 0),
        name=data.get("name", ""),
        email=data.get("email", ""),
        active=data.get("active", True),
        roles=data.get("roles", []),
        address=deserialize_address(data.get("address")),
        metadata=data.get("metadata", {}),
    )


# Request/Response serialization functions
def serialize_create_user_request(request: CreateUserRequest) -> bytes:
    """Serialize CreateUserRequest to JSON bytes."""
    data = {
        "user": serialize_user(request.user),
    }
    return json.dumps(data).encode("utf-8")


def deserialize_create_user_request(data: bytes) -> CreateUserRequest:
    """Deserialize JSON bytes to CreateUserRequest."""
    parsed_data = json.loads(data.decode("utf-8"))
    return CreateUserRequest(
        user=deserialize_user(parsed_data.get("user", {})),
    )


def serialize_create_user_response(response: CreateUserResponse) -> bytes:
    """Serialize CreateUserResponse to JSON bytes."""
    data = {
        "user": serialize_user(response.user),
        "status": response.status,
        "created_at": response.created_at,
    }
    return json.dumps(data).encode("utf-8")


def deserialize_create_user_response(data: bytes) -> CreateUserResponse:
    """Deserialize JSON bytes to CreateUserResponse."""
    parsed_data = json.loads(data.decode("utf-8"))
    return CreateUserResponse(
        user=deserialize_user(parsed_data.get("user", {})),
        status=parsed_data.get("status", ""),
        created_at=parsed_data.get("created_at", 0),
    )


def serialize_get_user_request(request: GetUserRequest) -> bytes:
    """Serialize GetUserRequest to JSON bytes."""
    data = {
        "id": request.id,
    }
    return json.dumps(data).encode("utf-8")


def deserialize_get_user_request(data: bytes) -> GetUserRequest:
    """Deserialize JSON bytes to GetUserRequest."""
    parsed_data = json.loads(data.decode("utf-8"))
    return GetUserRequest(
        id=parsed_data.get("id", 0),
    )


def serialize_get_user_response(response: GetUserResponse) -> bytes:
    """Serialize GetUserResponse to JSON bytes."""
    data = {
        "user": serialize_user(response.user) if response.user else None,
    }
    return json.dumps(data).encode("utf-8")


def deserialize_get_user_response(data: bytes) -> GetUserResponse:
    """Deserialize JSON bytes to GetUserResponse."""
    parsed_data = json.loads(data.decode("utf-8"))
    user_data = parsed_data.get("user")
    return GetUserResponse(
        user=deserialize_user(user_data) if user_data else None,
    )
