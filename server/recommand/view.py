
import math
import numpy as np

from recommand.type import Type
from recommand.chart import Chart

np.seterr(divide='ignore',invalid='ignore')
from numpy import corrcoef

from functools import reduce

class View(object):
    """
    Attributes:
        table(Table): the table corresponding to this view.
        fx(Feature): the attributes of axis x.
        fy(Feature): the attributes of axis y.
        x_name(str): the name of axis x.
        y_name(str): the name of axis y.
        series_num(int): the number of classification.
        X(list): the data of axis x.
        Y(list): the data of axis y.
        chart(str): the type of the chart, including bar, line ,scatter ans pie.
        tuple_num(int): tuple_num in the corresponding table (the number of columns after transformation).
        score_l(float): the score of the chart in learning_to_rank method.
        M(float): M value in the paper.
        Q(float): Q value in the paper.
        E(float): Effectiveness of visualization node
        A(float): Aesthetic of visualization node
        score(float): the score of the chart in partial_order method.
    """
    def __init__(self,table,x_id,y_id,z_id,series_num,X,Y,chart):
        self.table = table
        self.fx = table.features[x_id]
        self.fy = table.features[y_id]
        self.x_name = self.fx.name
        self.y_name = self.fy.name
        self.z_id = z_id
        self.series_num = series_num
        self.X = X
        self.Y = Y
        self.chart = chart
        self.tuple_num = table.tuple_num
        self.M = self.Q = self.W = self.score = 0
        self.E = self.A = 0
        # self.getM()
        # self.getQ()
        self.getE()

    def getCorrelation(self,series_id):
        """
        Calculate correlation coefficient of X and Y, log(X) and Y, X and log(Y), log(X) and log(Y)
        to determine the relationship of X and Y such as linear, exponential, logarithm and power.
        (especially for partial order and diversified ranking methods)

        Args:
            series_id(int): the index of X and Y(list), determining correlation coefficient of which
                            two columns are to be calculated.

        Returns:
            result(float): For the correlation coefficient of X and Y, log(X) and Y, X and log(Y),
                           log(X) and log(Y), result is the max of the four correlation coefficient.

        """
        if self.fx.type == Type.temporal:
            data1 = [i for i in range(self.tuple_num // self.series_num)]
        else:
            if series_id < len(self.X):
                data1 = self.X[series_id]
        data2 = self.Y[series_id]
        log_data1 = log_data2 = []
        if self.fx.type != Type.temporal and self.fx.min != '' and self.fx.min > 0:
            log_data1 = map(math.log, data1)
        if self.fy.minmin != '' and self.fy.minmin > 0:
            log_data2 = map(math.log, data2)
        log_data2 = map(math.log, data2)
        result = 0
        # linear
        try:
            result = abs(corrcoef(data1, data2)[0][1])
        except Exception as e:
            result = 0
        # else:
        #     pass


        # exponential
        if log_data2:
            try:
                r = abs(corrcoef(data1, log_data2)[0][1])
                if r > result:
                    result = r
            except Exception as e:
                pass
                # print("2 ", e)
                # result = 0
            # else:
            #     pass


        # logarithm
        if log_data1:
            try:
                r = abs(corrcoef(log_data1, data2)[0][1])
                if r > result:
                    result = r
            except Exception as e:
                pass
                # print("3 ", e)
                # result = 0
            else:
                pass


        # power
        if log_data1 and log_data2:
            try:
                r = abs(corrcoef(log_data1, log_data2)[0][1])
                if r > result:
                    result = r
            except Exception as e:
                pass
                # print("4 ", e)
                # result = 0
            else:
                pass

        return result

    def getE(self):
        """
        Calculate Effectiveness of each visualization node
        :return:
        """
        # self.tuple_num: 各series系列对应x的数据个数之和
        # self.Y[0]: 第一组数据的值
        if self.chart == Chart.bar:
            self.E = 1
        elif self.chart == Chart.pie:
            sumY = sum(self.Y[0])
            self.E = reduce(lambda x, y: x + y, map(lambda y: -(1.0 * y / sumY) * math.log(1.0 * y / sumY),self.Y[0]))
        # elif self.chart == Chart.scatter:
        else:
            if self.series_num == 1:
                self.E = self.getCorrelation(0)
            else:
                self.E = max([self.getCorrelation(i) for i in range(self.series_num)])
        # else:
        #     if self.series_num == 1:
        #         if self.getCorrelation(0) > 0.3:
        #             self.E = 1
        #         else:
        #             self.E = 0
        #     else:
        #         if max([self.getCorrelation(i) for i in range(self.series_num)]) > 0.3:
        #             self.E = 1
        #         else:
        #             self.E = 0

    def output(self,order):
        """
            Encapsulate the value of several variables in variable data(ruturned value).

        Args:
            order(int): Not an important argument, only used in the assignment of data.

        Returns:
            data(str): A string including the value of several variables:
                       order1, order2, describe, x_name, y_name, chart, classify, x_data, y_data.

        """
        classify = str([])
        if self.series_num > 1:
            classify = str([v[0] for v in self.table.classes]).replace("u'", '\'').replace("'",'"')
        x_data = str(self.X)
        if self.fx.type == Type.numerical:
            x_data = str(self.X).replace("'", '').replace('"', '').replace('L', '')
        elif self.fx.type == Type.categorical:
            x_data = str(self.X).replace("u'", '\'').replace("'", '"')
        else:
            len_x = len(self.X)
            # x_data = '[' + reduce(lambda s1, s2: s1 + s2, [str(map(str, self.X[i])) for i in range(len_x)]).replace("'",'"') + ']'
            x_data = '["%s"]' % ''.join(list(reduce(lambda s1, s2: s1 + s2, ['","'.join(list(map(str, self.X[i]))) for i in range(len_x)]).replace("'",'"')))
        y_data = str(self.Y)
        if self.fy.type == Type.numerical:
            y_data = str(self.Y).replace("'", '').replace('"', '').replace('L', '')
        elif self.fy.type == Type.categorical:
            y_data = str(self.Y).replace("u'", '\'').replace("'", '"')
        else:
            len_y = len(self.Y)
            # x_data = '[' + reduce(lambda s1, s2: s1 + s2, [str(map(str, self.X[i])) for i in range(len_x)]).replace("'",'"') + ']'
            y_data = '["%s"]' % ''.join(list(reduce(lambda s1, s2: s1 + s2, ['","'.join(list(map(str, self.Y[i]))) for i in range(len_y)]).replace("'",'"')))
        #if self.fy.type == Type.numerical:
        #    y_data = y_data.replace('L', '')
        table_name = '"' + self.table.instance.table_name + '"'
        data = '{"order1":' + str(order) + ',"order2":' + str(1) +  ',"describe":"' + self.table.describe + '","x_name":"' + self.fx.name + '","y_name":"' + self.fy.name + '","chart":"' + Chart.chart[self.chart] + '","classify":' + classify + ',"x_data":' + x_data + ',"y_data":' + y_data + ',"table_name":' + table_name + '}'
        #data = 'score:' + str(round(self.score, 2)) + '\tM:' + str(round(self.M, 2)) + '\tQ:' + str(round(self.Q, 2)) + '\tW:' + str(round(self.W, 2)) + '{"order":' + str(order) + ',"describe":"' + self.table.describe + '","x_name":"' + self.fx.name + '","y_name":"' + self.fy.name + '","chart":"' + Chart.chart[self.chart] + '","classify":' + classify + ',"x_data":' + x_data + ',"y_data":' + y_data + '}'
        return data

