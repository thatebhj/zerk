# This file is placed in the Public Domain.


from .handler import Handler


class CLI(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.orig = repr(self)

    def annnouce(self, txt):
        self.raw(txt)

    def raw(self, txt):
        print(txt)

    def say(self, channel, txt):
        self.raw(txt)


class Console(CLI):

    def handle(self, event):
        CLI.handle(self, event)
        event.wait()

    def poll(self):
        event = Message()
        event.txt = input("> ")
        event.orig = repr(self)
        return event
