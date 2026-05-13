from main import App
from .grpcclient import FurnaceGrpcClient

_client = None

def get_client():
    global _client
    return _client

def make_client(func):

    global _client

    if _client is None:
        _client = FurnaceGrpcClient(
            "192.168.168.103:5000",
            on_frame_received=lambda frame: func(frame)
        )
        _client.start()

    return _client