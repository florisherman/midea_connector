# Air Conditioner Control Application

This Python application allows you to control and monitor your air conditioner using MQTT protocol. It communicates with your air conditioner device and publishes its status information to an MQTT broker.

## Prerequisites
- Python 3.6 or higher
- Docker (optional, for containerized deployment)

## Installation

1. Clone the repository:

2. Install dependencies:

- pip install msmart-ng
- pip install paho-mqtt

## Configuration

### Environment Variables

- **DEVICE_IP**: IP address of your air conditioner device.
- **CONFIG_PATH**: Path to the configuration file (e.g., device.json).
- **DUMP_PATH**: Path to the output file for storing device information (e.g., acDump.json).
- **MQTT_BROKER**: MQTT broker address.
- **MQTT_PORT**: MQTT broker port (usually 1883).
- **MQTT_TOPIC**: MQTT topic to publish air conditioner information.
- **MQTT_USERNAME**: MQTT broker username.
- **MQTT_PASSWORD**: MQTT broker password.
- **LOG_LEVEL**: Logging level for the application (DEBUG, INFO, ERROR).

## Usage

1. Set the required environment variables.
2. Run the application using Python:


or using Docker Compose (if Dockerized):

The application will authenticate with the air conditioner device, retrieve its information, and publish it to the specified MQTT topic.

## Logging

The application provides logging for different levels of information (DEBUG, INFO, ERROR). You can adjust the log level by setting the **LOG_LEVEL** environment variable.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- This project uses the library of  https://github.com/mac-zhou/midea-msmart
- checkout the author for more of his work  https://github.com/mill1000/midea-msmart