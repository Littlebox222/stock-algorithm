#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as ny
import pandas as pd
import tushare as ts

class KLine():
    def __init__(self,data_value):
        data_list = data_value.tolist()
        self.date = data_list[0]
        self.open = data_list[1]
        self.close = data_list[2]
        self.high = data_list[3]
        self.low = data_list[4]
        self.volume = data_list[5]
        self.code = data_list[6]
        
data = ts.get_k_data('002049', start="2018-01-01", end="2018-03-07")

#data = ts.get_hist_data('002049', start="2018-01-01", end="2018-03-07")

print(data.values[0].tolist())
KLine0 = KLine(data.values[0])
print KLine0.date
print type(KLine0.date)
print KLine0.open
print KLine0.close
print KLine0.high
print KLine0.low
print KLine0.volume

print KLine0.code
print type(KLine0.code)

