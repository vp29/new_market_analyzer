from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy

Base = declarative_base()

class Simulation(Base):
    __tablename__ = 'Simulations'

    id = Column(Integer, primary_key=True)
    algor = Column(String(10), nullable=False)
    minimumPercent = Column(sqlalchemy.types.Float, nullable=False)
    stopLossPerc = Column(sqlalchemy.types.Float, nullable=False)
    evenStopLossPerc = Column(sqlalchemy.types.Float, nullable=False)
    bufferPercent = Column(sqlalchemy.types.Float, nullable=False)
    samplePeriod = Column(Integer, nullable=False)
    analysisRange = Column(Integer, nullable=False)
    stepSize = Column(Integer, nullable=False)
    longStocks = Column(sqlalchemy.types.Boolean, nullable=False)
    shortStocks = Column(sqlalchemy.types.Boolean, nullable=False)
    resCutoff = Column(sqlalchemy.types.Float, nullable=False)
    supCutoff = Column(sqlalchemy.types.Float, nullable=False)
    resMaxBuyPer = Column(sqlalchemy.types.Float, nullable=False)
    resMinBuyPer = Column(sqlalchemy.types.Float, nullable=False)
    supMaxBuyPer = Column(sqlalchemy.types.Float, nullable=False)
    supMinBuyPer = Column(sqlalchemy.types.Float, nullable=False)

    def __init__(self, algor, item=None):
        self.algor = algor
        if item is not None:
            self.convert_item(item)

    def convert_item(self, item):
        self.minimumPercent = item.minimumPercent
        self.stopLossPerc = item.stopLossPerc
        self.evenStopLossPerc = item.evenStopLossPerc
        self.bufferPercent = item.bufferPercent
        self.samplePeriod = item.samplePeriod
        self.analysisRange = item.analysisRange
        self.stepSize = item.stepSize
        self.longStocks = item.longStocks
        self.shortStocks = item.shortStocks
        self.resCutoff = item.resCutoff
        self.supCutoff = item.supCutoff
        self.resMaxBuyPer = item.resMaxBuyPer
        self.resMinBuyPer = item.resMinBuyPer
        self.supMaxBuyPer = item.supMaxBuyPer
        self.supMinBuyPer = item.supMinBuyPer