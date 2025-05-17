import random

class DummySensor:
    def __init__(self):
          self.env_values = {
            "mars_base_internal_temperature": None,
            "mars_base_external_temperature": None,
            "mars_base_internal_humidity": None,
            "mars_base_external_illuminance": None,
            "mars_base_internal_co2": None,
            "mars_base_internal_oxygen": None
        }

    def set_env(self):
        """Set random values to each environmental variable within defined ranges."""
        self.env_values["mars_base_internal_temperature"] = random.uniform(18, 30)
        self.env_values["mars_base_external_temperature"] = random.uniform(0, 21)
        self.env_values["mars_base_internal_humidity"] = random.uniform(50, 60)
        self.env_values["mars_base_external_illuminance"] = random.uniform(500, 715)
        self.env_values["mars_base_internal_co2"] = random.uniform(0.02, 0.1)
        self.env_values["mars_base_internal_oxygen"] = random.uniform(4.0, 7.0)

    def get_env(self):
        """Return the current environment values."""
        return self.env_values

ds = DummySensor()
ds.set_env()
env_data = ds.get_env()

for key, value in env_data.items():
    print(f"{key}: {value:.2f}")
