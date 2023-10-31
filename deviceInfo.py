from typing import Any
from dataclasses import dataclass
@dataclass
class DeviceInfo:
    id: float
    ip: str
    online: bool
    supported: bool
    power_state: bool
    beep: bool
    target_temperature: float
    operational_mode: int
    fan_speed: int
    swing_mode: int
    eco_mode: bool
    turbo_mode: bool
    fahrenheit: bool
    indoor_temperature: float
    outdoor_temperature: float

    @staticmethod
    def from_dict(obj: Any) -> 'DeviceInfo':
        _id = float(obj.get("id"))
        _ip = str(obj.get("ip"))
        _online = bool(obj.get("online"))
        _supported = bool(obj.get("supported"))
        _power_state = bool(obj.get("power_state"))
        _beep = bool(obj.get("beep"))
        _target_temperature = int(obj.get("target_temperature"))
        _operational_mode = int(obj.get("operational_mode"))
        _fan_speed = int(obj.get("fan_speed"))
        _swing_mode = int(obj.get("swing_mode"))
        _eco_mode = bool(obj.get("eco_mode"))
        _turbo_mode = bool(obj.get("turbo_mode"))
        _fahrenheit = bool(obj.get("fahrenheit"))
        _indoor_temperature = float(obj.get("indoor_temperature"))
        _outdoor_temperature = float(obj.get("outdoor_temperature"))
        return DeviceInfo(_id, _ip, _online, _supported, _power_state, _beep, _target_temperature, _operational_mode, _fan_speed, _swing_mode, _eco_mode, _turbo_mode, _fahrenheit, _indoor_temperature, _outdoor_temperature)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)