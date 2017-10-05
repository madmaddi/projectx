import threading

class Singleton(type):
    def __init__(self, name, bases, dict):
        super(Singleton, self).__init__(name, bases, dict)
        self.instance = None

    def __call__(self, *args, **kw):
        if self.instance is None:
            self.instance = super(Singleton, self).__call__(*args, **kw)

        return self.instance

class ThreadLock(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.lock = threading.Lock()

    def getLock(self):
        return self.lock

#print ThreadLock().getLock()
#print ThreadLock().getLock()
