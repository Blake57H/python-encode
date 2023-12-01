from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout

class Overlay(QWidget):
    def __init__(self, parent, widget):
        QWidget.__init__(self, parent)
        palette = QtGui.QPalette(self.palette())
        palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor.fromRgb(0,0,0,0))
        self.setPalette(palette)

        self.widget = widget
        self.widget.setParent(self)


    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.fillRect(event.rect(), QtGui.QBrush(QtGui.QColor(0, 0, 0, 127)))
        painter.end()

    def resizeEvent(self, event):
        position_x = (self.frameGeometry().width()-self.widget.frameGeometry().width())/2
        position_y = (self.frameGeometry().height()-self.widget.frameGeometry().height())/2

        self.widget.move(position_x, position_y)
        event.accept()


class CtmWidget(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.button = QPushButton("Close Overlay")
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.button)

        self.button.clicked.connect(self.hideOverlay)

    def paintEvent(self, event):

        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(self.rect()), 10, 10)
        mask = QtGui.QRegion(path.toFillPolygon().toPolygon())
        pen = QtGui.QPen(QtCore.Qt.white, 1)
        painter.setPen(pen)
        painter.fillPath(path, QtCore.Qt.white)
        painter.drawPath(path)
        painter.end()

    def hideOverlay(self):
        self.parent().hide()