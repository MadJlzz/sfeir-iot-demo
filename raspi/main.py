import datetime
import json
import ssl
import time

import jwt
import paho.mqtt.client as mqtt
from ledrgb import LedRGB
from sensor import DHT

components = {'dht11': DHT(), 'led_rgb': LedRGB(), 'is_client_down': True}


def main():
    project_id = "sfeir-iot-demo"
    cloud_region = "europe-west1"
    registry_id = "sfeir-iot-registry"
    device_id = "pi-madpi"
    private_key_file = "certs/rsa_private.pem"
    algorithm = "RS256"
    ca_certs = "certs/roots.pem"
    mqtt_bridge_hostname = "mqtt.googleapis.com"
    mqtt_bridge_port = 8883

    mqtt_topic = '/devices/{}/{}'.format("pi-madpi", "events")

    client = get_client(
        project_id, cloud_region, registry_id, device_id,
        private_key_file, algorithm, ca_certs,
        mqtt_bridge_hostname, mqtt_bridge_port)

    # Publish DHT11 temperature and humidity values.
    while True:

        client.loop()

        if components['is_client_down']:
            print('Client seems down, trying to reconnect.')
            client.reconnect()
            time.sleep(3)
        else:

            # Get temperature and humidity
            components['dht11'].read_dht11()

            payload = {"temperature": components['dht11'].temperature, "humidity": components['dht11'].humidity}
            print('Trying to publish the message {} to the GCP.'.format(payload))

            client.publish(mqtt_topic, json.dumps(payload), qos=1)

        # Send events every three second.
        time.sleep(3)


def create_jwt(project_id, private_key_file, algorithm):
    """Creates a JWT (https://jwt.io) to establish an MQTT connection."""

    token = {
        # The time that the token was issued at
        'iat': datetime.datetime.utcnow(),
        # The time the token expires.
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        # The audience field should always be set to the GCP project id.
        'aud': project_id
    }

    # Read the private key file.
    with open(private_key_file, 'r') as f:
        private_key = f.read()

    print('Creating JWT using {} from private key file {}'.format(
        algorithm, private_key_file))

    return jwt.encode(token, private_key, algorithm=algorithm)


def error_str(rc):
    return '{}: {}'.format(rc, mqtt.error_string(rc))


def on_connect(unused_client, user_data, unused_flags, rc):
    print('Trying to connect to the MQTT broker: ', mqtt.connack_string(rc))
    if rc == mqtt.CONNACK_ACCEPTED:
        components['is_client_down'] = False
        components['led_rgb'].set_color(100, 0, 100)


def on_disconnect(unused_client, user_data, rc):
    print('Disconnection from the MQTT broker. Reason: ', error_str(rc))
    if rc != mqtt.MQTT_ERR_SUCCESS:
        components['is_client_down'] = True
        components['led_rgb'].set_color(0, 100, 100)


def on_publish(unused_client, user_data, unused_mid):
    print('A new message has been successfully published !')
    components['led_rgb'].set_color(100, 100, 0)


def get_client(
        project_id, cloud_region, registry_id, device_id, private_key_file,
        algorithm, ca_certs, mqtt_bridge_hostname, mqtt_bridge_port):
    client = mqtt.Client(
        client_id=('projects/{}/locations/{}/registries/{}/devices/{}'
                   .format(project_id, cloud_region, registry_id, device_id)))

    # With Google Cloud IoT Core, the username field is ignored, and the
    # password field is used to transmit a JWT to authorize the device.
    client.username_pw_set(
        username='unused',
        password=create_jwt(
            project_id, private_key_file, algorithm))

    # Enable SSL/TLS support.
    client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    # Connect to the Google MQTT bridge.
    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

    return client


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        components['led_rgb'].reset_gpio()
