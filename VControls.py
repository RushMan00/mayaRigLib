from vtool.maya_lib import rigs
from vtool.maya_lib import attr
import maya.cmds as cmds


class vControls():
    def __init__(self,
                 name='Demo',
                 side='C',
                 geo=None,
                 guides='Joint',
                 controlShape='outwardCirclePointer',
                 subControlShape=None,
                 subControls=False,
                 matchToRotation=False,
                 controlSize=5,
                 controlColour=None,
                 #setBuffer=True,
                 addScaleAttr=True,
                 constraint=False,
                 parentTo=None,
                 ):

        self.name = name
        self.side = side
        self.geo = geo
        self.guides = guides
        self.controlShape = controlShape
        self.subControls = subControls
        self.controlSize = controlSize
        self.controlColour = controlColour
        self.parentTo = parentTo
        self.matchToRotation = matchToRotation
        self.subControlShape = subControlShape
        self.constraint = constraint
        self.addScaleAttr = addScaleAttr
        #self.setBuffer = setBuffer

        # Var
        self.rig = None
        self.controlList = []
        self.control_size = process.get_option('Control Size', 'Setup.Controls')

        # procs
        self.__create()

        '''
        Create a Full Control setup on a Joint or guide locators using vtool.maya_lib 

        -=Functions=-
        
        @type  name: moduleName control
        
        :param name: string [REQUIRED]

        @type  side: side of Control
        :param side: 'L', 'R', 'C' [REQUIRED]

        @type geo: name of geo, you can use this to parentConstraint
                   if not using skin weights.
        :param geo: string [optional]

        @type  guides: to parentConstraint guides under Control
        :param guides: 'string' or ['list'] [REQUIRED]

        @type  controlShape: string name of the shape
        :param controlShape: 'string' [REQUIRED]

        @type  controlSize: int of control size
        :param controlSize: int [REQUIRED]

         @type  parent: int of control size
        :param parent: string

        :return: Fully builds a control on a guides
        
        @TODO: to continue building the script overtime and make it in to a class
                -make different colour controls for back and front functions?
                -allow user to make a chain of FKrig with method
                -mirror joint function (might need to make adding tag module)
                 Mirror = True
                -add all scale fuction to each controls and connect them to guides 
        '''

    # main vetala
    def __vetalaSetup(self):
        # initial setup Vetala API
        self.rig = rigs.FkRig(self.name, self.side)
        self.rig.set_joints(self.guides)
        self.rig.set_control_shape(self.controlShape)
        self.rig.set_control_size(self.controlSize)
        self.rig.set_match_to_rotation(self.matchToRotation)
        #self.rig.set_buffer(self.setBuffer)
        # subcontrols
        if self.subControls:
            self.rig.set_create_sub_controls(True)
            self.rig.set_hide_sub_translates(False)
            self.rig.set_sub_control_size(self.control_size / 2)
            if self.subControlShape:
                self.rig.set_sub_control_shape(self.subControlShape)
            else:
                self.rig.set_sub_control_shape(self.controlShape)

            self.rig.set_sub_control_color(20)
            self.rig.set_sub_visibility(True)

        self.__colourChoices()

    def __addingStuff(self):
        # parenting geo under Controls

        if self.geo:
            countDown = 0
            for controlLists in self.controlList:
                for geos in self.geo:
                    cmds.parentConstraint(controlLists, geos, mo=True, weight=1)
                # countDown += 1

        # parenting build controls under other controls
        if self.parentTo:
            if self.constraint:
                cmds.parentConstraint(self.rig, self.parentTo, mo=True, weight=1)
            else:
                self.rig.set_control_parent(self.parentTo)

    def __cleanUp(self):
        # self.rig.set_buffer(self.setBuffer)
        # deletes empty group created as byproduct of Tool
        self.rig.delete_setup()



    def __colourChoices(self):
        # sides
        if self.controlColour:
            self.rig.set_control_color(self.controlColour)  # yellow

        elif not self.controlColour:
            if self.side in 'C':
                self.rig.set_control_color(17)  # yellow

            elif self.side in 'L':
                self.rig.set_control_color(6)  # red

            elif self.side in 'R':
                self.rig.set_control_color(13)  # blue

            # Figure this out later
            # elif self.side in 'F':
            #     self.rig.set_control_color(23)  #
            #
            # elif self.side in 'B':
            #     self.rig.set_control_color(8)  #

        else:
            print "nothin"

        # Create
        self.rig.create()
        self.controlList.append(cmds.ls(sl=True)[0])

    def __create(self):

        self.__vetalaSetup()
        self.__addingStuff()
        self.__cleanUp()


