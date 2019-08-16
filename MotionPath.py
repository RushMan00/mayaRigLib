import maya.cmds as cmds

def motionPath(name = 'Hatch_Door',
               side = 'C',
               curve='crv_hatch_0_C',
               numOfJoint= 7,
               attrSlider = 'CNT_LENS_2_C',
               numOfCrvPoints = 14.0,
               ):

    '''
    FUNCTION:      motionPath
    DESCRIPTION:   creates a motion path
    USAGE:         must have existing curve
                    addAttr(name = 'Hatch_Door', side = 'C',  curve='crv_hatch_0_C', numOfJoint= 7, attrSlider = 'CNT_LENS_2_C',
                            numOfCrvPoints = 14.0,
    RETURN:        creates a motion path on curve with attrSlider
    AUTHOR:        Tony K Song
    DATE:          02/07/19
    Version        1.0.0

    @TODO
    -replace numOfCrvPoints
    -added in rebuildCurve = True (for equal distance between joints)
    -rasie error
    '''

    # create group
    cmds.group(curve, n='curves', p='setup')

    allJointNames = []
    separate = numOfCrvPoints / numOfJoint

    # add attr to control
    cmds.addAttr(attrSlider, k=True, ln=name + '_Slider', at='double', min=0, max=10)
    # add remapValue as clamp
    remapName = cmds.shadingNode('remapValue', n=name + '_remapValue', asUtility=True)
    cmds.setAttr(remapName + ".inputMax", 10)
    # connect slider Attr to
    cmds.connectAttr(attrSlider + '.' + name + '_Slider', remapName + '.inputValue')

    defaultLen = numOfCrvPoints

    # create joints
    for numOfJoints in range(1, numOfJoint + 1):
        jointName = cmds.joint(name='joint' + '_' + name + '_' + str(numOfJoints) + '_' + side)
        # allJointNames.append(jointName)
        cmds.group(jointName, p='structure')

        # attach joint to curve as a path
        cmds.select(jointName, curve)
        cmds.pathAnimation(name = "anim_path_" + str(numOfJoints))
        cmds.select(deselect = True)

        # remove key from animation slider (find a better way to do this, this is shit)
        cmds.cutKey('anim_path_' + str(numOfJoints), attribute='uValue', option='keys')

        # find a better way to calulate
        numOfCrvPoints = numOfCrvPoints - separate

        # seperating and even out the joints on Curve
        cmds.setAttr('anim_path_' + str(numOfJoints) + '.uValue', numOfCrvPoints)

        # creating blend colours
        blendColourName = cmds.shadingNode('blendColors', n=name + '_blendColors' + '_' + str(numOfJoints),
                                           asUtility=True)
        cmds.setAttr(blendColourName + ".color1R", defaultLen)
        cmds.setAttr(blendColourName + ".color2R", numOfCrvPoints)

        # # find a better way to calulate
        # numOfCrvPoints = numOfCrvPoints - separate

        # // Result: Connected Hatch_Door_remapValue.inputValue to Hatch_Door_blendColors_4.color1.color1R. //
        cmds.connectAttr(remapName + '.outValue', blendColourName + '.blender')
        # connect blendColourName to anim_path
        cmds.connectAttr(blendColourName + '.output.outputR', "anim_path_" + str(numOfJoints)+'.uValue')
