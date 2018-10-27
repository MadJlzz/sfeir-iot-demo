import datetime
import ssl

import jwt
import paho.mqtt.client as mqtt


def create_jwt(project_id, private_key_file, algorithm):
    """Creates a JWT (https://jwt.io) to establish an MQTT connection.
        Args:
         project_id: The cloud project ID this device belongs to
         private_key_file: A path to a file containing either an RSA256 or
                 ES256 private key.
         algorithm: The encryption algorithm to use. Either 'RS256' or 'ES256'
        Returns:
            An MQTT generated from the given project_id and private key, which
            expires in 20 minutes. After 20 minutes, your client will be
            disconnected, and a new JWT will have to be generated.
        Raises:
            ValueError: If the private_key_file does not contain a known key.
        """

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


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    """Callback for when a device connects."""
    print("on_connect: " + mqtt.connack_string(rc))


iot_projectId = "sfeir-iot-demo"
iot_cloudRegion = "europe-west1"
iot_registryId = "sfeir-iot-registry"
iot_deviceId = "pi-madpi"

public_certificate_path = "/home/pi/Documents/repositories/sfeir-iot-demo/certs/rsa_cert.pem"
private_certificate_path = "/home/pi/Documents/repositories/sfeir-iot-demo/certs/rsa_private.pem"

client = mqtt.Client("projects/{}/locations/{}/registries/{}/devices/{}".format(iot_projectId, iot_cloudRegion,
                                                                                iot_registryId, iot_deviceId))

client.username_pw_set(
    username='unused',
    password=create_jwt(iot_projectId, private_certificate_path, "RS256")
)

client.tls_set(None, public_certificate_path, private_certificate_path, ssl.CERT_REQUIRED, ssl.PROTOCOL_TLS)

client.on_connect = on_connect

client.connect("mqtt.googleapis.com", 8883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
