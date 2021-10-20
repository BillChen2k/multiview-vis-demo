
class Features(object):
    """
    Store the attributes of a column in the table, such as min, max, etc.
    Attributes:
        name(str): 该列列名
        type(Type): 该列类型
        origin(list): 来自原始表的哪一列
        min(float): 该列数据最小值
        max(float): 该列数据最大值
        distinct(int): 该列不同元组的个数
        ratio(float): 该列不同元组数与总元组数比值
        minmin(float): 该列各分类中最小值
    """
    def __init__(self, name, type, origin):
        self.name = name
        self.type = type
        self.origin = origin
        self.min = self.minmin = self.max = self.distinct = self.ratio = self.bin_num = 0
        self.interval = ''
        self.distinct_values = []
        self.interval_bins = []
