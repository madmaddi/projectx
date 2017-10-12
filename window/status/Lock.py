#!/usr/bin/python
# coding=utf-8

import threading

from Singleton import Singleton

class ThreadLock(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.lock = threading.Lock()

    def getLock(self):
        return self.lock

