__author__ = 'Erics'

import urllib2
from classes.data.Data import Data
import time
import datetime

class Yahoo(object):
    base_url = "http://ichart.finance.yahoo.com/table.csv?g=d"

    def __init__(self):
        pass

    def getData(self, stock, start_year, end_year, start_month, end_month, start_day, end_day):
        url = self.base_url + "&f=" + end_year + \
              "&e=" + end_day + "&c=" + start_year + "&b=" + start_day + \
              "&a=" + start_month + "&d=" + end_month + "&s=" + stock
        resp = urllib2.urlopen(url)
        data = resp.read()

        out = file(stock + "_yahoo.csv", "w+")
        out.write(data)

    def getSplits(self, stock, fil):
        first = True
        data = []
        for line in fil:
            if first:
                first = False
                continue
            cs_item = line.split(",")
            timestamp = time.mktime(datetime.datetime.strptime(cs_item[0], "%Y-%m-%d").timetuple())
            item = Data(cs_item[1], cs_item[2], cs_item[3], cs_item[4], cs_item[5], timestamp)
            item.adj_close = cs_item[6]
            data.append(item)

        f = file("data/splits/" + stock + "_splits.csv", "w+")
        prev = None
        for item in reversed(data):
            if prev == None:
                prev = item
                continue
            close_ratio = round(float(prev.close)/float(item.close), 5)
            adj_ratio = round(float(prev.adj_close)/float(item.adj_close), 5)

            prev_ratio = round(float(prev.close)/float(prev.adj_close), 5)
            cur_ratio = round(float(item.close)/float(item.adj_close), 5)

            if close_ratio != adj_ratio:
                if(round(float(prev.close)/float(item.open_), 5) >= 1.1):
                    f.write(str(item.timestamp) + "," + str(round(prev_ratio/cur_ratio, 5)) + "\n")
                    #print str(item.timestamp) + "," + str(prev_ratio/cur_ratio)
                #print "prev_close: " + str(float(prev.close)) + " split_ratio: " + str(round(float(prev.close)/float(item.open_), 5)) + " on " + str(item.timestamp)


            prev = item