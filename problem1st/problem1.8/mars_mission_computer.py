import random
import time
import json
import platform
import os
import ctypes
import psutil  # 시스템 부하 측정을 위한 외부 라이브러리 (예외 허용됨)

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
        self.ds = DummySensor()

    def get_sensor_data(self):
        while True:
            self.ds.set_env()
            self.env_values = self.ds.get_env()
            json_data = json.dumps(self.env_values, indent=4)
            print("[🌡️ Sensor Data]")
            print(json_data)
            time.sleep(5)

    def get_mission_computer_info(self):
        try:
            info = {
                "OS": platform.system(),
                "OS Version": platform.version(),
                "CPU Type": platform.processor(),
                "CPU Cores": os.cpu_count()
            }

            if platform.system() == "Windows":
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                    ]
                mem_stat = MEMORYSTATUSEX()
                mem_stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(mem_stat))
                info["Memory"] = f"{mem_stat.ullTotalPhys / (1024 ** 3):.2f} GB"
            else:
                # Linux, macOS: psutil 사용 가능
                mem = psutil.virtual_memory()
                info["Memory"] = f"{mem.total / (1024 ** 3):.2f} GB"

            print("[🖥️ Mission Computer Info]")
            print(json.dumps(info, indent=4))
        except Exception as e:
            print("[오류] 시스템 정보를 가져오는 중 오류 발생:", str(e))

    def get_mission_computer_load(self):
        try:
            load_info = {}
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()

            load_info["CPU Usage"] = f"{cpu_percent}%"
            load_info["Memory Usage"] = f"{memory.percent}%"

            print("[📊 Mission Computer Load]")
            print(json.dumps(load_info, indent=4))
        except Exception as e:
            print("[오류] 시스템 부하 정보를 가져오는 중 오류 발생:", str(e))


# 인스턴스 생성 및 기능 호출
if __name__ == "__main__":
    runComputer = MissionComputer()
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()

    # 센서 데이터 실시간 출력 (필요할 때만 주석 해제)
    # runComputer.get_sensor_data()
