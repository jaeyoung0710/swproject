import random
import time
import json
import platform
import os
import threading
import multiprocessing

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
            try:
                self.sensor.set_env()
                self.env_values = self.sensor.get_env()
                json_data = json.dumps(self.env_values, indent=4)
                print("[Sensor Data]\n" + json_data)
                time.sleep(5)
            except Exception as e:
                print(f"[Sensor Error] {e}")

    def get_mission_computer_info(self):
        while True:
            try:
                info = {
                    "Operating System": platform.system(),
                    "OS Version": platform.version(),
                    "CPU Type": platform.processor(),
                    "CPU Cores": os.cpu_count(),
                    "Memory Size (bytes)": os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') if hasattr(os, 'sysconf') else "N/A"
                }
                print("[System Info]\n" + json.dumps(info, indent=4))
            except Exception as e:
                print(f"[Info Error] {e}")
            time.sleep(20)

    def get_mission_computer_load(self):
        while True:
            try:
                load = {
                    "CPU Load (1min avg)": os.getloadavg()[0] if hasattr(os, 'getloadavg') else "N/A",
                    "Memory Usage (bytes)": os.sysconf('SC_PAGE_SIZE') * (os.sysconf('SC_PHYS_PAGES') - os.sysconf('SC_AVPHYS_PAGES')) if hasattr(os, 'sysconf') else "N/A"
                }
                print("[System Load]\n" + json.dumps(load, indent=4))
            except Exception as e:
                print(f"[Load Error] {e}")
            time.sleep(20)


def run_instance(instance):
    threading.Thread(target=instance.get_sensor_data, daemon=True).start()
    threading.Thread(target=instance.get_mission_computer_info, daemon=True).start()
    threading.Thread(target=instance.get_mission_computer_load, daemon=True).start()

    while True:
        time.sleep(1)


if __name__ == "__main__":
    runComputer1 = MissionComputer()
    runComputer2 = MissionComputer()
    runComputer3 = MissionComputer()

    process1 = multiprocessing.Process(target=run_instance, args=(runComputer1,))
    process2 = multiprocessing.Process(target=run_instance, args=(runComputer2,))
    process3 = multiprocessing.Process(target=run_instance, args=(runComputer3,))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()
