# This file is placed in the Public Domain.


import queue
import textwrap
import threading


from ..objects import Object
from ..threads import launch


def __dir__():
    return (
            'Output',
            'mre'
           )


__all__ = __dir__()


class TextWrap(textwrap.TextWrapper):

    def __init__(self):
        super().__init__()
        self.break_long_words = False
        self.drop_whitespace = True
        self.fix_sentence_endings = True
        self.replace_whitespace = True
        self.tabsize = 4
        self.width = 450


class Output(Object):

    cache = Object()

    def __init__(self):
        Object.__init__(self)
        self.oqueue = queue.Queue()
        self.dostop = threading.Event()

    def dosay(self, channel, txt):
        raise NotImplementedError

    def extend(self, channel, txtlist):
        if channel not in self.cache:
            setattr(self.cache, channel, [])
        cache = getattr(self.cache, channel, None)
        cache.extend(txtlist)

    def gettxt(self, channel):
        txt = None
        try:
            cache = getattr(self.cache, channel, None)
            txt = cache.pop(0)
        except (KeyError, IndexError):
            pass
        return txt

    def oput(self, channel, txt):
        if channel not in self.cache:
            setattr(self.cache, channel, [])
        self.oqueue.put_nowait((channel, txt))

    def output(self):
        while not self.dostop.is_set():
            (channel, txt) = self.oqueue.get()
            if channel is None and txt is None:
                break
            if self.dostop.is_set():
                break
            wrapper = TextWrap()
            try:
                txtlist = wrapper.wrap(txt)
            except AttributeError:
                continue
            if len(txtlist) > 3:
                self.extend(channel, txtlist)
                self.dosay(channel, '%s put in cache, use !mre to show more' % len(txtlist))
                continue
            _nr = -1
            for txt in txtlist:
                _nr += 1
                self.dosay(channel, txt)

    def size(self, chan):
        if chan in self.cache:
            return len(getattr(self.cache, chan, []))
        return 0

    def start(self):
        self.dostop.clear()
        launch(self.output)
        return self

    def stop(self):
        self.dostop.set()
        self.oqueue.put_nowait((None, None))


def mre(event):
    if not event.channel:
        event.reply('channel is not set.')
        return
    bot = event.bot()
    if 'cache' not in dir(bot):
        event.reply('bot is missing cache')
        return
    if event.channel not in bot.cache:
        event.reply('no output in %s cache.' % event.channel)
        return
    for _x in range(3):
        txt = bot.gettxt(event.channel)
        if txt:
            bot.say(event.channel, txt)
    size = bot.size(event.channel)
    event.reply('%s more in cach' % size)
