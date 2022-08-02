# create arm with locators calv, humerous, radious, wrist - manual
import maya.cmds as cmds

# arg
side = "L"
armLocators = ['arm0', 'arm1', 'arm2', 'arm3']

controlSwitch = 'C_'

# Var
boneNames = ['clavicle', 'humerus', 'radius', 'wrist']
jnts = ['C_arm01_JNT', 'C_arm02_JNT', 'C_arm03_JNT']
controlSwitchName = 'switch'
jntNames = []
jntSize = 5

# crate jnts on the locators
for b, l in zip(boneNames, armLocators):
    trans = cmds.xform(l, q=1, ws=1, rp=1)
    jnt = cmds.joint(n=side + "_" + b + "_" + "JNT", radius=5)
    jntNames.append(jnt)
    cmds.setAttr(jnt + '.t', trans[0], trans[1], trans[2])
    cmds.select(d=True)
print jntNames

# parent JNTS
cmds.parent(side + '_wrist_JNT', side + '_radius_JNT')
cmds.parent(side + '_radius_JNT', side + '_humerus_JNT')
cmds.parent(side + '_humerus_JNT', side + '_clavicle_JNT')

# ordient JNTS on 'clavicle', 'humerus', 'radius', 'wrist'
cmds.select(side + '_clavicle_JNT', side + '_humerus_JNT', side + '_radius_JNT')
# if R change oj
cmds.joint(e=True, oj='yzx', sao='zup', ch=True, zso=True)
cmds.joint(side + '_wrist_JNT', e=True, oj='none', ch=True, zso=True)

# create IK and FK chain
newNames = ['humerus', 'radius', 'wrist']
for i in ['IK', 'FK']:
    copyNames = cmds.duplicate(side + '_humerus_JNT', rc=True)
    for cn, nn in zip(copyNames, newNames):
        cmds.rename(cn, side + '_' + nn + i + '_JNT')

# parent const IK and FK joints
nn = newNames[:-1]
for i in nn:
    cmds.parentConstraint(side + '_' + i + 'FK_JNT', side + '_' + i + 'IK_JNT', side + '_' + i + '_JNT')

# create controls for FK
controlFKList = []
controlFKoffsetList = []

controlsize = 5
for i in newNames:
    fkn = side + '_' + i + 'FK_JNT'
    trans = cmds.xform(fkn, q=1, ws=1, rp=1)
    rot = cmds.xform(fkn, q=1, ws=1, ro=1)

    # creating curves and groups
    c = cmds.circle(n=side + '_' + i + 'FK_CNT', nr=(0, 1, 0), c=(0, 0, 0))[0]
    controlFKList.append(c)
    print c
    # creating curves and groups
    g = cmds.group(n=side + '_' + i + 'FK_offset')
    controlFKoffsetList.append(g)

    cmds.setAttr(c + '.r', rot[0], rot[1], rot[2])
    cmds.setAttr(c + '.t', trans[0], trans[1], trans[2])
    cmds.setAttr(c + '.s', controlsize, controlsize, controlsize)
    print c
    cmds.makeIdentity(c, apply=True, t=1, r=1, s=1, n=0, pn=1)  # freeze transforms
    cmds.delete(c, constructionHistory=True)  # delete history

    cmds.parentConstraint(c, side + '_' + i + 'FK_JNT', mo=True)

# parent FK controls
print controlFKoffsetList
print controlFKList

del controlFKList[-1]
del controlFKoffsetList[0]
for cnt, grp in zip(controlFKList, controlFKoffsetList):
    cmds.parent(grp, cnt)

cmds.
# create IK control for the arm (wrist area)
# create IK control for the elbow (ebow area but -away on Z)
