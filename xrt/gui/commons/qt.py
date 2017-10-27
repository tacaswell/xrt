# -*- coding: utf-8 -*-
__author__ = "Roman Chernikov, Konstantin Klementiev"
__date__ = "18 Oct 2017"

try:
    from matplotlib.backends import qt_compat
except ImportError:
    from matplotlib.backends import qt4_compat
    qt_compat = qt4_compat

if 'pyqt4' in qt_compat.QT_API.lower():  # also 'PyQt4v2'
    QtName = "PyQt4"
#    from PyQt4 import QtGui, QtCore
#    import PyQt4.QtGui as myQtGUI
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
    import PyQt4
    locals().update(vars(PyQt4.QtCore.Qt))
    from PyQt4.QtOpenGL import QGLWidget
    import PyQt4.QtWebKit as QtWeb
    try:
        import PyQt4.Qwt5 as Qwt
    except:  # analysis:ignore
        pass
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as\
        FigCanvas
elif 'pyqt5' in qt_compat.QT_API.lower():
    QtName = "PyQt5"
#    from PyQt5 import QtGui, QtCore
#    import PyQt5.QtWidgets as myQtGUI
#    import PyQt5.QtOpenGL as myQtGL
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    import PyQt5
    locals().update(vars(PyQt5.QtCore.Qt))
    from PyQt5.QtWidgets import *
    from PyQt5.QtOpenGL import QGLWidget
    try:
        import PyQt5.QtWebEngineWidgets as QtWeb
    except ImportError:
        import PyQt5.QtWebKitWidgets as QtWeb
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as\
        FigCanvas
else:
    raise ImportError("Cannot import any Python Qt package!")

#QWidget, QApplication, QAction, QTabWidget, QToolBar, QStatusBar, QTreeView,\
#    QShortcut, QAbstractItemView, QHBoxLayout, QVBoxLayout, QSplitter,\
#    QComboBox, QMenu, QListWidget, QTextEdit, QMessageBox, QFileDialog,\
#    QListWidgetItem, QGLWidget, QGroupBox,\
#    QLabel, QSizePolicy, QLineEdit, QCheckBox, QSpinBox, QSlider = (
#        myQtGUI.QWidget, myQtGUI.QApplication, myQtGUI.QAction,
#        myQtGUI.QTabWidget, myQtGUI.QToolBar, myQtGUI.QStatusBar,
#        myQtGUI.QTreeView, myQtGUI.QShortcut, myQtGUI.QAbstractItemView,
#        myQtGUI.QHBoxLayout, myQtGUI.QVBoxLayout, myQtGUI.QSplitter,
#        myQtGUI.QComboBox, myQtGUI.QMenu, myQtGUI.QListWidget,
#        myQtGUI.QTextEdit, myQtGUI.QMessageBox, myQtGUI.QFileDialog,
#        myQtGUI.QListWidgetItem, myQtGL.QGLWidget, myQtGUI.QGroupBox,
#        myQtGUI.QLabel, myQtGUI.QSizePolicy,
#        myQtGUI.QLineEdit, myQtGUI.QCheckBox, myQtGUI.QSpinBox,
#        myQtGUI.QSlider)
#QIcon, QFont, QKeySequence, QStandardItemModel, QStandardItem, QPixmap,\
#    QDoubleValidator, QIntValidator =\
#    (QtGui.QIcon, QtGui.QFont, QtGui.QKeySequence, QtGui.QStandardItemModel,
#     QtGui.QStandardItem, QtGui.QPixmap,
#     QtGui.QDoubleValidator, QtGui.QIntValidator)


class mySlider(QSlider):
    def __init__(self, parent, scaleDirection, scalePosition):
        super(mySlider, self).__init__(scaleDirection)
        self.setTickPosition(scalePosition)
        self.scale = 1.

    def setRange(self, start, end, step):
        self.scale = 1. / step
        QSlider.setRange(self, start / step, end / step)

    def setValue(self, value):
        QSlider.setValue(self, int(value*self.scale))


try:
    glowSlider = Qwt.QwtSlider
    glowTopScale = Qwt.QwtSlider.TopScale
except:  # analysis:ignore
    glowSlider = mySlider
    glowTopScale = QSlider.TicksAbove