class TrainTwin:
    def __init__(
        self,
        initial_position=0.0,
        initial_velocity=0.0,
        initial_acceleration=0.5,
        dt=5.0
    ):
        self.position = initial_position
        self.velocity = initial_velocity
        self.acceleration = initial_acceleration
        self.dt = dt

        self.timestamp = 0

        # twin belief state
        self.estimated_position = initial_position
        self.estimated_velocity = initial_velocity

        # dynamic uncertainty model
        self.uncertainty = 0.0
        self.confidence = 1.0

        # store history for dashboard and signal twin
        self.history = []

    def update(self, observed_position, acceleration):
        """
        Update train twin state every 5 seconds
        using observed position and acceleration
        """
        self.timestamp += self.dt
        self.acceleration = acceleration
        self.position = observed_position

        v_pred = self.estimated_velocity + acceleration * self.dt # v = u+at

        v_meas = (observed_position - self.estimated_position) / self.dt # v= dx/dt

        alpha = 0.8
        self.estimated_velocity = alpha * v_meas + (1 - alpha) * v_pred

        # predict position
        predicted_position = (
            self.estimated_position
            + self.estimated_velocity * self.dt
            + 0.5 * acceleration * self.dt ** 2
        )

        # update uncertainty dynamically
        estimation_error = abs(observed_position - predicted_position)

        self.uncertainty = 0.2 * self.uncertainty + 0.8 * estimation_error

        self.confidence = max(0.0, min(1.0, 1.0 - self.uncertainty / 10))
        
        beta = 0.8
        self.estimated_position = (
            beta * observed_position +
            (1 - beta) * self.estimated_position
        )

        snapshot = {
            "timestamp": self.timestamp,
            "observed_position": observed_position,
            "estimated_position": self.estimated_position,
            "estimated_velocity": abs(self.estimated_velocity),
            "acceleration": acceleration,
            "uncertainty": self.uncertainty,
            "confidence": self.confidence
        }

        self.history.append(snapshot)

        return snapshot

    def get_latest_state(self):
        return self.history[-1] if self.history else None

    def get_history(self):
        return self.history


class SignalTwin:
    def __init__(
        self,
        crossing_position,
        confidence_threshold=0.6
    ):
        self.crossing_position = crossing_position
        self.confidence_threshold = confidence_threshold

        self.state = "GREEN"

        # distance thresholds 
        self.warning_distance = 40
        self.danger_distance = 20

        self.history = []

    def update(self, train_state):
        """
        Update signal state using distance-based logic
        """

        position = train_state["estimated_position"]
        confidence = train_state["confidence"]
        timestamp = train_state["timestamp"]

        distance = self.crossing_position - position

        if distance >= self.warning_distance:
            self.state = "GREEN"

        elif 0 <= distance <= self.danger_distance:
            self.state = "RED"

        elif self.danger_distance < distance <= self.warning_distance:
            self.state = "YELLOW"
        
        elif distance < -2:
            self.state = "GREEN"

        else:
            self.state = "RED"

        snapshot = {
            "timestamp": timestamp,
            "signal_state": self.state,
            "distance_to_crossing": round(distance,2),
            "confidence": confidence
        }

        self.history.append(snapshot)
        return snapshot

    def get_latest_state(self):
        return self.history[-1] if self.history else None

    def get_history(self):
        return self.history