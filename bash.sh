#!/bin/bash

# Set up project folder structure for Dubbo Python Serialization Demo
set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Creating Dubbo Python Serialization Demo project...${NC}"

# Create the main project directory
mkdir -p dubbo-serialization-demo
cd dubbo-serialization-demo

# Create directories
echo -e "${GREEN}Creating directory structure...${NC}"
mkdir -p proto
mkdir -p current_approach
mkdir -p improved_approach

# Create empty __init__.py files
touch current_approach/__init__.py
touch improved_approach/__init__.py

# Create requirements.txt
echo -e "${GREEN}Creating requirements.txt...${NC}"
cat > requirements.txt << 'EOF'
pydantic>=2.0.0
protobuf>=4.0.0
betterproto>=2.0.0
EOF

# Create Proto file
echo -e "${GREEN}Creating proto/user.proto...${NC}"
cat > proto/user.proto << 'EOF'
syntax = "proto3";

package usermanagement;

message Address {
  string street = 1;
  string city = 2;
  string country = 3;
  string postal_code = 4;
}

message User {
  int32 id = 1;
  string name = 2;
  string email = 3;
  bool active = 4;
  repeated string roles = 5;
  Address address = 6;
  map<string, string> metadata = 7;
}

message CreateUserRequest {
  User user = 1;
}

message CreateUserResponse {
  User user = 1;
  string status = 2;
  int64 created_at = 3;
}

message GetUserRequest {
  int32 id = 1;
}

message GetUserResponse {
  User user = 1;
}

service UserService {
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
}
EOF

# Create current approach files
echo -e "${GREEN}Creating current approach files...${NC}"

# models.py
cat > current_approach/models.py << 'EOF'
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
EOF

# serializers.py
cat > current_approach/serializers.py << 'EOF'
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
EOF

# service.py
cat > current_approach/service.py << 'EOF'
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
    
    # In a real Dubbo service, these methods would be exposed as RPC endpoints
    # Here we're simulating the process with serialization/deserialization steps
    
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
EOF

# Create improved approach files
echo -e "${GREEN}Creating improved approach files...${NC}"

# models.py
cat > improved_approach/models.py << 'EOF'
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
EOF

# serializers.py
cat > improved_approach/serializers.py << 'EOF'
"""Improved serialization with Pydantic and Protobuf."""
import json
from enum import Enum
from typing import Type, TypeVar, Any, Dict, Union
from pydantic import BaseModel

# Import generated protobuf classes
# In a real implementation, these would be generated from the proto file
from google.protobuf import json_format
from betterproto import Casing

# For this demo, we'll directly import the protobuf models
# This would typically be generated using the protoc compiler
import sys
import os
sys.path.append(os.path.abspath('..'))
try:
    # This is a placeholder - in a real implementation, 
    # you would import the actual generated pb2 modules
    from proto import user_pb2 as pb
except ImportError:
    # Mock implementation for the demo
    class MockProto:
        """Mock protobuf implementation for demonstration."""
        
        @staticmethod
        def SerializeToString():
            return b"mock_serialized_protobuf"
        
        @classmethod
        def FromString(cls, data):
            return cls()
    
    class pb:
        """Mock protobuf module."""
        class Address(MockProto):
            pass
        
        class User(MockProto):
            pass
        
        class CreateUserRequest(MockProto):
            pass
        
        class CreateUserResponse(MockProto):
            pass
        
        class GetUserRequest(MockProto):
            pass
        
        class GetUserResponse(MockProto):
            pass


# Type for Pydantic models
T = TypeVar('T', bound=BaseModel)
P = TypeVar('P')  # Type for protobuf messages


class SerializationFormat(str, Enum):
    """Available serialization formats."""
    JSON = "json"
    PROTOBUF = "protobuf"


# Mapping between Pydantic models and Protobuf message types
PROTOBUF_MAPPING = {
    "Address": pb.Address,
    "User": pb.User,
    "CreateUserRequest": pb.CreateUserRequest,
    "CreateUserResponse": pb.CreateUserResponse,
    "GetUserRequest": pb.GetUserRequest,
    "GetUserResponse": pb.GetUserResponse,
}


