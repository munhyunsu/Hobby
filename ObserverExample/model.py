import copy


class Model(object):
    def __init__(self):
        self.default_form = {'time': -1,
                             'who': None}
        self.data = list()

    def archive(self, who):
        data = copy.deepcopy(self.default_form)
        data['who'] = who
        self.data.append(data)

