import json
import paho.mqtt.client as mqtt
from twins import SignalTwin

TRAIN_TOPIC = "rail/train/state"
SIGNAL_TOPIC = "rail/signal/state"

signal = SignalTwin(crossing_position=50)

client = mqtt.Client()

def on_message(client, userdata, msg):
    train_state = json.loads(msg.payload.decode())

    signal_state = signal.update(train_state)

    # publish signal state
    client.publish(SIGNAL_TOPIC, json.dumps(signal_state))

    print("\n🚦 SIGNAL UPDATE")
    print(signal_state)

def main():
    client.on_message = on_message

    client.connect("localhost", 1883, 60)

    client.subscribe(TRAIN_TOPIC)

    print("\n🚦 Signal Subscriber Running...\n")

    client.loop_forever()

if __name__ == "__main__":
    main()