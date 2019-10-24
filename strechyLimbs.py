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

