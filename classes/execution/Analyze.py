__author__ = 'Erics'

from datetime import datetime


class Analyze(object):
    sim_id = None
    db = None

    def __init__(self, sim_id, db):
        self.sim_id = sim_id
        self.db = db


    def analyze_db(self, initial_val, margin_perc=0):
        trades = []

        dbtrades = self.db.read_trades(self.sim_id)
        for trade in dbtrades:
            trades.append(trade.revert_item())

        print len(trades)


        prof_sideways_trade = 0
        prof_updwards_trade = 0
        prof_downwards_trade = 0

        unprof_sideways_trade = 0
        unprof_upwards_trade = 0
        unprof_downwards_trade = 0

        long_prof_sideways_trade = 0
        long_prof_updwards_trade = 0
        long_prof_downwards_trade = 0

        long_unprof_sideways_trade = 0
        long_unprof_upwards_trade = 0
        long_unprof_downwards_trade = 0

        short_prof_sideways_trade = 0
        short_prof_updwards_trade = 0
        short_prof_downwards_trade = 0

        short_unprof_sideways_trade = 0
        short_unprof_upwards_trade = 0
        short_unprof_downwards_trade = 0

        start_time = trades[0].enter_date#trades[0].buy_time if trades[0].long_short == "long" else trades[0].sell_time
        end_time = trades[-1].exit_date#trades[-1].buy_time if trades[-1].long_short == "short" else trades[-1].sell_time
        open_trades = []
        max_trades = 10
        single_trade = False #only allow once entrance into stock at any given time
        stocks = []
        total = initial_val
        total_used = 0
        total_possible = 0

        max_drawdown = total/max_trades
        max_gain = total/max_trades

        #we cant be long and short at the same time, so we have to keep track
        long_stocks = []
        short_stocks = []

        fmt = "%Y-%m-%d %H:%M:%S"

        start_year = 2007
        cur_year_start = 1167631200 #2007 timestamp
        year_time = 31536000 #seconds in a year
        long_gain = [0]
        short_gain = [0]
        long_trades = [0]
        short_trades = [0]
        total_long_gain = [1]
        total_short_gain = [1]
        end_value = [initial_val]
        j = 0



        for i in range(start_time, end_time+60, 60):
            for trade in trades:
                enter_time = trade.enter_date
                if enter_time < i:
                    trades.remove(trade)
                    continue
                if i == enter_time:
                    if len(open_trades) < max_trades and (not single_trade or (single_trade and trade.symbol not in stocks)):
                        if (trade.trade_type == "long" and trade.symbol not in short_stocks) or \
                            (trade.trade_type == "short" and trade.symbol not in long_stocks):
                            stocks.append(trade.symbol)
                            if trade.trade_type == "long":
                                long_stocks.append(trade.symbol)
                            else:
                                short_stocks.append(trade.symbol)
                            investment_amount = total/(max_trades)
                            print trade.symbol + " -  " + str(investment_amount)
                            #total -= investment_amount
                            #t = Trade(trade.enter_time, trade.exit_time, 0.0, trade.enter_price, trade.exit_price, trade.l_short, investment_amount, trade.symbol, trade.actual_type)
                            #t.exit_url = trade.exit_url
                            trade.investment = investment_amount
                            open_trades.append(trade)
                            total_used += len(open_trades)
                            total_possible += max_trades
                elif trade.enter_date > i:
                    break

            for trade in open_trades:
                exit_time = trade.exit_date
                if i >= exit_time:
                    if exit_time > cur_year_start + year_time:
                        j += 1
                        end_value.append(total)
                        long_gain.append(0)
                        short_gain.append(0)
                        long_trades.append(0)
                        short_trades.append(0)
                        total_long_gain.append(1)
                        total_short_gain.append(1)
                        cur_year_start += year_time
                    if single_trade:
                        stocks.remove(trade.symbol)
                    pgain = 0.0
                    open_trades.remove(trade)
                    if trade.trade_type == "long":
                        long_stocks.remove(trade.symbol)
                        pgain = float((trade.exit_price - trade.enter_price))/float(trade.enter_price)
                        long_gain[j] += pgain
                        long_trades[j] += 1
                        total_long_gain[j] *= (1 + pgain/max_trades)
                        t = datetime.fromtimestamp(float(trade.exit_date))
                        time = datetime.fromtimestamp(float(trade.enter_date)).strftime(fmt) + " - " + t.strftime(fmt)
                    else:
                        try:
                            short_stocks.remove(trade.symbol)
                        except:
                            None
                        pgain = float((trade.enter_price - trade.exit_price))/float(trade.enter_price)
                        short_gain[j] += pgain
                        short_trades[j] += 1
                        total_short_gain[j] *= (1 + pgain/max_trades)
                        t = datetime.fromtimestamp(float(trade.enter_date))
                        time = t.strftime(fmt) + " - " + datetime.fromtimestamp(float(trade.exit_date)).strftime(fmt)
                    if pgain > .7 or pgain < -.7:
                        continue
                    total += float(1.0/(1.0-margin_perc))*trade.investment*(1.0 + pgain) - float(1.0/(1.0-margin_perc))*trade.investment
                    gain = str(pgain)
                    print "stock: " + trade.symbol + " gain: " + gain + " type: " + trade.trade_type + \
                          "\n\tsell: " + str(trade.exit_price) + " buy : " + str(trade.enter_price)
                    print time

                    #if pgain > .5 or pgain < -.5:
                    #    raw_input("Press Enter to continue...")

                    '''if float(gain) > 0.000000000000:
                        if 'Upward' in trade.actual_type:
                            prof_updwards_trade += 1
                            if trade.long_short=="long": long_prof_updwards_trade +=1
                            else: short_prof_updwards_trade += 1
                        elif 'Downward' in trade.actual_type:
                            prof_downwards_trade += 1
                            if trade.long_short=="long": long_prof_downwards_trade +=1
                            else: short_prof_downwards_trade += 1
                        elif 'Sideways' in trade.actual_type:
                            prof_sideways_trade += 1
                            if trade.long_short=="long": long_prof_sideways_trade +=1
                            else: short_prof_sideways_trade += 1
                    if float(gain) < 0.000000000000:
                        print trade.exit_url
                        if 'Upward' in trade.actual_type:
                            unprof_upwards_trade += 1
                            if trade.long_short=="long": long_unprof_upwards_trade +=1
                            else: short_unprof_upwards_trade += 1
                        elif 'Downward' in trade.actual_type:
                            unprof_downwards_trade += 1
                            if trade.long_short=="long": long_unprof_downwards_trade +=1
                            else: short_unprof_downwards_trade += 1
                        elif 'Sideways' in trade.actual_type:
                            unprof_sideways_trade += 1
                            if trade.long_short=="long": long_unprof_sideways_trade +=1
                            else: short_unprof_sideways_trade += 1'''

                    #print trade.actual_type

        print "# sideways profitable: ",  prof_sideways_trade
        print "# upwards profitable counter: " , prof_updwards_trade
        print "# downwards profitable: ", prof_downwards_trade

        print "# sideways unprofitable: ", unprof_sideways_trade
        print "# upwards unprofitable: " , unprof_upwards_trade
        print "# downwards unproftiable: ", unprof_downwards_trade

        print "total # of trades: " + str(unprof_downwards_trade+prof_downwards_trade+ prof_updwards_trade + unprof_upwards_trade + unprof_sideways_trade + prof_sideways_trade)

        try:
            print "percent of profitable sideways trades: " + str(float(prof_sideways_trade)/(float(prof_sideways_trade)+float(unprof_sideways_trade)))
            print "percent of profitable upwards trades: " + str(float(prof_updwards_trade)/(float(prof_updwards_trade)+float(unprof_upwards_trade)))
            print "percent of profitable downwards trades: " + str(float(prof_downwards_trade)/(float(prof_downwards_trade)+float(unprof_downwards_trade)))

            print "LONG: percent of profitable sideways trades: " + str(float(long_prof_sideways_trade)/(float(long_prof_sideways_trade)+float(long_unprof_sideways_trade)))
            print "LONG: percent of profitable upwards trades: " + str(float(long_prof_updwards_trade)/(float(long_prof_updwards_trade)+float(long_unprof_upwards_trade)))
            print "LONG: percent of profitable downwards trades: " + str(float(long_prof_downwards_trade)/(float(long_prof_downwards_trade)+float(long_unprof_downwards_trade)))


            print "SHORT: percent of profitable sideways trades: " + str(float(short_prof_sideways_trade)/(float(short_prof_sideways_trade)+float(short_unprof_sideways_trade)))
            print "SHORT: percent of profitable upwards trades: " + str(float(short_prof_updwards_trade)/(float(short_prof_updwards_trade)+float(short_unprof_upwards_trade)))
            print "SHORT: percent of profitable downwards trades: " + str(float(short_prof_downwards_trade)/(float(short_prof_downwards_trade)+float(short_unprof_downwards_trade)))
        except:
            None

        for i, x in enumerate(long_gain):
            try:
                print str(start_year) + " long avg gain: " + str(float(long_gain[i])/float(long_trades[i])) + \
                    " total gain: " + str(total_long_gain[i])
            except:
                None
            try:
                print str(start_year) + " short avg gain: " + str(float(short_gain[i])/float(short_trades[i])) + \
                    " total gain: " + str(total_short_gain[i])
            except:
                None
            if i < len(long_gain)-1:
                print str(start_year) + " start value: " + str(end_value[i]) + " end value: " + str(end_value[i+1])
                print str(start_year) + " total gain: " + str(float((end_value[i+1] - end_value[i])/end_value[i]))
                start_year += 1
        print str(start_year-1) + " start value: " + str(end_value[-1]) + " end value: " + str(total)
        print str(start_year-1) + " total gain: " + str(float((total - end_value[-1])/end_value[-1]))

        print "lowest_account_balance: ", max_drawdown
        print "highest_account_balance: ", max_gain
        print "end total: " + str(total)
        print "end gain:  " + str((total-initial_val)/initial_val)
        print "utilisation: " + str(float(total_used)/float(total_possible))