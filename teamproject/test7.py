import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QLabel, QGraphicsRectItem
)
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtCore import QRectF, Qt, QTimer


class VehicleItem(QGraphicsRectItem):
    def __init__(self, direction, x, y, width=40, height=25, color=QColor(30, 144, 255)):
        super().__init__(0, 0, width, height)
        self.setBrush(QBrush(color))
        self.setPen(QPen(Qt.NoPen))
        self.setPos(x, y)
        self.direction = direction
        self.speed = 3

        if direction == 'north':
            self.setRotation(0)
        elif direction == 'south':
            self.setRotation(180)
        elif direction == 'west':
            self.setRotation(180)
        elif direction == 'east':
            self.setRotation(0)

    def move_forward(self, is_green):
        if not is_green:
            return
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


class RoadDrawer:
    def __init__(self, scene, scene_width, scene_height, parent=None):
        self.scene = scene
        self.scene_width = scene_width
        self.scene_height = scene_height
        self.parent = parent
        self.vert_road_width = 200
        self.horiz_road_height = 200
        self.center_box_size = 200
        self.center_x = self.scene_width / 2
        self.center_y = self.scene_height / 2

    def draw_intersection(self):
        csx, csy = self.center_x, self.center_y
        vrw, hrh, cb = self.vert_road_width, self.horiz_road_height, self.center_box_size
        self.scene.addRect(QRectF(csx - vrw / 2, 0, vrw, self.scene_height), brush=QBrush(QColor("dimgray")))
        self.scene.addRect(QRectF(0, csy - hrh / 2, self.scene_width, hrh), brush=QBrush(QColor("dimgray")))
        self.scene.addRect(QRectF(csx - cb / 2, csy - cb / 2, cb, cb), brush=QBrush(QColor("dimgray")))

    def draw_lane_markings(self):
        csx, csy = self.center_x, self.center_y
        vrw, hrh, cb = self.vert_road_width, self.horiz_road_height, self.center_box_size
        white = QPen(QColor("white")); white.setWidth(2); white.setStyle(Qt.DashLine)
        yellow = QPen(QColor("yellow")); yellow.setWidth(3)
        stop = QPen(QColor("white")); stop.setWidth(4)
        border = QPen(QColor("white")); border.setWidth(2)

        self.scene.addLine(csx, 0, csx, csy - cb / 2, yellow)
        self.scene.addLine(csx, csy + cb / 2, csx, self.scene_height, yellow)
        for x in [csx - vrw / 4, csx + vrw / 4]:
            self.scene.addLine(x, 0, x, csy - cb / 2, white)
            self.scene.addLine(x, csy + cb / 2, x, self.scene_height, white)

        self.scene.addLine(0, csy, csx - cb / 2, csy, yellow)
        self.scene.addLine(csx + cb / 2, csy, self.scene_width, csy, yellow)
        for y in [csy - hrh / 4, csy + hrh / 4]:
            self.scene.addLine(0, y, csx - cb / 2, y, white)
            self.scene.addLine(csx + cb / 2, y, self.scene_width, y, white)

        self.scene.addRect(csx - vrw / 2, 0, vrw, self.scene_height, border)
        self.scene.addRect(0, csy - hrh / 2, self.scene_width, hrh, border)

    def draw_stop_lines(self):
        csx, csy = self.center_x, self.center_y
        cb = self.center_box_size
        vrw, hrh = self.vert_road_width, self.horiz_road_height

        stop_pen = QPen(QColor("black"))
        stop_pen.setWidth(5)

        # North ↓ (Y 기준 가로선)
        self.scene.addLine(csx - vrw / 2, csy - cb / 2, csx + vrw / 2, csy - cb / 2, stop_pen)

        # South ↑
        self.scene.addLine(csx - vrw / 2, csy + cb / 2, csx + vrw / 2, csy + cb / 2, stop_pen)

        # East →
        self.scene.addLine(csx + cb / 2, csy - hrh / 2, csx + cb / 2, csy + hrh / 2, stop_pen)

        # West ←
        self.scene.addLine(csx - cb / 2, csy - hrh / 2, csx - cb / 2, csy + hrh / 2, stop_pen)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Intersection with Stop Lines")
        self.setGeometry(100, 100, 1000, 1000)

        self.scene = QGraphicsScene(0, 0, 1000, 1000)
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        self.road_drawer = RoadDrawer(self.scene, 1000, 1000, parent=self)
        self.road_drawer.draw_intersection()
        self.road_drawer.draw_lane_markings()
        self.road_drawer.draw_stop_lines()

        self.vehicles = []
        self.add_detected_vehicles({"north": 19, "south": 21, "east": 15, "west": 24})

        self.traffic_lights = {d: False for d in ["north", "south", "east", "west"]}
        self.green_durations = {
            "north": 4000,
            "south": 8000,
            "east": 7000,
            "west": 5000
        }
        self.red_durations = {
            "north": 3000,
            "south": 3000,
            "east": 3000,
            "west": 3000
        }

        self.signal_timers = {}
        for direction in self.traffic_lights:
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.timeout.connect(lambda d=direction: self.toggle_light(d))
            self.signal_timers[direction] = timer

        self.start_traffic_cycle()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(30)

    def start_traffic_cycle(self):
        for direction in self.traffic_lights:
            self.set_green(direction)

    def set_green(self, direction):
        self.traffic_lights[direction] = True
        self.signal_timers[direction].start(self.green_durations[direction])

    def toggle_light(self, direction):
        if self.traffic_lights[direction]:
            self.traffic_lights[direction] = False
            QTimer.singleShot(self.red_durations[direction], lambda: self.set_green(direction))

    def add_detected_vehicles(self, vehicle_counts):
        car_width, car_height = 40, 25
        spacing = 30
        car_gap = 10
        cx, cy = 500, 500
        vrw, hrh = 200, 200

        def distribute(n):
            h = n // 2
            return [h + n % 2, h]

        lanes = {
            "north": [cx - vrw / 4 - spacing - 14, cx - vrw / 4 + spacing - 25],
            "south": [cx + vrw / 4 - 4, cx + vrw / 4 + spacing + 16],
            "east": [cy - hrh / 4 - spacing - 10, cy - hrh / 4 + spacing - 14],
            "west": [cy + hrh / 4 - spacing + 20, cy + hrh / 4 + spacing + 5]
        }

        for dir in ["north", "south"]:
            for i, x in enumerate(lanes[dir]):
                for j in range(distribute(vehicle_counts.get(dir, 0))[i]):
                    y = 0 - j * (car_height + car_gap) if dir == "north" else 1000 + j * (car_height + car_gap)
                    car = VehicleItem(dir, x, y)
                    self.scene.addItem(car)
                    self.vehicles.append(car)

        for dir in ["east", "west"]:
            for i, y in enumerate(lanes[dir]):
                for j in range(distribute(vehicle_counts.get(dir, 0))[i]):
                    x = 1000 + j * (car_width + car_gap) if dir == "east" else 0 - j * (car_width + car_gap)
                    car = VehicleItem(dir, x, y)
                    self.scene.addItem(car)
                    self.vehicles.append(car)

    def update_simulation(self):
        for car in self.vehicles:
            car.move_forward(self.traffic_lights.get(car.direction, False))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
