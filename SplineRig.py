import maya.cmds as cmds

# vtools
from vtool.maya_lib import rigs

#tony's tools
import VControls as vCtrls

'''

splineIK setup
Create joint chain and save it in structure

'''

class splineIK():
    def __init__(self,
                 name='node',
                 side='C',
                 startJointChain='JNT_ribbon_14_C',
                 numberOfCtrls = 5,
                 curve = False,
                 controlSize = 1,
                 parentTo=None,
                 scaleOrTranslate = 'scale',
                 axisDirection='X',
                 rotateControl = {'z':0},
                 ):
        '''
        FUNCTION:      SplineRig.splineIK()
        DESCRIPTION:   adds a SplineRig on a joint chain, with strechky function, turn on off
        USAGE:         must create a joint chain
                       splineIK(name='node', side='C', startJointChain='JNT_ribbon_14_C',
                                numberOfCtrls = 5, controlSize = 1, parentTo=None)
        RETURN:        SplineRig
        AUTHOR:        Tony K Song
        DATE:          02/07/19
        Version        1.0.0

        EXAMPLE: prp_seatbelt in kingdomforce season 1



        @todo
        VControl replacement
        :type rotateControl: the ordation axis and then rotation degrees    Ex.{"r":45}
        :type rotateControl: the ordation axis and then rotation degrees

        '''

        self.name=name
        self.side=side
        self.startJointChain=startJointChain
        self.parentTo=parentTo
        self.controlSize=controlSize
        self.numberOfCtrls = numberOfCtrls + 1
        self.axisDirection = axisDirection
        self.curve = curve
        self.scaleOrTranslate = scaleOrTranslate.lower()
        self.rotateControl = rotateControl

        # Var
        self.clustName = None
        self.colour = 22
        self.control_size = process.get_option('Control Size', 'Setup.Controls')
        self.ikh = None
        self.crvName = None
        self.effector = None
        self.lastChild = cmds.listRelatives(startJointChain, ad=True)[0]
        self.jntClusGrp = []

        # procs
        self.__create()

    def __adjGrp(self):

        myParent = cmds.listRelatives(self.clustName, p=True)
        posGroup = cmds.group(empty=True, name="pos_" + self.clustName)
        if myParent != None: cmds.parent(posGroup, myParent)
        orient = cmds.orientConstraint(self.clustName, posGroup)
        point = cmds.pointConstraint(self.clustName, posGroup)
        cmds.delete(orient, point)
        adjGroup = cmds.group(empty=True, name="adj_" + self.clustName)
        orient = cmds.orientConstraint(self.clustName, adjGroup)
        point = cmds.pointConstraint(self.clustName, adjGroup)
        cmds.delete(orient, point)
        sdkGroup = cmds.group(empty=True, name="sdk_" + self.clustName)
        orient = cmds.orientConstraint(self.clustName, sdkGroup)
        point = cmds.pointConstraint(self.clustName, sdkGroup)
        cmds.delete(orient, point)
        cmds.parent(self.clustName, sdkGroup)
        cmds.parent(sdkGroup, adjGroup)
        cmds.parent(adjGroup, posGroup)
        cmds.select(cl=True)

    # Make spline IK
    def __initialSetup(self):
        # get last name string of the chain
        self.ikh = cmds.ikHandle(sj=self.startJointChain, ee=self.lastChild,
                                 sol='ikSplineSolver', scv=False, pcv=False,
                                 n='self.ikh_{0}Spline_01_{1}'.format(self.name, self.side))


        # Rebuild curve with desired cv count
        self.crvName = cmds.rebuildCurve(self.ikh[2], rpo=1, rt=0, end=1,
                                         kr=0, kcp=0, kep=1, kt=0,
                                         s=self.numberOfCtrls - 2, d=3, tol=0.01)
        self.effector = cmds.rename('effector1', '{0}_{1}_effector'.format(self.side, self.name))


        # cluster setup
        num = 1
        numLst = ['0:1']
        numLst.extend(range(2,  self.numberOfCtrls-1))
        numLst.append('{0}:{1}'.format(str(self.numberOfCtrls - 1), str(self.numberOfCtrls)))

        for cv in numLst:
            clus = cmds.cluster('{0}.cv[{1}]'.format(self.ikh[2], str(cv)))

            # if first two points
            if cv == '0:1':
                # find the first point position on curve
                startPnt = cmds.xform(self.ikh[2] + '.cv[0]', q=True, t=True)
                # positioned the cluster to the Start point
                cmds.xform(clus, piv=(startPnt))

            # if last two points
            if cv == '{0}:{1}'.format(str(self.numberOfCtrls - 1), str(self.numberOfCtrls)):
                # find the end point position on curve
                endPnt = cmds.xform('{0}.cv[{1}]'.format(self.ikh[2], str(self.numberOfCtrls)), q=True, t=True)
                # positioned the cluster to the End point
                cmds.xform(clus, piv=(endPnt))

            self.clustName = cmds.rename(clus[1], 'cls_{0}_{1}_{2}'.format(self.name, str(num), self.side))
            self.__adjGrp()
            num += 1

            # creating joints to replace cluster as base
            jntNames = cmds.joint(name= 'jnt_cluster{0}_{1}_{2}'.format(self.name, str(num-1), self.side))
            self.jntClusGrp.append(jntNames)

            # rotate for control
            if self.rotateControl:
                cmds.setAttr(jntNames+'.r'+self.rotateControl.keys()[0], self.rotateControl.values()[0])

            # find the cluster position
            bah=cmds.parentConstraint(self.clustName, jntNames, sr=['x','y','z'])
            cmds.delete(bah)
            cmds.parentConstraint(jntNames, self.clustName, sr=['x','y','z'],mo=True)


    def __createControls(self):
        # create controls
        if self.side == "C":
            colour = 22
        else:
            colour = 13 if self.side == 'R' else 6

        # Make controls
        rig = rigs.FkRig(self.name, self.side)


        # posCls = []
        # for ii in range(1,  self.numberOfCtrls):
        #     posCls.append('pos_cls_{0}_{1}_{2}'.format(self.name,str(ii),self.side))


        rig.set_joints(self.jntClusGrp)
        rig.set_control_shape('circleDoubleNub')
        rig.set_control_color(colour)
        rig.set_control_size(self.control_size + self.controlSize)
        #if self.matchToRotation:
        rig.set_match_to_rotation(True)
        rig.set_create_sub_controls(True)
        rig.set_sub_control_shape('circleGrabber')
        rig.set_sub_control_size(self.control_size/2)
        rig.set_sub_control_color(21)
        rig.set_hide_sub_translates(False)
        rig.set_sub_visibility(True)
        rig.create()
        rig.delete_setup()

    def __cleanUp(self):

        # Re-sort controls to free up subs
        upperName = self.name.upper()
        count = 1
        for i in range(1, self.numberOfCtrls - 1):
            cmds.parent('xform_CNT_{0}_{1}_{2}'.format(upperName,  str(1 + count), self.side),
                        'CNT_{0}_{1}_{2}'.format(upperName,  str(count), self.side)
                        )
            count += 1

        # Remove unwanted extra sub
        cmds.delete('cls_'+self.name+'_*_'+self.side+'_parentConstraint1',
                    'CNT_SUB_'+upperName+'_SUB_*_'+self.side,

                    )
        # parentConst on cluster group
        for i in range(1, self.numberOfCtrls, 1):
            cmds.parentConstraint('CNT_SUB_'+upperName+'_' + str(i) + '_'+self.side,
                                  'pos_cls_'+self.name+'_' + str(i) + '_'+self.side, mo=True)

        # Clean scene
        ikGr = cmds.group(self.ikh[0], self.ikh[2], n='IKH_'+self.name+'_gr_'+self.side)
        cmds.rename(self.ikh[2], 'crv_'+self.name+'IkSpline_01_'+self.side)

        clsGr = cmds.group('pos_cls_'+self.name+'_*', n='cls_'+self.name+'_gr_'+self.side,  em=True)
        cmds.parent('pos_cls_'+self.name+'_*', clsGr)
        tailGr = cmds.group(ikGr, clsGr, n='setup_'+self.name+'_'+self.side)
        cmds.parent(tailGr, 'setup')

        # for Joint on cluster
        cmds.group(self.jntClusGrp, name='clusterJoint_{0}_gr_{1}'.format(self.name, self.side), parent=tailGr)


        # Lock rotate on mid sub cnts
        for i in range(2, self.numberOfCtrls, 1):
            for axis in ['x', 'y', 'z']:
                cmds.setAttr('CNT_SUB_{0}_{1}_{2}.r{3}'.format(upperName, str(i), self.side, axis), lock=True, k=False, cb=False)

        # scaling attrs structure to cluster grp
        # bufferClustGRP = cmds.group(n='{0}_buffer_{1}_cluster_grp'.format(self.side, self.name), em=True)
        # cmds.parent(clsGr, bufferClustGRP)
        for axis in ['x', 'y', 'z']:
            cmds.connectAttr("structure.s%s"% axis, clsGr+'.s%s'%axis)

        #cmds.hide(self.jntClusGrp)
        cmds.delete(self.jntClusGrp)

        # parent to
        if self.parentTo:
            cmds.parent('controls_' + self.name + '_1_' + self.side, self.parentTo)
            # this is to fix the odd twisting when parenting to the same shit
            jntGrp = cmds.group(self.startJointChain, p='setup',
                                name="{0}_{1}JointChain_GRP".format(self.side, self.name),
                                )
            cmds.parentConstraint(self.parentTo, jntGrp, mo = True)

            jntGrpBuff = cmds.group(jntGrp, name="{0}_Buffer_{1}JointChain_GRP".format(self.side, self.name), )

            for i in 'XYZ':
                cmds.connectAttr('CNT_GOD.globalScale', '{0}.scale{1}'.format(jntGrpBuff, i))


    def __createStretchy(self):
        # arclen        -|
        #                |->multiDiv-> multiDiv-> blendColour -> to all joints Scale or Translate
        # globalScale   -|

        # arclen/scale crv
        arcLenName = cmds.arclen(self.crvName, ch=True, name="%s_IKHandleCrvInfo" % self.side)

        multiDivCrv = cmds.shadingNode('multiplyDivide', asUtility=True,
                                          name='{0}_{1}_crvScale_multiDiv'.format(self.side, self.name)
                                       )
        cmds.setAttr('%s.operation' % multiDivCrv, 2)
        arcLenNum = cmds.getAttr('%s.arcLength' % arcLenName)

        cmds.connectAttr('%s.arcLength' % arcLenName, '%s.input1X' % multiDivCrv)
        cmds.connectAttr('CNT_GOD.globalScale', '%s.input2X' % multiDivCrv)

        # arclen/stablizing
        multiDivStable = cmds.shadingNode('multiplyDivide', asUtility=True,
                                          name='{0}_{1}_stable_multiDiv'.format(self.side, self.name)
                                          )

        cmds.setAttr('%s.operation' % multiDivStable, 2)

        ## area reserved for input2X
        # cmds.setAttr('%s.input2X' % multiDivStable, arcLenNum) #for scale
        # cmds.connectAttr('%s.arcLength' % arcLenName, '%s.input2X' % multiDivStable) # for scale replace

        cmds.connectAttr('%s.outputX' % multiDivCrv, '%s.input1X' % multiDivStable)

        # blendColour
        blendColor = cmds.shadingNode('blendColors', asUtility=True,
                                      name='{0}_{1}_blendColors'.format(self.side, self.name)
                                      )
        cmds.setAttr('%s.color2R' % blendColor, 1)
        cmds.connectAttr('%s.outputX' % multiDivStable, '%s.color1R' % blendColor)

        # create Switch
        controlOne = 'CNT_{0}_1_{1}'.format(self.name.upper(), self.side)
        cmds.addAttr(controlOne, ln="Stretchy", at='double', min=0, max=1, dv=1, keyable=True)
        cmds.connectAttr('%s.Stretchy' % controlOne, '%s.blender' % blendColor)

        # remove other strings in the jointChain List
        chainLst = cmds.listRelatives(self.startJointChain, ad=True)
        for removes in [self.lastChild, self.effector]:
            chainLst.remove(removes)
        chainLst.append(self.startJointChain)

        if self.axisDirection:
            axis = self.axisDirection.upper()
            allAxis = ['X', 'Y', 'Z']
            allAxis.remove(axis)

            if self.scaleOrTranslate == 'scale':
                # cmds.setAttr('%s.input2X' % multiDivStable, arcLenNum)                      # for scale
                cmds.connectAttr('%s.arcLength' % arcLenName, '%s.input2X' % multiDivStable)  # for scale replace
                for lst in chainLst:
                    cmds.connectAttr('%s.outputR' % blendColor, '{0}.scale{1}'.format(lst,axis))
                    # # global Switch
                    # for i in allAxis:
                    #     cmds.connectAttr('CNT_GOD.globalScale', '{0}.scale{1}'.format(lst, i))

            elif self.scaleOrTranslate == 'translate':
                # get the joint translate number on joint
                midJnt = cmds.listRelatives(self.startJointChain, ad=True)[len(self.lastChild)/2]
                transAxisNum = cmds.getAttr('{0}.t{1}'.format(midJnt, axis.lower()))
                cmds.setAttr('%s.input2X' % multiDivStable, arcLenNum / transAxisNum)

                for lst in chainLst:
                    cmds.connectAttr('%s.outputR' % blendColor, '{0}.translate{1}'.format(lst,axis))

            else:
                print ("please specify a string. 'scale' or 'translate'")

            # # global Switch
            #     for i in allAxis:
            #         cmds.connectAttr('CNT_GOD.globalScale', '{0}.scale{1}'.format(lst, i))
        else:
            print "add in one of the following axis, 'X' 'Y' 'Z', direction depends on the chain axis "

    def __create(self):
        self. __initialSetup()
        self.__createControls()
        self.__createStretchy()
        self.__cleanUp()


