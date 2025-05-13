# Bidirectional Stream Example (Server Side)
import dubbo
from dubbo.configs import ServiceConfig
from dubbo.proxy.handlers import RpcMethodHandler, RpcServiceHandler
from common import RequestMessage, ResponseMessage

def request_deserializer(data: bytes) -> RequestMessage:
    return RequestMessage.deserialize(data)

def response_serializer(result: str) -> bytes:
    return ResponseMessage(result=result).serialize()

class ChatServicer:
    def chat(self, request_iterator):
        """
        Bidirectional chat implementation.
        For each message received, sends a response back.
        """
        # Process each incoming message and yield responses
        message_count = 0
        
        for request in request_iterator:
            message_count += 1
            message = request.params.get("message", "")
            print(f"Received message #{message_count}: {message}")
            
            # Generate a response based on the incoming message
            if "hello" in message.lower():
                yield "Hello! Welcome to our service!"
            elif "how are you" in message.lower():
                yield "I'm doing well, thank you for asking!"
            elif "services" in message.lower():
                yield "We provide various streaming examples for Dubbo Python."
            elif "thank you" in message.lower():
                yield "You're welcome! Anything else I can help with?"
            elif "goodbye" in message.lower():
                yield "Goodbye! Have a great day!"
            else:
                yield f"I received your message: '{message}'"
                
        # Send a final message after all client messages are processed
        yield f"Chat session complete. Processed {message_count} messages."

def build_service_handler():
    # Build a bidirectional stream method handler
    method_handler = RpcMethodHandler.bi_stream(
        method=ChatServicer().chat,
        method_name="chat",
        request_deserializer=request_deserializer,
        response_serializer=response_serializer
    )
    
    # Build a service handler
    service_handler = RpcServiceHandler(
        service_name="example.ChatService",
        method_handlers=[method_handler],
    )
    return service_handler

if __name__ == "__main__":
    # Build service config
    service_handler = build_service_handler()
    service_config = ServiceConfig(
        service_handler=service_handler, 
        host="127.0.0.1", 
        port=50053
    )
    
    # Start the server
    server = dubbo.Server(service_config).start()
    print("Chat server running on 127.0.0.1:50051")
    print("Ready for bidirectional communication...")
    input("Press Enter to stop the server...\n")