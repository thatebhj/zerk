# This file is placed in the Public Domain.


import threading
import time


from ..objects import Object, name, update
from ..utility import elapsed


def __dir__():
    return (
            'thr',
           )


__all__ = __dir__()



starttime = time.time()


def thr(event):
    result = []
    for thread in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thread).startswith('<_'):
            continue
        obj = Object()
        update(obj, vars(thread))
        if getattr(obj, 'sleep', None):
            uptime = obj.sleep - int(time.time() - obj.state.latest)
        else:
            uptime = int(time.time() - starttime)
        result.append((uptime, thread.name))
    res = []
    for uptime, txt in sorted(result, key=lambda x: x[0]):
        res.append('%s/%s' % (txt, elapsed(uptime)))
    if res:
        event.reply(' '.join(res))
    else:
        event.reply('no threads running')
