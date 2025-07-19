import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QLabel, QGraphicsRectItem
)
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtCore import QRectF, Qt


class VehicleItem(QGraphicsRectItem):
    def __init__(self, x, y, width=40, height=25, color=QColor(30, 144, 255)):
        super().__init__(0, 0, width, height)
        self.setBrush(QBrush(color))
        self.setPen(QPen(Qt.NoPen))
        self.setPos(x, y)


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
        cb_size = self.center_box_size
        self.scene.addRect(QRectF(csx - vrw / 2, 0, vrw, self.scene_height), brush=QBrush(QColor("dimgray")))
        self.scene.addRect(QRectF(0, csy - hrh / 2, self.scene_width, hrh), brush=QBrush(QColor("dimgray")))
        self.scene.addRect(QRectF(csx - cb_size / 2, csy - cb_size / 2, cb_size, cb_size), brush=QBrush(QColor("dimgray")))

    def draw_lane_markings(self):
        csx, csy = self.center_x, self.center_y
        vrw = self.vert_road_width
        hrh = self.horiz_road_height
        cb_size = self.center_box_size
        white_pen = QPen(QColor("white")); white_pen.setWidth(2); white_pen.setStyle(Qt.DashLine)
        yellow_pen = QPen(QColor("yellow")); yellow_pen.setWidth(3)
        stop_pen = QPen(QColor("white")); stop_pen.setWidth(4)
        border_pen = QPen(QColor("white")); border_pen.setWidth(2)

        self.scene.addLine(csx, 0, csx, csy - cb_size / 2, yellow_pen)
        self.scene.addLine(csx, csy + cb_size / 2, csx, self.scene_height, yellow_pen)
        for x in [csx - vrw / 4, csx + vrw / 4]:
            self.scene.addLine(x, 0, x, csy - cb_size / 2, white_pen)
            self.scene.addLine(x, csy + cb_size / 2, x, self.scene_height, white_pen)

        self.scene.addLine(0, csy, csx - cb_size / 2, csy, yellow_pen)
        self.scene.addLine(csx + cb_size / 2, csy, self.scene_width, csy, yellow_pen)
        for y in [csy - hrh / 4, csy + hrh / 4]:
            self.scene.addLine(0, y, csx - cb_size / 2, y, white_pen)
            self.scene.addLine(csx + cb_size / 2, y, self.scene_width, y, white_pen)

        self.scene.addLine(csx - vrw / 2, csy - cb_size / 2, csx + vrw / 2, csy - cb_size / 2, stop_pen)
        self.scene.addLine(csx - vrw / 2, csy + cb_size / 2, csx + vrw / 2, csy + cb_size / 2, stop_pen)
        self.scene.addLine(csx - cb_size / 2, csy - hrh / 2, csx - cb_size / 2, csy + hrh / 2, stop_pen)
        self.scene.addLine(csx + cb_size / 2, csy - hrh / 2, csx + cb_size / 2, csy + hrh / 2, stop_pen)

        self.scene.addRect(csx - vrw / 2, 0, vrw, self.scene_height, border_pen)
        self.scene.addRect(0, csy - hrh / 2, self.scene_width, hrh, border_pen)

    def add_road_labels(self, labels):
        label_positions = [
            (self.center_x - 50, 10),
            (self.scene_width - 110, self.center_y - 15),
            (self.center_x - 50, self.scene_height - 40),
            (10, self.center_y - 15),
        ]
        for i, (x, y) in enumerate(label_positions):
            road_label = QLabel(labels[i], self.parent)
            road_label.setGeometry(int(x), int(y), 100, 30)
            road_label.setAlignment(Qt.AlignCenter)
            road_label.setStyleSheet("font-weight: bold; font-size: 16px; background: rgba(255,255,255,180); border-radius: 8px;")
            road_label.show()


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
        self.road_drawer.add_road_labels(["Road #1", "Road #2", "Road #3", "Road #4"])

        vehicle_counts = {
            "north": 7,
            "south": 6,
            "east": 4,
            "west": 5
        }
        self.add_detected_vehicles(vehicle_counts)

    def add_detected_vehicles(self, vehicle_counts):
        car_width, car_height = 40, 25
        lane_spacing = 30
        car_spacing = 10
        center_x, center_y = 500, 500
        vrw, hrh = 200, 200

        def distribute(count):
            half = count // 2
            return [half + (count % 2), half]

        # 북쪽 ↓
        north_lanes = [center_x - vrw / 4 - lane_spacing, center_x - vrw / 4 + lane_spacing]
        for i, x in enumerate(north_lanes):
            for j in range(distribute(vehicle_counts.get("north", 0))[i]):
                y = 0 - j * (car_height + car_spacing)
                car = VehicleItem(x, y)
                car.setRotation(0)
                self.scene.addItem(car)

        # 남쪽 ↑
        south_lanes = [center_x + vrw / 4 - lane_spacing, center_x + vrw / 4 + lane_spacing]
        for i, x in enumerate(south_lanes):
            for j in range(distribute(vehicle_counts.get("south", 0))[i]):
                y = 1000 + j * (car_height + car_spacing)
                car = VehicleItem(x, y)
                car.setRotation(180)
                self.scene.addItem(car)

        # 동쪽 →
        east_lanes = [center_y + hrh / 4 - lane_spacing, center_y + hrh / 4 + lane_spacing]
        for i, y in enumerate(east_lanes):
            for j in range(distribute(vehicle_counts.get("east", 0))[i]):
                x = 0 - j * (car_width + car_spacing)
                car = VehicleItem(x, y)
                car.setRotation(0)
                self.scene.addItem(car)

        # 서쪽 ←
        west_lanes = [center_y - hrh / 4 - lane_spacing, center_y - hrh / 4 + lane_spacing]
        for i, y in enumerate(west_lanes):
            for j in range(distribute(vehicle_counts.get("west", 0))[i]):
                x = 1000 + j * (car_width + car_spacing)
                car = VehicleItem(x, y)
                car.setRotation(180)
                self.scene.addItem(car)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
