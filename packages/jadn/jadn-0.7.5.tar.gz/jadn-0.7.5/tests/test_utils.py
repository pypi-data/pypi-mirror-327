"""
Test JADN Codec
"""
import copy
import os
import random
import unittest
import jadn


class Order(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(jadn.data_dir(), 'jadn_v2.0_schema.jadn')) as fp:
            self.schema1 = jadn.load(fp)
        jadn.check(self.schema1)
        self.schema2 = copy.deepcopy(self.schema1)
        random.shuffle(self.schema2['types'])
        self.deps1 = jadn.build_deps(self.schema1)
        self.deps2 = jadn.build_deps(self.schema2)

    def test_adjacency(self):
        """
        Same dependencies for different input orders
        """
        self.assertEqual(self.deps1, self.deps2)
        self.assertNotEqual(list(self.deps1), list(self.deps2))

    def test_sort(self):
        """
        Sort returns fixed order with different inputs
        """
        roots1 = (i := self.schema1['meta']).get('roots', '')     # exports is deprecated
        roots2 = (i := self.schema2['meta']).get('roots', '')
        names1 = jadn.utils.topo_sort(self.deps1, roots1)
        names2 = jadn.utils.topo_sort(self.deps2, roots2)
        self.assertEqual(names1, names2)


if __name__ == '__main__':
    unittest.main()
