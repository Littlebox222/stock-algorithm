#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tushare as ts
import csv
import matplotlib.pyplot as plt
import numpy as np  
import datetime
from scipy.interpolate import spline

# 配置参数
should_update_stock_list = False # 是否更新全部股票列表
date_window = 30                 # 时间窗口
calculation_type = 'mean'        # 计算类型：mean，open，close

# 当前时间
current_time = datetime.datetime.now()

# 时间偏移，回退到最后一个交易日
if current_time.isoweekday() > 5 :
    date_offset = current_time.isoweekday() - 5
elif current_time.hour < 9 or (current_time.hour > 9 and current_time.hour < 10 and current_time.minute < 30) :
    date_offset = 1
else :
    date_offset = 0

# 更新股票列表
if should_update_stock_list :
    all_list = ts.get_stock_basics()
    all_list.to_csv('./stock_list.csv')

# 计算起止时间
end_time = current_time - datetime.timedelta(days=date_offset)
start_time = end_time - datetime.timedelta(days=date_window)

# 获取数据
# with open('stock_list.csv','rb') as csvfile:
#     reader = csv.DictReader(csvfile)
#     codes = [row['code'] for row in reader]


data = ts.get_k_data('601001', start=start_time.strftime("%Y-%m-%d"), end=end_time.strftime("%Y-%m-%d"))

if calculation_type == 'mean' :
    point = data['open'] + (data['close'] - data['open'])/2
elif calculation_type == 'open' :
    point = data['open']
else :
    point = data['close']


# 画图
x = np.arange(0, len(point), 1) 
xnew = np.linspace(x.min(),x.max(),300)

point_smooth = spline(x,point,xnew)

plt.plot(point, 'ro-')
plt.plot(xnew, point_smooth)
plt.grid()
plt.show()