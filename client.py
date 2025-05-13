# client.py - Based on the Apache Dubbo Python documentation
import dubbo
from dubbo.configs import ReferenceConfig
from common import RequestMessage, ResponseMessage
from typing import Callable


def request_serializer(name: str) -> bytes:
    message = RequestMessage(method="sayHello", params={"name": name})
    return message.serialize()

def response_deserializer(data: bytes) -> str:
    return ResponseMessage.deserialize(data).result

class GreeterServiceStub:
    def __init__(self, client: dubbo.Client):
        self.unary = client.unary(
            method_name="sayHello",
            request_serializer=request_serializer,
            response_deserializer=response_deserializer
        )
        
    def say_hello(self, name: str) -> str:
        return self.unary(name)

if __name__ == "__main__":
    # Create a client
    reference_config = ReferenceConfig.from_url(
        "tri://127.0.0.1:50051/example.GreeterService"
    )
    dubbo_client = dubbo.Client(reference_config)
    stub = GreeterServiceStub(dubbo_client)

    # Call the remote method
    try:
        result = stub.say_hello("PythonUser")
        print(f"Received reply: {result}")
    except Exception as e:
        print(f"Error calling RPC: {str(e)}")