from classes.data import Variables
from classes.algorithm.stochastic.StochasticAlg import *
from classes.algorithm.supRes.SR import *
from classes.execution.Backtest import Backtest
from classes.execution.Database import Database
from classes.execution.Analyze import Analyze
from classes.execution.Yahoo import Yahoo

import cProfile


if __name__ == '__main__':
    yahoo = Yahoo()

    sandp = open('sandp500stocklist.txt')
    stock_list = []
    for line in sandp:
        stock_list.append(line[:-1])
    #stock_list = ['A']

    '''for stock in stock_list:
        try:
            yahoo.getData(stock, "2007", "2015", "00", "01", "01", "01")
        except:
            print "error with: " + stock
    for stock in stock_list:
        try:
            f = file("data/yahoo/" + stock + "_yahoo.csv")
            yahoo.getSplits(stock, f)
        except:
            None
    exit(0)'''

    stop_loss_list = [0, 1, 2, 3]
    min_gain_list = [0, 1, 2, 3, 4, 5, 6]

    db = Database()

    for sl in stop_loss_list:
        for min_gain in min_gain_list:
            var = Variables.Variables()
            var.stopLossPerc = sl
            var.minimumPercent = min_gain
            var.database = True
            var.plotting = True

            # Stochastic
            stoch = SR(var)
            stoch_back = Backtest(db, stock_list, stoch)
            stoch_back.run_pool()
            #cProfile.run('stoch_back.run()', 'foo.profile')

    '''analyze = Analyze(213, db)

    analyze.analyze_db(15000)'''