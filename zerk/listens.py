# This file is placed in the Public Domain.


from .objects import Object


def __dir__():
    return (
            'Listens',
           ) 


class Listens(Object):

    objs = []

    @staticmethod
    def add(obj):
        if repr(obj) not in [repr(x) for x in Listens.objs]:
            Listens.objs.append(obj)

    @staticmethod
    def announce(txt):
        for obj in Listens.objs:
            obj.announce(txt)

    @staticmethod
    def byorig(orig):
        res = None
        for obj in Listens.objs:
            if repr(obj) == orig:
                res = obj
                break
        return res

    @staticmethod
    def say(orig, txt, channel=None):
        bot = Listens.byorig(orig)
        if bot:
            if channel:
                bot.say(channel, txt)
            else:
                bot.raw(txt)
