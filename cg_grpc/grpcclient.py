from __future__ import annotations

import json
import queue
import threading
from enum import IntEnum
from typing import Any, Callable, Optional

import grpc

from .stream_pb2 import *
from .stream_pb2_grpc import *
from .event_pb2 import *
from .event_pb2_grpc import *


class EventType(IntEnum):
    NewFurnace = 0
    RemoveFurnace = 1
    ModifyFurnace = 2
    NewProfile = 3
    RemoveProfile = 4
    ModifyProfile = 5
    RequestProfiles = 6
    RequestFurnaces = 7
    SetFurnaceProfile = 8
    AckFurnaceAlarm = 9


class FurnaceGrpcClient:
    def __init__(
        self,
        address: str,
        on_frame_received: Callable[[Frame], None],
        channel_options: Optional[list[tuple[str, Any]]] = None,
    ) -> None:
        self._address = address
        self._on_frame_received = on_frame_received

        self._channel = grpc.insecure_channel(address, options=channel_options or [])
        self._stream_client = StreamServiceStub(self._channel)
        self._events_client = EventsStub(self._channel)

        self._stop_event = threading.Event()

        self._frame_call = None
        self._frame_receive_thread: Optional[threading.Thread] = None

        self._outgoing_frames: queue.Queue[Optional[Frame]] = queue.Queue()
        self._frame_write_lock = threading.Lock()

        self._started = False

    def start(self) -> None:
        if self._started:
            raise RuntimeError("Client already started.")

        self._started = True
        self._stop_event.clear()

        self._frame_call = self._stream_client.Stream(self._frame_request_iter())

        self._frame_receive_thread = threading.Thread(
            target=self._receive_frames_loop,
            name="grpc-frame-recv",
            daemon=True,
        )
        self._frame_receive_thread.start()

    def send_frame(
        self,
        frame: Frame,
        timeout: Optional[float] = None,
    ) -> None:
        if not self._started or self._frame_call is None:
            raise RuntimeError("Call start() first.")

        if self._stop_event.is_set():
            return

        with self._frame_write_lock:
            self._outgoing_frames.put(frame, timeout=timeout)

    def send_event(
        self,
        event_type: int | EventType,
        payload: Any = None,
        timeout: Optional[float] = None,
    ) -> EventResponse:
        ev = Event(
            type=int(event_type),
            index=0,
            payload=json.dumps(payload),
        )
        return self._events_client.SendEvent(ev, timeout=timeout)

    def stop(self) -> None:
        self._stop_event.set()

        try:
            self._outgoing_frames.put_nowait(None)
        except Exception:
            pass

        if self._frame_call is not None:
            try:
                self._frame_call.cancel()
            except Exception:
                pass

        if self._frame_receive_thread is not None:
            self._frame_receive_thread.join(timeout=2.0)

        self._started = False

    def close(self) -> None:
        self.stop()
        self._channel.close()

    def _frame_request_iter(self):
        while not self._stop_event.is_set():
            try:
                item = self._outgoing_frames.get(timeout=0.1)
            except queue.Empty:
                continue

            if item is None:
                break

            yield item

    def _receive_frames_loop(self) -> None:
        try:
            assert self._frame_call is not None
            for frame in self._frame_call:
                if self._stop_event.is_set():
                    break
                self._on_frame_received(frame)
        except grpc.RpcError as ex:
            if ex.code() != grpc.StatusCode.CANCELLED:
                raise