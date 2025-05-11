"""User service implementation using improved serialization."""
import time
from typing import Dict

from .models import User, Address, CreateUserRequest, CreateUserResponse, GetUserRequest, GetUserResponse
from .serializers import serialize_model, deserialize_model, SerializationFormat


class UserService:
    """User service with Pydantic and Protobuf serialization."""
    
    def __init__(self, serialization_format: SerializationFormat = SerializationFormat.PROTOBUF):
        """Initialize with an empty user database and serialization format."""
        self.users: Dict[int, User] = {}
        self.serialization_format = serialization_format
    
    # In a real Dubbo service, these methods would be exposed as RPC endpoints
    
    def create_user(self, request_bytes: bytes) -> bytes:
        """Create a user from serialized request."""
        # Deserialize request using Pydantic and Protobuf
        request = deserialize_model(
            request_bytes, 
            CreateUserRequest, 
            self.serialization_format
        )
        
        # Process request
        user = request.user
        self.users[user.id] = user
        
        # Create response
        response = CreateUserResponse(
            user=user,
            status="created",
            created_at=int(time.time())
        )
        
        # Serialize response using Pydantic and Protobuf
        return serialize_model(response, self.serialization_format)
    
    def get_user(self, request_bytes: bytes) -> bytes:
        """Get a user from serialized request."""
        # Deserialize request using Pydantic and Protobuf
        request = deserialize_model(
            request_bytes, 
            GetUserRequest, 
            self.serialization_format
        )
        
        # Process request
        user = self.users.get(request.id)
        
        # Create response
        response = GetUserResponse(user=user)
        
        # Serialize response using Pydantic and Protobuf
        return serialize_model(response, self.serialization_format)


# Example usage
if __name__ == "__main__":
    # Create service
    service = UserService(serialization_format=SerializationFormat.PROTOBUF)
    
    # Create test data using Pydantic models
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
    
    # Serialize request using Pydantic and Protobuf
    create_request_bytes = serialize_model(create_request, service.serialization_format)
    print(f"Serialized create request: {create_request_bytes}")
    
    # Send to service
    create_response_bytes = service.create_user(create_request_bytes)
    print(f"Got create response: {create_response_bytes}")
    
    # Deserialize response using Pydantic and Protobuf
    create_response = deserialize_model(
        create_response_bytes, 
        CreateUserResponse, 
        service.serialization_format
    )
    print(f"Created user with ID: {create_response.user.id}, status: {create_response.status}")
    
    # Get the user
    get_request = GetUserRequest(id=1)
    get_request_bytes = serialize_model(get_request, service.serialization_format)
    
    # Send to service
    get_response_bytes = service.get_user(get_request_bytes)
    
    # Deserialize response using Pydantic and Protobuf
    get_response = deserialize_model(
        get_response_bytes, 
        GetUserResponse, 
        service.serialization_format
    )
    print(f"Got user: {get_response.user.name}, email: {get_response.user.email}")


    # Try with JSON format
    print("\nTesting with JSON format:")
    json_service = UserService(serialization_format=SerializationFormat.JSON)
    
    # Serialize to JSON
    json_request_bytes = serialize_model(create_request, SerializationFormat.JSON)
    print(f"JSON request: {json_request_bytes.decode('utf-8')}")
    
    # Process with JSON
    json_response_bytes = json_service.create_user(json_request_bytes)
    json_response = deserialize_model(
        json_response_bytes, 
        CreateUserResponse, 
        SerializationFormat.JSON
    )
    print(f"JSON response user: {json_response.user.name}")
