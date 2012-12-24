#!/usr/bin/env python3
import math, sys
from PyQt4 import QtCore, QtGui

class MainWindow(QtGui.QFrame):
    def __init__(self):
        super(MainWindow, self).__init__()
        c = Canvas()
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(c)
        self.setLayout(layout)
        self.show()

class Canvas(QtGui.QWidget):
    def __init__(self):
        super(Canvas, self).__init__()
        self.init = True
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
        self.color = QtCore.Qt.green
        self.radius = 8
        self.brush = QtGui.QBrush(self.color, QtCore.Qt.SolidPattern)
        self.pen = QtGui.QPen(self.color)
        self.lastPoint = None
        self.drawQueue = []

    def mousePressEvent(self, event):
        self.lastPoint = None 
        self.drawQueue.append(event.pos())
        self.update()

    def mouseMoveEvent(self, event):
        self.drawQueue.append(event.pos())
        self.update()

    def paintEvent(self, event):
        if self.init:
            qp = QtGui.QPainter()
            qp.begin(self)
            qp.fillRect(self.contentsRect(), QtCore.Qt.white)
            qp.end()
            self.init = False
            return

        queue = self.drawQueue
        self.drawQueue = []
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        qp.setBrush(self.brush)
        qp.setPen(self.pen)
        for p in queue:
            if self.lastPoint:
                self.drawStroke(qp, self.lastPoint, p)
            qp.drawEllipse(p, self.radius, self.radius)
        if queue:
            self.lastPoint = queue[-1]
        qp.end()

    def drawStroke(self, qp, p1, p2):
        x1, y1 = p1.x(), p1.y()
        x2, y2 = p2.x(), p2.y()

        xn = x2-x1
        yn = y2-y1
        steps = math.hypot(xn, yn)/(self.radius/2)
        if steps == 0:
            return

        xstep = xn/steps
        ystep = yn/steps

        for n in range(int(steps)+1):
            qp.drawEllipse(QtCore.QPointF(x1+xstep*n, y1+ystep*n), self.radius, self.radius) 
        


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    a = MainWindow()
    sys.exit(app.exec_())
