# This file is placed in the Public Domain.


import unittest


from zerk.handler import Handler
from zerk.listens import Listens


class Client(Handler):

    gotcha = False

    def announce(self, txt):
        Client.gotcha = True

    def raw(self, txt):
        Client.gotcha = True

class TestListens(unittest.TestCase):

    def test_construct(self):
        bus = Listens()
        self.assertEqual(type(bus), Listens)

    def test_add(self):
        bus = Listens()
        clt = Client()
        bus.add(clt)
        self.assertTrue(clt in bus.objs)

    def test_announce(self):
        bus = Listens()
        clt = Client()
        bus.add(clt)
        bus.announce("test")
        self.assertTrue(Client.gotcha)

    def test_byorig(self):
        clt = Client()
        self.assertEqual(Listens.byorig(repr(clt)), clt)

    def test_say(self):
        bus = Listens()
        clt = Client()
        bus.add(clt)
        bus.say(repr(clt), "#test", "test")
        self.assertTrue(Client.gotcha)
