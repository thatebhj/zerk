# This file is placed in the Public Domain.


import unittest


from zerk.message import Message


class TestEvent(unittest.TestCase):

    def testconstructor(self):
        evt = Message()
        self.assertEqual(type(evt), Message)
