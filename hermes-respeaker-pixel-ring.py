import json
import os
from gpiozero import LED
import usb
try:
    import pixel_ring
except usb.core.NoBackendError:
    pass
from pixel_ring.apa102_pixel_ring import PixelRing
import paho.mqtt.client as mqtt

TOPIC_WAKEUP = 'hermes/hotword/+/detected'
TOPIC_THINK  = 'hermes/asr/textCaptured'
TOPIC_SPEAK  = 'hermes/tts/say'
# TOPIC_FINISH = 'hermes/tts/sayFinished'
TOPIC_FINISH = 'hermes/dialogueManager/sessionEnded'

led_power = LED(5)
pattern = os.environ.get('PATTERN', 'google') # or 'echo'
pixel_ring = PixelRing(pattern)
site_id = os.environ.get('SITE_ID', 'default')
host = os.environ.get('HOST', 'localhost')
port = int(os.environ.get('PORT', '1883'))
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe([(TOPIC_WAKEUP, 0), (TOPIC_THINK, 0), (TOPIC_SPEAK, 0), (TOPIC_FINISH, 0)])
    pixel_ring.set_brightness(10)
    pixel_ring.off()
    led_power.on()

def on_message(client, userdata, msg):
    if json.loads(msg.payload.decode('utf-8'))['siteId'] == site_id:
        if msg.topic.startswith('hermes/hotword/'):
            pixel_ring.wakeup()
        elif msg.topic == TOPIC_THINK:
            pixel_ring.think()
        elif msg.topic == TOPIC_SPEAK:
            pixel_ring.speak()
        elif msg.topic == TOPIC_FINISH:
            pixel_ring.off()

client.on_connect = on_connect
client.on_message = on_message
client.connect(host, port)
try:
    client.loop_forever()
except KeyboardInterrupt:
    print('Stopping...')
    pixel_ring.off()
    led_power.off()