#DO NOT DELETE =======================================# for Limbs >.<

# def __createStrechy():
#
# name = "test"
# side = "C"
# startJointChain = "joint_belt_15_L"
#
# # create distanceLength of the chain
# lastChild = cmds.listRelatives(startJointChain, ad=True)[0]
# distBtwn = cmds.shadingNode('distanceBetween', asUtility = True, name = 'distanceBetween' + name)
# cmds.connectAttr('%s.worldMatrix' %startJointChain, '%s.inMatrix1' %distBtwn)
# cmds.connectAttr('%s.worldMatrix' %lastChild, '%s.inMatrix2' %distBtwn)
#
# # to Sum/add up all the joint TranslateX
# chainLst = cmds.listRelatives(startJointChain, ad=True)
# # remove effector1 from chainLst
# chainLst.remove('effector1')
# plusMinAvg = cmds.shadingNode('plusMinusAverage', asUtility = True, name = 'plusMinusAverage' + name)
# for leng,lst in enumerate(chainLst): #translateZ???? this can change depending on how the chain is created
#     cmds.connectAttr('%s.translateZ' %lst, '%s.input1D[%s]' %(plusMinAvg,leng))
#
# # create multiplyDivide
# multiDiv = cmds.shadingNode('multiplyDivide', asUtility = True, name = 'multiplyDivide' + name)
# cmds.setAttr('%s.operation' %multiDiv,2)
# cmds.connectAttr('%s.distance' %distBtwn, '%s.input1X' %multiDiv)
# # sum of all chains
# cmds.connectAttr('%s.output1D' %plusMinAvg, '%s.input2X' %multiDiv)
#
# # create condition

