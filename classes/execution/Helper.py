__author__ = 'Erics'

import csv
import time

from datetime import datetime

from classes.data.Data import Data


class Helper:

    @staticmethod
    def check_day_change(prev_ts, cur_ts, period):
        day_change = False

        if(prev_ts + period*10 < cur_ts):
            day_change = True

        return day_change

    @staticmethod
    def read_file(filename):
        print filename
        data = []
        with open(filename, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            i = 0
            for row in spamreader:
                if len(row) != 7:
                    continue
                if '.' not in str(row[4]) and len(str(row[4])) >=4:
                    continue
                if i % 5 == 0:
                    try:
                        data_val = Data(float(row[3]), float(row[1]), float(row[2]), float(row[4]), int(row[5]), time.mktime(datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").timetuple()))
                        data.append(data_val)
                    except:
                        None
                        #print "Cannot parse line: " + row
                i += 1

        return data