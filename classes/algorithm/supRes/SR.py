__author__ = 'Erics'

import traceback

from classes.execution.Helper import Helper
from classes.data.Line import Scatter
from classes.data.PlotTrade import PlotTrade
from classes.models.DBTrade import DBTrade
from classes.algorithm import Algorithm


class SR(Algorithm.Algorithm):

    def __init__(self, sim_vars, run_id=0):
        self.type = "SR"
        super(SR, self).__init__(sim_vars, run_id)

    def run_algo(self, stock):
        try:
            print "Running SR: %s" % (stock,)

        except Exception, e:
            traceback.print_exc()