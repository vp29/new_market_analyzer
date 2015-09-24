__author__ = 'Erics'
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.ext.declarative import declarative_base
from classes.models import DBTrade
import pymysql

Base = declarative_base()


class Database(object):
    engine = None
    session = None

    def __init__(self):

        self.engine = self.create_connection()
        Base.metadata.bind = self.engine
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()
        inspector = Inspector.from_engine(self.engine)
        table_names = inspector.get_table_names()

        # If tables do not exist, create them
        if len(table_names) == 0:
            Base.metadata.create_all()

    def insert_item(self, item):
        self.session.add(item)
        self.session.flush()
        self.session.commit()

    def row2dict(self, row):
        d = {}
        for column in row.__table__.columns:
            if column.name != "id":
                d[column.name] = str(getattr(row, column.name))

        return d

    def direct_trade_insert(self, items):
        self.engine.execute(
            DBTrade.DBTrade.__table__.insert(),
            [self.row2dict(i) for i in items]
        )

    def finish_insert(self):
        self.session.flush()
        self.session.commit()

    def read_trades(self, sim_id):
        return self.session.query(DBTrade.DBTrade).filter(DBTrade.DBTrade.sim_id==sim_id).order_by(DBTrade.DBTrade.enter_date.asc()).all()

    def create_connection(self):
        # Keep trying to connect until succesful
        while True:
            try:
                url = sqlalchemy.engine.url.URL('mysql+pymysql', 'eric', 'StockTests',
                                                '216.155.145.161', 3306, 'algor')
                print url
                return create_engine(url)
            except Exception, e:
                print e
                print "Failed to connect to database"