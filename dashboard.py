import json
import time
import streamlit as st
import plotly.graph_objects as go
import paho.mqtt.client as mqtt

st.set_page_config(page_title="Railway Digital Twin", layout="wide")
st.title("🚆 Railway Crossing Digital Twin Dashboard")


# persistent shared state
if "shared_data" not in st.session_state:
    st.session_state.shared_data = {
        "train": None,
        "signal": None
    }


# MQTT callback
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())

    if msg.topic == "rail/train/state":
        userdata["train"] = payload

    elif msg.topic == "rail/signal/state":
        userdata["signal"] = payload

# create client only once
if "mqtt_client" not in st.session_state:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.user_data_set(st.session_state.shared_data)
    client.on_message = on_message

    client.connect("localhost", 1883, 60)

    client.subscribe("rail/train/state")
    client.subscribe("rail/signal/state")

    client.loop_start()

    st.session_state.mqtt_client = client


# read latest states
train = st.session_state.shared_data["train"]
signal = st.session_state.shared_data["signal"]


# display dashboard
if train is not None:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Position (m)", round(train["estimated_position"], 2))
    col2.metric("Velocity (m/s)", round(train["estimated_velocity"], 2))
    col3.metric("Confidence", round(train["confidence"], 2))

    if signal:
        col4.metric("Signal", signal["signal_state"])
    else:
        col4.metric("Signal", "-")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[0, 80],
        y=[0, 0],
        mode="lines",
        name="Track"
    ))

    fig.add_trace(go.Scatter(
        x=[train["estimated_position"]],
        y=[0],
        mode="markers",
        marker=dict(size=20),
        name="Train"
    ))

    fig.add_trace(go.Scatter(
        x=[50],
        y=[0],
        mode="markers",
        marker=dict(size=20),
        name="Crossing"
    ))

    fig.update_layout(
        height=300,
        xaxis_title="Track Position (m)",
        yaxis=dict(showticklabels=False)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🚦 Signal Twin State")

    if signal:
        st.write(signal)

else:
    st.warning("Waiting for train data...")

# auto refresh
time.sleep(0.25)
st.rerun()