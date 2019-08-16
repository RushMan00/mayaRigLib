import maya.cmds as mc

def renamer(prefix = "prefix_",
            suffix = "_jnt"
            ):
    '''
    FUNCTION:      renamer
    DESCRIPTION:   The script will list of object selected in order, rename the object with the new name + 2 digit numbers
    USAGE:         select all the
    RETURN:        rename nodes
    AUTHOR:        Tony K Song
    DATE:          02/08/19
    Version        1.0.0

    @todo
    make UI with pyside2 for maya 2018+
    add few more options for flexibility
    '''

    # Rename selected objects with specified string

    selected_objects = mc.ls(selection=True, long=True)
    selected_objects.reverse()
    totalObjects = len(selected_objects)

    # We are doing this in reverse, last object renamed first

    for number, object in enumerate(selected_objects):
        print 'Old Name:', object
        # print 'New Name:', '%s%02d' % (prefix, totalObjects-number)
        # mc.rename(object, ('%s%02d' % (prefix, totalObjects-number)))
        print 'New Name:', '%s%01d' % (prefix, totalObjects-number)
        mc.rename(object, ('%s%01d' % (prefix, totalObjects-number)))

    # Add user specifid suffix to selected objects

    selected_objects = mc.ls(selection=True, long=True)
    selected_objects_short = mc.ls(selection=True, long=False)

    selected_objects.reverse()
    selected_objects_short.reverse()
    totalObjects = len(selected_objects)

    # We are doing this in reverse, last object get suffix added first

    for number, object in enumerate(selected_objects):
        print 'Old Name:', object
        print 'New Name:', selected_objects_short[number]+suffix
        mc.rename(object, selected_objects_short[number]+suffix)


