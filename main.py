import asyncio
import logging
from msmart.device import AirConditioner as AC

logging.basicConfig(level=logging.DEBUG)

DEVICE_IP = "192.168.1.15"
DEVICE_KEY = "5ade700052574ba28187e247723907cd736407d682564514bf698485b880ecfc"
DEVICE_TOKEN = "7de5c29468883b2b7b7fb4889431a1914bdcbdb386e98861008d6efe484bcb8b0af3b78fa3a39b27ded0157ab23e1571f71573b39172f0fe8aad7d6137031eec"
DEVICE_ID = "151732604943721"

async def get_deviceAndAuth():
    device = AC(ip=DEVICE_IP, port=6444, device_id=int(DEVICE_ID))
    if DEVICE_TOKEN and DEVICE_KEY:
        await device.authenticate(DEVICE_TOKEN, DEVICE_KEY)
        return device

async def main():
    device = await get_deviceAndAuth()
    await device.get_capabilities()
    
    await device.refresh()

    print({
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
    })

    await asyncio.sleep(2)
    device.power_state = False
    device.eco_mode = False
    device.target_temperature = 24.0
    await device.apply()

asyncio.run(main())
