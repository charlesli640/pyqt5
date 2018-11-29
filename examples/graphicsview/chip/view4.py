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


from Qt.QtCore import (QRectF, Qt, Slot, QSize)
from Qt.QtGui import (QPainter, QPixmap, QTransform, QIcon)
from Qt.QtOpenGL import QGLFormat, QGLWidget, QGL
from Qt.QtWidgets import (QGraphicsView, QStyle, QFrame, QToolButton, QSlider, QVBoxLayout,
                             QHBoxLayout, QLabel, QButtonGroup, QGridLayout, QWidget, QPushButton)
from Qt import __binding__

if __binding__ == "PySide2":
    import images_rc_pyside2
elif __binding__ == "PySide":
    import images_rc_pyside
elif __binding__ == "PyQt":
    import images_rc_pyqt
elif __binding__ == "PyQt5":
    import images_rc_pyqt5



class GraphicsView(QGraphicsView):
    view = None

    def __init__(self, view):
        super(GraphicsView, self).__init__()
        self.view = view

    def wheelEvent(self, e):
        if e.modifiers() & Qt.ControlModifier:
            if e.delta() > 0:
                self.view.zoomIn(6)
            else:
                self.view.zoomOut(6)
            e.accept()
        else:
            super(GraphicsView, self).wheelEvent(e)


