import maya.cmds as cmds
import pymel.core as pm
import logging

# Create a logger
_logger = logging.getLogger(__name__)


from see import see


class controlCurves():
    def __init__(self,
                 name='ACME',
                 side='C',
                 shape='acme',
                 scale=1,
                 joints=['C_object01_JNT', 'C_object2_JNT'],
                 maintainTransform=True,
                 maintainRotation=True,
                 orientation=[0, 0, 0],
                 adjGrpNumber=3,


                 # ControlChain = False
                 # subControl=False,
                 # subScale = 0.8,
                 # subRotatePos=[0, 0, 0],
                 # subAdjGrpNumber=2,
                 ):
        '''
        FUNCTION:      ControlCurves.controlCurves()
        DESCRIPTION:   Creates Control Curves for animation
        USAGE:
                       CC.controlCurves(name='ACME', side='C', shape='acme', joints=['joint1'], scale = 3,
t        RETURN:        ControlsCruves
        AUTHOR:        Tony K Song
        DATE:          02/07/21
        Version        beta 1.0.0

        RULES:
        when creating Cruve in maya curveShape1 is always named in crvShape, we haev to manually rename it
        how to rename   :   cmds.rename('curveShape1', self.fullName + _crvShape')
                            cmds.rename(crvName | curveShape1, self.fullName + _crvShape')

        == Naming Conventions ==

        SIDE
        Center  : C
        left    : L
        Right   : R

        Control Name Example
        Side_Discription01_TYPE                 :   C_object01_CNT
        Side_Discription01_Discription02_TYPE   :   C_Objects01_adj01_GRP

        GROUP           : GRP
        Controls        : CNT
        Adjustment Group: adj01_GRP
        Constraint      : CONST

        '''

        self.name = name
        self.side = side
        self.shape = shape
        self.scale = scale
        self.jointList = joints
        self.maintainTransform = maintainTransform
        self.maintainRotation = maintainRotation
        self.orientation = orientation
        self.adjGrpNumber = adjGrpNumber

        # TODO Create SubControls
        # self.subControl = subControl
        # self.subScale = subScale
        # self.subRotatePos = subRotatePos
        # self.subAdjGrpNumber = subAdjGrpNumber

        # Var
        self.fullName = side + '_' + name

        self.controlNames = None
        self.grpLst = []
        self.counts = 0
        self.controlAndGrpLstNames = []
        self.crvShapeNames = []
        self.trans = cmds.xform(self.joints, q=1, ws=1, rp=1)
        self.rot = cmds.xform(self.joints, q=1, ws=1, ro=1)

        # procs
        self.__create()

    def __initialSetup(self):
        for i in self.jointList:
            self.joint = i
            self.counts +=1
            if not cmds.objExists(self.fullName + ):
                self.__createControl()
            else:
                logging.warning("same name exists.")
    # End of __initialSetup

    def __createControl(self):
        if self.shape == 'acme':  # Done
            self.acmeControl()
        # elif self.shape == 'pyramid':  # Done
        #     self.pyramidControl()
        # elif self.shape == 'cube':  # Done
        #     self.cubeControl()
        # elif self.shape == 'god':  # Done
        #     self.godControl()
        # elif self.shape == 'square':  # Done
        #     self.squareControl()
        # elif self.shape == 'arrowoutward':  # Done
        #     self.arrowoutwardControl()
        # elif self.shape == 'pinsquare':  # Done
        #     self.pinsquareControl()
        # elif self.shape == 'arrow':  #
        #     self.arrowControl()
        else:
            logging.warning(" wrong shape string. please chose one of the following in shapes: /n "
                            " acme | pyramid | cube | god | square | arrowoutward | pinsquare | arrow")

    # ================================ CONTROL LIBRARY ================================
    def acmeControl(self):
        """ACME usually for things to put any attrs or pramas on over all rig """
        starcurve = pm.curve(name='Test1',
                             r=False, d=1,  # k = True, a = True,
                             p=[
                               (-2.2107888630062657e-16, 0.0, -0.9956507899629861),
                               (-0.24952876335791113, 0.0, -0.2792005778709363),
                               (-0.9706272589838668, 0.0, -0.23240215451241358),
                               (-0.29665382659753176, 0.0, 0.08216864315416685),
                               (-0.6115845176017596, 0.0, 0.7854009785356567),
                               (7.138106503438919e-17, 0.0, 0.3214717378901843),
                               (0.61158451760176, 0.0, 0.7854009785356565),
                               (0.29665382659753176, 0.0, 0.0821686431541667),
                               (0.9706272589838668, 0.0, -0.23240215451241403),
                               (0.24952876335791102, 0.0, -0.2792005778709364),
                               (-2.2107888630062657e-16, 0.0, -0.9956507899629861),
                           ])

        circleCurve = pm.circle(n= name+'01'+"circle", nr=[0,180,0], ch = 0)[0]

        starcurve.getShape()
        circleCurve.getShape()

        pm.group(em=True, n='AMCE')
        test = cmds.parent(starcurve.getShape(),circleCurve.getShape(), self.controlNames, s=True, r=True)

    # print(see(starcurve.getShape.getName()))
    # testwhole = pm.parent(starcurve.getShapes(), circlecurve.getShapes(), s=True, r=True)


# print(see(starcurve))
