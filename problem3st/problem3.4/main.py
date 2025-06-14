import threading
import time
import random
from datetime import datetime
import mysql.connector 


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


def insert_sensor_data(sensor_name, temperature, illuminance, humidity):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='yourpassword',
            database='smartfarm'
        )
        cursor = connection.cursor()

        query = (
            'INSERT INTO parm_data (sensor_name, input_time, temperature, illuminance, humidity) '
            'VALUES (%s, %s, %s, %s, %s)'
        )
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = (sensor_name, now, temperature, illuminance, humidity)
        cursor.execute(query, data)
        connection.commit()

        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f'MySQL 오류: {err}')


def sensor_worker(sensor):
    while True:
        sensor.set_data()
        temp, light, humi = sensor.get_data()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print(f'{now} {sensor.name} — temp {temp}, light {light}, humi {humi}')
        insert_sensor_data(sensor.name, temp, light, humi)

        time.sleep(10)


def main():
    sensors = [ParmSensor(f'Parm{i}') for i in range(1, 6)]

    for sensor in sensors:
        thread = threading.Thread(target=sensor_worker, args=(sensor,))
        thread.daemon = True
        thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('종료합니다.')


if __name__ == '__main__':
    main()
