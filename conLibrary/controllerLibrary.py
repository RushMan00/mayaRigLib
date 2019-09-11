from maya import cmds
import os
import json
import pprint

'''
pyQt Docs
https://doc.bccnsoft.com/docs/PyQt5/

for Examples
http://nullege.com/codes/search?cq=PyQt5.QtWidgets.QDialog
'''


# finds the path of the maya folder
USERAPPDIR = cmds.internalVar(userAppDir = True)
print USERAPPDIR

# os.path.join - this will add \ or / what ever the OS system is
DIRECTORY = os.path.join(USERAPPDIR, 'controllerLibrary')

def createDirectory(directory=DIRECTORY):
    """
    create the given directory if it doesn't exist already
    :param directory(str): create a directory

    """
    if not os.path.exists(directory):
        os.mkdir(directory)

class ControllerLibrary(dict):

    # **info is a store variable just empty dic. ex. info = {}
    def save(self, name, directory=DIRECTORY, screenshot = True, **info):

        createDirectory(directory)

        # os.path.join() = path and member of path
        # ex. C:/Users/tsong/Documents/maya/ + test.ma
        path = os.path.join(directory,'%s.ma'%name )
        infoFile = os.path.join(directory,'%s.jason'%name)

        # to store info?
        info['name'] = name
        info['path'] = path

        cmds.file(rename = path)

        # anything that is selected in the scene save it
        if cmds.ls(selection = True):
            cmds.file(force = True, type = 'mayaAscii', exportSelected = True)

        else:
            cmds.file(save=True, type='mayaAscii', force=True)

        if screenshot:
            info['screenshot'] = self.saveScreenshot(name, directory = directory)

        # with open file info Dictionary "write" w as f
        with open(infoFile,'w') as f:

             # dump that info Dictionary (f) with indent of 4
             json.dump(info, f, indent=4)

        self[name] = info

    def find(self, directory=DIRECTORY):
        # list the directory

        self.clear()
        if not os.path.exists(directory):
            return

        files = os.listdir(directory)
        mayaFiles = [f for f in files if f.endswith('.ma')]

        for ma in mayaFiles:
            name, ext = os.path.splitext(ma)
            path = os.path.join(directory,ma)

            infoFile = '%s.json' %name
            if infoFile in files:
                infoFile = os.path.join(directory, infoFile)

                with open(infoFile,'r') as f:
                    info = json.load(f)
            else:
                info = {}

            screenshot = '%s.jpg' % name
            if screenshot in files:
                info['screenshot'] = os.path.join(directory, name)


            info['name'] = name
            info['path'] = path

            self[name] = info


    def load(self, name):
        path = self[name]['path']
        cmds.file(path, i=True, usingNamespaces = False)


    def saveScreenshot(self, name , directory = DIRECTORY):
        path = os.path.join(directory, '%s.jpg' % name)

        cmds.viewFit()
        cmds.setAttr('defaultRenderGlobals.imageFormat', 8)

        cmds.playblast(completeFilename = path, forceOverwrite = True, format = 'image',
                       width = 200, height = 200,showOrnaments = False, startTime = 1,
                       endTime = 1, viewer =False)
        return path
