import threading
import time
import random
from datetime import datetime


class ParmSensor:


    def __init__(self, name):
        self.name = name
        self.temperature = 0
        self.illuminance = 0
        self.humidity = 0

    def set_data(self):
        self.temperature = random.randint(20, 30)
        self.illuminance = random.randint(5000, 10000)
        self.humidity = random.randint(40, 70)

    def get_data(self):
        return self.temperature, self.illuminance, self.humidity


def sensor_worker(sensor):
    while True:
        sensor.set_data()
        temp, light, humi = sensor.get_data()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{timestamp} {sensor.name} — temp {temp}, light {light}, humi {humi}')
        time.sleep(10)


def main():
    sensors = []

    for i in range(1, 6):
        name = f'Parm{i}'
        sensor = ParmSensor(name)
        sensors.append(sensor)

    for sensor in sensors:
        thread = threading.Thread(target=sensor_worker, args=(sensor,))
        thread.daemon = True  
        thread.start()

    try:
        while True:
            time.sleep(1)  
    except KeyboardInterrupt:
        print('프로그램을 종료합니다.')


if __name__ == '__main__':
    main()
