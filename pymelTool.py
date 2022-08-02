"""
This is a pratice for me
"""
import pymel.core as pm
import logging

def copyAttrs(translation=True,
              rotation = True,
              scale = True
              ):
    """
    To get transform, rotation, scale Xform(matrix) printed out
    first selected object as the point reference
    The second selected + other selected after
    will be placposition
    """

    # example for pymel

    if not pm.ls(sl=True)[0]:
        logging.warning('no objects are selected, must select more than one object')
    # if not pm.ls(sl=True)[0:1]:

    item = pm.ls(sl=True)[0]
    stuffA = pm.PyNode(pm.ls(sl=True)[0])
    item == stuffA # is True

    # Get position
    firstElements = pm.ls(sl=True)[0]
    trans = firstElements.getTranslation()
    rotations = firstElements.getRotation()
    scales = firstElements.getScale()

    # set position
    otherElements = pm.ls(sl=True)[1:]
    for oe in otherElements:
        if translation:
            oe.setTranslation(trans)
        if rotation:
            oe.setRotation(rotations)
        if scale:
            oe.setScale(scales)

    logging.info('all object translation position is now at %s' %trans)
    logging.info('all object rotations position is now at %s' %rotations)
    logging.info('all object scale position is now at %s' %scales)
