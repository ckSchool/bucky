import time, datetime, wx

from datetime import datetime, date

from calendar import timegm



if __name__ == '__main__':
    a = wx.DateTime.Today()

    print a

    print type(a)

    print a.FormatDate('dd/mm/yy')

