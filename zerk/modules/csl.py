# This file is placed in the Public Domain.


from zerk.command import CLI
from zerk.message import Message
from zerk.utility import wait


import zerk.modules


def __dir__():
    return (
            "Console",
            "csl"
           ) 


__all__ = __dir__()


class Console(CLI):

    def handle(self, event):
        CLI.handle(self, event)
        event.wait()

    def poll(self):
        event = Message()
        event.txt = input("> ")
        event.orig = repr(self)
        return event


def csl(event):
    console = Console()
    console.scandir(zerk.modules.__path__[0])
    console.start()
    wait()