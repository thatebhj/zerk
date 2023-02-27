# This file is placed in the Public Domain.


from .objects import Object


def __dir__():
    return (
            'Default',
           ) 


__all__ = __dir__()


class Default(Object):

    __slots__ = ('__default__',)

    def __init__(self, *args, **kwargs):
        Object.__init__(self, *args, **kwargs)
        self.__default__ = ''

    def __getattr__(self, key):
        return self.__dict__.get(key, self.__default__)
