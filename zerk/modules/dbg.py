# This file is placed in the Public Domain.


def __dir__():
    return (
            'dbg',
           )


def dbg(event):
    raise Exception("debug!")
