from vtool.maya_lib import attr
from vtool.maya_lib import deform

# IBRigLib
import VControls

reload(VControls)


def latticeRig(name='lattice',
               side='C',
               geo=['geo'],
               divisions=(3, 3, 3),
               falloff=(2, 2, 2),
               flatten=None,
               controlSize=1,
               controlShape='sphere',
               controlColour=16,
               parentTo='CNT_SUB_GOD_2_C'
               ):
    # setup
    latRigGrp = None
    if not cmds.objExists('latticeRig_gr'):
        latRigGrp = cmds.group(name='latticeRig_gr', p='setup', em=True)

    # create lattice
    cmds.select(geo)
    latticeNode = cmds.lattice(name=name,
                               dv=divisions,
                               ldv=falloff,
                               oc=True)

    # if cmds.objExists('lat_{0}_1_{1}'.format(name, side)):
    latGrp = cmds.group(latticeNode, name='lat_%s_1_gr' % name)
    cmds.parent(latGrp, latRigGrp)

    # adding control to cluster
    latClsGrp = cmds.group(name='latCls_%s_1_gr' % name, p=latRigGrp, em=True)

    if flatten == str():
        flatten = flatten.lower()
        if flatten == 'x':
            for div1 in range(divisions[1]):
                for div2 in range(divisions[2]):
                    cls = \
                    cmds.cluster('{0}Lattice.pt[{1}][{2}][0:{3}]'.format(name, divisions[0], div1, div2), name=name)[
                        1]
                    cmds.parent(cls, latClsGrp)
        elif flatten == 'y':
            for div1 in range(divisions[0]):
                for div2 in range(divisions[2]):
                    cls = \
                    cmds.cluster('{0}Lattice.pt[0:{1}][{2}][{3}]'.format(name, div0, divisions[1], div2), name=name)[
                        1]
                    cmds.parent(cls, latClsGrp)
        elif flatten == 'z':
            for div0 in range(divisions[0]):
                for div1 in range(divisions[1]):
                    cls = \
                    cmds.cluster('{0}Lattice.pt[{1}][{2}][0:{3}]'.format(name, div0, div1, divisions[2]), name=name)[
                        1]
                    cmds.parent(cls, latClsGrp)

    elif flatten == None:
        for div0 in range(divisions[0]):
            for div1 in range(divisions[1]):
                for div2 in range(divisions[2]):
                    cls = cmds.cluster('{0}Lattice.pt[{1}][{2}][{3}]'.format(name, div0, div1, div2), name=name)[1]
                    cmds.parent(cls, latClsGrp)
    else:
        print "please specify a axis as string - 'x' or 'y' or 'z'"

    # createing control with cluster
    for guides in cmds.listRelatives(latClsGrp):
        VControls.vControls(name=name,
                            side=side,
                            guides=guides,
                            controlShape=controlShape,
                            controlSize=controlSize,
                            controlColour=controlColour,
                            parentTo=parentTo
                            )
        cmds.parentConstraint(parentTo, name + 'Base', mo=True)
        cmds.scaleConstraint(parentTo, name + 'Base', mo=True)


def main():
    latticeRig(name='boxPart',
               side='C',
               geo=['g_juiceBox'],
               divisions=(3, 3, 3),
               falloff=(2, 2, 2),
               flatten=None,
               controlSize=.1,
               controlShape='sphere',
               controlColour=16,
               parentTo='CNT_JUICEBOX_1_C'
               )
