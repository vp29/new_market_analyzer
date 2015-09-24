__author__ = 'Erics'
from classes.data import Trade


# Trade class with extra information for Plotting
class PlotTrade(Trade.Trade):
    exit_point = None
    stop_loss_point = None
    data = None
    enter_url = None
    exit_url = None
    sup_line = None
    res_line = None

    def __init__(self, trade_type, enter_date, exit_date, enter_price, exit_price, enter_url, exit_url,
                 exit_point, stop_loss_point, data, sup_line, res_line, symbol):
        self.data = data
        self.sup_line = sup_line
        self.res_line = res_line
        self.enter_url = enter_url
        self.exit_url = exit_url

        super(PlotTrade, self).__init__(trade_type, enter_date, exit_date, enter_price, exit_price,
                                         exit_point, stop_loss_point, symbol)