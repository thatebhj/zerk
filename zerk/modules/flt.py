# This file is placed in the Public Domain.


from ..handler import Listens
from ..objects import name


def __dir__():
    return (
            'flt',
           )


__all__ = __dir__()


def flt(event):
    try:
        index = int(event.args[0])
        event.reply(Listens.objs[index])
        return
    except (KeyError, TypeError, IndexError, ValueError):
        pass
    event.reply(' | '.join([name(o) for o in Listens.objs]))
