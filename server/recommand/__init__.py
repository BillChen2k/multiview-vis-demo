import os
import sys

from pprint import *
import pandas as pd
import re # use regular expressions when recognizing the date type

from pyecharts.charts import Bar, Line, Scatter, Pie, Grid, Page
from pyecharts import options as opts

from recommand.table import Table
from recommand.type import Type
from recommand.chart import Chart
from recommand.instance import Instance

class myrecommend(object):
    """
    Attributes:
        is_table_info(bool): Whether or not the table info has been completely set.
        table_name(str): the name of the table to be visualized.
        column_names(list): the name of each column in the table.
        column_types(list): the type of each column in the table.
        csv_path(str): the path of the csv dataset to be visualized.
        csv_dataframe(pandas.Dataframe): Dataframe of table.
        instance(Instance): an Instance object corresponding to the dataset.
    """
    def __init__(self):
        self.is_table_info = False


    def read_csv(self,path):
        """
        read csv file
        :param path:
        cols: columns to read.
        :return:
        """
        self.csv_path = path

        try:
            fh = open(self.csv_path, "r")
        except IOError:
            print("Error: no such file or directory")

        # 不读第一行列名 只取数据
        self.csv_dataframe = pd.DataFrame(pd.read_csv(self.csv_path, header=0, keep_default_na=False)).dropna(axis=0, how='any')
        # 包含第一行列名
        test = pd.DataFrame(pd.read_csv(self.csv_path)).dropna(axis=0, how='any')

        # 创建types数组 初始为0
        types = [0 for i in range(len(test.dtypes))]
        # 读取第一行，去除结尾回车符
        a = fh.readline()
        a = a[:-1] # remove '\n'
        # 得到每列列名
        x = a.split(',') # x stores the name of each column
        fh.close()

        #type transformation
        for i in range(len(test.dtypes)):
            if test.dtypes[i].name[0:3] == 'int' or test.dtypes[i].name[0:5] == 'float':
                if (x[i][0] == "'" or x[i][0] == '"'):
                    x[i] = x[i].replace('\'', '').replace('"', '')
                for j in test[x[i]]:
                    if not (j == 0 or (j > 1000 and j < 2100)):
                        types[i] = test.dtypes[i].name[0:5]
                        break
                    else:
                        types[i] = 'year'
            elif test.dtypes[i].name[0:6] == 'object':
                if (x[i][0] == "'" or x[i][0] == '"'):
                    x[i] = x[i].replace('\'', '').replace('"', '')
                for j in test[x[i]]:
                    if j != 0 and not(re.search(r'\d+[/-]\d+[/-]\d+', j)):
                        types[i] = 'varchar'
                        break
                    else:
                        types[i] = 'date'

        name = path.rsplit('/', 1)[-1][:-4]
        self.set_table_info(name, x, types)

    def set_table_info(self,name,column_info,*column_info2):
        """
        set table info
        :return:
        """
        self.table_name = name
        self.column_names = []
        self.column_types = []
        if isinstance(column_info,list) and isinstance(column_info2[0],list):
            self.column_names = column_info
            self.column_types = column_info2[0]
        for idx, val in enumerate(self.column_types):
            if Type.getType(val.lower()) == 0: # not a normal type
                raise Exception("doesnt support this column_type \' %s \' of column name \' %s \',please check Readme for specification " %(val,self.column_names[idx]))
        self.is_table_info = True

    def init_instance(self,instance):
        """
        initialize the info of instance and format data type.
        :param instance
        :return:
            the instance object with the infomation(names, types, etc.)
            initialized attributions as follow:
            instance.column_num,
            instance.tables[0].names[],
            instance.tables[0].types[],
            instance.tables[0].origins[],
            instance.tables[0].tuple_num,
            instance.tuple_num,
        """
        instance.addTable(Table(instance,False,'',''))
        table_origin = self.csv_dataframe
        in_column_num = len(self.column_names)
        in_column_name = self.column_names
        in_column_type = self.column_types

        # 初始化instance，加入初始表的names、types、origin、tuple_num等信息
        instance.column_num = instance.tables[0].column_num = in_column_num
        for i in range(instance.column_num):
            instance.tables[0].names.append(in_column_name[i])
            instance.tables[0].types.append(Type.getType(in_column_type[i].lower()))# table.origins[]: 数据的来自哪列
        instance.tables[0].origins = [i for i in range(instance.tables[0].column_num)]# 获取数据的行数
        instance.tuple_num = instance.tables[0].tuple_num = table_origin.shape[0]
        # 统一时间格式
        for i in range(instance.tables[0].column_num):
            if instance.tables[0].types[i] == 3:
                col_name = table_origin.columns[i]
                col_type = self.column_types[i]
                self.date_format(col_name,col_type)
          #对于类型为时间的列重置列名
        for i in range(len(table_origin.columns)):
            table_origin.rename(columns={ table_origin.columns[i] : in_column_name[i] }, inplace=True)

        # D中存放出师表的全部数据，dataframe to list
        instance.tables[0].D = table_origin.values.tolist()
        return instance

    def date_format(self,col_name,col_type):
        """
        uniform date format
        :param col_name:
        :param col_type:
        :return:
        """
        table = self.csv_dataframe
        if col_type == 'date':
            table[col_name] = pd.to_datetime(table[col_name]).dt.date
        elif col_type == 'datetime':
            table[col_name] = pd.to_datetime(table[col_name]).dt.to_pydatetime()
        elif col_type == 'year':
            table[col_name] = pd.to_datetime(table[col_name].apply(lambda x: str(x)+'/1/1')).dt.date

    def generate_all_views(self,instance):
        """
        generate tables and generate all views from each tables
        :param instance
        :return:
        """
        if len(instance.tables[0].D) == 0:
            print ('no data in table')
            sys.exit(0)
        # 对出师表进行数据处理，处理后的数据生成多张新table
        instance.addTables(instance.tables[0].transformTable())

        # 对每张table生成visualization nodes
        begin_id = 1
        while begin_id < instance.table_num:
            instance.tables[begin_id].extract_feature()
            instance.tables[begin_id].generateViews()
            begin_id += 1
        if instance.view_num == 0:
            print ('no chart generated')
            sys.exit(0)
        return instance

    def ranking(self):
        """
        rank the views based on scores
        :return:
        """
        instance = Instance(self.table_name)
        instance = self.init_instance(instance)
        instance = self.generate_all_views(instance)
        instance.getW()
        instance.getE()
        instance.getA()
        instance.getScore()
        self.instance = instance

    # output function
    def to_list(self):
        """
        export as list type

        Args:
            None

        Returns:
            the export list

        """
        export_list = self.output('list')
        return export_list

    def to_single_html(self):
        """
        convert to html by pyecharts and output to single html file

        Args:
            None

        Returns:
            None

        """
        # self.error_throw('output')
        self.output('single_html')

    def output(self, output_method):
        """
        output function of partial_order and learning_to_rank for all kinds of output

        Args:
            output_method(str): output method:
                                list: to list
                                print: print to console
                                single_json/multiple_jsons: single/multiple json file(s)
                                single_html/multiple_htmls: single/multiple html file(s)

        Returns:
            None

        """
        instance = self.instance
        export_list = []
        order1 = order2 = 1
        old_view = ''
        if output_method == 'list':
            for i in range(instance.view_num):
                view = instance.tables[instance.views[i].table_pos].views[instance.views[i].view_pos]
                if old_view:
                    order2 = 1
                    order1 += 1
                export_list.append(view.output(order1))
                old_view = view
            return export_list
        elif output_method == 'print':
            for i in range(instance.view_num):
                view = instance.tables[instance.views[i].table_pos].views[instance.views[i].view_pos]
                if old_view:
                    order2 = 1
                    order1 += 1
                pprint (view.output(order1))
                old_view = view
            return
        elif output_method == 'single_json' or output_method == 'multiple_jsons':
            path2 = os.getcwd() + '/json/'
            if not os.path.exists(path2):
                os.mkdir(path2)
            if output_method == 'single_json':
                f = open(path2 + self.table_name + '.json','w')
                for i in range(instance.view_num):
                    view = instance.tables[instance.views[i].table_pos].views[instance.views[i].view_pos]
                    if old_view:
                        order2 = 1
                        order1 += 1
                    f.write(view.output(order1) + '\n')
                    old_view = view
                f.close() # Notice that f.close() is out of the loop to create only one file
            else: # if output_method == 'multiple_jsons'
                for i in range(instance.view_num):
                    view = instance.tables[instance.views[i].table_pos].views[instance.views[i].view_pos]
                    if old_view:
                        order2 = 1
                        order1 += 1
                    f = open(path2 + self.table_name + str(order1) + '.json','w')
                    f.write(view.output(order1))
                    f.close() # Notice that f.close() is in the loop to create multiple files
                    old_view = view
            return
        elif output_method == 'single_html' or output_method == 'multiple_htmls':
            path2 = os.getcwd() + '/html/'
            if not os.path.exists(path2):
                os.mkdir(path2)
            page = Page()
            if output_method == 'single_html':
                self.page = Page()
                for i in range(instance.view_num):
                    view = instance.tables[instance.views[i].table_pos].views[instance.views[i].view_pos]
                    if old_view:
                        order2 = 1
                        order1 += 1
                    old_view = view
                    self.html_output(order1, view, 'single')
                self.page.render('./html/' + self.table_name + '_all' + '.html')
            else: # if output_method == 'multiple_htmls'
                path3 = os.getcwd() + '/html/' + self.table_name
                if not os.path.exists(path3):
                    os.mkdir(path3)
                for i in range(instance.view_num):
                    view = instance.tables[instance.views[i].table_pos].views[instance.views[i].view_pos]
                    if old_view:
                        order2 = 1
                        order1 += 1
                    old_view = view
                    self.html_output(order1, view, 'multiple')
            return

    def html_output(self, order, view, mode):
        """
        output function of html

        Args:
            order(int): diversified_ranking use different order
            view(View): view object
            mode(str): single or multiple

        Returns:
            None

        """
        instance = self.instance
        data = {}
        data['order'] = order
        data['chartname'] = instance.table_name
        data['describe'] = view.table.describe
        data['x_name'] = view.fx.name
        data['y_name'] = view.fy.name
        data['chart'] = Chart.chart[view.chart]
        data['classify'] = [v[0] for v in view.table.classes]
        data['x_data'] = view.X
        data['y_data'] = view.Y
        data['title_top'] = 5

        [chart,filename] = self.html_handle(data)
        grid = Grid()
        grid.add(chart, grid_opts=opts.GridOpts(pos_bottom='20%', pos_top='20%'))
        if mode == 'single':
            self.page.add(grid) #the grid is added in the same page
        elif mode == 'multiple':
            grid.render('./html/' + self.table_name + '/' + filename) #the grid is added in a new file

    def html_handle(self,data):
        """
        convert function to html by pyecharts

        Args:
            data(dict): the data info

        Returns:
            chart: chart generated by pyecharts: Bar, Pie, Line or Scatter
            filename: html file name

        """

        filename = self.table_name + str(data['order']) + '.html'
        margin = str(data['title_top']) + '%'
        # 设置图标基本属性
        if data['chart'] == 'bar':
            chart = (Bar().set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                     .set_global_opts(title_opts=opts.TitleOpts(title=data['chartname'], subtitle=data['describe'], pos_left='center', pos_top=margin),
                                      xaxis_opts=opts.AxisOpts(name=data['x_name']),
                                      yaxis_opts=opts.AxisOpts(name=data['y_name'], splitline_opts=opts.SplitLineOpts(is_show=True))))
        elif data['chart'] == 'pie':
            chart = (Pie().set_global_opts(title_opts=opts.TitleOpts(title=data['chartname'], subtitle=data['describe'], pos_left='center', pos_top=margin)))
        elif data['chart'] == 'line':
            chart = (Line().set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                     .set_global_opts(title_opts=opts.TitleOpts(title=data['chartname'], subtitle=data['describe'], pos_left='center', pos_top=margin),
                                      xaxis_opts=opts.AxisOpts(name=data['x_name']),
                                      yaxis_opts=opts.AxisOpts(name=data['y_name'], splitline_opts=opts.SplitLineOpts(is_show=True))))
        elif data['chart']== 'scatter':
            chart = (Scatter().set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                     .set_global_opts(title_opts=opts.TitleOpts(title=data['chartname'], subtitle=data['describe'], pos_left='center', pos_top=margin),
                                      xaxis_opts=opts.AxisOpts(type_='value', name=data['x_name'], splitline_opts=opts.SplitLineOpts(is_show=True)),
                                      yaxis_opts=opts.AxisOpts(type_='value', name=data['y_name'], splitline_opts=opts.SplitLineOpts(is_show=True))))
        else :
            print ("not valid chart")

        if not data["classify"]: # 在图片上只需展示一组数据
            attr = data["x_data"][0] # 横坐标
            val = data["y_data"][0] # 纵坐标
            if data['chart'] == 'bar':
                chart.add_xaxis(attr).add_yaxis("", val, label_opts=opts.LabelOpts(is_show=False))
            elif data['chart'] == 'line':
                chart.add_xaxis(attr).add_yaxis("", val, label_opts=opts.LabelOpts(is_show=False))
            elif data['chart'] == 'pie':
                chart.add("", [list(z) for z in zip(attr, val)])
            elif data['chart'] == 'scatter':
                if isinstance(attr[0], str):
                    attr = [x for x in attr if x != '']
                    attr = list(map(float, attr))
                if isinstance(val[0], str):
                    val = [x for x in val if x != '']
                    val = list(map(float, val))
                chart.add_xaxis(attr).add_yaxis("", val, label_opts=opts.LabelOpts(is_show=False))
        else : # 在图片上需要展示多组数据
            attr = data["x_data"][0] # 横坐标
            for i in range(len(data["classify"])) : # 循环输出每组数据
                val = data["y_data"][i] # 每组纵坐标的值
                # name = (data["classify"][i][0] if mytype(data["classify"][i]) == type(('a', 'b')) else data["classify"][i])
                name = data["classify"][i]
                if i == 0:
                    if data['chart'] != 'pie' and data['chart'] != 'scatter':
                        chart.add_xaxis(attr)
                if data['chart'] == 'bar':
                    chart.add_yaxis(name, val, stack="stack1", label_opts=opts.LabelOpts(is_show=False))
                elif data['chart'] == 'line':
                    chart.add_yaxis(name, val, label_opts=opts.LabelOpts(is_show=False))
                elif data['chart'] == 'pie':
                    chart.add("", [list(z) for z in zip(attr, val)])
                elif data['chart'] == 'scatter':
                    attr_scatter = data["x_data"][i]
                    if isinstance(attr_scatter[0], str): # 去除散点图的空点，并将字符类型转化为数字类型
                        attr_scatter = [x for x in attr_scatter if x != '']
                        attr_scatter = list(map(float, attr_scatter))
                    if isinstance(val[0], str):
                        val = [x for x in val if x != '']
                        val = list(map(float, val))
                    chart.add_xaxis(attr_scatter).add_yaxis(name, val, label_opts=opts.LabelOpts(is_show=False))
        return chart,filename