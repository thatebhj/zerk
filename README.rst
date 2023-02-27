README
######


**NAME**

``ZERK`` - at any time


**SYNOPSIS**


``zerk <cmd> [key=val] [key==val]``


**INSTALL**


``pip3 install zerk``


**DESCRIPTION**


With ``ZERK`` your can have the commands of a irc bot available on your cli.
Instead of having to join a irc channel and give commands to your bot, you
can run these commands on your shell.

``ZERK`` stores it's data on disk where objects are time versioned and the
last version saved on disk is served to the user layer. Files are JSON dumps
that are read-only so thus should provide (disk) persistence. Paths carry the
type in the path name what makes reconstruction from filename easier then
reading type from the object.


**PROGRAMMING**


The ``zerk`` package provides an Object class, that mimics a dict while using
attribute access and provides a save/load to/from json files on disk.
Objects can be searched with database functions and uses read-only files
to improve persistence and a type in filename for reconstruction. Methods are
factored out into functions to have a clean namespace to read JSON data into.

basic usage is this::

>>> import zerk
>>> o = zerk.Object()
>>> o.key = "value"
>>> o.key
>>> 'value'

Objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided, the methods are
factored out into functions like get, items, keys, register, set, update
and values.

load/save from/to disk::

>>> from zerk import Object, load, save
>>> o = Object()
>>> o.key = "value"
>>> p = save(o)
>>> obj = Object()
>>> load(obj, p)
>>> obj.key
>>> 'value'

big Objects can be searched with database functions and uses read-only files
to improve persistence and a type in filename for reconstruction:

'zerk.objects.Object/11ee5f11bd874f1eaa9005980f9d7a94/2021-08-31/15:31:05.717063'

>>> from zerk import Object, save
>>> o = Object()
>>> save(o)  # doctest: +ELLIPSIS
'zerk.object.Object/...'

great for giving objects peristence by having their state stored in files.


**AUTHOR**

B.H.J. Thate <thatebhj@gmail.com>

**COPYRIGHT**

``CMDZ`` is placed in the Public Domain.
