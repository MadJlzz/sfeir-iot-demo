import datetime
import ssl
import time

import json
import jwt
import paho.mqtt.client as mqtt

from sensor import DHT11


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


def on_connect(unused_client, unused_userdata, unused_flags, rc):
    print('Trying to connect to the MQTT broker: ', mqtt.connack_string(rc))


def on_disconnect(unused_client, unused_userdata, rc):
    print('Disconnection from the MQTT broker. Reason: ', error_str(rc))


def on_publish(unused_client, unused_userdata, unused_mid):
    print('Message has been successfully published !')


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


def main():
    dht11 = DHT11()

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
        # Process network events.
        client.loop()

        # Get temperature and humidity
        dht11.read_dht11()

        payload = {"temperature": dht11.temperature, "humidity": dht11.humidity}
        print('Publishing message {}'.format(payload))

        client.publish(mqtt_topic, json.dumps(payload), qos=1)

        # Send events every three second.
        time.sleep(3)


if __name__ == '__main__':
    main()
