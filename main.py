import sys

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QRadioButton

from dijkstra import *
from mainWindow import *
from geopy.distance import distance


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.counter = 1

        # ================================================
        self.vertex_list = []
        self.adj_list = []
        with open("cities.txt", "r") as input_file:
            for line in input_file:
                line = line.replace("\n", "")
                info = line.split(";;")
                if len(info) == 4:
                    vertex = Vertex(int(info[0]) - 1, info[1], float(info[2]), float(info[3]))
                    self.vertex_list.append(vertex)
                    self.adj_list.append([])
                    self.createCity(vertex)

                elif len(info) == 2:
                    v1, v2 = int(info[0]) - 1, int(info[1]) - 1
                    y1 = self.vertex_list[v1].y_pos
                    y2 = self.vertex_list[v2].y_pos
                    x1 = self.vertex_list[v1].x_pos
                    x2 = self.vertex_list[v2].x_pos
                    dist = round(distance((y1, x1), (y2, x2)).km, 2)
                    self.adj_list[v1].append((v2, dist))
                    self.adj_list[v2].append((v1, dist))

        # ================================================
        self.ui.btn_city1.clicked.connect(lambda: self.btnstate(1))
        self.ui.btn_city2.clicked.connect(lambda: self.btnstate(2))
        self.ui.btn_route.clicked.connect(self.findPath)
        self.ui.btn_show_map.clicked.connect(self.showMap)
        self.ui.btn_close.clicked.connect(exit)
        self.show()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def createCity(self, vertex: Vertex):
        p = latlngToScreenXY(vertex.y_pos, vertex.x_pos)
        self.ui.cities.append(QRadioButton(self.ui.centralwidget))
        i = len(self.ui.cities) - 1
        self.ui.cities[-1].setStyleSheet("QRadioButton::indicator"
                                        "{"
                                        "width : 6px;"
                                        "height : 6px;"
                                        "}")

        self.ui.cities[i].setGeometry(QtCore.QRect(p['x'], p['y'], 8, 8))
        self.ui.cities[i].setObjectName(str(vertex.num))
        self.ui.cities[i].setText("")
        self.ui.city1.addItem(vertex.name)
        self.ui.city2.addItem(vertex.name)

    def btnstate(self, btn):
        for b in self.ui.cities:
            if b.isChecked():
                if btn == 1:
                    self.ui.city1.setCurrentIndex(int(b.objectName()))
                    break
                self.ui.city2.setCurrentIndex(int(b.objectName()))
                break

    def findPath(self):
        for b in self.ui.cities:
            b.setHidden(True)
        self.ui.label.lines.clear()
        paths, cost = dijkstra(self.adj_list, self.ui.city1.currentIndex(), self.ui.city2.currentIndex())
        self.ui.distance.setText(str(cost))
        self.ui.path.setText(" <<- ")
        target = self.ui.city2.currentIndex()
        prev_x, prev_y = self.ui.cities[target].x() + 5, self.ui.cities[target].y() + 5
        while target in paths:
            self.ui.path.setText(" > " + self.vertex_list[target].name + self.ui.path.text())
            target = paths[target]
            new_x, new_y = self.ui.cities[target].x() + 5, self.ui.cities[target].y() + 5
            self.ui.label.lines.append([prev_x, prev_y, new_x, new_y])
            prev_x, prev_y = new_x, new_y
        self.ui.path.setText(" ->> " + self.vertex_list[target].name + self.ui.path.text())
        self.ui.path.setWordWrap(True)
        self.ui.label.update()

    def showMap(self):
        for b in self.ui.cities:
            b.setHidden(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())