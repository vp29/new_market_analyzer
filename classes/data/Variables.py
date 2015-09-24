__author__ = 'Erics'


class Variables(object):
    minimumPercent = 3
    stopLossPerc = 3
    evenStopLossPerc = 5
    bufferPercent = 3
    samplePeriod = 300
    analysisRange = 960 #len(data.close) #set max points for analysis at a given step
    stepSize = 6
    startingMoney = 15000
    initial = 0.0
    total = startingMoney
    initial_investment = total/10 #invest 10% of the  money
    longStocks = True
    shortStocks = True
    resCutoff = 0.8
    supCutoff = 0.6
    resMaxBuyPer = 20
    resMinBuyPer = 10
    supMaxBuyPer = 20
    supMinBuyPer = 10
    num_iter = 1
    plotting = False
    database = True

    def __init__(self):
        None