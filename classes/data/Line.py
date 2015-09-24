__author__ = 'Erics'


class Scatter(object):
    x = []
    y = []

    def __init__(self, data):
        self.x = []
        self.y = []
        for i, item in enumerate(data):
            self.x.append(i)
            self.y.append(item.close)