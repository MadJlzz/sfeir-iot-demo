import paho.mqtt.client as mqtt
import ssl


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    """Callback for when a device connects."""
    print("on_connect" + mqtt.connack_string(rc))


iot_projectId = "sfeir-iot-demo"
iot_cloudRegion = "europe-west1"
iot_registryId = "sfeir-iot-registry"
iot_deviceId = "pi-madpi"

public_certificate_path = "/home/pi/Documents/repositories/sfeir-iot-demo/certs/rsa_cert.pem"
private_certificate_path = "/home/pi/Documents/repositories/sfeir-iot-demo/certs/rsa_private.pem"

client = mqtt.Client("projects/{}/locations/{}/registries/{}/devices/{}".format(iot_projectId, iot_cloudRegion,
                                                                                iot_registryId, iot_deviceId))
client.tls_set(None, public_certificate_path, private_certificate_path, ssl.CERT_REQUIRED, ssl.PROTOCOL_TLS)

client.on_connect = on_connect

client.connect("mqtt.googleapis.com", 8883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
