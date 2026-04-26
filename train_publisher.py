import json
import time
import paho.mqtt.client as mqtt
from twins import TrainTwin
import pandas as pd

TOPIC = "rail/train/state"


FT_TO_M = 0.3048

def load_sensor_data(csv_path):
    df = pd.read_csv(csv_path)

    df["position_m"] = df["pos_ft"] * FT_TO_M * 1000
    df["acceleration_m"] = df["acceleration"] * FT_TO_M * 1000

    return df[["position_m", "acceleration_m"]]

def main():
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    train = TrainTwin()

    data = load_sensor_data("Data.csv")

    for _, row in data.iterrows():
        position = row["position_m"]
        accel = row["acceleration_m"]

        state = train.update(position, accel)

        client.publish(TOPIC, json.dumps(state))

        print("PUBLISHED:", state)

        time.sleep(0.25)

if __name__ == "__main__":
    main()