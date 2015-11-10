__author__ = 'Erics'

import traceback

from classes.execution.Helper import Helper
from classes.data.Line import Straight, Scatter
from classes.data.PlotTrade import PlotTrade
from classes.data.Split import Split
from classes.models.DBTrade import DBTrade
from classes.algorithm import Algorithm


class SR(Algorithm.Algorithm):

    def __init__(self, sim_vars, run_id=0):
        self.type = "SR"
        super(SR, self).__init__(sim_vars, run_id)

    def run_algo(self, stock):
        finished_trades = []
        print "Running SR: %s" % (stock,)
        splits = []

        data = Helper.read_data_file(self.data_file_loc + stock + self.data_file_ext)
        # Not all stocks have split data
        try:
            splits = Helper.read_split_file(self.split_file_loc + stock + self.split_file_ext)
        except:
            None

        trades = []
        short_buffer_zone = False
        long_buffer_zone = False

        for i in range(0, len(data) - self.sim_vars.analysisRange, self.sim_vars.stepSize):
            prices = data[i: i+self.sim_vars.analysisRange]
            for j in range(0, len(prices)):
                prices[j].index = j
            close = prices[-1].close

            cur_split = Split(1.0, 0)
            for split in splits:
                if split.timestamp < prices[-1].timestamp < (split.timestamp + 86400):
                    cur_split = split

            # Check if we can exit trade
            finished_trades.extend(self.check_exit(trades, prices[-1], cur_split))

            # Find least square line of all prices
            inter, slope = Helper.least_square(prices)
            mean_least_square = Straight(inter, slope, 0, self.sim_vars.analysisRange)
            y_vals = mean_least_square.y_vals
            diff_vals = [prices[z].close - y_vals[z] for z in range(0, len(prices))]

            # Generate least square trend lines
            (res_least_square, res_diff) = self.trend_least_square(prices, diff_vals, self.sim_vars.resCutoff, 1)
            (sup_least_square, sup_diff) = self.trend_least_square(prices, diff_vals, self.sim_vars.supCutoff, -1)

            res_val = res_least_square.y_vals[-1]
            sup_val = sup_least_square.y_vals[-1]

            # Generate range to enter trade
            max_long_buy_point = sup_val + (res_val-sup_val)*self.sim_vars.resMaxBuyPer/100
            min_long_buy_point = sup_val + (res_val-sup_val)*self.sim_vars.resMinBuyPer/100

            max_short_sell_point = res_val - (res_val-sup_val)*self.sim_vars.supMinBuyPer/100
            min_short_sell_point = res_val - (res_val-sup_val)*self.sim_vars.supMaxBuyPer/100

            if long_buffer_zone or short_buffer_zone:

                # Find sections of line that have matches
                pos_matches = [False, False, False]
                neg_matches = [False, False, False]
                for k in range(0, 3):
                    for diff in res_diff:
                        if (k+1)*(len(prices))//3 > diff.index > k*(len(prices))//3:
                            pos_matches[k] = True
                    for diff in sup_diff:
                        if (k+1)*(len(prices))//3 > diff.index > k*(len(prices))//3:
                            neg_matches[k] = True

                buy_point, sell_point, pot_buy, actual_type = Helper.trendType(res_least_square.slope,
                                                                  sup_least_square.slope, res_least_square.intercept,
                                                                  sup_least_square.intercept,
                                                                  self.sim_vars.analysisRange, self.sim_vars.supMinBuyPer/100.0,
                                                                  self.sim_vars.resMinBuyPer/100.0, close,
                                                                  self.sim_vars.analysisRange-1, self.sim_vars.analysisRange-1)

                #only consider buying when support matches in middle and at least one side
                long_pot_buy = pot_buy and (neg_matches[1] and (neg_matches[0] or neg_matches[2])) \
                    and (pos_matches[1] and (pos_matches[0] and pos_matches[2]))
                short_pot_buy = long_pot_buy

                if self.sim_vars.longStocks and long_buffer_zone and sell_point > close*(1.0 + self.sim_vars.minimumPercent/100.0) and long_pot_buy:
                    if min_long_buy_point <= close <= max_long_buy_point:

                        long_buffer_zone = False

                        t = PlotTrade("long", prices[-1].timestamp, None, close, None, None, None, sell_point,
                            close - close*self.sim_vars.stopLossPerc/100.0, prices, sup_least_square, res_least_square, stock)
                        t.mean_line = mean_least_square
                        trades.append(t)
                elif self.sim_vars.shortStocks and short_buffer_zone and buy_point < close/(1.0 + self.sim_vars.minimumPercent/100.0) and short_pot_buy:
                    if min_short_sell_point <= close <= max_short_sell_point:

                        short_buffer_zone = False

                        t = PlotTrade("short", prices[-1].timestamp, None, close, None, None, None, buy_point,
                            close + close*self.sim_vars.stopLossPerc/100, prices, sup_least_square, res_least_square, stock)
                        t.mean_line = mean_least_square
                        trades.append(t)

            # We only want to allow trades if we go below a buffer zone
            # Check if within buffer zone
            if sup_val + (res_val-sup_val)*(self.sim_vars.bufferPercent/100.0) >= close:
                long_buffer_zone = True
            elif close < min_long_buy_point and long_buffer_zone:
                long_buffer_zone = True
            else:
                long_buffer_zone = False

            if res_val - (res_val-sup_val)*(self.sim_vars.bufferPercent/100.0) <= close:
                short_buffer_zone = True
            elif close > max_short_sell_point and short_buffer_zone:
                short_buffer_zone = True
            else:
                short_buffer_zone = False

        return finished_trades

    def check_exit(self, trades, last_price, split):
        finished_trades = []
        for trade in trades:
            if trade.last_split < split.timestamp:
                trade.last_split = split.timestamp
                trade.split_mult *= split.ratio
            last_price.close *= trade.split_mult
            trade.data.append(last_price)
            if trade.trade_type == "long":
                if last_price.close <= trade.stop_loss_point:
                    trade.exit_price = last_price.close
                    trade.exit_date = last_price.timestamp
                    if self.sim_vars.plotting:
                        trade.res_line.end = len(trade.data)-1
                        trade.sup_line.end = len(trade.data)-1
                        trade.mean_line.end = len(trade.data)-1
                        if trade.enter_price < trade.exit_price:
                            gl = "gain"
                        else:
                            gl = "loss"
                        url = self.plot_trade(trade, trade.symbol + " long stop " + gl + " testing ")
                        trade.exit_url = url
                    if self.sim_vars.database:
                        finished_trades.append(DBTrade(trade.symbol, self.sim_id, trade))
                    trades.remove(trade)
                elif last_price.close > trade.stop_loss_point/(1-self.sim_vars.stopLossPerc/100.0):
                    trades.remove(trade)
                    trade.stop_loss_point = last_price.close - last_price.close*self.sim_vars.stopLossPerc/100
                    trades.append(trade)
                else:
                    continue
            elif trade.trade_type == "short":
                if last_price.close >= trade.stop_loss_point:
                    trade.exit_price = last_price.close
                    trade.exit_date = last_price.timestamp
                    if self.sim_vars.plotting:
                        trade.res_line.end = len(trade.data)-1
                        trade.sup_line.end = len(trade.data)-1
                        trade.mean_line.end = len(trade.data)-1
                        if trade.exit_price < trade.enter_price:
                            gl = "gain"
                        else:
                            gl = "loss"
                        url = self.plot_trade(trade, trade.symbol + " short stop " + gl + " testing ")
                        trade.exit_url = url
                    if self.sim_vars.database:
                        finished_trades.append(DBTrade(trade.symbol, self.sim_id, trade))
                    trades.remove(trade)
                elif last_price.close < trade.stop_loss_point/(1+self.sim_vars.stopLossPerc/100.0):
                    trades.remove(trade)
                    trade.stop_loss_point = last_price.close + last_price.close*self.sim_vars.stopLossPerc/100.0
                    trades.append(trade)
                else:
                    continue
        return finished_trades

    def trend_least_square(self, prices, diff_vals, cutoff, mult):
        diff = self.find_matches(diff_vals, cutoff, mult)
        temp_prices = self.match_indexes(diff, prices)
        inter, slope = Helper.least_square(temp_prices)
        return Straight(inter, slope, 0, self.sim_vars.analysisRange), diff

    def find_matches(self, diff, cutoff, mult):

        temp_diff = []
        cur_max_diff = 0.0

        for i, val in enumerate(diff):
            if mult*val > cur_max_diff:
                cur_max_diff = mult*val
            temp_diff.append(self.Diff(val, i))

        temp_diff = [g for g in temp_diff if mult*g.diff >= cutoff*cur_max_diff]

        return temp_diff

    def match_indexes(self, list1, list2):
        matched = []
        for item1 in list1:
            matched.append(list2[item1.index])
        return matched

    def plot_trade(self, trade, title):
        line = Scatter(trade.data)
        x_vals = [i for i in range(0, len(trade.data)-1)]
        plot_data = []
        plot_data.append(self.plot.gen_line(line.x, line.y, 'Stock Data'))
        plot_data.append(self.plot.gen_line(x_vals, len(x_vals)*[trade.exit_point], 'Exit Point', 1, 'dash'))
        plot_data.append(self.plot.gen_line(x_vals, len(x_vals)*[trade.stop_loss_point], 'Stop Loss Point', 1, 'dash'))
        plot_data.append(self.plot.gen_line(x_vals, trade.res_line.get_values(), 'Resistance Line'))
        plot_data.append(self.plot.gen_line(x_vals, trade.sup_line.get_values(), 'Support Line'))
        plot_data.append(self.plot.gen_line(x_vals, trade.mean_line.get_values(), 'Mean Line'))
        plot_data.append(self.plot.gen_point(self.sim_vars.analysisRange, trade.enter_price, 'Enter Price'))
        plot_data.append(self.plot.gen_point(len(trade.data)-1, trade.data[-1].close, 'Exit Price'))

        return self.plot.generate_a_graph(title, plot_data)

    class Diff(object):
        diff = 0.0
        index = 0

        def __init__(self, diff, index):
            self.diff = diff
            self.index = index