import view


class Control(object):
    def __init__(self):
        self.view = view.View()
        self.view.register_observer(self.something)

    def something(self, *args, **kargs):
        print('Something happend', args, kargs)


if __name__ == '__main__':
    control = Control()
    control.view._notify_observers(1, 2, 3, keyword='Ok')

