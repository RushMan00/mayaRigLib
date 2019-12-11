import maya.cmds as cmds
from vtool.maya_lib import rigs
from vtool import util

util.show('Hellow World.')
#===========================
"""
As a warmup in creating this rigging system
importing and testing
"""
#===========================
import sys
sys.path.append( 'C:/Program Files (x86)/Vetala' )
from vtool import util
maya.utils.executeDeferred(run_tools_ui, '')

#===========================
import sys
sys.path.append('E:/workspace/rigLib')

#to print the list of sys.paths
paths = sys.path
for i in paths:
    print i

#import the test
import tonyTest as tt
reload(tt)
tt.printThis()

#===========================
import sys
sys.path.append('C:\ProgramData\Autodesk\ApplicationPlugins\ngskintools')

#to print the list of sys.paths
paths = sys.path
for i in paths:
    print i
    
from ngSkinTools.ui.mainwindow import MainWindow; MainWindow.open()

path = 'U:/IBRigLib'
if path not in sys.path:
    sys.path.append(path)

#to print the list in sys.paths
paths = sys.path
for i in paths:
    print i
