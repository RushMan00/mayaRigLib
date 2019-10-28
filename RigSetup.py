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
    if cmds.objExists('MASTER'):
        print 'warning --- there is another MASTER group you slave!'
    else:
        master = cmds.group(em = True, n = 'MASTER')
        for lst in ['geo', 'pass', 'md', 'controls', 'rig']:
            grplst = cmds.group(n = lst, em = True)
            cmds.parent(grplst,'MASTER')
            for attr in ['.r', '.t', '.s']:
                cmds.setAttr(grplst+attr, l = True, k = False, cb = False)
            if lst == 'rig':
                setupGrp = cmds.group(n = 'setup', em = True)
                cmds.parent(setupGrp,lst)
                for lst in ['structure', 'guide']:
                    riglst = cmds.group(n = lst, em = True)
                    cmds.parent(riglst,setupGrp)
                    for attr in ['.r', '.t', '.s']:
                        cmds.setAttr(riglst+attr, l = True, k = False, cb = False)
