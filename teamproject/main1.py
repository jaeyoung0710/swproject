import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem, QWidget, QVBoxLayout, QSpinBox, QPushButton, QLabel, QGraphicsProxyWidget
)
from PyQt5.QtGui import QBrush, QColor, QPen, QFont
from PyQt5.QtCore import QRectF, Qt, QTimer
import random

class VehicleItem(QGraphicsRectItem):
    def __init__(self, direction, x, y, width=40, height=25):
        super().__init__(0, 0, width, height)
        self.setBrush(QBrush(QColor(30, 144, 255)))
        self.direction = direction
        self.setPos(x, y)
        self.speed = 3

    def move_forward(self):
        dx, dy = 0, 0
        if self.direction == 'north':
            dy = self.speed
        elif self.direction == 'south':
            dy = -self.speed
        elif self.direction == 'west':
            dx = self.speed
        elif self.direction == 'east':
            dx = -self.speed
        self.moveBy(dx, dy)

class OverheadIntersection(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("사거리 시뮬레이터")
        self.init_ui()

    def init_ui(self):
        self.showFullScreen()

        screen = QApplication.primaryScreen()
        screen_size = screen.size()

        self.scene_width = screen_size.width()
        self.scene_height = screen_size.height()
        self.vert_road_width = 400
        self.horiz_road_height = 300

        self.center_x = self.scene_width / 2
        self.center_y = self.scene_height / 2

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.view = QGraphicsView()
        layout.addWidget(self.view)

        self.scene = QGraphicsScene(0, 0, self.scene_width, self.scene_height)
        self.scene.setBackgroundBrush(QBrush(QColor("#B0D9A0")))
        self.view.setScene(self.scene)
        self.view.setSceneRect(0, 0, self.scene_width, self.scene_height)

        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setDragMode(QGraphicsView.NoDrag)
        self.view.setInteractive(True)

        self.draw_intersection()
        self.draw_lane_markings()
        self.draw_crosswalks()

        self.vehicles = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)

        self.create_controls()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def draw_intersection(self):
        csx, csy = self.center_x, self.center_y
        vrw = self.vert_road_width
        hrh = self.horiz_road_height

        vertical_road = QGraphicsRectItem(QRectF(csx - vrw / 2, 0, vrw, self.scene_height))
        vertical_road.setBrush(QBrush(QColor("dimgray")))
        self.scene.addItem(vertical_road)

        horizontal_road = QGraphicsRectItem(QRectF(0, csy - hrh / 2, self.scene_width, hrh))
        horizontal_road.setBrush(QBrush(QColor("dimgray")))
        self.scene.addItem(horizontal_road)

        center_box = QGraphicsRectItem(QRectF(csx - vrw / 2, csy - hrh / 2, vrw, hrh))
        center_box.setBrush(QBrush(QColor("dimgray")))
        self.scene.addItem(center_box)

    def draw_lane_markings(self):
        csx, csy = self.center_x, self.center_y
        vrw = self.vert_road_width
        hrh = self.horiz_road_height
        crosswalk_len = 75

        white_pen = QPen(QColor("white"))
        white_pen.setWidth(2)

        yellow_pen = QPen(QColor("yellow"))
        yellow_pen.setWidth(3)
        yellow_pen.setStyle(Qt.DashLine)

        self.scene.addLine(csx, 0, csx, csy - hrh / 2 - crosswalk_len, yellow_pen)
        self.scene.addLine(csx, csy + hrh / 2 + crosswalk_len, csx, self.scene_height, yellow_pen)

        for x in [csx - vrw / 4, csx + vrw / 4]:
            self.scene.addLine(x, 0, x, csy - hrh / 2 - crosswalk_len, white_pen)
            self.scene.addLine(x, csy + hrh / 2 + crosswalk_len, x, self.scene_height, white_pen)

        self.scene.addLine(0, csy, csx - vrw / 2 - crosswalk_len, csy, yellow_pen)
        self.scene.addLine(csx + vrw / 2 + crosswalk_len, csy, self.scene_width, csy, yellow_pen)

        for y in [csy - hrh / 4, csy + hrh / 4]:
            self.scene.addLine(0, y, csx - vrw / 2 - crosswalk_len, y, white_pen)
            self.scene.addLine(csx + vrw / 2 + crosswalk_len, y, self.scene_width, y, white_pen)

    def draw_crosswalks(self):
        csx, csy = self.center_x, self.center_y
        vrw = self.vert_road_width
        hrh = self.horiz_road_height
        stripe_width = 10
        stripe_len = 70
        gap = 12
        brush = QBrush(QColor("white"))

        x_start = csx - vrw / 2
        x_end = csx + vrw / 2
        y = csy - hrh / 2 - stripe_len - 5
        x = x_start
        while x + stripe_width <= x_end:
            self.scene.addRect(x, y, stripe_width, stripe_len, brush=brush)
            x += stripe_width + gap

        y = csy + hrh / 2 + 5
        x = x_start
        while x + stripe_width <= x_end:
            self.scene.addRect(x, y, stripe_width, stripe_len, brush=brush)
            x += stripe_width + gap

        y_start = csy - hrh / 2
        y_end = csy + hrh / 2
        x = csx - vrw / 2 - stripe_len - 5
        y = y_start
        while y + stripe_width <= y_end:
            self.scene.addRect(x, y, stripe_len, stripe_width, brush=brush)
            y += stripe_width + gap

        x = csx + vrw / 2 + 5
        y = y_start
        while y + stripe_width <= y_end:
            self.scene.addRect(x, y, stripe_len, stripe_width, brush=brush)
            y += stripe_width + gap

    def create_controls(self):
        self.north_input = QSpinBox()
        self.south_input = QSpinBox()
        self.east_input = QSpinBox()
        self.west_input = QSpinBox()
        for spin in [self.north_input, self.south_input, self.east_input, self.west_input]:
            spin.setRange(0, 50)
            spin.setStyleSheet("background-color: white; color: black;")

        label = QLabel("↑북↓남 →동←서")
        start_btn = QPushButton("시뮬레이션 시작")
        start_btn.setStyleSheet("background-color: lightgreen; font-weight: bold;")
        start_btn.clicked.connect(self.start_simulation)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(QLabel("북쪽 차량 수:"))
        layout.addWidget(self.north_input)
        layout.addWidget(QLabel("남쪽 차량 수:"))
        layout.addWidget(self.south_input)
        layout.addWidget(QLabel("동쪽 차량 수:"))
        layout.addWidget(self.east_input)
        layout.addWidget(QLabel("서쪽 차량 수:"))
        layout.addWidget(self.west_input)
        layout.addWidget(start_btn)

        container = QWidget()
        container.setLayout(layout)
        container.setStyleSheet("background-color: rgba(255, 255, 255, 200); border-radius: 10px;")
        proxy = QGraphicsProxyWidget()
        proxy.setWidget(container)
        proxy.setPos(self.scene_width - 220, 50)
        self.scene.addItem(proxy)

    def start_simulation(self):
        counts = {
            'north': self.north_input.value(),
            'south': self.south_input.value(),
            'east': self.east_input.value(),
            'west': self.west_input.value(),
        }

        for car in self.vehicles:
            self.scene.removeItem(car)
        self.vehicles.clear()

        self.create_vehicles(counts)
        self.timer.start(30)

    def create_vehicles(self, vehicle_counts):
        csx, csy = self.center_x, self.center_y
        margin = 30
        lane_spacing = 45
        for direction, count in vehicle_counts.items():
            lane_index = 0
            for i in range(count):
                lane_index = i % 2
                depth = i // 2 + random.randint(0, 2)

                if direction == 'north':
                    offset = -70 + lane_index * lane_spacing
                    x = csx + offset - 20
                    y = csy - self.horiz_road_height / 2 - margin - depth * 70
                elif direction == 'south':
                    offset = 25 + lane_index * lane_spacing
                    x = csx + offset - 20
                    y = csy + self.horiz_road_height / 2 + margin + depth * 70
                elif direction == 'west':
                    offset = 25 + lane_index * lane_spacing
                    x = csx - self.vert_road_width / 2 - margin - depth * 70
                    y = csy + offset - 20
                elif direction == 'east':
                    offset = -70 + lane_index * lane_spacing
                    x = csx + self.vert_road_width / 2 + margin + depth * 70
                    y = csy + offset - 20

                car = VehicleItem(direction, x, y)
                self.scene.addItem(car)
                self.vehicles.append(car)

    def update_simulation(self):
        for car in self.vehicles:
            car.move_forward()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OverheadIntersection()
    window.show()
    sys.exit(app.exec_())
