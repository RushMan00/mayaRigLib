from vtool.maya_lib import attr

# IBRigLib
import VControls
reload(VControls)

#################################################################
def createACME(name='ACME',
               moveTY=20,
               controlColour=17,
               controlSize=6,
               parentTo='CNT_SUB_GOD_2_C',
               ):
    '''


    :param name:
    :param moveTY:
    :param controlColour:
    :param controlSize:
    :param parentTo:
    :return:
    '''


    locName = cmds.spaceLocator(name='loc_' + name)[0]
    cmds.parent(locName, 'guide')
    cmds.setAttr(locName + '.ty', moveTY)
    cmds.setAttr(locName + '.rx', 90)
    # ACME
    VControls.vControls(name='ACME',
                        side='C',
                        guides='loc_ACME',
                        controlShape='star',
                        parentTo=parentTo,
                        matchToRotation=True,
                        controlColour=controlColour,
                        controlSize=controlSize,
                        )
    # locking Attr
    attr.lock_attributes('CNT_' + name.upper() + '_1_C',
                         bool_value=True,
                         attributes=['tx', 'ty', 'tz',
                                     'ry', 'rz', 'rx'],
                         hide=True)

    # lockHide
    cmds.setAttr("CNT_ACME_1_C.ro", l=True, k=False, cb=False)

#################################################################

# Toggle between
def addVisToggle(addAttrTo='CNT_ACME_1_C',
                 attrName="caveWallMiddle",
                 enum={'whole': ['vis_caveWall_whole_cn_gr'],  'broken': ['vis_caveWall_broken_cn_gr']}
                 ):
    # to create 'string':'string':'string':'string':etc
    strList = []
    for i in range(len(enum)):
        strList.append(enum.keys()[i])
        strList.append(":")
    en = ''.join(strList)
    en = en[:-1]

    # add Attr
    cmds.addAttr(addAttrTo, ln=attrName, at='enum', k=True, en=en)

    # create em
    for iterNum in range(len(enum)):
        enum1 = cmds.shadingNode('condition', asUtility=True, name="{0}_condition_NODE".format(enum.keys()[iterNum]))
        # set attrs on condition
        cmds.setAttr("%s.operation" % enum1, 1)
        cmds.setAttr("%s.secondTerm" % enum1, iterNum)
        # IO on condition Node
        cmds.connectAttr('{0}.{1}'.format(addAttrTo, attrName), '%s.firstTerm' % enum1)
        print enum.values()[iterNum]
        for i in enum.values()[iterNum]:
            cmds.connectAttr('%s.outColorR' % enum1, '%s.v' % i)

#################################################################
def addScale(controlName='CNT_NAME_1_C', geo=['crystal_1_gr']):
    cmds.addAttr(controlName, ln="Scale", at="double", dv=1, k=True)
    for ax in 'xyz':
        cmds.setAttr(controlName + '.s{0}'.format(ax), l=False)
        cmds.connectAttr(controlName + '.Scale', '{0}.s{1}'.format(controlName, ax))
        for i in geo:
            cmds.connectAttr(controlName + '.Scale', '{0}.s{1}'.format(i, ax))
        cmds.setAttr(controlName + '.s{0}'.format(ax), l=True)

#################################################################
def DrivenKey(driver='node.attr',
              driven='node.tx',
              startDriverValue=0,
              endDriverValue=10,
              startDrivenValue=0,
              endDrivenValue=90):
    cmds.setDrivenKeyframe(driven, cd=driver, dv=startDriverValue, v=startDrivenValue)
    cmds.setDrivenKeyframe(driven, cd=driver, dv=endDriverValue, v=endDrivenValue)

#################################################################
# create ACME
createACME(name='ACME',
           moveTY=100,
           controlColour=20,
           controlSize=10,
           parentTo='CNT_SUB_GOD_2_C')
# Adding Attrs
cmds.addAttr('CNT_ACME_1_C', ln="VisToggle", at="bool",
             dv=1, k=True, min=0.0, max=1)

# line break
name = 'test'
cmds.addAttr('CNT_ACME_1_C', ln=name, at="enum", en="----:----:", k=True)
cmds.setAttr('CNT_ACME_1_C.' + name, lock=True)

cmds.addAttr('CNT_ACME_1_C', ln="pram", at="double",
             dv=0, k=True, min=0.0, max=10)

# add Scale
addScale(controlName='CNT_PLATE_3_C', geo=['pie_gr'])

# locking Attrs
for num in range(1,29):
    for axis in ['tx', 'tz', 'rx', 'rz', 'ry']:
        cmds.setAttr('CNT_KEY_{0}_C.{1}'.format(num,axis), k =False, cb = False, l = True)

# unlocking Attrs
cmds.setAttr('CNT_FLOATING_ICE_{0}_C.s{1}'.format(num, ax), k =True, cb = False, l = False)

# set Driven keys
cmds.addAttr('CNT_ACME_1_C', ln="MiddleDoor", at="double", dv=0, k=True, min=0.0, max=10)
DrivenKey(driver='CNT_ACME_1_C.MiddleDoor',
          driven='driver_CNT_DOOR_MID_TOP_1_C.ty',
          startDriverValue=0,
          endDriverValue=10,
          startDrivenValue=0,
          endDrivenValue=55)
DrivenKey(driver='CNT_ACME_1_C.MiddleDoor',
          driven='driver_CNT_DOOR_MID_BOT_1_C.ty',
          startDriverValue=0,
          endDriverValue=10,
          startDrivenValue=0,
          endDrivenValue=-65)