#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


import math

from Qt.QtCore import (qAbs, QLineF, QPointF, QRect, QRectF, qrand, qsrand, Qt,
                          QTime, QTimer)
from Qt.QtGui import (QBrush, QColor, QPainter, QPainterPath, QPixmap,
                         QPolygonF, QPen, QFont)
from Qt.QtWidgets import (QApplication, QGraphicsItem, QGraphicsScene,
                             QGraphicsView, QGraphicsWidget, QStyle)

from Qt import __binding__

if __binding__ == "PySide2":
    import images_rc_pyside2
elif __binding__ == "PySide":
    import images_rc_pyside
elif __binding__ == "PyQt":
    import images_rc_pyqt
elif __binding__ == "PyQt5":
    import images_rc_pyqt5


class Chip(QGraphicsItem):
    # Create the bounding rectangle once.
    BoundingRect = QRectF(0, 0, 110, 70)

    def __init__(self, color, x=0, y=0):
        super(Chip, self).__init__()

        self.color = color
        self.x = x
        self.y = y
        self.stuff = []

        self.setZValue((x + y) % 2)
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)

    def boundingRect(self):
        return Chip.BoundingRect

    def shape(self):
        path = QPainterPath()
        path.addRect(14, 14, 82, 42)
        return path

    def paint(self, painter, option, widget):
        fillColor = self.color
        if option.state & QStyle.State_Selected:
            fillColor = self.color.darker(150)
        if option.state & QStyle.State_MouseOver:
            fillColor = fillColor.lighter(125)

        lod = option.levelOfDetailFromTransform(painter.worldTransform())
        if lod < 0.2:
            if lod < 0.125:
                painter.fillRect(QRectF(0, 0, 110, 70), fillColor)
                return
            b = painter.brush()
            painter.setBrush(fillColor)
            painter.drawRect(13, 13, 97, 57)
            painter.setBrush(b)
            return

        oldPen = painter.pen()
        pen = oldPen
        width = 0
        if option.state & QStyle.State_Selected:
            width += 2

        pen.setWidth(width)
        b = painter.brush()
        painter.setBrush(QBrush(fillColor.darker(120 if (option.state & QStyle.State_Sunken) else 100)))

        painter.drawRect(QRect(14, 14, 79, 39))
        painter.setBrush(b)

        if lod >= 1:
            painter.setPen(QPen(Qt.gray, 1))
            painter.drawLine(15, 54, 94, 54)
            painter.drawLine(94, 53, 94, 15)
            painter.setPen(QPen(Qt.black, 0))

        # Draw text
        if lod >= 2:
            font = QFont("Times", 10)
            font.setStyleStrategy(QFont.ForceOutline)
            painter.setFont(font)
            painter.save()
            painter.scale(0.1, 0.1)
            painter.drawText(170, 180, "Model: VSC-2000 (Very Small Chip) at {}x{}".format(self.x, self.y))
            painter.drawText(170, 200, "Serial number: DLWR-WEER-123L-ZZ33-SDSJ")
            painter.drawText(170, 220, "Manufacturer: Chip Manufacturer")
            painter.restore()

        # Draw lines
        lines = []  # QVarLengthArray < QLineF, 36 >
        if lod >= 0.5:
            for i in range(0, 11, 1 if lod > 0.5 else 2):  # (int i = 0 i <= 10 i += (1 if lod > 0.5 else 2)):
                lines.append(QLineF(18 + 7 * i, 13, 18 + 7 * i, 5))
                lines.append(QLineF(18 + 7 * i, 54, 18 + 7 * i, 62))

            for i in range(0, 6, 1 if lod > 0.5 else 2):  # (int i = 0 i <= 6 i += (lod > 0.5 ? 1: 2)) {
                lines.append(QLineF(5, 18 + i * 5, 13, 18 + i * 5))
                lines.append(QLineF(94, 18 + i * 5, 102, 18 + i * 5))

        if lod >= 0.4:
            lineData = [
                QLineF(25, 35, 35, 35),
                QLineF(35, 30, 35, 40),
                QLineF(35, 30, 45, 35),
                QLineF(35, 40, 45, 35),
                QLineF(45, 30, 45, 40),
                QLineF(45, 35, 55, 35)
            ]
            lines.extend(lineData)

        painter.drawLines(lines)

        # Draw red ink
        if len(self.stuff) > 1:
            p = painter.pen()
            painter.setPen(QPen(Qt.red, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.setBrush(Qt.NoBrush)

            path = QPainterPath
            path.moveTo(self.stuff[0])
            for i in range(1, len(self.stuff)):
                path.lineTo(self.stuff[i])
                painter.drawPath(path)
                painter.setPen(p)

        """
        # Body.
        painter.setBrush(self.color)
        painter.drawEllipse(-10, -20, 20, 40)

        # Eyes.
        painter.setBrush(Qt.white)
        painter.drawEllipse(-10, -17, 8, 8)
        painter.drawEllipse(2, -17, 8, 8)

        # Nose.
        painter.setBrush(Qt.black)
        painter.drawEllipse(QRectF(-2, -22, 4, 4))

        # Pupils.
        painter.drawEllipse(QRectF(-8.0 + self.mouseEyeDirection, -17, 4, 4))
        painter.drawEllipse(QRectF(4.0 + self.mouseEyeDirection, -17, 4, 4))

        # Ears.
        if self.scene().collidingItems(self):
            painter.setBrush(Qt.red)
        else:
            painter.setBrush(Qt.darkYellow)

        painter.drawEllipse(-17, -12, 16, 16)
        painter.drawEllipse(1, -12, 16, 16)

        # Tail.
        path = QPainterPath(QPointF(0, 20))
        path.cubicTo(-5, 22, -5, 22, 0, 25)
        path.cubicTo(5, 27, 5, 32, 0, 30)
        path.cubicTo(-5, 32, -5, 42, 0, 35)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)
        """

    def mousePressEvent(self, event):
        super(Chip, self).mousePressEvent(event)
        self.update()

    def mouseMoveEvent(self, event):
        if event.modifiers() & Qt.ShiftModifier:
            self.stuff.append(event.pos())
            self.update()
            return

        super(Chip, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super(Chip, self).mouseReleaseEvent(event)
        self.update()




if __name__ == '__main__':

    import sys

    MouseCount = 70

    app = QApplication(sys.argv)

    scene = QGraphicsScene()
    scene.setSceneRect(-300, -300, 600, 600)
    scene.setItemIndexMethod(QGraphicsScene.NoIndex)

    for i in range(MouseCount):
        mouse = Chip(QColor(0.7, 0.4, 0.5))
        mouse.setPos(math.sin((i * 6.28) / MouseCount) * 200,
                     math.cos((i * 6.28) / MouseCount) * 200)
        scene.addItem(mouse)

    view = QGraphicsView(scene)
    view.setRenderHint(QPainter.Antialiasing)
    view.setBackgroundBrush(QBrush(QPixmap(':/cheese.jpg')))
    view.setCacheMode(QGraphicsView.CacheBackground)
    view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
    view.setDragMode(QGraphicsView.ScrollHandDrag)
    view.setWindowTitle("Colliding Mice")
    view.resize(400, 300)
    view.show()

    sys.exit(app.exec_())
