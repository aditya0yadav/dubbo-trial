# server.py - Based on the Apache Dubbo Python documentation
import dubbo
from dubbo.configs import ServiceConfig
from dubbo.proxy.handlers import RpcMethodHandler, RpcServiceHandler
from common import RequestMessage, ResponseMessage

def request_deserializer(data: bytes) -> RequestMessage:
    return RequestMessage.deserialize(data)

def response_serializer(result: str) -> bytes:
    return ResponseMessage(result=result).serialize()

class GreeterServicer:
    def say_hello(self, request: RequestMessage) -> str:
        name = request.params.get("name", "Guest")
        return f"Hello, {name}!"

def build_service_handler():
    # Build a method handler
    method_handler = RpcMethodHandler.unary(
        method=GreeterServicer().say_hello, 
        method_name="sayHello",
        request_deserializer=request_deserializer,
        response_serializer=response_serializer
    )
    
    # Build a service handler
    service_handler = RpcServiceHandler(
        service_name="example.GreeterService",
        method_handlers=[method_handler],
    )
    return service_handler

if __name__ == "__main__":
    # Build service config
    service_handler = build_service_handler()
    service_config = ServiceConfig(
        service_handler=service_handler, 
        host="127.0.0.1", 
        port=50051
    )
    
    # Start the server
    server = dubbo.Server(service_config).start()
    print("Server running on 127.0.0.1:50051")
    input("Press Enter to stop the server...\n")