# Dubbo Python Serialization Demo

This project demonstrates the problem of manual serialization in `dubbo-python` and provides a solution using Pydantic integrated with Protobuf. The goal is to make serialization more Pythonic and easier to use.

## Project Structure

- `proto/`: Contains the Protocol Buffer definitions
- `current_approach/`: Demonstrates the current manual serialization approach
- `improved_approach/`: Shows the improved approach using Pydantic with Protobuf

## The Problem

In the current `dubbo-python` implementation, serialization and deserialization is manual and requires significant boilerplate code. For each request/response type, users must define:

1. How to convert Python classes to dictionaries/JSON
2. How to convert dictionaries/JSON back to Python classes
3. How to serialize/deserialize each request/response

This approach is:
- Tedious and error-prone
- Not aligned with Python's simplicity philosophy
- Requires duplicating serialization logic for each new method

## The Solution

The improved approach leverages Pydantic and integrates it with Protocol Buffers to:

1. Define data models once, using Pydantic's declarative style
2. Support multiple serialization formats (JSON and Protobuf)
3. Handle serialization and deserialization automatically 

### Key Components:

1. **Pydantic Models**: Define data structures with validation
2. **Protobuf Integration**: Convert between Pydantic models and Protobuf messages
3. **Format Selection**: Choose between JSON or Protobuf serialization

## Benefits

The improved approach offers:

- **Less Code**: No manual serialization logic required
- **Type Safety**: Leverages Pydantic's validation and type checking
- **Format Flexibility**: Easily switch between JSON and Protobuf
- **Consistency**: Standardized approach across all services
- **Better Developer Experience**: More Pythonic and easier to use

## Running the Demo

1. Install requirements:
   ```
   pip install -r requirements.txt
   ```

2. Generate Protobuf Python code (in a real implementation):
   ```
   protoc --python_out=. proto/user.proto
   ```

3. Run the current approach example:
   ```
   python -m current_approach.service
   ```

4. Run the improved approach example:
   ```
   python -m improved_approach.service
   ```

## Integration with dubbo-python

In a real implementation, this approach would be integrated with `dubbo-python` by:

1. Creating a `PydanticSerializer` class that implements the `Serializer` interface
2. Allowing users to specify serialization format in service configuration
3. Automatically handling serialization/deserialization in the RPC layer

Users would simply define their Pydantic models and the framework would handle the rest.