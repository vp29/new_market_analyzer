__author__ = 'Erics'

import traceback

from classes.execution.Helper import Helper
from classes.data.Line import Scatter
from classes.data.PlotTrade import PlotTrade
from classes.models.DBTrade import DBTrade
from classes.algorithm import Algorithm


class StochasticAlg(Algorithm.Algorithm):

    def __init__(self, sim_vars, run_id=0):
        self.type = "stochastic"
        super(StochasticAlg, self).__init__(sim_vars, run_id)

    def run_algo(self, stock):
        try:
            print "Running Stochastic: %s" % (stock,)

            # Parameters
            long_mov_avg_range = 50
            short_mov_avg_range = 20
            k_size = 5
            d_size = 3
            atr_size = 14

            # State vars
            day_close = False
            in_trade = ""
            atr = None

            # Plotting vars
            plot_data = []
            trade_data = []
            sma_short_data = [0] * long_mov_avg_range
            sma_long_data = [0] * long_mov_avg_range
            atr_data = [0] * long_mov_avg_range
            enter_index = 0
            bought_time = 0
            bought_price = 0

            trades = []

            # Read data in
            data = Helper.read_data_file(self.data_file_loc + stock + self.data_file_ext)

            for i in range(0, len(data) - long_mov_avg_range, 1):
                prices = data[i: i+long_mov_avg_range+1]
                closes = []
                for j in range(0, len(prices)):
                    prices[j].index = j
                    closes.append(prices[j].close)

                close = closes[-2]

                # Check for day changes
                day_close = Helper.check_day_change(prices[-2].timestamp, prices[-1].timestamp, self.sim_vars.samplePeriod)

                # Perform sma checks
                sma_long = self.ind.simple_moving_average(closes[0:long_mov_avg_range])
                sma_short = self.ind.simple_moving_average(closes[-short_mov_avg_range-1:-1])

                stochastics = []
                # We need to populate this first using stochastic(5,3)
                # In cases where high=low this value doesnt make sense
                try:
                    for j in range(d_size, 0, -1):
                        per_k = self.ind.stochastic(prices[-k_size-j-1:-j-1])
                        stochastics.append(per_k)
                except:
                    continue
                per_d = self.ind.simple_moving_average(stochastics)

                # Need to subtract 1 extra to get prev close
                atr = self.ind.average_true_range(prices[-1-atr_size-1:-1], atr)

                long_in_range = prices[-2].close < prices[-3].high
                short_in_range = prices[-2].close > prices[-3].high

                # So far we only look at 2 most recent data for candle type
                candle_type = self.ind.candle_type(prices[-3:-1])

                if sma_short > sma_long and \
                   per_k < 25 and per_d < 25 and \
                   "bullish" in candle_type and \
                   long_in_range:
                        in_trade = "long"
                        bought_price = close
                        bought_time = prices[-2].timestamp
                        trade_data = prices
                        enter_index = len(prices)-2
                elif sma_short < sma_long and \
                    per_k > 75 and per_d > 75 and \
                    "bearish" in candle_type and \
                    short_in_range:
                        in_trade = "short"
                        bought_price = close
                        bought_time = prices[-2].timestamp
                        trade_data = prices
                        enter_index = len(prices)-2

                exit_price = bought_price + 2*atr if in_trade == "long" else bought_price - 2*atr
                sl_price = bought_price - atr if in_trade == "long" else bought_price + atr

                # Check for trade exit point
                exit_trade = False
                stop = False
                if in_trade == "long":
                    exit_trade = True if prices[-2].close > exit_price else False
                    stop = True if prices[-2].close < sl_price else False
                elif in_trade == "short":
                    exit_trade = True if prices[-2].close < exit_price else False
                    stop = True if prices[-2].close > sl_price else False

                # Store extra data when in trade for plotting
                if in_trade:
                    trade_data.append(prices[-1])

                sma_short_data.append(sma_short)
                sma_long_data.append(sma_long)
                atr_data.append(atr)

                # Exit trade
                if (day_close or exit_trade or stop) and in_trade != "":
                    plot_url = ""
                    # Plot the data
                    if self.sim_vars.plotting:
                        line = Scatter(trade_data)
                        x_vals = [i for i in range(0, len(trade_data)-1)]
                        plot_data = []
                        plot_data.append(self.plot.gen_line(line.x, line.y, 'Stock Data'))
                        plot_data.append(self.plot.gen_line(x_vals, len(x_vals)*[exit_price], 'Exit Point', 1, 'dash'))
                        plot_data.append(self.plot.gen_line(x_vals, len(x_vals)*[sl_price], 'Stop Loss Point', 1, 'dash'))
                        plot_data.append(self.plot.gen_line(x_vals, sma_long_data[-len(trade_data):], 'Long Mov Avg'))
                        plot_data.append(self.plot.gen_line(x_vals, sma_short_data[-len(trade_data):], 'short Mov Avg'))
                        plot_data.append(self.plot.gen_point(enter_index, bought_price, 'Enter Price'))
                        plot_data.append(self.plot.gen_point(len(trade_data)-2, prices[-2].close, 'Exit Price'))

                        subplot_data = []
                        subplot_data.append(self.plot.gen_line(x_vals, atr_data[-len(trade_data):], 'ATR(14)'))
                        plot_url = self.plot.generate_subplots(str(self.run_id) + " " + in_trade + " " + stock + " " + str(prices[-2].timestamp), [plot_data, subplot_data])
                        #plot_url = self.plot.generate_a_graph(str(self.var_id) + " " + in_trade + " " + stock + " " + str(prices[-2].timestamp), plot_data)

                    if self.sim_vars.database:
                        # Store trade in DB
                        trade = PlotTrade(in_trade, bought_time, prices[-2].timestamp,
                                          bought_price, prices[-2].close,
                                          "", plot_url,
                                          exit_price, sl_price,
                                          None, None, None, stock)

                        db_trade = DBTrade(stock, self.run_id, trade)
                        trades.append(db_trade)
                        '''self.db.insert_item(db_trade)
                        print "inserted trade with id: " + str(db_trade.id)'''

                    in_trade = ""

            return trades
        except Exception, e:
            traceback.print_exc()