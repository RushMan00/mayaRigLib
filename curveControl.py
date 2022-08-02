from maya.api.OpenMaya import MVector, MMatrix, MPoint
import maya.cmds as cmds

'''
Creates Control Curves for rigging and animation
'''

class controlCurves():
    def __init__(self,
                 name='ACME',
                 side='C',
                 shape='acme',
                 scale=1,
                 joints=['C_string01_JNT'],
                 maintainTransform=True,
                 maintainRotation=True,
                 orientation=[0, 0, 0],
                 adjGrpNumber=3,

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
            if not cmds.objExists(self.fullName + _):
                self.__createControl()
            else:
                print("Warning: same name exists.")

    # End of __initialSetup

    def __createControl(self):
        if self.shape == 'acme':  # Done
            self.acmeControl()
        elif self.shape == 'pyramid':  # Done
            self.pyramidControl()
        elif self.shape == 'cube':  # Done
            self.cubeControl()
        elif self.shape == 'god':  # Done
            self.godControl()
        elif self.shape == 'square':  # Done
            self.squareControl()
        elif self.shape == 'arrowoutward':  # Done
            self.arrowoutwardControl()
        elif self.shape == 'pinsquare':  # Done
            self.pinsquareControl()
        elif self.shape == 'arrow':  #
            self.arrowControl()
        else:
            print("Warning: wrong shape string. please chose one of the following in shapes: /n "
                  "acme | pyramid | cube | god | square | arrowoutward | pinsquare | arrow")


    ### --- CONTROL LIBRARY
    # ==========================================================
    ### --- ACME CONTROL
    # curveGrp = []
    def acmeControl(self):
        curveGrp = []
        starcurve = cmds.curve(name=self.fullName+"_star%02d" % (self.counts,)+'_CNT', r=False, d=1,  # k = True, a = True,
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
        curveGrp.append(starcurve)
        # store shape names in self.crvShapeNames

        rm = cmds.rename('curveShape1', self.fullName + '%02d' % (self.counts,)+'_star_crvShape')
        self.crvShapeNames.append(rm)
        # create circle curves
        circlecurve = cmds.CreateNURBSCircle(name=self.fullName+"_circle%02d" % (self.counts,)+'_CNT')
        curveGrp.append(circlecurve)
        # store shape names in self.crvShapeNames
        rm = cmds.rename('nurbsCircleShape1', self.fullName + '%02d' % (self.counts,) +'_circle_crvShape'.format())
        self.crvShapeNames.append(rm)
        # create groups
        self.controlNames = cmds.group(em=True, n=self.fullName + "%02d" % (self.counts,) + '_CNT')
        # combining Shapes
        test = cmds.parent(self.crvShapeNames[0], self.crvShapeNames[1], self.controlNames, s=True, r=True)
        # cleanup
        cmds.delete(starcurve, 'nurbsCircle1') # delete groups
        cmds.delete(self.controlNames, constructionHistory=True) # delete history

    # END of acmeControl
    # ==========================================================
    ### --- GOD CONTROL
    def godControl(self):
        curveGrp = []
        # create arrow curves
        arrowCrvName = cmds.curve(name=self.fullName+"_GodArrow%02d" % (self.counts,)+'_CNT', r=False, d=1,  # k = True, a = True,
                          p=[
                              (-0.24976468221459797, 0.0, -0.9990587288583922),
                              (-0.24976468221459788, 0.0, -1.4985880932875884),
                              (-0.49952936442919593, 0.0, -1.4985880932875884),
                              (2.1411146302991436e-16, 0.0, -1.9981174577167844),
                              (0.49952936442919627, 0.0, -1.4985880932875884),
                              (0.24976468221459822, 0.0, -1.4985880932875884),
                              (0.24976468221459813, 0.0, -0.9990587288583922),
                          ])
        # print (arrowCrvName)
        curveGrp.append(arrowCrvName)
        # store godArrow_crvShape01
        arrowShapeName = cmds.rename('curveShape1', self.fullName+"_GodArrow%02d" % (self.counts,)+'_crvShape')
        self.crvShapeNames.append(arrowShapeName)

        # create quarter of a circle
        circleCrvName = cmds.curve(name=self.fullName+"_GodCircle%02d" % (self.counts,)+'_CNT' , r=False, d=1,  # k = True, a = True,
                              p=[
                                  (-0.24976468221459794, 0.0, -0.9990587288583922),
                                  (-0.2965919365798677, 0.0, -0.9923691210919251),
                                  (-0.38934121742579897, 0.0, -0.9714072366081247),
                                  (-0.5214958437504207, 0.0, -0.9181227244860435),
                                  (-0.6434452788151456, 0.0, -0.8443475612891649),
                                  (-0.7519928599396136, 0.0, -0.7519928599396138),
                                  (-0.8443475612891649, 0.0, -0.6434452788151456),
                                  (-0.9181227244860434, 0.0, -0.5214958437504208),
                                  (-0.9714072366081238, 0.0, -0.38934121742579925),
                                  (-0.9923691210919247, 0.0, -0.296591936579868),
                                  (-0.9990587288583918, 0.0, -0.24976468221459822),
                              ])
        curveGrp.append(circleCrvName)
        #store shape
        circleShapeName = cmds.rename('curveShape1', self.fullName+"_GodCircle%02d" % (self.counts,)+'_crvShape')
        self.crvShapeNames.append(circleShapeName)

        # creating other shapes and placing them and rotating them 90 deg
        rotateTo = 90
        for i in range(1, 4):
            # duplicate arrow
            arrowDupName = cmds.duplicate(arrowCrvName, n=self.fullName+"_GodArrow%02d" % (1+i,)+'_CNT')
            curveGrp.append(arrowDupName[0])
            print(arrowDupName)

            arrowDupShapeName = cmds.rename(arrowDupName[0]+'|'+self.fullName+"_GodArrow%02d" % (1,)+'_crvShape',
                                            self.fullName + "_GodArrow%02d" % (1+i,) + '_crvShape')
            self.crvShapeNames.append(arrowDupShapeName)
            # rotate the arrow
            cmds.setAttr(arrowDupName[0] + '.ry', rotateTo)
            #do the same fot the circle part

            # duplicate  quarter of a circle
            CircleDupName= cmds.duplicate(circleCrvName, n=self.fullName+"_GodCircle%02d" % (1+i,)+'_CNT')
            curveGrp.append(CircleDupName[0])
            CircleDupShapeName = cmds.rename(CircleDupName[0]+'|'+self.fullName+"_GodCircle%02d" % (1,)+'_crvShape',
                                             self.fullName+"_GodCircle%02d" % (1+i,)+'_crvShape')
            self.crvShapeNames.append(CircleDupShapeName)
            # rotate the arrow
            cmds.setAttr(CircleDupName[0] + '.ry', rotateTo)

            # clear history
            for stuff in [arrowDupName, CircleDupName]:
                cmds.makeIdentity(stuff, apply=True, translate=True, rotate=True, scale=True)
            rotateTo += 90

        # combining Shapes
        self.controlNames = cmds.group(em=True, n='C_GOD_CNT')
        for shapeList in self.crvShapeNames:
            cmds.parent(shapeList, self.controlNames, s=True, r=True)
        # clean up
        cmds.delete(curveGrp)

    # END OF GODCONTROL

    # ==========================================================
    ### --- Pyramid CONTROL
    def pyramidControl(self):
        self.controlNames = cmds.curve(name=self.fullName+ "%02d" % (1,) + '_CNT', r=False, d=1,  # k = True, a = True,
                                       p=[(-0.7071066498756409, -0.5400000214576721, -0.70710688829422),
                                          (-0.7071068286895752, -0.5400000214576721, 0.7071067094802856),
                                          (0.0, 0.5400000214576721, 0.0),
                                          (-0.7071066498756409, -0.5400000214576721, -0.70710688829422),
                                          (0.7071067690849304, -0.5400000214576721, -0.7071067690849304),
                                          (0.0, 0.5400000214576721, 0.0),
                                          (0.7071067094802856, -0.5400000214576721, 0.7071068286895752),
                                          (0.7071067690849304, -0.5400000214576721, -0.7071067690849304),
                                          (0.0, 0.5400000214576721, 0.0),
                                          (-0.7071068286895752, -0.5400000214576721, 0.7071067094802856),
                                          (0.7071067094802856, -0.5400000214576721, 0.7071068286895752),
                                          ])
        # rename CurveShape and store name
        rm = cmds.rename('curveShape1', self.fullName + 'Pyramid_crvShape')
        self.crvShapeNames.append(rm)

    # END of pyramidControl
    # ==========================================================

    ### --- CUBE CONTROL
    def cubeControl(self):
        self.controlNames = cmds.curve(name=self.fullName, r=False, d=1,  # k = True, a = True,
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
        # rename CurveShape and store name
        rm = cmds.rename('curveShape1', self.fullName + 'Cube_crvShape')
        self.crvShapeNames.append(rm)
        # End of cubeControl

    # ==========================================================

    # --- SQUARE CONTROL
    def squareControl(self):
        self.controlNames = cmds.curve(name=self.fullName, r=False, d=1,  # k = True, a = True,
                   p=[
                       (0.5, 1.1102230246251565e-16, -0.5),
                       (0.5, -1.1102230246251565e-16, 0.5),
                       (-0.5, -1.1102230246251565e-16, 0.5),
                       (-0.5, 1.1102230246251565e-16, -0.5),
                       (0.5, 1.1102230246251565e-16, -0.5),
                   ])

    # END OF squareControl
    # ==========================================================

    # --- arrowoutward Control
    def arrowoutwardControl(self):
        self.controlNames = cmds.curve(name=self.fullName, r=False, d=1,  # k = True, a = True,
                   p=[
                       (-0.5934552956583314, 0.0, 0.5934552956583314),
                       (-0.19781843188611073, 0.0, 0.5934552956583314),
                       (-0.19781843188611073, 0.0, 1.1869105913166629),
                       (-0.5934552956583314, 0.0, 1.1869105913166629),
                       (0.0, 0.0, 1.9781843188611032),
                       (0.5934552956583314, 0.0, 1.1869105913166629),
                       (0.19781843188611073, 0.0, 1.1869105913166629),
                       (0.19781843188611073, 0.0, 0.5934552956583314),
                       (0.5934552956583314, 0.0, 0.5934552956583314),
                       (0.5934552956583314, 0.0, 0.19781843188611073),
                       (1.1869105913166629, 0.0, 0.19781843188611073),
                       (1.1869105913166629, 0.0, 0.5934552956583314),
                       (1.9781843188611032, 0.0, 0.0),
                       (1.1869105913166629, 0.0, -0.5934552956583314),
                       (1.1869105913166629, 0.0, -0.19781843188611073),
                       (0.5934552956583314, 0.0, -0.19781843188611073),
                       (0.5934552956583314, 0.0, -0.5934552956583314),
                       (0.19781843188611073, 0.0, -0.5934552956583314),
                       (0.19781843188611073, 0.0, -1.1869105913166629),
                       (0.5934552956583314, 0.0, -1.1869105913166629),
                       (0.0, 0.0, -1.9781843188611032),
                       (-0.5934552956583314, 0.0, -1.1869105913166629),
                       (-0.19781843188611073, 0.0, -1.1869105913166629),
                       (-0.19781843188611073, 0.0, -0.5934552956583314),
                       (-0.5934552956583314, 0.0, -0.5934552956583314),
                       (-0.5934552956583314, 0.0, -0.19781843188611073),
                       (-1.1869105913166629, 0.0, -0.19781843188611073),
                       (-1.1869105913166629, 0.0, -0.5934552956583314),
                       (-1.9781843188611032, 0.0, 0.0),
                       (-1.1869105913166629, 0.0, 0.5934552956583314),
                       (-1.1869105913166629, 0.0, 0.19781843188611073),
                       (-0.5934552956583314, 0.0, 0.19781843188611073),
                       (-0.5934552956583314, 0.0, 0.5934552956583314),
                   ])

    # END OF arrowoutward Control
    # ==========================================================
    ### pinsquare Control ###
    def pinsquareControl(self):
        self.controlNames = cmds.curve(name=self.fullName, r=False, d=1,  # k = True, a = True,
                   p=[
                       (0.0, 0.0, 0.0),
                       (-1.0, 0.0, 0.0),
                       (-1.0, 0.0, -2.0),
                       (1.0, 0.0, -2.0),
                       (1.0, 0.0, 0.0),
                       (0.0, 0.0, 0.0),
                       (0.0, 0.0, 4.0),
                   ])

    # END OF pinsquareControl
    # ==========================================================
    ### arrow Control ###
    def arrowControl(self):
        self.controlNames = cmds.curve(name=self.fullName, r=False, d=1,  # k = True, a = True,
                   p=[
                       (-0.328797177570344, 0.0, 1.315188710281376),
                       (0.328797177570344, 0.0, 1.315188710281376),
                       (0.328797177570344, 0.0, 0.0),
                       (0.986391532711032, 0.0, 0.0),
                       (0.0, 0.0, -0.986391532711032),
                       (-0.986391532711032, 0.0, 0.0),
                       (-0.328797177570344, 0.0, 0.0),
                       (-0.328797177570344, 0.0, 1.315188710281376),
                   ])

    # End of arrowControl
    # ==========================================================
    ### triangle Control ###
    def triangleControl(self):
        self.controlNames = cmds.curve(name=self.fullName, r=False, d=1,  # k = True, a = True,
                   p=[
                       (-0.328797177570344, 0.0, 1.315188710281376),
                       (0.328797177570344, 0.0, 1.315188710281376),
                       (0.328797177570344, 0.0, 0.0),
                       (0.986391532711032, 0.0, 0.0),
                       (0.0, 0.0, -0.986391532711032),
                       (-0.986391532711032, 0.0, 0.0),
                       (-0.328797177570344, 0.0, 0.0),
                       (-0.328797177570344, 0.0, 1.315188710281376),
                   ])

    # End of triangleControl
    # ==========================================================
    ### star Control ###
    def starControl(self):
        self.controlNames = cmds.curve(name=self.fullName, r=False, d=1,  # k = True, a = True,
                   p=[
                       (-0.9956507899629861, 0.0, 0.0),
                       (-0.27920057787093633, 0.0, 0.24952876335791108),
                       (-0.2324021545124138, 0.0, 0.9706272589838668),
                       (0.08216864315416678, 0.0, 0.29665382659753176),
                       (0.7854009785356566, 0.0, 0.6115845176017598),
                       (0.3214717378901843, 0.0, 0.0),
                       (0.7854009785356566, 0.0, -0.6115845176017598),
                       (0.08216864315416678, 0.0, -0.29665382659753176),
                       (-0.2324021545124138, 0.0, -0.9706272589838668),
                       (-0.27920057787093633, 0.0, -0.24952876335791108),
                       (-0.9956507899629861, 0.0, 0.0),
                   ])

    # End of starControl
    # ==========================================================
    ### gear Control  ###
    def gearControl(self):
        self.controlNames = cmds.curve(name=self.fullName, r=False, d=1,  # k = True, a = True,
                          p=[
                              (-0.02792703607711131, 0.0, -1.009885145746707),
                              (-1.9841134706071526e-08, 0.0, -0.8335609259098924),
                              (0.25758447114099936, 0.0, -0.7927635909956867),
                              (0.3386317963304868, 0.0, -0.9518280094926724),
                              (0.5710021397035888, 0.0, -0.8334294618410324),
                              (0.48995483935614026, 0.0, -0.6743650433440476),
                              (0.6743650434252879, 0.0, -0.48995488895897676),
                              (0.8334294122381959, 0.0, -0.571002238990503),
                              (0.9518280592579903, 0.0, -0.3386318956174008),
                              (0.7927636407610049, 0.0, -0.2575845455858748),
                              (0.8335604788344357, 0.0, -2.9761702059107213e-08),
                              (1.0098846986712504, 0.0, 0.027926970948000354),
                              (0.9690874134411226, 0.0, 0.2855113346146863),
                              (0.7927631439202305, 0.0, 0.2575843370102385),
                              (0.674364596268591, 0.0, 0.4899545810151854),
                              (0.8005987700864327, 0.0, 0.6161887548330273),
                              (0.6161887647535942, 0.0, 0.8005988595340201),
                              (0.4899545412516753, 0.0, 0.6743646360321011),
                              (0.25758432208876714, 0.0, 0.7927631836837407),
                              (0.28551134453525356, 0.0, 0.9690874035205551),
                              (0.0279269870790774, 0.0, 1.0098847881188378),
                              (-4.468317341724894e-08, 0.0, 0.8335605682820233),
                              (-0.2575844362971526, 0.0, 0.7927632333678183),
                              (-0.3386317863286785, 0.0, 0.951827651864803),
                              (-0.5710020303336264, 0.0, 0.8334290545290864),
                              (-0.48995468030209977, 0.0, 0.6743646857161786),
                              (-0.6743647850030926, 0.0, 0.4899546306992629),
                              (-0.8334291538160007, 0.0, 0.571001980730789),
                              (-0.9518277014676398, 0.0, 0.3386317615678806),
                              (-0.7927633823388097, 0.0, 0.2575843866943159),
                              (-0.833560717253015, 0.0, -2.9761702059107213e-08),
                              (-1.0098849370898295, 0.0, -0.027927024260894807),
                              (-0.9690875524915468, 0.0, -0.28551144382216753),
                              (-0.7927633823388097, 0.0, -0.25758444621772),
                              (-0.67436483468717, 0.0, -0.4899547399067444),
                              (-0.800599107873167, 0.0, -0.6161889137245863),
                              (-0.6161890031721738, 0.0, -0.8005990681096566),
                              (-0.4899547796702548, 0.0, -0.6743648942918147),
                              (-0.25758451082326855, 0.0, -0.7927635413116094),
                              (-0.28551153326975515, 0.0, -0.9690877611484243),
                              (-0.02792703607711131, 0.0, -1.009885145746707),
                          ])

    # End of gearControl

    # ==========================================================
    # End of Control Lib

    def __controlAdj(self):

        print (self.crvShapeNames)

        # --- self.orientation
        for i in self.crvShapeNames:
            num = cmds.getAttr(i + '.spans')
            cmds.rotate(self.orientation[0], self.orientation[1], self.orientation[2], i + '.cv[0:%s]' % num)

        # --- set all translate and rotation
        cmds.setAttr(self.controlNames + '.t', self.trans[0], self.trans[1], self.trans[2])
        cmds.setAttr(self.controlNames + '.r', self.rot[0], self.rot[1], self.rot[2])

        # --- scale
        if self.scale:
            """
            to scale curve with out effecting int of scale
            how it works: grab all the verties and scaling it togetehr 
            ex. scale xyz will always be 1
            """
            # print self.crvShapeNames
            for i in self.crvShapeNames:
                spans = cmds.getAttr(i + '.spans')
                foo = cmds.ls(i + '.cv[0:%s]' % spans, fl=True)
                cmds.scale(self.scale, self.scale, self.scale, foo, a=True, ws=True)
                # if self.rotatePos:
                #     cmds.rotate(self.rotatePos[0], self.rotatePos[1], self.rotatePos[2], foo, r=True, fo=True)

        # --- creating groups
        self.controlAndGrpLstNames.append(self.controlNames)
        grpLst = []
        grpLst.append(self.controlNames)
        if self.adjGrpNumber:
            for i in range(self.adjGrpNumber):
                trans = cmds.xform(self.joints, q=1, ws=1, rp=1)
                words = cmds.group(n=self.side + '_' + self.name + '{0:02}_adj{1:02}_GRP'.format(self.counts,i), em=True)
                cmds.setAttr(words + '.t', self.trans[0], self.trans[1], self.trans[2])
                cmds.setAttr(words + '.r', self.rot[0], self.rot[1], self.rot[2])
                grpLst.append(words)
                self.controlAndGrpLstNames.append(words)
            # go though the self.grplst parent ladder
            for i in range(self.adjGrpNumber):
                cmds.parent(grpLst[0], grpLst[1])
                grpLst.pop(0)

        # --- Constraints
        for jnt in self.joints:
            if self.maintainTransform and self.maintainRotation:
                bah = cmds.parentConstraint(self.controlAndGrpLstNames[0], self.joints, mo=False,
                                            n=self.fullName+'Const')
            elif self.maintainTransform is True and self.maintainRotation is False:
                bah = cmds.parentConstraint(self.controlAndGrpLstNames[0], self.joints, mo=False,
                                            skipRotate=['x', 'y', 'z'], n=self.fullName+'TransConst')
            elif self.maintainTransform is False and self.maintainRotation is True:
                bah = cmds.parentConstraint(self.controlAndGrpLstNames[0], self.joints, mo=False,
                                            skipTranslate=['x', 'y', 'z'], n=self.fullName+'RotConst')

    # def __createSubControls(self):
    #     self.subfullName = self.side + '_sub_' + self.name + '_CNT'
    #     self.scale = self.subScale
    #     self.subControlColor = self.subControlColor
    #     self.rotatePos = self.subRotatePos
    #     self.adjGrpNumber = self.subAdjGrpNumber
    #
    #     if self.subControl:
    #         print self.crvShapeNames
    #         for i in self.crvShapeNames:
    #             spans = cmds.getAttr(i + '.spans')
    #             foo = cmds.ls(i + '.cv[0:%s]' % spans, fl=True)
    #             cmds.scale(self.subScale, self.subScale, self.subScale, foo, a=True, ws=True)
    #             if self.subRotatePos:
    #                 cmds.rotate(self.subRotatePos[0], self.subRotatePos[1], self.subRotatePos[2], foo, r=True, fo=True)
    #
    #     #creating groups
    #     grpLst = []
    #     grpLst.append(self.subfullName)
    #     if self.subAdjGrpNumber:
    #         for i in range(self.subAdjGrpNumber):
    #             words = cmds.group(n=self.side + '_subAdj' + self.fullName + "%02d" % (i,) + '_CNT', em=True)
    #             grpLst.append(words)
    #             self.controlAndGrpLstNames.append(words)
    #         #go though the self.grplst parent ladder
    #         for i in range(self.subAdjGrpNumber):
    #             cmds.parent(grpLst[0],grpLst[1])
    #             grpLst.pop(0)

    # # final cleanup and addition
    # cmds.parentConstraint(self.controlAndGrpLstNames[0], self.joints, mo=True)

    # def __cleanUp(self)
    #     # maintainTransform
    #     if self.maintainTransform:
    #         bah = cmds.parentConstraint(self.joints, self.controlAndGrpLstNames[-1], mo=False,
    #                                     skipRotate=['x','y','z'])
    #     # rotatePos
    #     if self.rotatePos:
    #         bah = cmds.parentConstraint(self.joints, self.controlAndGrpLstNames[-1], mo=False,
    #                                     skipTranslate=['x', 'y', 'z'])
    #         cmds.delete(bah)
    #
    #     # final cleanup and addition
    #     cmds.parentConstraint(self.controlAndGrpLstNames[0], self.joints, mo=True)

    # Exacute process
    def __create(self):
        # Step 1
        self.__initialSetup()
        self.__controlAdj()
        # if self.subControl:
        #     self.__createSubControls()

################# TOOLS #################

# def scaleCurve(controlCurve = 'curve1',
#                scale = 3):
#     """
#     to scale curve with out effecting int of scale
#     ex. scale xyz will always be 1
#     """
#     spans = cmds.getAttr( controlCurve+'.spans' )
#     foo = cmds.ls('curve1.cv[0:%s]'%spans, fl = True)
#     cmds.scale( scale,scale,scale, foo ,a = True, ws = True)
#
# scaleCurve(controlCurve = 'curve1',
#            scale = 3)


# When you create a shape manullly for curve controls
# this will spit out a list where the point are located in worldspace
# use cmds.curves and place the printed list in to the function

# def printVertPos(node=cmds.ls(sl=True)[0]):
#     print '===== Copy ====='
#     spans = mc.getAttr(node + '.spans')
#     nbr = cmds.ls('curve1.cv[0:%s]' %spans, fl=True)
#     print nbr
#     for i in nbr:
#         foo = cmds.pointPosition(i)
#         print str(tuple(foo)) + ','
#     print '===== End ====='

# ==========================================================
