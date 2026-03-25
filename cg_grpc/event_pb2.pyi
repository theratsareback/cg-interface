from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Event(_message.Message):
    __slots__ = ("type", "index", "payload")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    type: int
    index: int
    payload: str
    def __init__(self, type: _Optional[int] = ..., index: _Optional[int] = ..., payload: _Optional[str] = ...) -> None: ...

class EventResponse(_message.Message):
    __slots__ = ("index", "payload")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    index: int
    payload: str
    def __init__(self, index: _Optional[int] = ..., payload: _Optional[str] = ...) -> None: ...
