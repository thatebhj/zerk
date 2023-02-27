# This file is placed in the Public Domain.


import os
import _thread


from .decoder import load
from .encoder import dump
from .objects import Object, items, kind, oid, search, update
from .utility import cdir, fnclass, fntime, locked


def __dir__():
    return (
            'Storage',
           )


__all__ = __dir__()


class NoClass(Exception):

    pass


hooklock = _thread.allocate_lock()


class Storage:

    cls = Object()
    workdir = ''

    @staticmethod
    def add(clz):
        setattr(Storage.cls, '%s.%s' % (clz.__module__, clz.__name__), clz)

    @staticmethod
    def files(oname=None):
        res = []
        path = Storage.path('')
        if not os.path.exists(path):
            return res
        for fnm in os.listdir(path):
            if oname and oname.lower() not in fnm.split('.')[-1].lower():
                continue
            if fnm not in res:
                res.append(fnm)
        return res

    @staticmethod
    def find(otp, selector=None):
        if selector is None:
            selector = {}
        if '.' in otp:
            tps = [otp]
        else:
            tps = Storage.types(otp)
        for typ in tps:
            for fnm in Storage.fns(typ):
                obj = Storage.hook(fnm)
                if '__deleted__' in obj and obj.__deleted__:
                    continue
                if selector and not search(obj, selector):
                    continue
                yield fnm, obj

    @staticmethod
    def fns(otp):
        assert Storage.workdir
        path = Storage.path(otp)
        dname = ''
        for rootdir, dirs, _files in os.walk(path, topdown=False):
            if dirs:
                dname = sorted(dirs)[-1]
                if dname.count('-') == 2:
                    ddd = os.path.join(rootdir, dname)
                    fls = sorted(os.listdir(ddd))
                    if fls:
                        path2 = os.path.join(ddd, fls[-1])
                        yield path2

    @staticmethod
    @locked(hooklock)
    def hook(otp):
        fqn = fnclass(otp)
        cls = getattr(Storage.cls, fqn, None)
        if not cls:
            raise NoClass(fqn)
        obj = cls()
        with open(otp, 'r', encoding='utf-8') as ofile:
            dct = load(ofile)
            update(obj, dct)
        return obj

    @staticmethod
    def last(obj, selector=None):
        if selector is None:
            selector = {}
        result = sorted(Storage.find(kind(obj), selector), key=lambda x: fntime(x[0]))
        if result:
            _fn, ooo = result[-1]
            if ooo:
                update(obj, ooo)

    @staticmethod
    def path(path=''):
        return os.path.join(Storage.workdir, 'store', path)

    @staticmethod
    def save(obj, opath=None):
        if not opath:
            opath = Storage.path(oid(obj))
        cdir(opath)
        with open(opath, 'w', encoding='utf-8') as ofile:
            dump(obj, ofile)
        return os.path.abspath(opath)

    @staticmethod
    def types(oname=None):
        for name, _typ in items(Storage.cls):
            if oname and oname in name.split('.')[-1].lower():
                yield name

    @staticmethod
    def strip(path):
        return path.split('store')[-1][1:]


Storage.add(Object)
