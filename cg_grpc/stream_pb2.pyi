from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Frame(_message.Message):
    __slots__ = ("seq", "payload")
    SEQ_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    seq: int
    payload: str
    def __init__(self, seq: _Optional[int] = ..., payload: _Optional[str] = ...) -> None: ...
