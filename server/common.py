# common.py - Remains the same
from dataclasses import dataclass
from typing import Any, Dict
import orjson

@dataclass
class RequestMessage:
    method: str
    params: Dict[str, Any]

    def serialize(self) -> bytes:
        return orjson.dumps({
            "method": self.method,
            "params": self.params
        })

    @staticmethod
    def deserialize(data: bytes) -> "RequestMessage":
        obj = orjson.loads(data)
        return RequestMessage(method=obj["method"], params=obj["params"])


@dataclass
class ResponseMessage:
    result: Any

    def serialize(self) -> bytes:
        return orjson.dumps({"result": self.result})

    @staticmethod
    def deserialize(data: bytes) -> "ResponseMessage":
        obj = orjson.loads(data)
        return ResponseMessage(result=obj["result"])