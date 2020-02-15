# -*- coding: utf-8 -*-
__author__ = 'james'

import unittest
import time
import logging
from tinylimit import AntiLimit

@AntiLimit(2, 1)
def Add(a, b):
    return a + b

class Foo():
    def __init__(self, a):
        self.a = a

    @AntiLimit(2, 1)
    def Bar(self, b):
        return self.a - b

class Test_TinyLimit(unittest.TestCase):
    def test_AntiLimitInFun(self):
        for i in range(10):
            s = Add(1, 2)
            self.assertEqual(s, 3)
            time.sleep(0.3)

    def test_AntiLimitInMethod(self):
        for i in range(10):
            s = Foo(3).Bar(1)
            self.assertEqual(s, 2)
            time.sleep(0.3)

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    unittest.main()
