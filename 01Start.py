
# ===========================
'''
To start up my Rig
'''

import sys

sys.path.append('/mayaRig')

# to print the list of sys.paths
paths = sys.path
for i in paths:
    print i

# ===========================

# import the test
import tonyTest as tt
reload(tt)
tt.printThis()

# ===========================

'''
To start up See module
'''
import sys
sys.path.append('/mayaRig/see')

# to print the list of sys.paths
paths = sys.path
for i in paths:
    print(i)

from see import see

# test see from local
print(see(pm.joint()))
pm.delete('joint1')


# ===========================

'''
To start up pymelTool
'''
# import the test
import pymelTool as pt
reload(pt)

pt.copyAttrs()
