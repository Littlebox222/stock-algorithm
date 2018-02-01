#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tushare as ts
import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np  
from scipy.interpolate import spline

should_update_stock_list = False

if should_update_stock_list :
	all_list = ts.get_stock_basics()
	all_list.to_csv('./stock_list.csv')

current_time = datetime.date.today()
end_time = current_time - datetime.timedelta(days=60)
start_time = end_time - datetime.timedelta(days=30)

# with open('stock_list.csv','rb') as csvfile:
#     reader = csv.DictReader(csvfile)
#     codes = [row['code'] for row in reader]


data = ts.get_k_data('601001', start=start_time.strftime("%Y-%m-%d"), end=end_time.strftime("%Y-%m-%d"))
point = data['open'] + (data['close'] - data['open'])/2

x = np.arange(0, len(point), 1) 
xnew = np.linspace(x.min(),x.max(),300)

point_smooth = spline(x,point,xnew)

plt.plot(point, 'ro-')
plt.plot(xnew, point_smooth)
plt.show()