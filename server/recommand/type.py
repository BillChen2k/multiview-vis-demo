
class Type(object):
    none = 0
    categorical = 1
    numerical = 2
    temporal = 3

    @staticmethod
    def getType(s):
        """

        :param s: data type.
        :return: id for each type.
        """
        if len(s) >= 7 and s[0:7] == 'varchar':
            return Type.categorical
        elif len(s) >= 4 and s[0:4] == 'year':
            return Type.temporal
        elif len(s) >= 4 and s[0:4] == 'char':
            return Type.categorical
        elif len(s) >= 3 and s[0:3] == 'int':
            return Type.numerical
        elif s == 'int' or s == 'double' or s == 'float':
            return Type.numerical
        elif s == 'date' or s == 'datetime' or s == 'year':
            return Type.temporal
        else:
            return Type.none