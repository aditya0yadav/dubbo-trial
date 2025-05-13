"""User service implementation using manual serialization."""
import time
from typing import Dict

from .models import User, Address, CreateUserRequest, CreateUserResponse, GetUserRequest, GetUserResponse
from .serializers import (
    serialize_create_user_request, deserialize_create_user_request,
    serialize_create_user_response, deserialize_create_user_response,
    serialize_get_user_request, deserialize_get_user_request,
    serialize_get_user_response, deserialize_get_user_response
)


class UserService:
    """User service with manual serialization."""
    
    def __init__(self):
        """Initialize with an empty user database."""
        self.users: Dict[int, User] = {}
    
    def create_user(self, request_bytes: bytes) -> bytes:
        """Create a user from serialized request."""
        # Deserialize request
        request = deserialize_create_user_request(request_bytes)
        
        # Process request
        user = request.user
        self.users[user.id] = user
        
        # Create response
        response = CreateUserResponse(
            user=user,
            status="created",
            created_at=int(time.time())
        )
        
        # Serialize response
        return serialize_create_user_response(response)
    
    def get_user(self, request_bytes: bytes) -> bytes:
        """Get a user from serialized request."""
        # Deserialize request
        request = deserialize_get_user_request(request_bytes)
        
        # Process request
        user = self.users.get(request.id)
        
        # Create response
        response = GetUserResponse(user=user)
        
        # Serialize response
        return serialize_get_user_response(response)


# Example usage
if __name__ == "__main__":
    # Create service
    service = UserService()
    
    # Create a user
    address = Address(
        street="123 Main St", 
        city="San Francisco", 
        country="USA", 
        postal_code="94105"
    )
    
    user = User(
        id=1, 
        name="John Doe", 
        email="john@example.com",
        active=True,
        roles=["admin", "user"],
        address=address,
        metadata={"department": "Engineering", "title": "Developer"}
    )
    
    create_request = CreateUserRequest(user=user)
    
    # Manually serialize the request
    create_request_bytes = serialize_create_user_request(create_request)
    print(f"Serialized create request: {create_request_bytes}")
    
    # Send to service
    create_response_bytes = service.create_user(create_request_bytes)
    print(f"Got create response: {create_response_bytes}")
    
    # Deserialize response
    create_response = deserialize_create_user_response(create_response_bytes)
    print(f"Created user with ID: {create_response.user.id}, status: {create_response.status}")
    
    # Get the user
    get_request = GetUserRequest(id=1)
    get_request_bytes = serialize_get_user_request(get_request)
    
    # Send to service
    get_response_bytes = service.get_user(get_request_bytes)
    
    # Deserialize response
    get_response = deserialize_get_user_response(get_response_bytes)
    print(f"Got user: {get_response.user.name}, email: {get_response.user.email}")
