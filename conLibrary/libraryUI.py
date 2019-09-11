import controllerLibrary
import pprint
reload(controllerLibrary)
from PySide2 import QtWidgets, QtGui, QtCore

class ControllerLibraryUI(QtWidgets.QDialog):
    '''
    The controller library is a dialog that import and saves controllers
    '''
    def __init__(self):
        super(ControllerLibraryUI,self).__init__()

        # The library variable points to an instance of our controller library
        self.setWindowTitle('Controller Library UI')
        self.library = controllerLibrary.ControllerLibrary()

        # everytime we create a new instance, we will automatically build our UI and populate it
        self.buildUI()
        self.populate()

    def buildUI(self):
        """This meathod builds out the UI"""
        # this is the master layout
        layout = QtWidgets.QVBoxLayout(self)

        # this is the child horizontal
        saveWidget = QtWidgets.QWidget()
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        layout.addWidget(saveWidget)


        self.saveNameField = QtWidgets.QLineEdit()
        saveLayout.addWidget(self.saveNameField)

        # creates buttons
        saveBtn = QtWidgets.QPushButton('Save')
        saveBtn.clicked.connect(self.save)
        saveLayout.addWidget(saveBtn)

        # theses are the prameters for our thhumb nail size
        size = 64
        buffer = 12
        #this will create a list widget to display our thumb nails
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.listWidget.setIconSize(QtCore.QSize(size, size))
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidget.setGridSize(QtCore.QSize(size+buffer, size+buffer))
        layout.addWidget(self.listWidget)

        # this is our child widget that holds the buttons
        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        layout.addWidget(btnWidget)

        importBtn = QtWidgets.QPushButton('Import!')
        importBtn.clicked.connect(self.load)
        btnLayout.addWidget(importBtn)

        refreshBtn = QtWidgets.QPushButton('Refresh')
        refreshBtn.clicked.connect(self.populate)
        btnLayout.addWidget(refreshBtn)

        closeBtn = QtWidgets.QPushButton('Close')
        closeBtn.clicked.connect(self.close)
        btnLayout.addWidget(closeBtn)

    def populate(self):
        """this clears the listWidgets and then repopulates it with the contents of our library"""
        self.listWidget.clear()
        self.library.find()

        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)
            self.listWidget.addItem(item)

            screenshot = info.get('screenshot')
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)

            item.setToolTip(pprint.pformat(info))

        print "populating"

    def load(self):
        """This loads the currently selected controllers"""
        currentItem = self.listWidget.currentItem()

        if not currentItem.text():
            return

        name = currentItem.text()
        self.library.load(name)

    def save(self):
        """this saves the controller with the given file name"""
        name = self.saveNameField.text()
        if not name.strip():
            cmds.warning("You must give a name!")
            return

        self.library.save(name)
        self.populate()
        self.saveNameField.saveText('')

        print "Name", name

def showUI():
    """
    This shows and returns a handle to the UI
    :return:
        Qdialog
    """
    ui = ControllerLibraryUI()
    ui.show()
    return ui