import asyncio
import logging
from msmart.device import AirConditioner as AC
from msmart.discover import Discover
import json
import os

from acSettings import Settings
from deviceInfo import DeviceInfo

logging.basicConfig(level=logging.DEBUG)

DEVICE_IP = "192.168.1.4"
PATH = "device.json"

def writeConfig(device):
    f = open(PATH, "w")
    settings = Settings(
        deviceId=device.id,
        deviceIp=device.ip,
        deviceToken=device.token,
        deviceKey=device.key
    )
    f.write(json.dumps(settings.__dict__))
    f.close()

async def readConfig():
    if os.path.exists(PATH):
        print('the file exists')
        f = open(PATH, "r")
        jsonstring = json.load(f)
        f.close()
        return Settings.from_dict(jsonstring)
    else:
        device = await getDevice()
        settings = Settings(
            deviceId=device.id,
            deviceIp=device.ip,
            deviceToken=device.token,
            deviceKey=device.key
        )
        return settings

async def getDevice():
    device = await Discover.discover_single(DEVICE_IP)
    writeConfig(device)
    return device

async def authDevice(acSettings : Settings):
    device = AC(ip=acSettings.deviceIp, port=6444, device_id=int(acSettings.deviceId))
    await device.authenticate(acSettings.deviceToken, acSettings.deviceKey)
    return device

async def main():
    acSettings = await readConfig()
    
    device = await authDevice(acSettings)
    await device.get_capabilities()
    
    await device.refresh()

    data =  DeviceInfo (
        id=device.id,
        ip=device.ip,
        online= device.online,
        supported= device.supported,
        power_state= device.power_state,
        beep= device.beep,
        target_temperature= device.target_temperature,
        operational_mode= device.operational_mode,
        fan_speed= device.fan_speed,
        swing_mode= device.swing_mode,
        eco_mode= device.eco_mode,
        turbo_mode= device.turbo_mode,
        fahrenheit= device.fahrenheit,
        indoor_temperature= device.indoor_temperature,
        outdoor_temperature= device.outdoor_temperature
    )
    
    f = open("acDump.json", "w")
    f.write(json.dumps(data.__dict__))
    f.close()

    await asyncio.sleep(2)
    device.power_state = True
    device.eco_mode = True
    device.beep = True
    device.target_temperature = 24.0
    device.fan_speed = 20
    await device.apply()

asyncio.run(main())
#asyncio.run(discoverDevice())



