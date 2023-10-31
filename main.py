import asyncio
import logging
import json
import os
from msmart.device import AirConditioner as AC
from msmart.discover import Discover
from acSettings import Settings
from deviceInfo import DeviceInfo
import paho.mqtt.client as mqtt

from pathlib import Path
#creating a new directory called pythondirectory


LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG").upper()
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

# Read variables from environment variables
DEVICE_IP = os.environ.get("DEVICE_IP", "192.168.1.15")
CONFIG_PATH = os.environ.get("CONFIG_PATH", "data/device.json")

# MQTT broker settings (provide default values if environment variables are not set)
MQTT_BROKER = os.environ.get("MQTT_BROKER", "192.168.1.51")
MQTT_PORT = int(os.environ.get("MQTT_PORT", 1883))
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "aircons/office/info_dump")
MQTT_USERNAME = os.environ.get("MQTT_USERNAME", "user1")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD", "Password1")

# Constants for authentication time and sleep time (in seconds)
REAUTH_INTERVAL = 30 * 60  # Re-authenticate every 30 minutes
SLEEP_INTERVAL = 60  # Sleep for 60 seconds between data retrieval and publication

async def publish_to_mqtt(data):
    logging.debug("In publish_to_mqtt function.")
    try:
        client = mqtt.Client()
        client.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWORD)
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()

        # Convert DeviceInfo object to JSON string
        json_data = json.dumps(data.__dict__)

        # Publish JSON data to MQTT topic
        client.publish(MQTT_TOPIC, json_data)

        # Wait for a moment to ensure the message is sent before disconnecting
        await asyncio.sleep(1)

        # Disconnect from the MQTT broker
        client.loop_stop()
        client.disconnect()
        logging.info("Published data to MQTT topic successfully.")
    except Exception as e:
        logging.error(f"Error publishing data to MQTT topic: {str(e)}")


async def write_config(device):
    logging.debug("In write_config function.")
    settings = Settings(
        deviceId=device.id,
        deviceIp=device.ip,
        deviceToken=device.token,
        deviceKey=device.key
    )
    with open(CONFIG_PATH, "w") as f:
        json.dump(settings.__dict__, f)


async def read_config():
    logging.debug("In read_config function.")
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            json_data = json.load(f)
            logging.debug("Read tokens needed for auth from config path.")
        return Settings(**json_data)
    else:
        device = await get_device()
        logging.debug("Discovering tokens needed for auth from config path.")
        settings = Settings(
            deviceId=device.id,
            deviceIp=device.ip,
            deviceToken=device.token,
            deviceKey=device.key
        )
        await write_config(device)
        return settings


async def get_device():
    logging.debug("In get_device function.")
    device = await Discover.discover_single(DEVICE_IP)
    await write_config(device)
    return device


async def auth_device(ac_settings: Settings):
    logging.debug("In auth_device function.")
    device = AC(ip=ac_settings.deviceIp, port=6444, device_id=int(ac_settings.deviceId))
    await device.authenticate(ac_settings.deviceToken, ac_settings.deviceKey)
    return device

async def authenticate_device():
    logging.info("authenticate device.")
    ac_settings = await read_config()
    return await auth_device(ac_settings)

async def get_device_info(device):
    await device.get_capabilities()
    await device.refresh()
    return DeviceInfo(
        id=device.id,
        ip=device.ip,
        online=device.online,
        supported=device.supported,
        power_state=device.power_state,
        beep=device.beep,
        target_temperature=device.target_temperature,
        operational_mode=device.operational_mode,
        fan_speed=device.fan_speed,
        swing_mode=device.swing_mode,
        eco_mode=device.eco_mode,
        turbo_mode=device.turbo_mode,
        fahrenheit=device.fahrenheit,
        indoor_temperature=device.indoor_temperature,
        outdoor_temperature=device.outdoor_temperature
    )

async def main():
    Path('data').mkdir(parents=True, exist_ok=True)
    logging.debug("Starting application main.")
    device = await authenticate_device()
    next_reauth_time = asyncio.get_event_loop().time() + REAUTH_INTERVAL

    while True:
        logging.debug("In loop start.")
        # Retrieve DeviceInfo object in a loop
        logging.info("Connect to device to get info.")
        data = await get_device_info(device)

        logging.info("Publish_to_mqtt device info.")
        # Publish DeviceInfo object to MQTT topic
        await publish_to_mqtt(data)
        
        # Check if it's time to re-authenticate
        current_time = asyncio.get_event_loop().time()
        logging.debug(F"Check if it's time to re-authenticate = {current_time >= next_reauth_time}")
        if current_time >= next_reauth_time:
            device = await authenticate_device()
            next_reauth_time = current_time + REAUTH_INTERVAL

        # Wait for the specified sleep interval before retrieving and publishing data again
        await asyncio.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())

