"""
"""


import unittest
import hou
import bakeparm



class BakeParmTests(unittest.TestCase):
    def setUp(self):
        hou.hipFile.clear(suppress_save_prompt=True)
        self.geo = hou.node('/obj').createNode('geo', 'TEST_geo')

    def tearDown(self):
        self.geo.destroy()

    def test_get_frame_range_returns_tuple(self):
        self.assertTrue(type(bakeparm.get_frame_range()) is tuple)

    def test_get_frame_range_returns_full_frame_range(self):
        start = int(hou.expandString('$FSTART'))
        end = int(hou.expandString('$FEND'))

        self.assertEqual(bakeparm.get_frame_range(), (start, end))

    def test_get_values_returns_parm_values_on_frame_range(self):
        parm = self.geo.parm('rx')
        parm.setExpression('$F4')

        parmvalues = bakeparm.get_values(1, 10, parm)

        self.assertEqual(parmvalues, list(range(1, 10)))

    def test_get_values_returns_parm_values_on_frame_range_2(self):
        parm = self.geo.parm('rx')
        parm.setExpression('$F4 * 2')

        parmvalues = bakeparm.get_values(1, 10, parm)

        self.assertNotEqual(parmvalues, list(range(1, 10)))#

    def test_bake_values_sets_right_values(self):
        parm = self.geo.parm('rx')
        values = [1.0, 3.0, 5.0, 3.0, 7.0, 5.0, 9.0, 1.0]

        for k, frame in enumerate(values):
            bakeparm.bake_values(1, len(values) + 1, parm, values)

        for i in range(len(values) + 1):
            hou.setFrame(i)
            self.assertAlmostEqual(values[i-1], parm.eval())



def main():
    print('\n'*5)
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(BakeParmTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
