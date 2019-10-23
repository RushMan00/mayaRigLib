
print '===== Copy ====='
for i in range(0,41):
    foo =  cmds.pointPosition('curve1.cv[{0}]'.format(i))
    print str(tuple(foo))+ ','
print '===== End ====='

# pyramid
cmds.curve(name='pyramid', r=False, d=1,  # k = True, a = True,
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
# cube
cmds.curve(name = 'cube', r=False, d = 1,# k = True, a = True,
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

# square
cmds.curve(name = 'square', r=False, d = 1,# k = True, a = True,
           p=[
            (0.5, 1.1102230246251565e-16, -0.5),
            (0.5, -1.1102230246251565e-16, 0.5),
            (-0.5, -1.1102230246251565e-16, 0.5),
            (-0.5, 1.1102230246251565e-16, -0.5),
            (0.5, 1.1102230246251565e-16, -0.5),
           ])

# arrowoutward
cmds.curve(name = 'arrowoutward', r=False, d = 1,# k = True, a = True,
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

# pin square
cmds.curve(name = 'pinsquare', r=False, d = 1,# k = True, a = True,
               p=[
                (0.0, 0.0, 0.0),
                (-1.0, 0.0, 0.0),
                (-1.0, 0.0, -2.0),
                (1.0, 0.0, -2.0),
                (1.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 4.0),
               ])

# arrow
cmds.curve(name = 'arrow', r=False, d = 1,# k = True, a = True,
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

# triangle
cmds.curve(name = 'triangle', r=False, d = 1,# k = True, a = True,
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

# star
cmds.curve(name = 'star', r=False, d = 1,# k = True, a = True,
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


def acmeControl(name='C_acme_CNT'):
    # create curves
    star = cmds.curve(name='star_crv', r=False, d=1,  # k = True, a = True,
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

    cmds.rename('curveShape1', 'star_crvShape')
    circlen = cmds.CreateNURBSCircle()
    cmds.rename('nurbsCircleShape1', 'circle_crvShape')
    # create groups
    names = cmds.group(em=True, n=name)
    # combining Shapes
    cmds.parent('circle_crvShape', 'star_crvShape', names, s=True, r=True)
    # cleanup
    cmds.delete(circlen, star)
    cmds.delete('nurbsCircle1')

# gear
gear = cmds.curve(name='gear', r=False, d=1,  # k = True, a = True,
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
