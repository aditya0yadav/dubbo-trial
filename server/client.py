# Bidirectional Stream Example (Client Side)
import dubbo
from dubbo.configs import ReferenceConfig
from common import RequestMessage, ResponseMessage
import time

def request_serializer(name: str) -> bytes:
    message = RequestMessage(method="chat", params={"message": name})
    return message.serialize()

def response_deserializer(data: bytes) -> str:
    return ResponseMessage.deserialize(data).result

class ChatServiceStub:
    def __init__(self, client: dubbo.Client):
        # Set up bidirectional stream method
        self.bi_stream = client.bi_stream(
            method_name="chat",
            request_serializer=request_serializer,
            response_deserializer=response_deserializer
        )

    def start_chat(self):
        """Start a bidirectional chat with the server"""
        # Start the stream without initial data
        stream = self.bi_stream()
        
        # Create a separate thread to handle responses
        import threading
        
        def read_responses():
            """Read responses from the server"""
            while True:
                response = stream.read(timeout=1.0)
                if response is dubbo.classes.EOF:
                    print("Server ended the conversation")
                    break
                elif response is None:
                    # No response within timeout
                    continue
                else:
                    print(f"Server: {response}")
        
        # Start the response reader thread
        reader_thread = threading.Thread(target=read_responses)
        reader_thread.daemon = True
        reader_thread.start()
        
        try:
            # Send messages to the server
            messages = [
                "Hello, I'm the client!",
                "How are you doing today?",
                "What services do you provide?",
                "Thank you for your help",
                "Goodbye!"
            ]
            
            for message in messages:
                print(f"Client: {message}")
                stream.write(message)
                time.sleep(1)  # Wait between messages
            
            # Signal that we're done writing
            stream.done_writing()
            
            # Wait for the reader thread to complete
            reader_thread.join(timeout=5.0)
            
        except Exception as e:
            print(f"Error in chat: {e}")
            
        return "Chat session completed"

if __name__ == "__main__":
    # Create a client
    reference_config = ReferenceConfig.from_url(
        "tri://127.0.0.1:50051/example.ChatService"
    )
    dubbo_client = dubbo.Client(reference_config)
    stub = ChatServiceStub(dubbo_client)

    # Start a bidirectional chat
    print("Starting chat session...")
    result = stub.start_chat()
    print(result)