import view
import model


class Control(object):
    def __init__(self):
        self.view = view.View()
        self.view.register_observer(self.something)
        self.model = model.Model()

    def something(self, *args, **kargs):
        self.model.archive(kargs['who'])


if __name__ == '__main__':
    control = Control()
    control.view._notify_observers(who='One')
    control.view._notify_observers(who='Two')
    control.view._notify_observers(who='Three')

