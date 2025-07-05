import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem, QWidget, QVBoxLayout
)
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtCore import QRectF, Qt

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
        self.vert_road_width = 400     # 수직 도로 (상하) 폭
        self.horiz_road_height = 300   # 수평 도로 (좌우) 높이

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

        # 🔒 화면 고정 설정
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setDragMode(QGraphicsView.NoDrag)
        self.view.setInteractive(False)

        self.draw_intersection()
        self.draw_lane_markings()
        self.draw_crosswalks()

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

        # 북쪽
        x_start = csx - vrw / 2
        x_end = csx + vrw / 2
        y = csy - hrh / 2 - stripe_len - 5
        x = x_start
        while x + stripe_width <= x_end:
            self.scene.addRect(x, y, stripe_width, stripe_len, brush=brush)
            x += stripe_width + gap

        # 남쪽
        y = csy + hrh / 2 + 5
        x = x_start
        while x + stripe_width <= x_end:
            self.scene.addRect(x, y, stripe_width, stripe_len, brush=brush)
            x += stripe_width + gap

        # 서쪽
        y_start = csy - hrh / 2
        y_end = csy + hrh / 2
        x = csx - vrw / 2 - stripe_len - 5
        y = y_start
        while y + stripe_width <= y_end:
            self.scene.addRect(x, y, stripe_len, stripe_width, brush=brush)
            y += stripe_width + gap

        # 동쪽
        x = csx + vrw / 2 + 5
        y = y_start
        while y + stripe_width <= y_end:
            self.scene.addRect(x, y, stripe_len, stripe_width, brush=brush)
            y += stripe_width + gap

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OverheadIntersection()
    sys.exit(app.exec_())
