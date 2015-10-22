from classes.data import Variables
from classes.algorithm.stochastic.StochasticAlg import *
from classes.algorithm.supRes.SR import *
from classes.execution.Backtest import Backtest
from classes.execution.Database import Database
from classes.execution.Analyze import Analyze


if __name__ == '__main__':
    db = Database()

    var = Variables.Variables()
    var.database = True
    var.plotting = True

    sandp = open('sandp500stocklist.txt')
    stock_list = []
    for line in sandp:
        stock_list.append(line[:-1])
    #stock_list = ['A']

    # Stochastic
    stoch = SR(var)
    stoch_back = Backtest(db, stock_list, stoch)
    stoch_back.run_pool()

    '''analyze = Analyze(166, db)

    analyze.analyze_db(15000)'''