from multiprocessing import Pool
import time

from classes.execution import Indicators, Database
from classes.models import Simulation


class Backtest(object):
    db = None
    trades = None
    stock_list = None
    sim_vars = None
    plot = None
    ind = None
    type = ""
    var_id = None
    alg = None

    year_seconds = 31536000
    begin_time = 1167609600

    def __init__(self, db, stock_list, alg):
        self.db = db
        self.stock_list = stock_list
        self.ind = Indicators.Indicators()
        self.sim_vars = alg.sim_vars
        self.type = alg.type
        self.alg = alg

        if alg.sim_vars.database:
            db_vars = Simulation.Simulation(self.type, self.sim_vars)
            self.db.insert_item(db_vars)
            self.var_id = db_vars.id
            self.alg.sim_id = db_vars.id
            print "Created simulation_id " + str(self.var_id)

    def run(self):
        start = time.time()

        for i in self.stock_list:
            trades = self.alg.run_algo(i)
            if len(trades) > 0:
                print "Inserting %d %s trades" % (len(trades), trades[0].symbol)
                self.db.direct_trade_insert(trades)

        self.db.session.commit()

        print "--- %s seconds to finish runs ---" % (time.time()-start)

    def run_pool(self):
        start = time.time()
        pool = Pool(processes=4)

        # For every stock in stock list read data
        p = pool.map(self.alg.run_algo, self.stock_list)
        pool.close()
        pool.join()

        print "--- %s seconds to finish runs ---" % (time.time()-start)

        self.db = Database.Database()
        for trades in p:
            if len(trades) > 0:
                print "Inserting %d %s trades" % (len(trades), trades[0].symbol)
                self.db.direct_trade_insert(trades)

        self.db.session.commit()

        print "--- %s seconds to finish insert ---" % (time.time()-start)

    #def
    # Generic plotting function
    #def plot_trade(self, trade):
    #    plot_data = []
    #    plot_data.append(self.plot.)