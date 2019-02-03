class View(object):
    def __init__(self):
        self._observers = set()

    def _notify_observers(self, *args, **kargs):
        for observser in self._observers:
            observser(*args, **kargs)

    def register_observer(self, observer):
        self._observers.add(observer)

    def clear_observer(self):
        self._observers.clear()


if __name__ == '__main__':
    viewer = View()
    viewer.register_observer(print)
    viewer._notify_observers((4, 6, 9))

