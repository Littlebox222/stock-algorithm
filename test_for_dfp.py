#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tushare as ts

data = ts.get_k_data('002049', start="2018-01-01", end="2018-03-07")

print data