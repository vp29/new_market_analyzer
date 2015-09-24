__author__ = 'Erics'

class Trade(object):

    trade_type = None
    enter_date = None
    exit_date = None
    enter_price = None
    exit_price = None
    exit_point = None
    stop_loss_point = None
    symbol = None
    investment = None

    def __init__(self, trade_type, enter_date, exit_date, enter_price, exit_price, exit_point, stop_loss_point, symbol):
        self.trade_type = trade_type
        self.enter_date = enter_date
        self.exit_date = exit_date
        self.enter_price = enter_price
        self.exit_price = exit_price
        self.exit_point = exit_point
        self.stop_loss_point = stop_loss_point
        self.symbol = symbol

