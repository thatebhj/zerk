# This file is placed in the Public Domain.


import time


from ..handler import Handler
from ..storage import Storage
from ..utility import elapsed, fntime
from ..objects import Object


class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ''


Storage.add(Todo)


def dne(event):
    if not event.args:
        return
    selector = {'txt': event.args[0]}
    for fnm, o in Storage.find('todo', selector):
        o.__deleted__ = True
        Storage.save(o, fnm)
        event.reply('ok')
        break


def tdo(event):
    if not event.rest:
        nr = 0
        for _fn, o in Storage.find('todo'):
            event.reply('%s %s %s' % (nr, o.txt, elapsed(time.time()-fntime(_fn))))
            nr += 1
        if not nr:
            event.reply('no todo entered yet.')
        return
    o = Todo()
    o.txt = event.rest
    Storage.save(o)
    event.reply('ok')
