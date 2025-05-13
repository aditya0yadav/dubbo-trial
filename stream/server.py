# Server-side implementation for Client Stream
import dubbo
from dubbo.configs import ServiceConfig
from dubbo.proxy.handlers import RpcMethodHandler, RpcServiceHandler
from common import RequestMessage, ResponseMessage

def request_deserializer(data: bytes) -> RequestMessage:
    return RequestMessage.deserialize(data)

def response_serializer(result: str) -> bytes:
    return ResponseMessage(result=result).serialize()

class StreamingServicer:
    def process_names(self, request_iterator) -> str:
        """
        This method processes multiple requests (names) from the client
        and returns a single combined response.
        """
        combined_names = ""
        
        # Process each request in the stream
        for request in request_iterator:
            name = request.params.get("name", "")
            print(f"Received name: {name}")
            
            # Add to the combined result
            if combined_names:
                combined_names += ", "
            combined_names += name
        
        # Return a single response after processing all requests
        return f"Processed {len(combined_names.split(', '))} names: {combined_names}"

def build_service_handler():
    # Build a client stream method handler
    method_handler = RpcMethodHandler.client_stream(
        method=StreamingServicer().process_names,
        method_name="processNames",
        request_deserializer=request_deserializer,
        response_serializer=response_serializer
    )
    
    # Build a service handler
    service_handler = RpcServiceHandler(
        service_name="example.StreamingService",
        method_handlers=[method_handler],
    )
    return service_handler

if __name__ == "__main__":
    # Build service config
    service_handler = build_service_handler()
    service_config = ServiceConfig(
        service_handler=service_handler, 
        host="127.0.0.1", 
        port=50052
    )
    
    # Start the server
    server = dubbo.Server(service_config).start()
    print("Server running on 127.0.0.1:50051")
    print("Ready to receive client stream requests...")
    input("Press Enter to stop the server...\n")