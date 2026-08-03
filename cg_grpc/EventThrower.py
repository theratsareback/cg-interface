from typing import Any, Optional
from .grpcclient import FurnaceGrpcClient, EventType


class FurnaceEventBus:
    """
    High-level wrapper around FurnaceGrpcClient.send_event()
    Matches the C# Handle(Event _event) switch cases.
    """

    def __init__(self, client: FurnaceGrpcClient):
        self.client = client

    # ---------------- core ----------------

    def throw(self, event_type: EventType, payload: Any = None) -> Any:
        return self.client.send_event(event_type, payload)

    # ---------------- furnace ops ----------------

    def new_furnace(self, init):
        return self.throw(EventType.NewFurnace, init)

    def remove_furnace(self, guid):
        return self.throw(EventType.RemoveFurnace, guid)

    def modify_furnace(self, guid, init):
        return self.throw(EventType.ModifyFurnace, {"Key" : guid, "Value": init})

    def set_furnace_profile(self, guid, profile):
        return self.throw(EventType.SetFurnaceProfile, {"Key" : guid, "Value": profile})

    def ack_furnace_alarm(self, guid):
        return self.throw(EventType.AckFurnaceAlarm, guid)

    # ---------------- profiles ----------------

    def new_profile(self, profile):
        return self.throw(EventType.NewProfile, profile)

    def remove_profile(self, profile):
        return self.throw(EventType.RemoveProfile, profile)

    def modify_profile(self, index: int, profile):
        # mirrors your C# ModifyProfile(index, profile)
        return self.client.send_event(
            EventType.ModifyProfile,
            profile,
        )

    def request_profiles(self):
        return self.throw(EventType.RequestProfiles)

    def request_furnaces(self):
        return self.throw(EventType.RequestFurnaces)

    def set_profile_status(self, guid, status):
        return self.throw(EventType.SetProfileStatus, {"Key" : guid, "Value": status})

    # ---------------- control ----------------

    def enable(self, guid):
        return self.throw(EventType.Enable, guid)

    def set_setpoint(self, guid, value: float):
        return self.throw(EventType.SetSetpoint, {"Key" : guid, "Value": value})

    def set_man_trim(self, guid, trim: float):
        return self.throw(EventType.SetManTrim, {"Key" : guid, "Value": trim})

    def set_gains(self, guid, kp, ki):
        return self.throw(EventType.SetGains, {"Key" : guid, "Value": {"X": kp, "Y": ki}})

    def seek_time(self, guid, ms: int):
        return self.throw(EventType.SeekTime, {"Key" : guid, "Value": ms})

    # ---------------- steppers ----------------

    def set_steppers(self, stepper_buf):
        return self.throw(EventType.SetSteppers, stepper_buf)

    # ---------------- control systems ----------------

    def start_diameter_control(self, guid):
        return self.throw(EventType.StartDiameterControl, guid)

    def reset_diameter_control(self, guid):
        return self.throw(EventType.ResetDiameterControl, guid)

    def set_target(self, guid, point):
        return self.throw(EventType.SetSpotTarget, {"Key" : guid, "Value": {"X": point[0], "Y": point[1]}})