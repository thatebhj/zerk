# This file is placed in the Public Domain.


import datetime
import os
import types
import uuid
import _thread


from functools import wraps


def __dir__():
    return (
            'Object',
            'format',
            'get',
            'items',
            'keys',
            'kind',
            'name',
            'oid',
            'register',
            'search',
            'update',
            'values'
            )


__all__ = __dir__()


olock = _thread.allocate_lock()


def locked(lock):

    def lockeddec(func, *args, **kwargs):

        @wraps(func)
        def lockedfunc(*args, **kwargs):
            lock.acquire()
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                lock.release()
            return res

        return lockedfunc

    return lockeddec



class Object:

    def __init__(self, *args, **kwargs):
        if args:
            val = args[0]
            if isinstance(val, list):
                update(self, dict(val))
            elif isinstance(val, zip):
                update(self, dict(val))
            elif isinstance(val, dict):
                update(self, val)
            elif isinstance(val, Object):
                update(self, vars(val))
        if kwargs:
            self.__dict__.update(kwargs)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)



def format(obj, args='', skip='', plain=False):
    res = []
    keyz = []
    if ',' in args:
        keyz = args.split(',')
    if not keyz:
        keyz = keys(obj)
    for key in sorted(keyz):
        if key.startswith('_'):
            continue
        if skip:
            skips = skip.split(',')
            if key in skips:
                continue
        value = getattr(obj, key, None)
        if not value:
            continue
        if ' object at ' in str(value):
            continue
        txt = ''
        if plain:
            value = str(value)
        if isinstance(value, str) and len(value.split()) >= 2:
            txt = f'{key}="{value}"'
        else:
            txt = f'{key}={value}'
        res.append(txt)
    txt = ' '.join(res)
    return txt.strip()


def get(obj, key, default=None):
    return getattr(obj, key, default)


def items(obj):
    if isinstance(obj, type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj):
    return obj.__dict__.keys()


def kind(obj):
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == 'type':
        kin = obj.__name__
    return kin


def name(obj):
    typ = type(obj)
    if isinstance(typ, types.ModuleType):
        return obj.__name__
    if '__self__' in dir(obj):
        return '%s.%s' % (obj.__self__.__class__.__name__, obj.__name__)
    if '__class__' in dir(obj) and '__name__' in dir(obj):
        return '%s.%s' % (obj.__class__.__name__, obj.__name__)
    if '__class__' in dir(obj):
        return obj.__class__.__name__
    if '__name__' in dir(obj):
        return '%s.%s' % (obj.__class__.__name__, obj.__name__)
    return None


def oid(obj):
    return os.path.join(
                        kind(obj),
                        str(uuid.uuid4().hex),
                        os.sep.join(str(datetime.datetime.now()).split()),
                       )


def register(obj, key, value) -> None:
    setattr(obj, key, value)


def search(obj, selector):
    res = False
    select = Object(selector)
    for key, value in items(select):
        try:
            val = getattr(obj, key)
        except AttributeError:
            continue
        if str(value) in str(val):
            res = True
            break
    return res


def update(obj, data):
    for key, value in items(data):
        setattr(obj, key, value)


def values(obj):
    return obj.__dict__.values()
