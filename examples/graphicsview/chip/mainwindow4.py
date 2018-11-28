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


from PySide.QtCore import (QRectF, Qt, QSize, QPointF)
from PySide.QtGui import (QPainter, QPixmap, QTransform, QImage, QColor)
from PySide.QtOpenGL import QGLFormat, QGLWidget, QGL
from PySide.QtGui import (QGraphicsView, QStyle, QFrame, QToolButton, QSlider, QVBoxLayout,
                             QHBoxLayout, QLabel, QButtonGroup, QGridLayout, QWidget, QSplitter, QGraphicsScene)

from view4 import View
from chip4 import Chip
import images_rc4


class MainWindow(QWidget):
    scene = None
    h1Splitter = None
    h2Splitter = None

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.populateScene()

        self.h1Splitter = QSplitter()
        self.h2Splitter = QSplitter()

        vSplitter = QSplitter()
        vSplitter.setOrientation(Qt.Vertical)
        vSplitter.addWidget(self.h1Splitter)
        vSplitter.addWidget(self.h2Splitter)

        view = View("Top left view")
        view.view().setScene(self.scene)
        self.h1Splitter.addWidget(view)

        view = View("Top right view")
        view.view().setScene(self.scene)
        self.h1Splitter.addWidget(view)

        view = View("Bottom left view")
        view.view().setScene(self.scene)
        self.h2Splitter.addWidget(view)

        view = View("Bottom right view")
        view.view().setScene(self.scene)
        self.h2Splitter.addWidget(view)

        layout = QHBoxLayout()
        layout.addWidget(vSplitter)
        self.setLayout(layout)

        self.setWindowTitle("Chip Demo")

    def populateScene(self):
        self.scene = QGraphicsScene()
        image = QImage(":/qt4logo.png")

        # Populate scene
        xx = 0
        nitems = 0
        for i in range(-11000, 11000, 110):
            xx += 1
            yy = 0
            for j in range(-7000, 7000, 70):
                yy += 1
                x = (i + 11000) / 22000.0
                y = (j + 7000) / 14000.0

                color = QColor(image.pixel(int(image.width() * x), int(image.height() * y)))
                item = Chip(color, xx, yy)
                item.setPos(QPointF(i, j))
                self.scene.addItem(item)
                nitems += 1
