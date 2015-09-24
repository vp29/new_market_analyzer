import os
import inspect

from classes.execution.Indicators import Indicators
from classes.execution.Plot import Plot


class Algorithm(object):
    sim_vars = None
    ind = None
    plot = None
    file_loc = None
    file_ext = None
    run_id = None
    type = None

    file_loc = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '\..\..\data\sandp\\'
    file_ext = '-20050101 075000-60sec.csv'

    def __init__(self, sim_vars, run_id=0):
        self.sim_vars = sim_vars
        self.run_id = run_id

        self.ind = Indicators()
        self.plot = Plot()