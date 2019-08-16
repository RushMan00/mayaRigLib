import maya.cmds as cmds

'''

Joint Guide setup
Create joints and guides before creating rig

'''
def guideJoint(name='node', side='C', number=3,
               mirrorTransform=False,
               mirrorRotataion=False):
    '''
    FUNCTION:      GuideJoint.guideJoint()
    DESCRIPTION:   create GuideJoints for easy creation
    USAGE:         add in the necessary flags to build...
                   jointGuide(name='frontProller', number=1,
                              mirrorTransform = True,
                              mirrorRotataion = True)
                    jointGuide(name='cog', side='C', number=1)
    RETURN:        Creates Joints on Locator and add in structure, guide
    AUTHOR:        Tony K Song
    DATE:          05/02/19
    Version        1.0.0

    @todo
    Make UI using GUI and pyside2

    '''

    # for mirror
    # for Both side mirror
    if mirrorTransform:

        for num in range(1, number + 1):
            locList = []
            for side in "LR":
                num = str(num)
                # create joints
                jnt = cmds.joint(name='jnt_{0}_{1}_{2}'.format(name, num, side))
                cmds.parent(jnt, 'structure')
                # create loc
                loc = cmds.spaceLocator(name='loc_{0}_{1}_{2}'.format(name, num, side))[0]
                locList.extend([loc])
                cmds.parent(loc, 'guide')
                cmds.parentConstraint(loc, jnt, mo=True)
            print locList
            # create mirror setup
            decompMatrixT = cmds.shadingNode('decomposeMatrix', asUtility=True,
                                             name='DM_tran_{0}_{1}_{2}'.format(name, num, 'GNODE'))
            multiDivT = cmds.shadingNode('multiplyDivide', asUtility=True,
                                         name='MD_tran_{0}_{1}_{2}'.format(name, num, 'GNODE'))

            cmds.setAttr(multiDivT + '.operation', 1)
            cmds.setAttr(multiDivT + '.input2X', -1)

            cmds.connectAttr(locList[0] + '.worldMatrix', decompMatrixT + '.inputMatrix')
            cmds.connectAttr(decompMatrixT + '.outputTranslate', multiDivT + '.input1')
            cmds.connectAttr(multiDivT + '.output', locList[1] + '.translate')

            if mirrorRotataion:
                decompMatrixR = cmds.shadingNode('decomposeMatrix', asUtility=True,
                                                 name='DM_rot_{0}_{1}_{2}'.format(name, num, 'GNODE'))
                multiDivR = cmds.shadingNode('multiplyDivide', asUtility=True,
                                             name='MD_rot_{0}_{1}_{2}'.format(name, num, 'GNODE'))
                cmds.setAttr(multiDivR + '.operation', 1)
                cmds.setAttr(multiDivR + '.input2Y', -1)
                cmds.setAttr(multiDivR + '.input2Z', -1)

                cmds.connectAttr(locList[0] + '.worldMatrix', decompMatrixR + '.inputMatrix')
                cmds.connectAttr(decompMatrixR + '.outputRotate', multiDivR + '.input1')
                cmds.connectAttr(multiDivR + '.output', locList[1] + '.rotate')

        cmds.setAttr(loc + '.overrideEnabled', 1)
        cmds.setAttr(loc + '.overrideDisplayType', 2)

    else:
        # for single
        for num in range(1, number + 1):
            num = str(num)

            jnt = cmds.joint(name='jnt_{0}_{1}_{2}'.format(name, num, side))
            cmds.parent(jnt, 'structure')
            loc = cmds.spaceLocator(name='loc_{0}_{1}_{2}'.format(name, num, side))
            cmds.parent(loc, 'guide')
            cmds.parentConstraint(loc, jnt, mo=True)
