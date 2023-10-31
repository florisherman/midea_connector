from typing import Any
from dataclasses import dataclass
@dataclass
class Settings:
    deviceToken: str
    deviceKey: str
    deviceId: float
    deviceIp: str

    @staticmethod
    def from_dict(obj: Any) -> 'Settings':
        _deviceToken = str(obj.get("deviceToken"))
        _deviceKey = str(obj.get("deviceKey"))
        _deviceId = float(obj.get("deviceId"))
        _deviceIp = str(obj.get("deviceIp"))
        return Settings(_deviceToken, _deviceKey, _deviceId, _deviceIp)
