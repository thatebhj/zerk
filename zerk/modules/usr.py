# This file is placed in the Public Domain.


import time


from ..objects import Object, update
from ..storage import Storage
from ..utility import elapsed, fntime


def __dir__():
    return (
            'NoUser',
            'User',
            'Users',
            'dlt',
            'met'
           )


__all__ = __dir__()


class NoUser(Exception):

    pass


class User(Object):

    def __init__(self, val=None):
        Object.__init__(self)
        self.user = ''
        self.perms = []
        if val:
            update(self, val)


Storage.add(User)


class Users(Object):

    @staticmethod
    def allowed(origin, perm):
        perm = perm.upper()
        user = Users.get_user(origin)
        val = False
        if user and perm in user.perms:
            val = True
        return val

    @staticmethod
    def delete(origin, perm):
        res = False
        for user in Users.get_users(origin):
            try:
                user.perms.remove(perm)
                Storage.save(user)
                res = True
            except ValueError:
                pass
        return res

    @staticmethod
    def get_users(origin=''):
        selector = {'user': origin}
        return Storage.find('user', selector)

    @staticmethod
    def get_user(origin):
        users = list(Users.get_users(origin))
        res = None
        if len(users) > 0:
            res = users[-1]
        return res

    @staticmethod
    def perm(origin, permission):
        user = Users.get_user(origin)
        if not user:
            raise NoUser(origin)
        if permission.upper() not in user.perms:
            user.perms.append(permission.upper())
            Storage.save(user)
        return user


def dlt(event):
    if not event.args:
        event.reply('dlt <username>')
        return
    selector = {'user': event.args[0]}
    for obj in Storage.find('user', selector):
        obj.__deleted__ = True
        Storage.save(obj)
        event.reply('ok')
        break


def met(event):
    if not event.args:
        nmr = 0
        for obj in Storage.find('user'):
            event.reply('%s %s %s %s' % (
                                         nmr,
                                         obj.user,
                                         obj.perms,
                                         elapsed(time.time() - fntime(obj.__fnm__)))
                                        )
            nmr += 1
        if not nmr:
            event.reply('no users introduced yet')
        return
    user = User()
    user.user = event.rest
    user.perms = ['USER']
    Storage.save(user)
    event.reply('ok')
