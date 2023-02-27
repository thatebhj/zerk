# This file is placed in the Public Domain.


from ..listens import Listens


def __dir__():
    return (
            'cmd',
           )


__all__ = __dir__()


def cmd(event):
    bot = Listens.byorig(event.orig)
    event.reply(','.join(sorted(bot.cmds)))
