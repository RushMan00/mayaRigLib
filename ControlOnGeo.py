import maya.cmds as cmds


def controlOnGeo(name='name',
                 side='C',
                 controlShape='sphere',
                 controlSize=2,
                 geo=['geo'],
                 groundIt=False,
                 controlColour=20,
                 subControls=False,
                 parentTo='CNT_SUB_GOD_2_C'):
                     
    for num, lst in enumerate(geo, 1):
        clust = cmds.cluster(lst, n='clust_{0}_{1}_{2}'.format(name, num, side))
        jnt = cmds.joint(n='jnt_{0}_{1}_{2}'.format(name, num, side))

        cmds.parent(jnt, 'structure')
        parcon = cmds.parentConstraint(clust, jnt)

        # cleanup
        cmds.delete(parcon)
        cmds.delete(clust)

        if groundIt:
            cmds.select(jnt)
            cmds.move(0, y=True)

        rig = rigs.FkRig(name, side)
        rig.set_joints(jnt)
        rig.set_control_size(controlSize)
        rig.set_control_shape(controlShape)
        rig.set_control_color(controlColour)
        rig.set_create_sub_controls(subControls)
        rig.create()
        rig.set_control_parent(parentTo)
        rig.delete_setup()
        
        
        if subControls:
            for subNames in ['CNT_SUB_{0}_{1}_C'.format(name.upper(), num),
                             'CNT_SUB_{0}_SUB_{1}_C'.format(name.upper(), num)]:
                attr.unlock_attributes(subNames,
                                       attributes=['tx', 'ty', 'tz',
                                                   'ry', 'rz', 'rx'],
                                       only_keyable=False)
                cmds.parentConstraint('CNT_SUB_{0}_SUB_{1}_C'.format(name.upper(), num),
                                      lst, mo = True)                       
        else:                               
            cmds.parentConstraint('CNT_{0}_{1}_C'.format(name.upper(), num),
                                  lst, mo = True)
            
#########################################################################################

def jointChainOnGeo(name='treeB_leaf',
                    side='C',
                    geo='g_treeB_leaf_01',
                    list=['.vtx[762]', '.vtx[755]', '.vtx[750]', '.vtx[808]', '.vtx[799]'],
                    parentTo=None
                    ):
    # first joint
    jntpos = cmds.xform(geo + list[0], q=True, t=True, ws=True)
    firstjnt = cmds.joint(p=jntpos, n='jnt_{0}_1_{1}'.format(name, side))

    if parentTo:
        cmds.parent(firstjnt, parentTo)

    # rest of the joints
    for num, lst in enumerate(list, 2):
        jntpos = cmds.xform(geo + lst, q=True, t=True, ws=True)
        cmds.joint(p=jntpos, n='jnt_{0}_{1}_{2}'.format(name, num, side))
        cmds.joint('jnt_{0}_{1}_{2}'.format(name, num - 1, side), e=True, zso=True, oj='xyz')
