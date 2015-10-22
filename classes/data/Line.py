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


class Straight(object):
    intercept = 0.0
    slope = 0.0
    start = 0
    end = 0
    y_vals = []

    def __init__(self, intercept, slope, start, end):
        self.intercept = intercept
        self.slope = slope
        self.start = start
        self.end = end
        self.y_vals = self.get_values()

    def get_values(self):
        y_values = []
        for i in range(self.start, self.end):
            y_values.append(self.intercept + self.slope*i)

        return y_values

    def get_spec_value(self, x):
        return self.intercept + self.slope*x