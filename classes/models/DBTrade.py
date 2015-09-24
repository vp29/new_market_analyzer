from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy

from classes.data.Trade import Trade

Base = declarative_base()

class DBTrade(Base):
    __tablename__ = 'Trades'

    id = Column(Integer, primary_key=True)
    sim_id = Column(Integer, None, ForeignKey('Simulations.id'))
    symbol = Column(String(5), nullable=False)
    enter_date = Column(Integer, nullable=False)
    exit_date = Column(Integer, nullable=False)
    enter_price = Column(sqlalchemy.types.Float, nullable=False)
    exit_price = Column(sqlalchemy.types.Float, nullable=False)
    enter_url = Column(String(256), nullable=False)
    exit_url = Column(String(256), nullable=False)
    trade_type = Column(String(5), nullable=False)

    def __init__(self, symbol, sim_id, item=None):
        self.sim_id = sim_id
        self.symbol = symbol
        if item is not None:
            self.convert_item(item)

    def convert_item(self, item):
        self.enter_date = item.enter_date
        self.exit_date = item.exit_date
        self.enter_price = item.enter_price
        self.exit_price = item.exit_price
        self.enter_url = item.enter_url
        self.exit_url = item.exit_url
        self.trade_type = item.trade_type

    def revert_item(self):
        return Trade(self.trade_type, self.enter_date, self.exit_date, self.enter_price, self.exit_price, None, None, self.symbol)