#! python

__version__     = '0.1'
__authot__      = 'forgacs.daniel@gmail.com'


"""
links selected nodes multi value parameters
use carefully, it links range parameters too
"""


import hou


def get_selection():
    return hou.selectedNodes()


def get_parm_list(node):
    parmTuples = []

    for parms in node.parmTuples():
        if len(parms) > 1:
            parmTuples.append(parms)

    return parmTuples


def main():
    print '\n' + ('='*25)
    selection = get_selection()

    for node in selection:
        for parms in get_parm_list(node):
            for id in range(parms.__len__() - 1):
                print parms.__getitem__(id + 1).path()

                expression = 'ch("%s")' % parms.__getitem__(0).name()
                parms.__getitem__(id + 1).setExpression(expression)
