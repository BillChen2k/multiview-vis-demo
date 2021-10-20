"""
该文件实现了Table类，是整份代码中最重要和最复杂的一个类：
Table类实现了对原始数据分类整合以产生不同类型图表的重要功能，其顶层函数为dealWithTable，该函数先调用generateViews函数
进行必要的预处理后调用getClassifyTable函数，由getClassifyTable函数根据数据类型进行不同的处理和操作，实现较复杂，代码
量较大。经过处理后，原始数据表格分散为若干个小的数据表格，为后续产生不同的图表以及图标的排序做好准备工作。
"""

import datetime

from .type import Type
from .features import Features
from .view import View
from .chart import Chart

month = ['','Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']


class Table(object):
    """
    Attributes:
        D(list): store the origin table.
        instance(Instance): the Instance Object corresponding to this table.
        transformed(bool): whether or not the table has been transformed.
        describe1(str): description to 2D views.
        describe2(str): description to 3D views.
        describe(str): describe1 + describe2.
        column_num(int): the number of columns in the table.
        tuple_num(int): the number of columns after transformation.
        view_num(int): the number of views generated from the table.
        names(list): name of each column.
        types(list): type of each column.
        origins(list): which column the data from.
        features(list): store the attributes of each column.
        views(list): list of views generated from the table.
        classify_id(int): index of classification.
        classify_num(int): the number of classification.
        classes(list): store the classification.
    """
    def __init__(self,instance,transformed,describe1,describe2):
        self.D = [] # the original table
        self.instance = instance # to remember who its parent is
        self.transformed = transformed
        self.describe1, self.describe2 = describe1, describe2
        self.describe = self.describe1+', ' + self.describe2 if self.describe2 else self.describe1
        self.column_num = self.tuple_num = self.view_num = 0
        self.names = []
        self.types = []
        self.origins = []
        self.features = []
        self.views = []
        self.classify_id = -1
        self.classify_num = 1
        self.classes = []

    def getIntervalBins(self,f): #f: features
        """

        :param f: features of table
        :return:
        """
        bins = []
        minTime = f.minmin
        maxTime = f.max
        # type of minTime is datetime.datetime
        if type(minTime) != type(datetime.date(1995,10,11)) and minTime.year == maxTime.year and minTime.month == maxTime.month and minTime.day == maxTime.day:
            minHour = minTime.hour
            minMinute = minTime.minute
            minSecond = minTime.second
            maxHour = maxTime.hour
            maxMinute = maxTime.minute
            maxSecond = maxTime.second
            if minHour == maxHour:
                if minMinute == maxMinute:
                    # year, month, day, hour, minute of max and min is the same, so interval = 'SECOND'
                    for i in range(minSecond, maxSecond + 1):
                        t = datetime.datetime(minTime.year, minTime.month, minTime.day, minHour, minMinute, i)
                        bins.append([str(i) + 's', t, t, 0])
                else:
                    # year, month, day, hour of max and min is the same, but minute is different, so interval = 'MINUTE'
                    for i in range(minMinute, maxMinute + 1):
                        t1 = datetime.datetime(minTime.year, minTime.month, minTime.day, minHour, i, 0)
                        t2 = datetime.datetime(minTime.year, minTime.month, minTime.day, minHour, i, 59)
                        bins.append([str(i) + 'm', t1, t2, 0])
            else:
                # year, month, day of max and min is the same, but hour is different, so interval = 'HOUR'
                for i in range(minHour, maxHour + 1):
                    t1 = datetime.datetime(minTime.year, minTime.month, minTime.day, i, 0, 0)
                    t2 = datetime.datetime(minTime.year, minTime.month, minTime.day, i, 59, 59)
                    bins.append([str(i) + ' oclock', t1, t2, 0])
        else: # type of minTime is datetime.date
            minYear = minTime.year
            minMonth = minTime.month
            minDay = minTime.day
            maxYear = maxTime.year
            maxMonth = maxTime.month
            maxDay = maxTime.day
            if minYear == maxYear:
                if minMonth == maxMonth:
                    # year, month of max and min is the same, but hour is different, so interval = 'DAY'
                    for i in range(minDay, maxDay + 1):
                        bins.append([str(i)+'th',datetime.date(minYear, minMonth, i),datetime.date(minYear, minMonth, i), 0])
                else:
                    # year of max and min is the same, but hour is different, so interval = 'MONTH'
                    for i in range(minMonth, maxMonth):
                        bins.append([month[i],datetime.date(minYear, i, 1), datetime.date(minYear, i + 1, 1)-datetime.timedelta(1), 0])
                    if maxMonth == 12:
                        bins.append(['Dec', datetime.date(minYear, 12, 1), datetime.date(minYear, 12, 31), 0])
                    else:
                        bins.append([month[maxMonth],datetime.date(minYear, maxMonth, 1),datetime.date(minYear, maxMonth + 1, 1) - datetime.timedelta(1), 0])
            else:
                # year of max and min is different, so interval = 'YEAR'
                yearNum = maxYear - minYear + 1
                if yearNum > 20:
                    if yearNum % 10 > yearNum // 10:
                        yearDelta = yearNum // 10 + 1
                    else:
                        yearDelta = yearNum // 10
                    beginYear = minYear
                    while True:
                        endYear = beginYear + yearDelta - 1
                        if endYear > maxYear:
                            endYear = maxYear
                        if beginYear == endYear:
                            bins.append([str(beginYear), datetime.date(beginYear, 1, 1), datetime.date(endYear, 12, 31),0])
                        else:
                            bins.append([str(beginYear) + '~' + str(endYear), datetime.date(beginYear, 1, 1),datetime.date(endYear, 12, 31), 0])
                        if endYear == maxYear:
                            break
                        beginYear += yearDelta
                else:
                    for i in range(minYear, maxYear + 1):
                        bins.append([str(i), datetime.date(i, 1, 1), datetime.date(i, 12, 31), 0])
        f.interval_bins = bins
        f.bin_num = len(bins)
        f.interval = 'TIME'

    def extract_feature(self):
        # 转制，将dataframe中的列转化成行
        T = list(map(list,zip(*self.D)))
        if self.transformed:
            for column_id in range(self.column_num):
                f = Features(self.names[column_id],self.types[column_id],self.origins[column_id])
                #calculate min,max for numerical
                if f.type == Type.numerical:
                    # 未分类
                    if self.classify_num == 1 or not self.describe2:
                        f.min,f.max = min(T[column_id]),max(T[column_id])
                        f.minmin = f.min
                        if f.min == f.max:
                            self.types[column_id] = f.type = Type.none
                            self.features.append(f)
                            continue
                    else: # 进过分类
                        delta = self.tuple_num // self.classify_num
                        f.min = [min(T[column_id][class_id*delta:(class_id+1)*delta]) for class_id in range(self.classify_num)]
                        f.minmin = min(f.min)
                        f.max = [max(T[column_id][class_id*delta:(class_id+1)*delta]) for class_id in range(self.classify_num)]
                        if sum([f.max[class_id]-f.min[class_id] for class_id in range(self.classify_num)]) == 0:
                            self.types[column_id] = f.type = Type.none
                            self.features.append(f)
                            continue
                        if min(f.min) == max(f.min) and min(f.max) == max(f.max):
                            if sum([0 if T[column_id][class_id*delta:(class_id+1)*delta] == T[column_id][(class_id+1)*delta:(class_id+2)*delta] else 1 for class_id in range(self.classify_num-1)]) == 0:
                                self.types[column_id] = f.type = Type.none
                                self.features.append(f)
                                continue



                #calculate distinct,ratio for categorical,temporal
                if f.type == Type.categorical or f.type == Type.temporal:
                    f.distinct = self.tuple_num
                    f.ratio = 1.0

                self.features.append(f)
        else: # not transformed
            for column_id in range(self.column_num):
                f = Features(self.names[column_id],self.types[column_id],self.origins[column_id])

                #calculate min,max for numerical,temporal
                if f.type == Type.numerical or f.type == Type.temporal:
                    f.min, f.max = min(T[column_id]), max(T[column_id])
                    f.minmin = f.min
                    if f.min == f.max:
                        # ？？？
                        self.types[column_id] = f.type = Type.none
                        self.features.append(f)
                        continue

                d = {}
                #calculate distinct,ratio for categorical,temporal
                if f.type == Type.categorical or f.type == Type.temporal:
                    for i in range(self.tuple_num):
                        if self.D[i][column_id] in d:
                            d[self.D[i][column_id]] += 1
                        else:
                            d[self.D[i][column_id]] = 1
                    # 计算distinct
                    f.distinct = len(d)
                    if f.distinct == 1:
                        self.types[column_id] = f.type = Type.none
                        self.features.append(f)
                        continue
                    # 计算ratio
                    f.ratio = 1.0 * f.distinct / self.tuple_num
                    # 获取distinct的value和对应cnt
                    f.distinct_values = [(k,d[k]) for k in sorted(d)]
                    if f.type == Type.temporal:
                        self.getIntervalBins(f)

                self.features.append(f)

    def generateViews(self):
        """
        Generate views according to the type of each column before dealing with table.

        Args:
            None.

        Returns:
            None.

        """
        T = list(map(list,zip(*self.D)))
        #generate 2D views
        # 处理未分类的表
        if self.describe2 == '' and self.classify_id == -1:
            self.generate2dViews(T)
        #generate 3D views
        else:
            self.generate3dViews(T)

        self.instance.view_num += self.view_num


    def generate2dViews(self, T):
        """

        :return:
        """
        for i in range(self.column_num):
            for j in range(self.column_num):
                if i == j:
                    continue
                #选择两列作为x、y轴数据，更具x、y的类型及特征，选择合适的可视化图表类型
                fi = self.features[i]
                fj = self.features[j]

                if self.transformed:
                    if fi.type == Type.categorical and fj.type == Type.numerical and fi.ratio == 1.0:
                        charts = []
                        if fj.minmin != '' and fj.minmin > 0 and fi.distinct > 1 and fi.distinct <= 6 and  not (len(fj.name) >= 6 and fj.name[0:4] == 'AVG(' and fj.name[-1] == ')'):
                            charts.append(Chart.pie)
                        if fi.distinct > 1 and fi.distinct <= 20 :
                            charts.append(Chart.bar)
                        # charts.append(Chart.bar)
                    elif fi.type == Type.temporal and fj.type == Type.numerical and fi.ratio == 1.0:
                        charts = []
                        if fi.distinct >= 7:
                            charts.append(Chart.line)
                        else:
                            charts.append(Chart.bar)
                    else:
                        charts = []
                else: # not transfromed
                    if fi.type == Type.numerical and fj.type == Type.numerical and i < j:
                        charts = [Chart.scatter]
                    else:
                        charts = []

                # 生成view节点
                for chart in charts:
                    v = View(self,i,j,-1,1,[T[i]],[T[j]],chart)
                    self.views.append(v)
                    self.view_num += 1

    def generate3dViews(self, T):
        """

        :return:
        """
        if self.describe2:
            for i in range(self.column_num):
                for j in range(self.column_num):
                    fi = self.features[i]
                    fj = self.features[j]
                    if fi.type == Type.categorical and fj.type == Type.numerical:
                        charts = [Chart.bar]
                    elif fi.type == Type.temporal and fj.type == Type.numerical:
                        if self.tuple_num / self.classify_num < 7:
                            charts = [Chart.bar]
                        else:
                            charts = [Chart.line]
                    else:
                        charts = []
                    for chart in charts:
                        delta = self.tuple_num // self.classify_num
                        series_data = [T[j][series * delta:(series + 1) * delta] for series in range(self.classify_num)]
                        v = View(self, i, j, self.classify_id, self.classify_num, [T[i][0:delta]], series_data, chart)
                        self.views.append(v)
                        self.view_num += 1

        else: # 处理初始分类后的表
            for i in range(self.column_num):
                for j in range(self.column_num):
                    if i >= j or self.types[i] != Type.numerical or self.types[j] != Type.numerical:
                        continue
                    X = []
                    Y = []
                    id = 0
                    for k in range(self.classify_num):
                        x = T[i][id:id+self.classes[k][1]]
                        y = T[j][id:id+self.classes[k][1]]
                        id += self.classes[k][1]
                        X.append(x)
                        Y.append(y)
                    v = View(self,i,j,self.classify_id,self.classify_num,X,Y,Chart.scatter)
                    self.views.append(v)
                    self.view_num+=1


    # The following functions deal with different types of data and return new_table

    def dealWithGroup(self,column_id,begin,end,get_head,get_data):
        """
        generate a new table by operation "GROUP BY $(name)"

        Args:
            column_id(int): id of the column need to be dealt with
            begin(int): the first row to be dealt with
            end(int): the last row to be dealt with
            get_head(bool): whether or not add 'CNT', 'SUM', 'AVG' operation to the new table
            get_data(bool): whether or not add data to the new table

        Returns:
            new_table(Table): A new table generated by operation "GROUP BY $(name)"

        """
        # 对于抽象类型 分组操作
        new_table = Table(self.instance, True, 'GROUP BY ' + self.names[column_id], '')
        type = self.types[column_id]
        if get_head:
            new_table.tuple_num = self.features[column_id].distinct
            # new_table的第一列为该列本身
            new_table.column_num = 1
            new_table.names.append(self.names[column_id])
            new_table.types.append(self.types[column_id])
            new_table.origins.append(column_id)

            if type ==Type.categorical:
                #  抽象类型分类后的个数cnt
                new_table.column_num += 1
                new_table.names.append('CNT(' + self.names[column_id] + ')')
                new_table.types.append(Type.numerical)
                new_table.origins.append(column_id)

            # 遍历各列，若为数值类型，则在new_table中添加两列，分别为sum，avg
            for i in range(self.column_num):
                if self.types[i] == Type.numerical: # when the type is numerical, add 'SUM' and 'AVG' to new_table
                    new_table.column_num += 2
                    new_table.names.extend(['SUM(' + self.names[i] + ')', 'AVG(' + self.names[i] + ')'])
                    if self.features[i].minmin != '' and self.features[i].minmin < 0:
                        new_table.types.extend([Type.none, Type.numerical])
                    else:
                        new_table.types.extend([Type.numerical,Type.numerical])
                    new_table.origins.extend([i, i])

        # 根据head获取对应数据
        if get_data:
            d = {}
            cnt = {}
            # calculate cnt
            for i in range(0, self.features[column_id].distinct):
                cnt[self.features[column_id].distinct_values[i][0]] = [0]
                # hash初始化。取column_id列中的distinct值作为map d{} 的 d.key，d.value为[0]，对应cnt。
                d[self.features[column_id].distinct_values[i][0]] = [self.features[column_id].distinct_values[i][0]]
            for i in range(begin, end):
                cnt[self.D[i][column_id]][0] += 1

            first_sum = 1
            num = 1 #numerical column number

            if type == Type.categorical:
                first_sum = 2
                num += 1
                for k in d:
                    d[k].extend([0])
                for i in d:
                    # 遍历column_id列的行，从begin行至end行，统计ditinct_value的cnt
                    d[i][1] = cnt[i][0]

            # 求sum()、avg() d.value初始化为[cnt,0,0...] 对应sum、avg
            for i in range(self.column_num):
                if self.types[i] == Type.numerical:
                    num += 2
                    for k in d:
                        d[k].extend([0,0])
            # 计算数值类型列的sum
            for i in range(begin,end):
                sum_column = first_sum
                for j in range(self.column_num):
                    if self.types[j] == Type.numerical:
                        if isinstance(self.D[i][j], int) or isinstance(self.D[i][j], float) or (isinstance(self.D[i][j], str) and self.D[i][j].isdigit()):#self.D[i][j] != '' and :
                            d[self.D[i][column_id]][sum_column] += int(self.D[i][j])
                        sum_column += 2
            # 根据d.key遍历d 求avg
            for k in d:
                for i in range(first_sum, num, 2):
                    if cnt[k][0]:
                        d[k][i + 1] = 1.0 * d[k][i] / cnt[k][0]

            for k in d:
                new_table.D.append(d[k])
            # 如果本身为时序类型，按照时间排序
            if self.features[column_id].type == Type.temporal:
                new_table.D.sort(key=lambda l:l[0])
        return new_table

    def dealWithIntervalBin(self,column_id,begin,end,get_head,get_data):
        """
        genarate a new table by operation "BIN BY $(interval)"

        Args:
            column_id(int): id of the column need to be dealt with
            begin(int): the first row to be dealt with
            end(int): the last row to be dealt with
            get_head(bool): whether or not add 'CNT', 'SUM', 'AVG' operation to the new table
            get_data(bool): whether or not add data to the new table

        Returns:
            new_table(Table): A new table generated by operation "BIN BY $(interval)"

        """
        bins = self.features[column_id].interval_bins
        bin_num = self.features[column_id].bin_num
        interval = self.features[column_id].interval
        new_table = Table(self.instance, True, 'BIN ' + self.names[column_id] + ' BY ' + interval,'')
        if get_head:
            new_table.tuple_num = bin_num
            for i in range(self.column_num):
                if self.types[i] == Type.numerical:
                    new_table.column_num += 2
                    new_table.names.extend(['SUM(' + self.names[i] + ')', 'AVG(' + self.names[i] + ')'])
                    if self.features[i].minmin != '' and self.features[i].minmin < 0:
                        new_table.types.extend([Type.none,Type.numerical])
                    else:
                        new_table.types.extend([Type.numerical, Type.numerical])
                    new_table.origins.extend([i, i])
            # 加入本身数据
            new_table.column_num += 1
            new_table.names.extend([self.names[column_id]])
            new_table.types.extend([Type.temporal])
            new_table.origins.extend([column_id])
        if get_data:
            num = 0
            new_table.D = [[] for i in range(bin_num)]
            for i in range(self.column_num):
                if self.types[i] == Type.numerical:
                    num += 2
                    for j in range(bin_num):
                        new_table.D[j].extend([0,0])
            for i in range(begin,end):
                date = self.D[i][column_id]
                # bin[min, start_date, end_date, cnt]
                # 统一时间格式
                if type(date) != type(bins[0][1]):
                    date = datetime.date(date.year, date.month, date.day)
                for j in range(bin_num):
                    # bin[min, start_date, end_date, cnt]
                    # 若date 在 start_date 与 end_date 之间，cnt+1
                    if bins[j][1] <= date <= bins[j][2]:
                        bins[j][3] += 1
                        sum_column = 0
                        for k in range(self.column_num):
                            if self.types[k] == Type.numerical:
                                if isinstance(self.D[i][k], int) or isinstance(self.D[i][k], float) or (isinstance(self.D[i][k], str) and self.D[i][k].isdigit()):
                                    new_table.D[j][sum_column] += int(self.D[i][k])
                                sum_column += 2
                        break
            for i in range(bin_num):
                for j in range(0, num, 2):
                    if bins[i][3]:
                        new_table.D[i][j + 1] = 1.0 * new_table.D[i][j] / bins[i][3]
                new_table.D[i].extend([bins[i][0]])
        return new_table

    def dealWithHourBin(self,column_id,begin,end,get_head,get_data):
        """
        genarate a new table by operation "BIN BY HOUR"

        Args:
            column_id(int): id of the column need to be dealt with
            begin(int): the first row to be dealt with
            end(int): the last row to be dealt with
            get_head(bool): whether or not add 'CNT', 'SUM', 'AVG' operation to the new table
            get_data(bool): whether or not add data to the new table

        Returns:
            new_table(Table): A new table generated by operation "BIN BY HOUR"

        """
        new_table = Table(self.instance, True, 'BIN ' + self.names[column_id] + ' BY HOUR','')
        if get_head:
            new_table.column_num = 2
            new_table.tuple_num = 24
            new_table.names.extend([self.names[column_id] + ' oclock','CNT(' + self.names[column_id] + ')'])
            new_table.types.extend([Type.categorical,Type.numerical])
            new_table.origins.extend([column_id, column_id])
            for i in range(self.column_num):
                if self.types[i] == Type.numerical:
                    new_table.column_num += 2
                    new_table.names.extend(['SUM(' + self.names[i] + ')', 'AVG(' + self.names[i] + ')'])
                    if self.features[i].minmin < 0:
                        new_table.types.extend([Type.none, Type.numerical])
                    else:
                        new_table.types.extend([Type.numerical, Type.numerical])
                    new_table.origins.extend([i, i])
        if get_data:
            num = 0
            new_table.D = [[str(i), 0] for i in range(24)]
            for i in range(self.column_num):
                if self.types[i] == Type.numerical:
                    num += 2
                    for j in range(24):
                        new_table.D[j].extend([0,0])
            for i in range(begin,end):
                hour = self.D[i][column_id].hour
                new_table.D[hour][1] += 1
                sum_column = 2
                for j in range(self.column_num):
                    if self.types[j] == Type.numerical:
                        new_table.D[hour][sum_column] += self.D[i][j]
                        sum_column += 2
            for i in range(24):
                for j in range(2,num + 2,2):
                    if new_table.D[i][1]:
                        new_table.D[i][j+1] = 1.0 * new_table.D[i][j] / new_table.D[i][1]
        return new_table

    def dealWithWeekBin(self,column_id,begin,end,get_head,get_data):
        """
        genarate a new table by operation "BIN BY WEEKDAY"

        Args:
            column_id(int): id of the column need to be dealt with
            begin(int): the first row to be dealt with
            end(int): the last row to be dealt with
            get_head(bool): whether or not add 'CNT', 'SUM', 'AVG' operation to the new table
            get_data(bool): whether or not add data to the new table

        Returns:
            new_table(Table): A new table generated by operation "BIN BY WEEKDAY"

        """
        weekdays = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
        new_table = Table(self.instance, True, 'BIN ' + self.names[column_id] + ' BY WEEKDAY', '')
        if get_head:
            new_table.column_num = 1
            new_table.tuple_num = 7
            new_table.names.extend([self.names[column_id]])
            new_table.types.extend([Type.categorical])
            new_table.origins.extend([column_id])
            for i in range(self.column_num):
                if self.types[i] == Type.numerical:
                    new_table.column_num += 2
                    new_table.names.extend(['SUM(' + self.names[i] + ')', 'AVG(' + self.names[i] + ')'])
                    if self.features[i].minmin != '' and self.features[i].minmin < 0:
                        new_table.types.extend([Type.none,Type.numerical])
                    else:
                        new_table.types.extend([Type.numerical, Type.numerical])
                    new_table.origins.extend([i, i])
        if get_data:
            # 初始化
            num = 0
            new_table.D = [[weekdays[i]] for i in range(7)]
            cnt = [0 for i in range(7)]
            for i in range(self.column_num):
                if self.types[i] == Type.numerical:
                    num += 2
                    for j in range(7):
                        new_table.D[j].extend([0,0])
            # 计算sum、cnt
            for i in range(begin,end):
                weekday = self.D[i][column_id].weekday()
                # new_table.D[weekday][1] += 1
                cnt[weekday] += 1
                sum_column = 1
                for j in range(self.column_num):
                    if self.types[j] == Type.numerical:
                        if isinstance(self.D[i][j], int) or isinstance(self.D[i][j], float) or (isinstance(self.D[i][j], str) and self.D[i][j].isdigit()):
                            new_table.D[weekday][sum_column] += int(self.D[i][j])
                        sum_column += 2
            # 计算 avg
            for i in range(7):
                for j in range(1,num + 1,2):
                    if cnt[i]:
                        new_table.D[i][j+1] = 1.0 * new_table.D[i][j] / cnt[i]
        return new_table

    def dealWithPNBin(self,column_id,begin,end,get_head,get_data):
        """
        genarate a new table by operation "BIN BY ZERO"

        Args:
            column_id(int): id of the column need to be dealt with
            begin(int): the first row to be dealt with
            end(int): the last row to be dealt with
            get_head(bool): whether or not add 'CNT', 'SUM', 'AVG' operation to the new table
            get_data(bool): whether or not add data to the new table

        Returns:
            new_table(Table): A new table generated by operation "BIN BY ZERO"

        """
        new_table = Table(self.instance,True,'BIN ' + self.names[column_id] + ' BY ZERO','')
        if get_head:
            new_table.column_num = new_table.tuple_num = 2
            new_table.names.extend([self.names[column_id], 'CNT(' + self.names[column_id] + ')'])
            new_table.types.extend([Type.categorical, Type.numerical])
            new_table.origins.extend([column_id, column_id])
        if get_data:
            new_table.D = [['>0', 0], ['<=0', 0]]
            for i in range(begin,end):
                if self.D[i][column_id] > 0:
                    new_table.D[0][1] += 1
                else:
                    new_table.D[1][1] += 1
        return new_table


    def getClassifyTable(self, classify_id, x_id, f, agg): # f: new_table(function), agg: aggregate
        """
        This function calls function f first, then assign the info to the data member of new table and
        return the new_table generated by function f.

        Args:
            classify_id(int): id of the column to be grouped
            x_id(int): id of the column to be dealt with
            f(function): dealWith* function to be called
            agg(bool): whether or not add 'CNT', 'SUM', 'AVG' operation to the new table

        Returns:
            new_table(Table): A new table generated by function f.

        """
        t = f(x_id,0,0,True,False)
        new_table = Table(self.instance, True, 'GROUP BY ' + self.names[classify_id], t.describe1)
        # t.tuple_num * self.features[classify_id].distinct 表示每个分类项（classify）都有t.tuple_num个数据
        new_table.tuple_num, new_table.column_num = t.tuple_num * self.features[classify_id].distinct, t.column_num
        new_table.names, new_table.types, new_table.origins = t.names[:], t.types[:], t.origins[:]
        new_table.classify_id = classify_id
        new_table.classify_num = self.features[classify_id].distinct
        new_table.classes = self.features[classify_id].distinct_values

        if not agg:
            for k in range(new_table.column_num):
                if new_table.names[k][0:4] == 'SUM(':
                    new_table.names[k] = new_table.names[k][4:-1]
                    new_table.types[k] = Type.numerical
                elif new_table.names[k][0:4] == 'AVG(' or new_table.names[k][0:4] == 'CNT(':
                    new_table.types[k] = Type.none

        begin_id = 0
        for k in range(self.features[classify_id].distinct):
            end_id = begin_id + self.features[classify_id].distinct_values[k][1]
            new_table.D.extend(f(x_id, begin_id, end_id, False, True).D)
            begin_id = end_id
        return new_table

    def transformTable(self):
        """
        generate new tables based on original table through group by and bin
        :return:
        """
        self.extract_feature()
        self.generateViews()

        new_tables=[]

        if self.transformed:
            return new_tables
        new_tables.extend(self.generateTables())
        new_tables.extend(self.generateClassifyTables())

        return new_tables

    def generateTables(self):
        """
        :return:
        """
        new_tables=[]

        # 对于未transformed的table进行transform操作
        for i in range(self.column_num):
            # 若该列i为时序或抽象类型且含有重复项，则分组操作，并根据分组，计算其他数值类型列的sum与avg。
            if self.features[i].ratio < 1.0 and (self.types[i] == Type.temporal or (self.types[i] == Type.categorical and self.features[i].distinct <= 20)):
                new_tables.append(self.dealWithGroup(i, 0, self.tuple_num, True, True))
            # 时序类型按时间划分操作
            if self.types[i] == Type.temporal:
                new_tables.append(self.dealWithIntervalBin(i,0,self.tuple_num,True,True))
                new_tables.append(self.dealWithWeekBin(i,0,self.tuple_num,True,True))
                if type(self.features[i].minmin) != type(datetime.date(1995, 10, 11)):
                    new_tables.append(self.dealWithHourBin(i,0,self.tuple_num,True,True))
            # 数值类型按0划分
            if self.types[i] == Type.numerical and self.features[i].minmin != '' and self.features[i].minmin < 0:
                new_tables.append(self.dealWithPNBin(i,0,self.tuple_num,True,True))

        return new_tables


    def generateClassifyTables(self):
        """

        :return:
        """

        new_tables=[]

        # 按抽象类型进行分类
        for i in range(self.column_num):
            # 对于类型为抽象类型，且不同值小于6（过多不易显示）的列 对i列进行分类
            if self.types[i] != Type.categorical or self.features[i].distinct > 6:
                continue

            self.D.sort(key=lambda tuple:tuple[i]) # 根据该列排序
            # 按i列分类
            new_table = Table(self.instance,True,'GROUP BY '+self.names[i],'')
            new_table.tuple_num = self.tuple_num
            new_table.D = [[] for tuple in range(self.tuple_num)]
            new_table.classify_id = i       # classify指分组后的数据项
            new_table.classify_num = self.features[i].distinct
            new_table.classes = self.features[i].distinct_values
            for j in range(self.column_num):
                if self.types[j] == Type.numerical:
                    new_table.names.append(self.names[j])
                    new_table.types.append(Type.numerical)
                    new_table.origins.append(j)
                    new_table.column_num += 1
                    for k in range(self.tuple_num):
                        new_table.D[k].append(self.D[k][j])
            new_tables.append(new_table)

            # 分类后 进行分组或划分
            for j in range(self.column_num):
                if i == j:
                    continue
                if (self.types[j] == Type.categorical and self.features[j].distinct <= 20) or self.types[j] == Type.temporal:
                    s = set()
                    for k in range(self.tuple_num):
                            s.add((self.D[k][i], self.D[k][j]))
                    if len(s) > self.features[j].distinct and ((self.types[j] == Type.categorical and self.features[i].distinct <= self.features[j].distinct) or self.types[j]==Type.temporal):
                        if len(s) == self.instance.tuple_num:
                            new_table = self.getClassifyTable(i, j, self.dealWithGroup, False)
                        else:
                            new_table = self.getClassifyTable(i, j, self.dealWithGroup, True)
                        new_tables.append(new_table)

                if self.types[j] == Type.temporal:
                    new_tables.append(self.getClassifyTable(i, j, self.dealWithIntervalBin, True))
                    new_tables.append(self.getClassifyTable(i, j, self.dealWithWeekBin, True))
                    if type(self.features[j].minmin) != type(datetime.date(1995, 10, 11)):
                        new_tables.append(self.getClassifyTable(i, j, self.dealWithHourBin, True))

                if self.types[j] == Type.numerical and self.features[j].minmin != '' and self.features[j].minmin < 0:
                    new_tables.append(self.getClassifyTable(i, j, self.dealWithPNBin, True))

        return new_tables
