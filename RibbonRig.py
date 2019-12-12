import maya.cmds as cmds
import maya.OpenMaya as OpenMaya1
import math

import rigSetup as rs
reload(rs)



'''
# tutorial: http://www.riganimator.com/procedural-ribbon/
'''

class RibbonRig():
    def __init__(self,
                 name='Demo',
                 side='C',
                 width=10,
                 numJoints=10,
                 ):

        self.name = name
        self.side = side
        self.width = width
        self.numJoints = numJoints

        # var.
        self.topPoint = (width / 2)
        self.endPoint = (width / 2 * -1)

        # procs
        self.createRibbon()

    # GENERAL FUNCTION: CREATE A CONTROL MADE OUT OF A CURVE
    def __createCurveCtrl(self,
                          name='curveCtrl',
                          scale=1, color=6,
                          freezeTransforms=0,
                          pos=(0, 0, 0),):

        # Create the controller
        crvCtrl = cmds.curve(name=name, r=False, d=1,  # k = True, a = True,
                   p=[
                       (-0.5, 0.5, 0.5),
                       (-0.5, 0.5, -0.5),
                       (-0.5, -0.5, -0.5),
                       (0.5, -0.5, -0.5),
                       (0.5, 0.5, -0.5),
                       (0.5, 0.5, 0.5),
                       (0.5, -0.5, 0.5),
                       (-0.5, -0.5, 0.5),
                       (-0.5, 0.5, 0.5),
                       (0.5, 0.5, 0.5),
                       (0.5, -0.5, 0.5),
                       (0.5, -0.5, -0.5),
                       (0.5, 0.5, -0.5),
                       (-0.5, 0.5, -0.5),
                       (-0.5, -0.5, -0.5),
                       (-0.5, -0.5, 0.5),
                   ])
        # crvCtrl = cmds.curve(
        #     p=[(0, 1, 0), (0, -1, 0), (0, 0, 0), (0, 0, 1), (0, 0, -1), (0, 0, 0), (1, 0, 0), (-1, 0, 0)],
        #     d=1)
        crvCtrl = cmds.rename(crvCtrl, name)
        # Set the scale
        cmds.setAttr((crvCtrl + '.scale'), scale, scale, scale)
        cmds.makeIdentity(crvCtrl, apply=True, translate=False, rotate=False, scale=True)
        # Set the color for the curve
        cmds.setAttr((cmds.listRelatives(crvCtrl, shapes=True)[0] + '.overrideEnabled'), 1)
        cmds.setAttr((cmds.listRelatives(crvCtrl, shapes=True)[0] + '.overrideColor'), color)
        # If a position was defined
        if len(pos) == 3:
            # Position the locator
            cmds.setAttr((crvCtrl + '.translate'), pos[0], pos[1], pos[2])
            # If freeze transforms was set to true
            if freezeTransforms:
                cmds.makeIdentity(crvCtrl, apply=True, translate=True)
        # Return the locator
        return crvCtrl

# NOTES
    def createRibbon(self):
        # checking for master group
        if cmds.objExists('MASTER'):
            print 'warning --- there is another MASTER group you slave!'
        else:
            rs.createMasterAsset()
        # End of master group


        cmds.nurbsPlane(n = self.name + "_" + self.side,
                        axis=(0, 1, 0), width= self.width,
                        lengthRatio=(1.0 / self.width),
                        u=self.numJoints, v=1, degree=3, ch=0)

        ctrlTop = self.__createCurveCtrl(name=(self.name + '_top_CNT'), freezeTransforms=1, color=9, pos=(self.topPoint,0, 0))
        ctrlMid = self.__createCurveCtrl(name=(self.name + '_mid_CNT'), freezeTransforms=1, color=9, pos=(0, 0, 0))
        ctrlEnd = self.__createCurveCtrl(name=(self.name + '_end_CNT'), freezeTransforms=1, color=9, pos=(self.endPoint, 0, 0))

        # PointConstraint the midCtrl between the top/end
        midConst = cmds.pointConstraint(ctrlTop, ctrlEnd, grpMid)
    # Group the controllers


# NOTES
# guide will be 2 end points rather be to a locator or joints
# it must be build in a world position then attatch/ parent to other end points

# main setup
# create nurbs plane
# add in hair folical to each plane of the of the nurbs plane
# remove nuclues/ hairSystem1OutputCurve/ hairSystem, remove all the grp under Folicles
# create adj grp under Folicles then Crv control then joints, ex. adj_grp -> crv -> jnts
# create controls on both ends and in the middle with adjs group underneath called Start_cnt, end_cnt, middle_cnt
# add attribute called twist on Start_cnt and end_cnt,
# add attribute on middle_cnt, ROLL: Roll, RollOffSet. Sine: Ampltude, SineOffset, SineTwist
# select Start_cnt & end_cnt and PointConstraint to the middle controller on the adjs group


# ribbon Twist Setup
# dup the nurbs ribbon, call it twist_ribbin_nurb, add in the twist deformer to dup nurbs,
# name the deformer twist_handle, group the deformer call it deformer_grp
# create two plusMinus end and start for both end of the Controls
# setAttr both to sum

# connectAttr   Start_cnt.twist >> ribbon_twist_start_sum_pma.input1D[0]
# connectAttr   Start_cnt.Offset >> ribbon_twist_start_sum_pma.input1D[1]
# connectAttr ribbon_twist_start_sum_pma.output1D >> twist_handle.startAngle

# connectAttr   middle_cnt.roll >> ribbon_twist_start_sum_pma.input1D[2]
# connectAttr   middle_cnt.RollOffSet >> ribbon_twist_start_sum_pma.input1D[3]
# connectAttr   middle_cnt.roll >> ribbon_twist_end_sum_pma.input1D[2]
# connectAttr   middle_cnt.RollOffSet >> ribbon_twist_end_sum_pma.input1D[3]

# connectAttr   End_cnt.twist >> ribbon_twist_end_sum_pma.input1D[0]
# connectAttr   End_cnt.Offset >> ribbon_twist_end_sum_pma.input1D[1]
# connectAttr ribbon_twist_top_sum_pma.output1D >> twist_handle.startAngle

# ribbon Sine Setup
# dup the nurbs ribbon, call it sine_ribbin_nurb,
# add in the sine deformer to dup nurbs, name it sine_ribbin_def
# rotate the sign deformorer rz 90, rename it to sine_ribbin_nurb
# setAttr sine_ribbin_nurb.dropOff 1
# connectAttr middle_cnt.Ampltude >> sine_ribbin_def.Ampltude
# connectAttr middle_cnt.SineOffset >> sine_ribbin_def.Offset
# connectAttr middle_cnt.SineTwist >> sine_ribbin_def.ry
