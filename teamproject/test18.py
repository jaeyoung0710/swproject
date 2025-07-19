import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QLabel, QGraphicsRectItem
)
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtCore import QRectF, Qt


class VehicleItem(QGraphicsRectItem):
    def __init__(self, direction, x, y, width=40, height=25, color=QColor(30, 144, 255)):
        super().__init__(0, 0, width, height)
        self.setBrush(QBrush(color))
        self.setPen(QPen(Qt.NoPen))
        self.setPos(x, y)
        self.direction = direction

        if direction == 'north':
            self.setRotation(0)
        elif direction == 'south':
            self.setRotation(180)
        elif direction == 'west':
            self.setRotation(180)
        elif direction == 'east':
            self.setRotation(0)

    def move_forward(self):
        pass  # 움직이지 않음


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
        vrw = self.vert_road_width
        hrh = self.horiz_road_height
        cb = self.center_box_size

        self.scene.addRect(QRectF(csx - vrw / 2, 0, vrw, self.scene_height), QPen(Qt.NoPen), QBrush(QColor("dimgray")))
        self.scene.addRect(QRectF(0, csy - hrh / 2, self.scene_width, hrh), QPen(Qt.NoPen), QBrush(QColor("dimgray")))
        self.scene.addRect(QRectF(csx - cb / 2, csy - cb / 2, cb, cb), QPen(Qt.NoPen), QBrush(QColor("dimgray")))

    def draw_lane_markings(self):
        csx, csy = self.center_x, self.center_y
        vrw = self.vert_road_width
        hrh = self.horiz_road_height
        cb = self.center_box_size

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

        self.scene.addLine(csx - vrw / 2, csy - cb / 2, csx + vrw / 2, csy - cb / 2, stop)
        self.scene.addLine(csx - vrw / 2, csy + cb / 2, csx + vrw / 2, csy + cb / 2, stop)
        self.scene.addLine(csx - cb / 2, csy - hrh / 2, csx - cb / 2, csy + hrh / 2, stop)
        self.scene.addLine(csx + cb / 2, csy - hrh / 2, csx + cb / 2, csy + hrh / 2, stop)

        self.scene.addRect(csx - vrw / 2, 0, vrw, self.scene_height, border)
        self.scene.addRect(0, csy - hrh / 2, self.scene_width, hrh, border)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("4-Way Intersection GUI")
        self.setGeometry(100, 100, 1000, 1000)

        self.scene = QGraphicsScene(0, 0, 1000, 1000)
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        self.road_drawer = RoadDrawer(self.scene, 1000, 1000, parent=self)
        self.road_drawer.draw_intersection()
        self.road_drawer.draw_lane_markings()

        self.vehicles = []
        vehicle_counts = {
            "north": 6,
            "south": 5,
            "west": 4,
            "east": 3
        }
        self.add_detected_vehicles(vehicle_counts)

    def add_detected_vehicles(self, vehicle_counts):
        car_width, car_height = 40, 25
        lane_spacing = 30
        car_spacing = 10
        center_x, center_y = 500, 500
        vrw, hrh = 200, 200
        cb = 200  # center box size

        def distribute(count):
            half = count // 2
            return [half + (count % 2), half]

        # 북쪽 ↓
        north_lanes = [center_x - vrw / 4 - lane_spacing - 14, center_x - vrw / 4 + lane_spacing - 25]
        for i, x in enumerate(north_lanes):
            for j in range(distribute(vehicle_counts.get("north", 0))[i]):
                y = center_y - cb / 2 - (j + 1) * (car_height + car_spacing)
                car = VehicleItem("north", x, y)
                self.scene.addItem(car)
                self.vehicles.append(car)

        # 남쪽 ↑
        south_lanes = [center_x + vrw / 4 - 4, center_x + vrw / 4 + lane_spacing + 16]
        for i, x in enumerate(south_lanes):
            for j in range(distribute(vehicle_counts.get("south", 0))[i]):
                y = center_y + cb / 2 + (j + 1) * (car_height + car_spacing)
                car = VehicleItem("south", x, y)
                self.scene.addItem(car)
                self.vehicles.append(car)

        # 서쪽 ←
        west_lanes = [center_y - hrh / 4 + 40, center_y - hrh / 4 - 15]
        for i, y in enumerate(west_lanes):
            for j in range(distribute(vehicle_counts.get("west", 0))[i]):
                x = center_x + cb / 2 + (j + 1) * (car_width + car_spacing)
                car = VehicleItem("west", x, y)
                self.scene.addItem(car)
                self.vehicles.append(car)

        # 동쪽 →
        east_lanes = [center_y + hrh / 4 - lane_spacing - 10, center_y + hrh / 4 + lane_spacing - 14]
        for i, y in enumerate(east_lanes):
            for j in range(distribute(vehicle_counts.get("east", 0))[i]):
                x = center_x - cb / 2 - (j + 1) * (car_width + car_spacing)
                car = VehicleItem("east", x, y)
                self.scene.addItem(car)
                self.vehicles.append(car)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
