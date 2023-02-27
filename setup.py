# This file is placed in the Public Domain.


import os


from setuptools import setup


def read():
    return open("README.rst", "r").read()


def uploadlist(dir):
    upl = []
    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        if file.endswith(".pyc") or file.startswith("__pycache"):
            continue
        print(file)
        d = dir + os.sep + file
        if not os.path.isdir(d):
            upl.append(d)
        else:
            upl.extend(uploadlist(d))
    return upl


setup(
    name="zerk",
    version="1",
    author="B.H.J. Thate",
    author_email="thatebhj@gmail.com",
    url="http://github.com/thatebhj/zerk",
    description="at any time",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license="Public Domain",
    packages=["zerk", "zerk.modules"],
    scripts=["bin/zerk"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python",
        "Intended Audience :: System Administrators",
        "Topic :: Communications :: Chat :: Internet Relay Chat",
        "Topic :: Software Development :: Libraries :: Python Modules",
     ],
)
