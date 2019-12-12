import maya.cmds as cmds

def offsetGroup(node='C_GOD_CNT', hook=None,
                groupNames=['xform', 'driver', 'offset', 'buffer']):
    """
    creates group above the chosen node
    how it works xform(parent) -> driver -> offset -> buffer -> node(child)
    """
    hookbox = []
    for groupName in groupNames:
        grp = cmds.group(node, n=groupName + '_' + node)
        if groupName == groupNames[0]:
            hookbox.append(grp)
    if hook:
        cmds.parent(hookbox, hook)

offsetGroup(node='C_GOD_CNT', hook='test_loc',
            groupNames=['xform', 'driver', 'offset', 'buffer'])

def createMasterAsset():
    """
    creates MASTER grp to start with a rigging template
    """
    if cmds.objExists('MASTER'):
        print 'warning --- there is another MASTER group you slave!'
    else:
        strLst = ['.rx','.ry', '.rz', 
                  '.tx','.ty', '.tz', 
                  '.sx','.sy', '.sz',]
        # creating groups
        master = cmds.group(em = True, n = 'MASTER')
        for lst in ['geo', 'pass', 'md', 'controls', 'rig']:
            grplst = cmds.group(n = lst, em = True)
            cmds.parent(grplst,'MASTER')
            for attr in strLst:
                cmds.setAttr(grplst+attr, l = True, k = False, cb = False)
            if lst == 'rig':
                setupGrp = cmds.group(n = 'setup', em = True)
                for attr in strLst:
                    cmds.setAttr(setupGrp+attr, l = True, k = False, cb = False)
                cmds.parent(setupGrp,lst)
                for lst in ['structure', 'guide']:
                    riglst = cmds.group(n = lst, em = True)
                    cmds.parent(riglst,setupGrp)
                    for attr in strLst:
                        cmds.setAttr(riglst+attr, l = True, k = False, cb = False)
                        
        # adding attrs and clean up
        cmds.addAttr(master, ln="Scale", at="double", dv=1, k=True)
        for axis in 'xyz':
            cmds.connectAttr(master+'.Scale', master+'.s'+axis)
            cmds.setAttr(master+'.s'+axis, l = True, k = False, cb = False)
        #for attr in strLst:
        #    cmds.setAttr(master+attr, l = True, k = False, cb = False)
            
createMasterAsset()
