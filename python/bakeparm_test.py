"""
"""


import unittest
# import sys
# import os


# modulepath = os.path.dirname(__file__)
# # houpath = 'C:/Apps/HOUDIN~1.313/houdini/python2.7libs\hou.pyc'
# houpath = 'c:/Apps/HOUDIN~1.313/houdini/python2.7libs'
# sys.path.insert(0, houpath)

# if modulepath not in sys.path:
#     sys.path.insert(0, modulepath)


# import hou
# # import bakeparm
# # from bakeparm import bake_parm



class BakeParmTests(unittest.TestCase):
    def setUp(self):
        geo = hou.node('/obj').createNode('geo')

    def tearDown(self):
        pass


def main():
    pass
