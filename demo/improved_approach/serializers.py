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
