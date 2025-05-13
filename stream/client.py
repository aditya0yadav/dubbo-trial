# Client-side implementation for Client Stream
import dubbo
from dubbo.configs import ReferenceConfig
from common import RequestMessage, ResponseMessage

def request_serializer(name: str) -> bytes:
    message = RequestMessage(method="processNames", params={"name": name})
    return message.serialize()

def response_deserializer(data: bytes) -> str:
    return ResponseMessage.deserialize(data).result

class StreamingServiceStub:
    def __init__(self, client: dubbo.Client):
        # Set up client stream method
        self.client_stream = client.client_stream(
            method_name="processNames",
            request_serializer=request_serializer,
            response_deserializer=response_deserializer
        )

    def process_names(self, names: list[str]) -> str:
        # Method 1: Using an iterator (generator) to send multiple requests
        def request_generator():
            for name in names:
                yield name
        
        # Call the remote method with the generator and get a read stream
        stream = self.client_stream(request_generator())
        
        # Read the single response
        result = stream.read()
        return result

if __name__ == "__main__":
    # Create a client
    reference_config = ReferenceConfig.from_url(
        "tri://127.0.0.1:50052/example.StreamingService"
    )
    dubbo_client = dubbo.Client(reference_config)
    stub = StreamingServiceStub(dubbo_client)

    # Send multiple names and get a single combined response
    names = ["Alice", "Bob", "Charlie", "David"]
    result = stub.process_names(names)
    print(f"Combined result: {result}")