# conditions = cmds.shadingNode('condition', asUtility = True, name = 'condition' + name)
# cmds.setAttr('%s.operation' %conditions,2)
# cmds.connectAttr('%s.outputX' %multiDiv, '%s.colorIfTrueR' %conditions)
# cmds.connectAttr('%s.distance' %distBtwn, '%s.firstTerm' %conditions)
# cmds.connectAttr('%s.input2X' %multiDiv, '%s.secondTerm' %conditions)
#
# # connect condition to joint scale direction
# chainLst.remove(lastChild)
# chainLst.append(startJointChain)
# for lst in chainLst:
#     cmds.connectAttr('%s.outColorR' %conditions, '%s.scaleZ' %lst)
#
# print multiDiv
# print lst
# print chainLst
#DO NOT DELETE =======================================

import maya.cmds as cmds

# vtools
from vtool.maya_lib import rigs

#tony's tools
import VControls as vCtrls

'''

splineIK setup
Create joint chain and save it in structure

'''

class splineIK2():
    def __init__(self,
                 name='node',
                 side='C',
                 startJointChain='JNT_ribbon_14_C',
                 numberOfCtrls = 5,
                 curve = False,
                 controlSize = 1,
                 parentTo=None,
                 scaleOrTranslate = 'scale',
                 axisDirection='X',
                 rotateControl = {'z':0},
                 ):
        '''
        FUNCTION:      SplineRig.splineIK()
        DESCRIPTION:   adds a SplineRig on a joint chain, with strechky function, turn on off
        USAGE:         must create a joint chain
                       splineIK(name='node', side='C', startJointChain='JNT_ribbon_14_C',
                                numberOfCtrls = 5, controlSize = 1, parentTo=None)
        RETURN:        SplineRig
        AUTHOR:        Tony K Song
        DATE:          02/07/19
        Version        1.0.0

        EXAMPLE: prp_seatbelt in kingdomforce



        @todo
        VControl replacement
        :type rotateControl: the ordation axis and then rotation degrees    Ex.{"r":45}
        :type rotateControl: the ordation axis and then rotation degrees

        '''

        self.name=name
        self.side=side
        self.startJointChain=startJointChain
        self.parentTo=parentTo
        self.controlSize=controlSize
        self.numberOfCtrls = numberOfCtrls + 1
        self.axisDirection = axisDirection
        self.curve = curve
        self.scaleOrTranslate = scaleOrTranslate.lower()
        self.rotateControl = rotateControl

        # Var
        self.clustName = None
        self.colour = 22
        self.control_size = process.get_option('Control Size', 'Setup.Controls')
        self.ikh = None
        self.crvName = None
        self.effector = None
        self.lastChild = cmds.listRelatives(startJointChain, ad=True)[0]

        # procs
        self.__create()

    def __adjGrp(self):

        myParent = cmds.listRelatives(self.clustName, p=True)
        posGroup = cmds.group(empty=True, name="pos_" + self.clustName)
        if myParent != None: cmds.parent(posGroup, myParent)
        orient = cmds.orientConstraint(self.clustName, posGroup)
        point = cmds.pointConstraint(self.clustName, posGroup)
        cmds.delete(orient, point)
        adjGroup = cmds.group(empty=True, name="adj_" + self.clustName)
        orient = cmds.orientConstraint(self.clustName, adjGroup)
        point = cmds.pointConstraint(self.clustName, adjGroup)
        cmds.delete(orient, point)
        sdkGroup = cmds.group(empty=True, name="sdk_" + self.clustName)
        orient = cmds.orientConstraint(self.clustName, sdkGroup)
        point = cmds.pointConstraint(self.clustName, sdkGroup)
        cmds.delete(orient, point)
        cmds.parent(self.clustName, sdkGroup)
        cmds.parent(sdkGroup, adjGroup)
        cmds.parent(adjGroup, posGroup)
        cmds.select(cl=True)

    # Make spline IK
    def __initialSetup(self):
        # get last name string of the chain
        self.ikh = cmds.ikHandle(sj=self.startJointChain, ee=self.lastChild,
                                 sol='ikSplineSolver', scv=False, pcv=False,
                                 n='self.ikh_{0}Spline_01_{1}'.format(self.name, self.side))


        # Rebuild curve with desired cv count
        self.crvName = cmds.rebuildCurve(self.ikh[2], rpo=1, rt=0, end=1,
                                         kr=0, kcp=0, kep=1, kt=0,
                                         s=self.numberOfCtrls - 2, d=3, tol=0.01)
        self.effector = cmds.rename('effector1', '{0}_{1}_effector'.format(self.side, self.name))


        jntClusGrp = cmds.group(name = 'testtest',empty = True)


        # cluster setup
        bah = []
        num = 1
        numLst = ['0:1']
        numLst.extend(range(2,  self.numberOfCtrls-1))
        numLst.append('{0}:{1}'.format(str(self.numberOfCtrls - 1), str(self.numberOfCtrls)))

        for cv in numLst:
            clus = cmds.cluster('{0}.cv[{1}]'.format(self.ikh[2], str(cv)))

            # if first two points
            if cv == '0:1':
                # find the first point position on curve
                startPnt = cmds.xform(self.ikh[2] + '.cv[0]', q=True, t=True)
                # positioned the cluster to the Start point
                cmds.xform(clus, piv=(startPnt))

            # if last two points
            if cv == '{0}:{1}'.format(str(self.numberOfCtrls - 1), str(self.numberOfCtrls)):
                # find the end point position on curve
                endPnt = cmds.xform('{0}.cv[{1}]'.format(self.ikh[2], str(self.numberOfCtrls)), q=True, t=True)
                # positioned the cluster to the End point
                cmds.xform(clus, piv=(endPnt))

            self.clustName = cmds.rename(clus[1], 'cls_{0}_{1}_{2}'.format(self.name, str(num), self.side))
            self.__adjGrp()

            num += 1

            jntNames = cmds.joint(name= 'jnt_clus{0}_{1}_{2}'.format(self.name, str(num), self.side))
            break
         #   bah.append(jntNames)

        #jntClusGrp = cmds.group(bah, name = '{1}_test_{0}_gr'.format(self.name, self.side), empty = True)



        # num = 1
        # numLst = ['0']
        # numLst.extend(range(2, self.numberOfCtrls - 1))
        # numLst.append('{0}'.format(self.numberOfCtrls))
        #
        # # Create clusters
        # for cv in numLst:
        #
        #     clus = cmds.cluster('{0}.cv[{1}]'.format(self.ikh[2], cv))
        #
        #     if self.rotateControl:
        #         cmds.setAttr(clus[1]+'.r'+self.rotateControl.keys()[0], self.rotateControl.values()[0])
        #
        #     if cv == '0':
        #         cmds.sets('{0}.cv[1]'.format(self.ikh[2]), fe='{0}Set'.format(clus[0]))
        #
        #     if cv == '{0}'.format(self.numberOfCtrls):
        #         cmds.sets('{0}.cv[{1}]'.format(self.ikh[2], self.numberOfCtrls - 1), fe='{0}Set'.format(clus[0]))
        #
        #     self.clustName = cmds.rename(clus[1], 'cls_{0}_{1}_{2}'.format(self.name, str(num), self.side))
        #     self.__adjGrp()
        #
        #     num += 1


        # # Create clusters (ends get 2 points)
        # num = 1
        # numLst = ['0:1']
        # numLst.extend(range(2,  self.numberOfCtrls-1))
        # numLst.append('{0}:{1}'.format(self.numberOfCtrls - 1, self.numberOfCtrls))
        #
        # for cv in numLst:
        #
        #     clus = cmds.cluster('{0}.cv[{1}]'.format(self.ikh[2], cv))
        #     if self.rotateControl:
        #         cmds.setAttr(clus[1]+'.r'+self.rotateControl.keys()[0], self.rotateControl.values()[0])
        #
        #     # if first two points
        #     if cv == '0:1':
        #         startPnt = cmds.xform(self.ikh[2] + '.cv[0]', q=True, t=True)
        #         cmds.xform(clus, piv=(startPnt))
        #
        #     # if last two points
        #     if cv == '{0}:{1}'.format(self.numberOfCtrls - 1, self.numberOfCtrls):
        #         endPnt = cmds.xform('{0}.cv[{1}]'.format(self.ikh[2], self.numberOfCtrls), q=True, t=True)
        #         cmds.xform(clus, piv=(endPnt))
        #
        #     self.clustName = cmds.rename(clus[1], 'cls_{0}_{1}_{2}'.format(self.name, str(num), self.side))
        #
        #     jnt = cmds.joint(n='jnt_{0}_{1}_{2}'.format(self.name, str(num), self.side))
        #     parConst = cmds.parentConstraint(self.clustName, jnt)
        #     cmds.delete(parConst)
        #     parConst = cmds.parentConstraint(jnt, self.clustName, mo=True)
        #
        #     if self.rotateControl:
        #         cmds.setAttr(jnt[1]+'.r'+self.rotateControl.keys()[0], self.rotateControl.values()[0])
        #
        #
        #     self.__adjGrp()
        #
        #     num += 1

    def __createControls(self):
        # create controls
        if self.side == "C":
            colour = 22
        else:
            colour = 13 if self.side == 'R' else 6

        # Make controls
        rig = rigs.FkRig(self.name, self.side)
        posCls = []
        for ii in range(1,  self.numberOfCtrls):
            posCls.append('pos_cls_{0}_{1}_{2}'.format(self.name,str(ii),self.side))

        rig.set_joints(posCls)
        rig.set_control_shape('circleDoubleNub')
        rig.set_control_color(colour)
        rig.set_control_size(self.control_size + self.controlSize)
        rig.set_create_sub_controls(True)
        rig.set_sub_control_shape('circleGrabber')
        rig.set_sub_control_size(self.control_size/2)
        rig.set_sub_control_color(21)
        rig.set_hide_sub_translates(False)
        rig.set_sub_visibility(True)
        rig.create()
        rig.delete_setup()

    def __cleanUp(self):

        # Re-sort controls to free up subs
        upperName = self.name.upper()
        count = 1
        for i in range(1, self.numberOfCtrls - 1):
            cmds.parent('xform_CNT_{0}_{1}_{2}'.format(upperName,  str(1 + count), self.side),
                        'CNT_{0}_{1}_{2}'.format(upperName,  str(count), self.side)
                        )
            count += 1

        # Remove unwanted extra sub
        cmds.delete('pos_cls_'+self.name+'_*_'+self.side+'_parentConstraint1',
                    'CNT_SUB_'+upperName+'_SUB_*_'+self.side)
        # parentConst on cluster group
        for i in range(1, self.numberOfCtrls, 1):
            cmds.parentConstraint('CNT_SUB_'+upperName+'_' + str(i) + '_'+self.side,
                                  'pos_cls_'+self.name+'_' + str(i) + '_'+self.side, mo=True)

        # Clean scene
        ikGr = cmds.group(self.ikh[0], self.ikh[2], n='IKH_'+self.name+'_gr_'+self.side)
        cmds.rename(self.ikh[2], 'crv_'+self.name+'IkSpline_01_'+self.side)

        clsGr = cmds.group('pos_cls_'+self.name+'_*', n='cls_'+self.name+'_gr_'+self.side,  em=True)
        cmds.parent('pos_cls_'+self.name+'_*', clsGr)
        tailGr = cmds.group(ikGr, clsGr, n='setup_'+self.name+'_'+self.side)
        cmds.parent(tailGr, 'setup')

        # Lock rotate on mid sub cnts
        for i in range(2, self.numberOfCtrls, 1):
            for axis in ['x', 'y', 'z']:
                cmds.setAttr('CNT_SUB_{0}_{1}_{2}.r{3}'.format(upperName, str(i), self.side, axis), lock=True, k=False, cb=False)

        # scaling attrs structure to cluster grp
        # bufferClustGRP = cmds.group(n='{0}_buffer_{1}_cluster_grp'.format(self.side, self.name), em=True)
        # cmds.parent(clsGr, bufferClustGRP)
        for axis in ['x', 'y', 'z']:
            cmds.connectAttr("structure.s%s"% axis, clsGr+'.s%s'%axis)

        # parent to
        if self.parentTo:
            cmds.parent('controls_' + self.name + '_1_' + self.side, self.parentTo)
            # this is to fix the odd twisting when parenting to the same shit
            jntGrp = cmds.group(self.startJointChain, p='setup',
                                name="{0}_{1}JointChain_GRP".format(self.side, self.name),
                                )
            cmds.parentConstraint(self.parentTo, jntGrp, mo = True)

            jntGrpBuff = cmds.group(jntGrp, name="{0}_Buffer_{1}JointChain_GRP".format(self.side, self.name), )

            for i in 'XYZ':
                cmds.connectAttr('CNT_GOD.globalScale', '{0}.scale{1}'.format(jntGrpBuff, i))


    def __createStretchy(self):
        # arclen        -|
        #                |->multiDiv-> multiDiv-> blendColour -> to all joints Scale or Translate
        # globalScale   -|

        # arclen/scale crv
        arcLenName = cmds.arclen(self.crvName, ch=True, name="%s_IKHandleCrvInfo" % self.side)

        multiDivCrv = cmds.shadingNode('multiplyDivide', asUtility=True,
                                          name='{0}_{1}_crvScale_multiDiv'.format(self.side, self.name)
                                       )
        cmds.setAttr('%s.operation' % multiDivCrv, 2)
        arcLenNum = cmds.getAttr('%s.arcLength' % arcLenName)

        cmds.connectAttr('%s.arcLength' % arcLenName, '%s.input1X' % multiDivCrv)
        cmds.connectAttr('CNT_GOD.globalScale', '%s.input2X' % multiDivCrv)

        # arclen/stablizing
        multiDivStable = cmds.shadingNode('multiplyDivide', asUtility=True,
                                          name='{0}_{1}_stable_multiDiv'.format(self.side, self.name)
                                          )

        cmds.setAttr('%s.operation' % multiDivStable, 2)

        ## area reserved for input2X
        # cmds.setAttr('%s.input2X' % multiDivStable, arcLenNum) #for scale
        # cmds.connectAttr('%s.arcLength' % arcLenName, '%s.input2X' % multiDivStable) # for scale replace

        cmds.connectAttr('%s.outputX' % multiDivCrv, '%s.input1X' % multiDivStable)

        # blendColour
        blendColor = cmds.shadingNode('blendColors', asUtility=True,
                                      name='{0}_{1}_blendColors'.format(self.side, self.name)
                                      )
        cmds.setAttr('%s.color2R' % blendColor, 1)
        cmds.connectAttr('%s.outputX' % multiDivStable, '%s.color1R' % blendColor)

        # create Switch
        controlOne = 'CNT_{0}_1_{1}'.format(self.name.upper(), self.side)
        cmds.addAttr(controlOne, ln="Stretchy", at='double', min=0, max=1, dv=1, keyable=True)
        cmds.connectAttr('%s.Stretchy' % controlOne, '%s.blender' % blendColor)

        # remove other strings in the jointChain List
        chainLst = cmds.listRelatives(self.startJointChain, ad=True)
        for removes in [self.lastChild, self.effector]:
            chainLst.remove(removes)
        chainLst.append(self.startJointChain)

        if self.axisDirection:
            axis = self.axisDirection.upper()
            allAxis = ['X', 'Y', 'Z']
            allAxis.remove(axis)

            if self.scaleOrTranslate == 'scale':
                # cmds.setAttr('%s.input2X' % multiDivStable, arcLenNum)                      # for scale
                cmds.connectAttr('%s.arcLength' % arcLenName, '%s.input2X' % multiDivStable)  # for scale replace
                for lst in chainLst:
                    cmds.connectAttr('%s.outputR' % blendColor, '{0}.scale{1}'.format(lst,axis))
                    # # global Switch
                    # for i in allAxis:
                    #     cmds.connectAttr('CNT_GOD.globalScale', '{0}.scale{1}'.format(lst, i))

            elif self.scaleOrTranslate == 'translate':
                # get the joint translate number on joint
                midJnt = cmds.listRelatives(self.startJointChain, ad=True)[len(self.lastChild)/2]
                transAxisNum = cmds.getAttr('{0}.t{1}'.format(midJnt, axis.lower()))
                cmds.setAttr('%s.input2X' % multiDivStable, arcLenNum / transAxisNum)

                for lst in chainLst:
                    cmds.connectAttr('%s.outputR' % blendColor, '{0}.translate{1}'.format(lst,axis))

            else:
                print ("please specify a string. 'scale' or 'translate'")

            # # global Switch
            #     for i in allAxis:
            #         cmds.connectAttr('CNT_GOD.globalScale', '{0}.scale{1}'.format(lst, i))
        else:
            print "add in one of the following axis, 'X' 'Y' 'Z', direction depends on the chain axis "

    def __create(self):
        self. __initialSetup()
        self.__createControls()
        self.__createStretchy()
        self.__cleanUp()