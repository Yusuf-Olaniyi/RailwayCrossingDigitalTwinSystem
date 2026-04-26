# RailwayCrossingDigitalTwinSystem

A **Digital Twin-based Railway Crossing Safety System** developed as a graduate-level Engineering AI project.  
The system models both the **train** and the **crossing signal** as interacting digital twins that communicate in real time using **MQTT** and **Mosquitto**.

The project is designed to improve railway crossing safety through **real-time train state estimation**, **uncertainty-aware decision-making**, and **live dashboard monitoring**.

---

## Project Overview

Railway crossing incidents remain a major public safety concern.  
This project proposes an intelligent digital twin framework that monitors train movement and automatically controls crossing signals based on train proximity and system confidence.

The framework consists of:

- **Train Twin** → estimates train position, velocity, and confidence
- **Signal Twin** → determines gate status based on train distance
- **MQTT Communication Layer** → enables distributed twin interaction
- **Live Dashboard** → provides real-time visualization using Streamlit

---

## System Architecture

The system contains three major components:

### 1. Train Publisher (`train_publisher.py`)
Reads train position and acceleration data from a CSV file and publishes the train state through MQTT.

Published topic:

```text
train/state
```

This includes:

- estimated position
- estimated velocity
- acceleration
- confidence level
- uncertainty

---

### 2. Signal Subscriber (`signal_subscriber.py`)
Subscribes to the train state topic and performs intelligent gate control decisions based on:

- distance to crossing
- estimated velocity
- confidence level
- clearance zone logic

Published topic:

```text
signal/state
```

Signal states include:

- `GREEN`
- `YELLOW`
- `RED`

---

### 3. Dashboard (`dashboard.py`)
A Streamlit-based real-time monitoring dashboard that subscribes to both MQTT topics and visualizes:

- train position
- distance to crossing
- signal state
- confidence level
- live system updates

---

## Technologies Used

- **Python**
- **MQTT**
- **Mosquitto**
- **Streamlit**
- **Pandas**

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/RailwayCrossingDigitalTwinSystem.git
cd RailwayCrossingDigitalTwinSystem
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the System

Run the following in separate terminals.

### Terminal 1 — Start Mosquitto Broker
```bash
mosquitto
```

### Terminal 2 — Start Signal Subscriber
```bash
python signal_subscriber.py
```

### Terminal 3 — Launch Dashboard
```bash
streamlit run dashboard.py
```

### Terminal 4 — Start Train Publisher
```bash
python train_publisher.py
```

---

## Project Features

- Real-time train state estimation
- Confidence-aware decision logic
- Intelligent gate control
- Distributed communication using MQTT
- Live browser-based dashboard
- Scalable digital twin architecture

---

## Future Work

Possible future extensions include:

- GPS-based localization
- real-time sensor streaming
- Kalman filter state estimation
- anomaly detection
- multi-train support
- edge-cloud deployment
- computer vision integration

---

## License

This project is licensed under the **MIT License**.

---


## Author

## License

This project is licensed under the **MIT License**.

---

## Contributors

This project was collaboratively developed as part of a **Digital Twins and AI for Predictive Analytics course project**.

- **Yusuf Olaniyi** – [@your-github-username](https://github.com/your-github-username)
- **Zainab Akintayo** – [@partner-github-username](https://github.com/partner-github-username)
