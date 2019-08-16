import maya.cmds as cmds

import VControls
reload(VControls)

'''

to make controls on each geo
without going though the structure process 

Great tool if you have many objects that needs one control or COG

Example in KingdomForce - prp_rock_Group

'''

def controlOnGeo(name='name',
                 side='C',
                 controlShape = 'sphere',
                 controlSize = 2,
                 geo=['geo'],
                 groundIt=False,
                 controlColour=20,
                 subControls=False,
                 parentTo = 'CNT_SUB_GOD_2_C'):

    for num, lst in enumerate(geo, 1):
        clust = cmds.cluster(lst, n = 'clust_{0}_{1}_{2}'.format(name, num, side))
        loc = cmds.spaceLocator(n='guilds_{0}_{1}_{2}'.format(name, num, side))


        cmds.parent(loc, 'guide')
        parcon = cmds.parentConstraint(clust, loc)

        # cleanup
        cmds.delete(parcon)
        cmds.delete(clust)

        if groundIt:
            cmds.select(loc)
            cmds.move(0, y=True)

        # creating
        VControls.vControls(name=name,
                            side=side,
                            geo=[lst],
                            guides=loc,
                            controlShape=controlShape,
                            controlSize=controlSize,
                            subControls=subControls,
                            controlColour=controlColour,
                            parentTo=parentTo
                            )

#######################################################

def controlOnGeo2(name='name',
                  side='C',
                  controlShape = 'sphere',
                  controlSize = 2,
                  geoList=['geo'],
                  groundIt=False,
                  controlColour=20,
                  subControls=False,
                  parentTo = 'CNT_SUB_GOD_2_C'):

    for num, lst in enumerate(geoList, 1):
        clust = cmds.cluster(lst, n = 'clust_{0}_{1}_{2}'.format(name, num, side))
        loc = cmds.spaceLocator(n='guilds_{0}_{1}_{2}'.format(name, num, side))


        cmds.parent(loc, 'guide')
        parcon = cmds.parentConstraint(clust, loc)

        # cleanup
        cmds.delete(parcon)
        cmds.delete(clust)

        if groundIt:
            cmds.select(loc)
            cmds.move(0, y=True)

        # creating
        VControls.vControls(name=name,
                            side=side,
                            geo=[lst],
                            guides=loc,
                            controlShape=controlShape,
                            controlSize=controlSize,
                            subControls=subControls,
                            controlColour=controlColour,
                            parentTo=parentTo
                            )


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