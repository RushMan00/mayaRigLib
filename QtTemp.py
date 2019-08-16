"""

Source: https://www.patreon.com/posts/pyside2-for-maya-21014669

pyside has about 3 classes QWidgets/ Qdaillog / QmainWindow:

QWidget is the base class for all windows, it is a blank slate
Qdailog is a Qwiget but is design to display as a window abititly to accpect or reject like a normal windows with a OK button and a cancel button
QmainWindow to meet the needs of new window, like menu bar/ status bar /docking function as well, This can be over kill sometimes.

This is a Template called boiler Plate Code, where you would use it over and over again.

"""

from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

# Qt5 Maya 2018 +
from Qt import QtWidgets, QtGui, QtCore
from PySide2 import QtWidgets, QtGui,QtCore
from PyQt5 import QtWidgets, QtGui,QtCore

# #####Qt4 maya 2011 - 2017
# from Qt import QtWidgets, QtGui, QtCore
# from PySide import QtGui, QtCore
# from PyQt4 import QtGui, QtCore





# to access OpenMayaQT thought openmaya API
def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

    # To extend QtWidgets.QDialog in a class


class TestDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        # pass prameters to the parent class it self
        super(TestDialog, self).__init__(parent)

        self.setWindowTitle("Test Dialog")
        self.setMinimumWidth(200)
        # this is to remove the [?] on the top right hand window, the [?] exist because
        # is that windows creates it as defualt.
        # ^ means remove.
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()

    def create_widgets(self):
        self.lineedit = QtWidgets.QLineEdit()
        self.checkbox1 = QtWidgets.QCheckBox("Checkbot1")
        self.checkbox2 = QtWidgets.QCheckBox("Checkbot1")
        self.button1 = QtWidgets.QPushButton("button 1")
        self.button2 = QtWidgets.QPushButton("button 2")

    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.lineedit)
        main_layout.addWidget(self.checkbox1)
        main_layout.addWidget(self.checkbox2)
        main_layout.addWidget(self.button1)
        main_layout.addWidget(self.button2)


if __name__ == "__main__":
    d = TestDialog()
    d.show()

