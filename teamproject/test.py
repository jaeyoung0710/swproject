import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSpinBox,
    QLabel, QPushButton
)
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QTimer


class RoadWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("교통 시뮬레이션 - 정지선 및 신호 제어 완성본")
        self.setGeometry(100, 100, 1600, 1200)

        # 도로 및 차량 설정
        self.road_length_m = 500
        self.pixels_per_meter = 1300 / 500
        self.road_pixel_length = int(self.road_length_m * self.pixels_per_meter)
        self.num_lanes = 4
        self.lane_height = 60
        self.road_pixel_height = self.num_lanes * self.lane_height
        self.window_width = 1600
        self.window_height = 1200
        self.road_start_x = (self.window_width - self.road_pixel_length) // 2
        self.road_start_y = (self.window_height - self.road_pixel_height) // 2 - 350
        self.stop_line_x = self.road_start_x + int(self.pixels_per_meter * 300)

        # 차량 속도 및 이동량
        self.car_width = 40
        self.car_height = 25
        self.car_gap = 20
        self.car_speed_kmph = 200
        self.update_interval_ms = 25
        self.meters_per_frame = (self.car_speed_kmph * 1000 / 3600) * (self.update_interval_ms / 1000)
        self.pixels_per_frame = self.meters_per_frame * self.pixels_per_meter

        # 기본값
        self.total_cars = 20
        self.green_duration = 1
        self.yellow_duration = 2
        self.red_duration = 3
        self.lane_vehicles = [[] for _ in range(self.num_lanes)]

        # 신호등 설정
        self.signal_states = ['green', 'yellow', 'red']
        self.current_signal_index = 0
        self.signal_frame_counter = 0
        self.frames_per_signal = self.get_frames_per_signal()

        # 타이머 (초기 비작동)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)

        self.init_vehicle_positions()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()

        control_layout = QHBoxLayout()
        control_layout.setSpacing(20)

        self.car_input = QSpinBox()
        self.car_input.setRange(1, 100)
        self.car_input.setValue(self.total_cars)
        control_layout.addWidget(QLabel("차량 수:"))
        control_layout.addWidget(self.car_input)

        self.green_input = QSpinBox()
        self.green_input.setRange(1, 10)
        self.green_input.setValue(self.green_duration)
        control_layout.addWidget(QLabel("녹색 (초):"))
        control_layout.addWidget(self.green_input)

        self.yellow_input = QSpinBox()
        self.yellow_input.setRange(1, 10)
        self.yellow_input.setValue(self.yellow_duration)
        control_layout.addWidget(QLabel("황색 (초):"))
        control_layout.addWidget(self.yellow_input)

        self.red_input = QSpinBox()
        self.red_input.setRange(1, 10)
        self.red_input.setValue(self.red_duration)
        control_layout.addWidget(QLabel("적색 (초):"))
        control_layout.addWidget(self.red_input)

        start_button = QPushButton("시뮬레이션 시작")
        start_button.clicked.connect(self.apply_user_settings)
        control_layout.addWidget(start_button)

        layout.addLayout(control_layout)
        self.setLayout(layout)

    def apply_user_settings(self):
        self.total_cars = self.car_input.value()
        self.green_duration = self.green_input.value()
        self.yellow_duration = self.yellow_input.value()
        self.red_duration = self.red_input.value()

        self.frames_per_signal = self.get_frames_per_signal()
        self.current_signal_index = 0
        self.signal_frame_counter = 0

        self.init_vehicle_positions()
        self.timer.start(self.update_interval_ms)

    def get_frames_per_signal(self):
        return {
            'green': int(self.green_duration * 1000 / self.update_interval_ms),
            'yellow': int(self.yellow_duration * 1000 / self.update_interval_ms),
            'red': int(self.red_duration * 1000 / self.update_interval_ms),
        }

    def init_vehicle_positions(self):
        self.lane_vehicles = [[] for _ in range(self.num_lanes)]
        for i in range(self.total_cars):
            lane = i % self.num_lanes
            pos_in_lane = len(self.lane_vehicles[lane])
            x = self.road_start_x + pos_in_lane * (self.car_width + self.car_gap)
            self.lane_vehicles[lane].append(x)

    def update_simulation(self):
        self.signal_frame_counter += 1
        state = self.signal_states[self.current_signal_index]
        if self.signal_frame_counter >= self.frames_per_signal[state]:
            self.current_signal_index = (self.current_signal_index + 1) % len(self.signal_states)
            self.signal_frame_counter = 0

        current_signal = self.signal_states[self.current_signal_index]
        min_gap = 10

        for lane in self.lane_vehicles:
            for i in range(len(lane)):
                x = lane[i]
                car_front = x + self.car_width
                next_front = car_front + self.pixels_per_frame

                # (1) 앞차가 있다면 간격 체크
                if i < len(lane) - 1:
                    front_car_x = lane[i + 1]
                    max_x = front_car_x - self.car_width - min_gap
                    if x >= max_x:
                        continue  # 간격 유지: 이동 불가
                    max_move = max_x - x
                else:
                    max_move = self.pixels_per_frame

                # (2) 정지선 판단 (빨간불일 때만)
                if current_signal == 'red':
                    if car_front < self.stop_line_x and next_front >= self.stop_line_x:
                        continue  # 정지선 넘지 않게 정지
                    if car_front < self.stop_line_x:
                        remaining = self.stop_line_x - car_front
                        allowed_move = min(self.pixels_per_frame, remaining, max_move)
                        lane[i] += allowed_move
                    else:
                        lane[i] += min(self.pixels_per_frame, max_move)
                else:
                    lane[i] += min(self.pixels_per_frame, max_move)

            # 도로 밖 차량 제거
            while lane and lane[0] > self.road_start_x + self.road_pixel_length:
                lane.pop(0)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        # 도로
        for lane in range(self.num_lanes):
            y = self.road_start_y + lane * self.lane_height
            painter.setBrush(Qt.lightGray)
            painter.drawRect(self.road_start_x, y, self.road_pixel_length, self.lane_height)

        # 정지선
        painter.setPen(Qt.black)
        painter.drawLine(self.stop_line_x, self.road_start_y,
                         self.stop_line_x, self.road_start_y + self.road_pixel_height)

        # 신호등
        signal = self.signal_states[self.current_signal_index]
        if signal == 'green':
            painter.setBrush(Qt.green)
        elif signal == 'yellow':
            painter.setBrush(QColor(255, 165, 0))
        else:
            painter.setBrush(Qt.red)
        painter.drawEllipse(self.stop_line_x - 15, self.road_start_y - 50, 30, 30)

        # 차량
        for lane_index, vehicles in enumerate(self.lane_vehicles):
            lane_y = self.road_start_y + lane_index * self.lane_height
            car_y = lane_y + (self.lane_height - self.car_height) // 2
            for x in vehicles:
                painter.setBrush(QColor(30, 144, 255))
                painter.drawRect(int(x), car_y, self.car_width, self.car_height)
                painter.setBrush(Qt.white)
                painter.drawRect(int(x) + 6, car_y + 4, self.car_width - 12, 8)
                painter.setBrush(Qt.black)
                painter.drawEllipse(int(x) + 5, car_y + self.car_height, 8, 8)
                painter.drawEllipse(int(x) + self.car_width - 13, car_y + self.car_height, 8, 8)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RoadWidget()
    window.show()
    sys.exit(app.exec_())