class ProtobufSerializer:
    """Serializer that can convert between Pydantic models and Protobuf."""
    
    @staticmethod
    def get_protobuf_class(model_class: Type[BaseModel]) -> Type:
        """Get the corresponding Protobuf class for a Pydantic model."""
        model_name = model_class.__name__
        if model_name not in PROTOBUF_MAPPING:
            raise ValueError(f"No Protobuf mapping found for {model_name}")
        return PROTOBUF_MAPPING[model_name]
    
    @classmethod
    def model_to_protobuf(cls, model: BaseModel) -> Any:
        """Convert a Pydantic model to a Protobuf message."""
        # Get the corresponding Protobuf class
        proto_class = cls.get_protobuf_class(model.__class__)
        
        # Convert Pydantic model to dict
        model_dict = model.model_dump(by_alias=True)
        
        # For nested models, recursively convert them
        for field_name, field_value in model_dict.items():
            if isinstance(field_value, dict) and field_name in model.__annotations__:
                field_type = model.__annotations__[field_name]
                # Check if it's a Pydantic model (very simplified check)
                if hasattr(field_type, "__origin__") and field_type.__origin__ is not dict:
                    # Handle Optional types
                    if getattr(field_type, "__origin__", None) is Union:
                        for arg in field_type.__args__:
                            if arg is not type(None):  # noqa
                                field_type = arg
                                break
                    
                    if issubclass(field_type, BaseModel):
                        nested_model = getattr(model, field_name)
                        if nested_model is not None:
                            model_dict[field_name] = cls.model_to_dict_for_proto(nested_model)
        
        # Create Protobuf message from dict
        try:
            # Using json_format for the mock implementation
            # In a real implementation with generated protobuf classes,
            # you would use ParseDict directly
            proto_msg = proto_class()
            json_format.ParseDict(model_dict, proto_msg)
            return proto_msg
        except Exception as e:
            # Fallback for the mock implementation
            return proto_class()
    
    @classmethod
    def model_to_dict_for_proto(cls, model: BaseModel) -> Dict:
        """Convert a Pydantic model to a dict suitable for Protobuf."""
        return model.model_dump(by_alias=True)
    
    @classmethod
    def protobuf_to_model(cls, proto_msg: Any, model_class: Type[T]) -> T:
        """Convert a Protobuf message to a Pydantic model."""
        # Convert Protobuf message to dict
        try:
            # In a real implementation with generated protobuf classes,
            # you would use MessageToDict directly
            msg_dict = json_format.MessageToDict(
                proto_msg, 
                preserving_proto_field_name=True,
                including_default_value_fields=True
            )
        except Exception:
            # Fallback for the mock implementation
            msg_dict = {}
        
        # Create Pydantic model from dict
        return model_class.model_validate(msg_dict)
    
    @classmethod
    def serialize(cls, model: BaseModel, format: SerializationFormat = SerializationFormat.PROTOBUF) -> bytes:
        """Serialize a Pydantic model to bytes."""
        if format == SerializationFormat.JSON:
            return model.model_dump_json().encode("utf-8")
        else:  # PROTOBUF
            proto_msg = cls.model_to_protobuf(model)
            return proto_msg.SerializeToString()
    
    @classmethod
    def deserialize(cls, data: bytes, model_class: Type[T], 
                   format: SerializationFormat = SerializationFormat.PROTOBUF) -> T:
        """Deserialize bytes to a Pydantic model."""
        if format == SerializationFormat.JSON:
            return model_class.model_validate_json(data.decode("utf-8"))
        else:  # PROTOBUF
            proto_class = cls.get_protobuf_class(model_class)
            proto_msg = proto_class.FromString(data)
            return cls.protobuf_to_model(proto_msg, model_class)


# Convenience functions for specific models
def serialize_model(model: BaseModel, format: SerializationFormat = SerializationFormat.PROTOBUF) -> bytes:
    """Serialize any Pydantic model to bytes."""
    return ProtobufSerializer.serialize(model, format)


def deserialize_model(data: bytes, model_class: Type[T], 
                     format: SerializationFormat = SerializationFormat.PROTOBUF) -> T:
    """Deserialize bytes to any Pydantic model."""
    return ProtobufSerializer.deserialize(data, model_class, format)
EOF

# service.py
cat > improved_approach/service.py << 'EOF'
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
EOF

# Create README.md
