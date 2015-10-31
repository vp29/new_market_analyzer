__author__ = 'Erics'

import csv
import time

from datetime import datetime

from classes.data.Data import Data
from classes.data.Split import Split
from classes.data.Line import Straight


class Helper:

    @staticmethod
    def check_day_change(prev_ts, cur_ts, period):
        day_change = False

        if(prev_ts + period*10 < cur_ts):
            day_change = True

        return day_change

    @staticmethod
    def least_square(data):
        '''Y=a+bX, b=r*SDy/SDx, a=Y'-bX'
        b=slope
        a=intercept
        X'=Mean of x values
        Y'=Mean of y values
        SDx = standard deviation of x
        SDy = standard deviation of y'''

        num = len(data)
        xy = 0.0
        xx = 0.0
        x = 0.0
        y = 0.0
        for i, price in enumerate(data):
            xy += price.close*price.index
            xx += price.index*price.index
            x += price.index
            y += price.close

        try:
            b = (num*xy - x*y)/(num*xx-x*x)
            a = (y - b*x)/num
        except:
            b=0
            a=0

        return a, b

    @staticmethod
    def read_data_file(filename):
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
                        if data_val.low <= data_val.close <= data_val.high:
                            data.append(data_val)
                    except:
                        None
                        #print "Cannot parse line: " + row
                i += 1

        return data

    @staticmethod
    def read_split_file(filename):
        splits = []
        with open(filename, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                split = Split(float(row[1]), int(float(row[0])))
                splits.append(split)

        return splits

    '''@staticmethod
    def trend_type(res_line, sup_line, next_index, sup_per, res_per, curPrice, resRange, supRange):
        actual_type = ""

        pot_buy = False
        next_res = res_line.inter + res_line.slope*next_index
        next_sup = sup_line.inter + sup_line.slope*next_index
        res_rise = res_line.y_vals[-1] - res_line.y_vals[0]
        sup_rise = sup_line.y_vals[-1] - sup_line.y_vals[0]
        diff = nextRes - nextSup
        resNorm = resRise/curPrice
        supNorm = supRise/curPrice
        normCutoff = 0.01
        if -normCutoff < resNorm < normCutoff\
                and -normCutoff < supNorm < normCutoff:
            potBuy = True
            actual_type = "Sideways moving market."
        elif ((-normCutoff < resNorm < normCutoff)
                or (-normCutoff < supNorm < normCutoff)):
            if -normCutoff < resNorm < normCutoff and supNorm > 0:
                actual_type = "Triangle upward trend.  Predicted to break down."

            elif -normCutoff < supNorm < normCutoff and resNorm < 0:
                actual_type = "Triangle downward trend.  Predicted to break up."
                pass
        elif (resNorm > 0 and supNorm > 0) \
            and ((0.9*supNorm <= resNorm <= supNorm)
                 or (0.9*resNorm <= supNorm <= resNorm)):
                potBuy = True
                actual_type = "Upward trending channel."
        elif (resNorm < 0 and supNorm < 0) \
                and ((resNorm <= supNorm and abs(0.9*resNorm) <= abs(supNorm))
                     or (supNorm <= resNorm and abs(0.9*supNorm) <= abs(resNorm))):
                potBuy = True
                actual_type = "Downward trending channel."
        elif (resNorm < 0 > supNorm) \
                or (resNorm < 0 and resNorm < supNorm)\
                or (supNorm > resNorm > 0):
            actual_type = "Wedge trend.  May break up or down."

        #print "buy point:  " + str((nextSup + diff*bsPoint))
        #print "sell point: " + str((nextRes - diff*bsPoint))
        return (nextSup + diff*sup_per), (nextRes - diff*res_per), potBuy, actual_type'''

    @staticmethod
    def trendType(resSlope, supSlope, resInt, supInt, nextInd, sup_per, res_per, curPrice, resRange, supRange):
        actual_type = ""

        potBuy = False
        nextRes = resInt + resSlope*nextInd
        nextSup = supInt + supSlope*nextInd
        resRise = resSlope*resRange
        supRise = supSlope*supRange
        diff = nextRes - nextSup
        resNorm = resRise/curPrice
        supNorm = supRise/curPrice
        normCutoff = 0.01
        if -normCutoff < resNorm < normCutoff\
                and -normCutoff < supNorm < normCutoff:
            potBuy = True
            actual_type = "Sideways moving market."
        elif ((-normCutoff < resNorm < normCutoff)
                or (-normCutoff < supNorm < normCutoff)):
            if -normCutoff < resNorm < normCutoff and supNorm > 0:
                actual_type = "Triangle upward trend.  Predicted to break down."

            elif -normCutoff < supNorm < normCutoff and resNorm < 0:
                actual_type = "Triangle downward trend.  Predicted to break up."
                pass
        elif (resNorm > 0 and supNorm > 0) \
            and ((0.9*supNorm <= resNorm <= supNorm)
                 or (0.9*resNorm <= supNorm <= resNorm)):
                potBuy = True
                actual_type = "Upward trending channel."
        elif (resNorm < 0 and supNorm < 0) \
                and ((resNorm <= supNorm and abs(0.9*resNorm) <= abs(supNorm))
                     or (supNorm <= resNorm and abs(0.9*supNorm) <= abs(resNorm))):
                potBuy = True
                actual_type = "Downward trending channel."
        elif (resNorm < 0 > supNorm) \
                or (resNorm < 0 and resNorm < supNorm)\
                or (supNorm > resNorm > 0):
            actual_type = "Wedge trend.  May break up or down."

        #print "buy point:  " + str((nextSup + diff*bsPoint))
        #print "sell point: " + str((nextRes - diff*bsPoint))
        return (nextSup + diff*sup_per), (nextRes - diff*res_per), potBuy, actual_type