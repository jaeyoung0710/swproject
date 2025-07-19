import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsRectItem
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


class RoadDrawer:
    def __init__(self, scene, scene_width, scene_height):
        self.scene = scene
        self.scene_width = scene_width
        self.scene_height = scene_height
        self.vert_road_width = 200
        self.horiz_road_height = 200
        self.center_box_size = 200
        self.center_x = scene_width / 2
        self.center_y = scene_height / 2

    def draw(self):
        csx, csy = self.center_x, self.center_y
        vrw, hrh, cb = self.vert_road_width, self.horiz_road_height, self.center_box_size

        # 도로 및 교차로 배경
        self.scene.addRect(QRectF(csx - vrw / 2, 0, vrw, self.scene_height), brush=QBrush(QColor("dimgray")))
        self.scene.addRect(QRectF(0, csy - hrh / 2, self.scene_width, hrh), brush=QBrush(QColor("dimgray")))
        self.scene.addRect(QRectF(csx - cb / 2, csy - cb / 2, cb, cb), brush=QBrush(QColor("dimgray")))

        white = QPen(QColor("white")); white.setWidth(2); white.setStyle(Qt.DashLine)
        yellow = QPen(QColor("yellow")); yellow.setWidth(3)
        stop_pen = QPen(QColor("black")); stop_pen.setWidth(5)

        # 중앙선 및 차선
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

        # 정지선
        self.scene.addLine(csx - vrw / 2, csy - cb / 2, csx + vrw / 2, csy - cb / 2, stop_pen)  # North
        self.scene.addLine(csx - vrw / 2, csy + cb / 2, csx + vrw / 2, csy + cb / 2, stop_pen)  # South
        self.scene.addLine(csx + cb / 2, csy - hrh / 2, csx + cb / 2, csy + hrh / 2, stop_pen)  # East
        self.scene.addLine(csx - cb / 2, csy - hrh / 2, csx - cb / 2, csy + hrh / 2, stop_pen)  # West


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("방향별 차량 정지선 배치")
        self.setGeometry(100, 100, 1000, 1000)

        self.scene = QGraphicsScene(0, 0, 1000, 1000)
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        self.drawer = RoadDrawer(self.scene, 1000, 1000)
        self.drawer.draw()

        self.vehicles = []

        # 차량 수 설정 (이 부분만 바꿔서 조정 가능!)
        vehicle_counts = {
            "north": 5,
            "south": 6,
            "east": 4,
            "west": 3
        }

        self.spawn_vehicles(vehicle_counts)

    def spawn_vehicles(self, vehicle_counts):
        car_width, car_height = 40, 25
        car_gap = 10
        cx, cy = 500, 500
        vrw, hrh = 200, 200

        def distribute(n):  # 두 차선에 균등 분배
            h = n // 2
            return [h + n % 2, h]

        lanes = {
            "north": [cx - vrw / 4 - 45, cx - vrw / 4 + 5],
            "south": [cx + vrw / 4 - 45, cx + vrw / 4 + 5],
            "east": [cy - hrh / 4 - 40, cy - hrh / 4 + 10],
            "west": [cy + hrh / 4 - 40, cy + hrh / 4 + 10]
        }

        for dir in ["north", "south"]:
            for i, x in enumerate(lanes[dir]):
                for j in range(distribute(vehicle_counts.get(dir, 0))[i]):
                    if dir == "north":
                        y = cy - 100 - (j + 1) * (car_height + car_gap)
                    else:
                        y = cy + 100 + j * (car_height + car_gap)
                    car = VehicleItem(dir, x, y)
                    self.scene.addItem(car)
                    self.vehicles.append(car)

        for dir in ["east", "west"]:
            for i, y in enumerate(lanes[dir]):
                for j in range(distribute(vehicle_counts.get(dir, 0))[i]):
                    if dir == "east":
                        x = cx + 100 + j * (car_width + car_gap)
                    else:
                        x = cx - 100 - (j + 1) * (car_width + car_gap)
                    car = VehicleItem(dir, x, y)
                    self.scene.addItem(car)
                    self.vehicles.append(car)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
