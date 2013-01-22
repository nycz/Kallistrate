#!/usr/bin/env python3

import math
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt


class Canvas(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent)

        self.setAttribute(Qt.WA_StaticContents)
        self.modified = False
        self.drawing = False
        self.radius = 30
        self.color = Qt.black
        self.image = QtGui.QImage(800,800, QtGui.QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.update()
        self.lastPoint = QtCore.QPoint()
        self.resize(self.image.size())

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.lastPoint = event.pos()
            self.drawLineTo(event.pos())
            self.drawing = True

    def mouseMoveEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton) and self.drawing:
            self.drawLineTo(event.pos())

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.drawing:
            self.drawing = False

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0,0, self.image)
        
    def drawLineTo(self, endPoint):
        painter = QtGui.QPainter(self.image)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QtGui.QBrush(self.color, Qt.SolidPattern))
        self.drawStroke(painter, self.lastPoint, endPoint)
        self.modified = True

        self.update()
        self.lastPoint = QtCore.QPoint(endPoint)

    def drawStroke(self, painter, firstPoint, endPoint):
        if firstPoint != endPoint:
            x1, y1 = firstPoint.x(), firstPoint.y()
            x2, y2 = endPoint.x(), endPoint.y()

            xn = x2-x1
            yn = y2-y1
            steps = math.hypot(xn, yn)/(self.radius/4)
            if steps == 0:
                return

            xstep = xn/steps
            ystep = yn/steps

            for n in range(int(steps)+1):
                painter.drawEllipse(QtCore.QPointF(x1+xstep*n, y1+ystep*n), 
                                    self.radius, self.radius) 
        painter.drawEllipse(endPoint, self.radius, self.radius)

    def resizeImage(self, image, newSize):
        if image.size() == newSize:
            return

        newImage = QtGui.QImage(newSize, QtGui.QImage.Format_RGB32)
        newImage.fill(QtGui.qRgb(255, 255, 255))
        painter = QtGui.QPainter(newImage)
        painter.drawImage(QtCore.QPoint(0, 0), image)
        self.image = newImage


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.drawingArea = Canvas()

        scrollarea = QtGui.QScrollArea()
        scrollarea.setWidget(self.drawingArea)

        toolbar = QtGui.QToolBar()

        # Brush size
        slider = QtGui.QSlider(Qt.Horizontal)
        slider.setMaximumWidth(200)
        slider.setRange(1,200)
        slider.setValue(self.drawingArea.radius)
        lbl = QtGui.QLabel(str(self.drawingArea.radius))
        def setBrushSize(v):
            lbl.setText(str(v))
            self.drawingArea.radius = v/2
        slider.valueChanged.connect(setBrushSize)

        # Brush color
        colorPicker = QtGui.QPushButton()


        toolbar.addWidget(slider)
        toolbar.addWidget(lbl)
        toolbar.addSeparator()
        toolbar.addWidget(colorPicker)

        self.addToolBar(toolbar)
        self.setCentralWidget(scrollarea)
        self.setWindowTitle('Kallistrate')


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