class View(QFrame):
    graphicsView = None
    label = None
    label2 = None
    selectModeButton = None
    dragModeButton = None
    openGlButton = None
    antialiasButton = None
    resetButton = None
    zoomSlider = None
    rotateSlider = None

    def __init__(self, name, parent=None):
        super(View, self).__init__(parent)
        self.init_ui(name)

    def init_ui(self, name):
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.graphicsView = GraphicsView(self)
        self.graphicsView.setRenderHint(QPainter.Antialiasing, False)
        self.graphicsView.setDragMode(QGraphicsView.RubberBandDrag)
        self.graphicsView.setOptimizationFlags(QGraphicsView.DontSavePainterState)
        self.graphicsView.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.graphicsView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        size = self.style().pixelMetric(QStyle.PM_ToolBarIconSize)
        iconSize = QSize(size, size)

        zoomInIcon = QToolButton()
        zoomInIcon.setAutoRepeat(True)
        zoomInIcon.setAutoRepeatInterval(33)
        zoomInIcon.setAutoRepeatDelay(0)
        zoomInIcon.setIcon(QIcon(":/zoomin.png"))
        zoomInIcon.setIconSize(iconSize)
        zoomOutIcon = QToolButton()
        zoomOutIcon.setAutoRepeat(True)
        zoomOutIcon.setAutoRepeatInterval(33)
        zoomOutIcon.setAutoRepeatDelay(0)
        zoomOutIcon.setIcon(QIcon(":/zoomout.png"))
        zoomOutIcon.setIconSize(iconSize)
        self.zoomSlider = QSlider()
        self.zoomSlider.setMinimum(0)
        self.zoomSlider.setMaximum(500)
        self.zoomSlider.setValue(250)
        self.zoomSlider.setTickPosition(QSlider.TicksRight)

        # Zoom slider layout
        zoomSliderLayout = QVBoxLayout()
        zoomSliderLayout.addWidget(zoomInIcon)
        zoomSliderLayout.addWidget(self.zoomSlider)
        zoomSliderLayout.addWidget(zoomOutIcon)

        rotateLeftIcon = QToolButton()
        rotateLeftIcon.setIcon(QIcon(":/rotateleft.png"))
        rotateLeftIcon.setIconSize(iconSize)
        rotateRightIcon = QToolButton()
        rotateRightIcon.setIcon(QIcon(":/rotateright.png"))
        rotateRightIcon.setIconSize(iconSize)
        self.rotateSlider = QSlider()
        self.rotateSlider.setOrientation(Qt.Horizontal)
        self.rotateSlider.setMinimum(-360)
        self.rotateSlider.setMaximum(360)
        self.rotateSlider.setValue(0)
        self.rotateSlider.setTickPosition(QSlider.TicksBelow)

        # Rotate slider layout
        rotateSliderLayout = QHBoxLayout()
        rotateSliderLayout.addWidget(rotateLeftIcon)
        rotateSliderLayout.addWidget(self.rotateSlider)
        rotateSliderLayout.addWidget(rotateRightIcon)

        self.resetButton = QToolButton()
        self.resetButton.setText("0")
        self.resetButton.setEnabled(False)

        # Label layout
        labelLayout = QHBoxLayout()
        self.label = QLabel(name)
        self.label2 = QLabel("Pointer Mode")
        self.selectModeButton = QToolButton()
        self.selectModeButton.setText("Select")
        self.selectModeButton.setCheckable(True)
        self.selectModeButton.setChecked(True)
        self.dragModeButton = QToolButton()
        self.dragModeButton.setText("Drag")
        self.dragModeButton.setCheckable(True)
        self.dragModeButton.setChecked(False)
        self.antialiasButton = QToolButton()
        self.antialiasButton.setText("Antialiasing")
        self.antialiasButton.setCheckable(True)
        self.antialiasButton.setChecked(False)
        self.openGlButton = QToolButton()
        self.openGlButton.setText("OpenGL")
        self.openGlButton.setCheckable(True)
        self.openGlButton.setEnabled(QGLFormat.hasOpenGL())

        pointerModeGroup = QButtonGroup()
        pointerModeGroup.setExclusive(True)
        pointerModeGroup.addButton(self.selectModeButton)
        pointerModeGroup.addButton(self.dragModeButton)

        labelLayout.addWidget(self.label)
        labelLayout.addStretch()
        labelLayout.addWidget(self.label2)
        labelLayout.addWidget(self.selectModeButton)
        labelLayout.addWidget(self.dragModeButton)
        labelLayout.addStretch()
        labelLayout.addWidget(self.antialiasButton)
        labelLayout.addWidget(self.openGlButton)

        topLayout = QGridLayout()
        topLayout.addLayout(labelLayout, 0, 0)
        topLayout.addWidget(self.graphicsView, 1, 0)
        topLayout.addLayout(zoomSliderLayout, 1, 1)
        topLayout.addLayout(rotateSliderLayout, 2, 0)
        topLayout.addWidget(self.resetButton, 2, 1)
        self.setLayout(topLayout)

        self.resetButton.clicked.connect(self.resetView)
        self.zoomSlider.valueChanged.connect(self.setupTransform)
        self.rotateSlider.valueChanged.connect(self.setupTransform)

        self.graphicsView.verticalScrollBar().valueChanged.connect(self.setResetButtonEnabled)
        self.graphicsView.horizontalScrollBar().valueChanged.connect(self.setResetButtonEnabled)
        self.selectModeButton.toggled.connect(self.togglePointerMode)
        self.dragModeButton.toggled.connect(self.togglePointerMode)
        self.antialiasButton.toggled.connect(self.toggleAntialiasing)
        self.openGlButton.toggled.connect(self.toggleOpenGL)
        rotateLeftIcon.clicked.connect(self.rotateLeft)
        rotateRightIcon.clicked.connect(self.rotateRight)
        zoomInIcon.clicked.connect(self.zoomIn)
        zoomOutIcon.clicked.connect(self.zoomOut)

        self.setupTransform()

    def view(self):
        return self.graphicsView

    @Slot()
    def zoomIn(self):
        self.zoomSlider.setValue(self.zoomSlider.value() + 1)

    @Slot()
    def zoomOut(self):
        self.zoomSlider.setValue(self.zoomSlider.value() - 1)

    @Slot()
    def resetView(self):
        self.zoomSlider.setValue(250)
        self.rotateSlider.setValue(0)
        self.setupTransform()
        self.graphicsView.ensureVisible(QRectF(0, 0, 0, 0))

        self.resetButton.setEnabled(False)

    @Slot()
    def setResetButtonEnabled(self):
        self.resetButton.setEnabled(True)

    @Slot()
    def setupTransform(self):
        scale = pow(2.0, (self.zoomSlider.value() - 250) / 50.0)
        trans = QTransform()
        trans.scale(scale, scale)
        trans.rotate(self.rotateSlider.value())

        self.graphicsView.setTransform(trans)
        self.setResetButtonEnabled()

    @Slot()
    def togglePointerMode(self):
        self.graphicsView.setDragMode(
            QGraphicsView.RubberBandDrag if self.selectModeButton.isChecked() else QGraphicsView.ScrollHandDrag)
        self.graphicsView.setInteractive(self.selectModeButton.isChecked())

    @Slot()
    def toggleOpenGL(self):
        self.graphicsView.setViewport(
            QGLWidget(QGLFormat(QGL.SampleBuffers)) if self.openGlButton.isChecked() else QWidget())

    @Slot()
    def toggleAntialiasing(self):
        self.graphicsView.setRenderHint(QPainter.Antialiasing, self.antialiasButton.isChecked())

    @Slot()
    def rotateLeft(self):
        self.rotateSlider.setValue(self.rotateSlider.value() - 10)

    @Slot()
    def rotateRight(self):
        self.rotateSlider.setValue(self.rotateSlider.value() + 10)
