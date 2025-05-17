import random
import time
import json
import platform
import os

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
        self.env_values["mars_base_internal_temperature"] = random.uniform(18, 30)
        self.env_values["mars_base_external_temperature"] = random.uniform(0, 21)
        self.env_values["mars_base_internal_humidity"] = random.uniform(50, 60)
        self.env_values["mars_base_external_illuminance"] = random.uniform(500, 715)
        self.env_values["mars_base_internal_co2"] = random.uniform(0.02, 0.1)
        self.env_values["mars_base_internal_oxygen"] = random.uniform(4.0, 7.0)

    def get_env(self):
        return self.env_values


class MissionComputer:
    def __init__(self):
        self.env_values = {
            "mars_base_internal_temperature": None,
            "mars_base_external_temperature": None,
            "mars_base_internal_humidity": None,
            "mars_base_external_illuminance": None,
            "mars_base_internal_co2": None,
            "mars_base_internal_oxygen": None
        }
        self.sensor = DummySensor()

    def get_sensor_data(self):
        while True:
            self.sensor.set_env()
            self.env_values = self.sensor.get_env()
            json_data = json.dumps(self.env_values, indent=4)
            print(json_data)
            time.sleep(5)

    def get_mission_computer_info(self):
        try:
            info = {
                "Operating System": platform.system(),
                "OS Version": platform.version(),
                "CPU Type": platform.processor(),
                "CPU Cores": os.cpu_count(),
                "Memory Size (bytes)": os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') if hasattr(os, 'sysconf') else "N/A"
            }
        except Exception as e:
            info = {"Error": str(e)}

        print(json.dumps(info, indent=4))

    def get_mission_computer_load(self):
        """Get system load (CPU and Memory usage) and display in JSON format."""
        try:
            load = {
                "CPU Load (1min avg)": os.getloadavg()[0] if hasattr(os, 'getloadavg') else "N/A",
                "Memory Usage (bytes)": os.sysconf('SC_PAGE_SIZE') * (os.sysconf('SC_PHYS_PAGES') - os.sysconf('SC_AVPHYS_PAGES')) if hasattr(os, 'sysconf') else "N/A"
            }
        except Exception as e:
            load = {"Error": str(e)}

        print(json.dumps(load, indent=4))

runComputer = MissionComputer()
runComputer.get_mission_computer_info()
runComputer.get_mission_computer_load()