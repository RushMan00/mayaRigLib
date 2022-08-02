'''
usage
      relative_position = worldPos('pSphere1') * worldMatrix('pCube1').inverse()
      print relative_position
      # (0.756766, -0.0498943, 3.38499, 1)
'''
def worldMatrix(self, obj):
    """'
    convenience method to get the world matrix of <obj> as a matrix object
    """
    return MMatrix(cmds.xform(obj, q=True, matrix=True, ws=True))

def worldPos(self, obj):
    """'
    convenience method to get the world position of <obj> as an MPoint
    """
    return MPoint(cmds.xform(obj, q=True, t=True, ws=True))
