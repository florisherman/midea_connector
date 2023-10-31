import asyncio
import logging
from msmart.device import AirConditioner as AC
from msmart.discover import Discover
import json

logging.basicConfig(level=logging.DEBUG)

DEVICE_IP = "*"
DEVICE_KEY = "*"
DEVICE_TOKEN = "*"
DEVICE_ID = 0

async def authDevice():
    device = AC(ip=DEVICE_IP, port=6444, device_id=int(DEVICE_ID))
    if DEVICE_TOKEN and DEVICE_KEY:
        await device.authenticate(DEVICE_TOKEN, DEVICE_KEY)
        return device

async def main():
    device = await authDevice()
    await device.get_capabilities()
    
    await device.refresh()

    print(
        json.dumps({
        'id': device.id,
        'ip': device.ip,
        "online": device.online,
        "supported": device.supported,
        'power_state': device.power_state,
        'beep': device.beep,
        'target_temperature': device.target_temperature,
        'operational_mode': device.operational_mode,
        'fan_speed': device.fan_speed,
        'swing_mode': device.swing_mode,
        'eco_mode': device.eco_mode,
        'turbo_mode': device.turbo_mode,
        'fahrenheit': device.fahrenheit,
        'indoor_temperature': device.indoor_temperature,
        'outdoor_temperature': device.outdoor_temperature
    }))

    await asyncio.sleep(2)
    device.power_state = True
    device.eco_mode = True
    device.beep = True
    device.target_temperature = 24.0
    device.fan_speed = 20
    #await device.apply()

asyncio.run(main())
#asyncio.run(discoverDevice())



