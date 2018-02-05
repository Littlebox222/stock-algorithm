#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tushare as ts
import csv
import matplotlib.pyplot as plt
import numpy as np
import datetime
from scipy.interpolate import spline

def get_min_point( points ):

    min_points = []

    if len(points) < 3 :
        return []

    for i in range(1,len(points)-1) :
        if points[i] < points[i-1] and points[i] <= points[i+1] :
            min_points.append([i,points[i]])

    return min_points;

def mean_filter( points, width ):

    if window_width%2 == 0:
        print "Error: window_width 必须是奇数"
        return []

    mean_filter_output = []

    if len(points) < width :
        return []

    for i in range(0,(width-1)/2) :
        mean_filter_output.append(points[i])

    for i in range((width-1)/2,len(points) - (width-1)/2) :
        sum_value = 0.
        for j in range(-(width-1)/2,(width-1)/2+1) :
            sum_value += points[i+j]
        mean_filter_output.append(sum_value/width)

    for i in range(len(points)-(width-1)/2,len(points)) :
        mean_filter_output.append(points[i])

    return mean_filter_output;

# 配置参数
should_update_stock_list = False # 是否更新全部股票列表
should_plot = True               # 是否画图
date_window = 60                 # 时间窗口
calculation_type = 'close'       # 计算类型：high，low，close
window_width = 3                 # 均值滤波窗口大小

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

data = ts.get_k_data('002027', start=start_time.strftime("%Y-%m-%d"), end=end_time.strftime("%Y-%m-%d"))

if calculation_type == 'high' :
    point = data['high']
elif calculation_type == 'low' :
    point = data['low']
else :
    point = data['close']

point = list(point)

# 画图
if should_plot :

    plt.subplot2grid((1,4),(0,0))
    plt.plot(point)
    plt.grid()
    plt.title(u"原始数据")

    mean_filtered_point = mean_filter(point,window_width)
    plt.subplot2grid((1,4),(0,1))
    plt.plot(mean_filtered_point)
    plt.grid()
    plt.title(u"1次均值滤波")

    mean_filtered_point = mean_filter(mean_filtered_point,window_width)
    plt.subplot2grid((1,4),(0,2))
    plt.plot(mean_filtered_point)
    plt.grid()
    plt.title(u"2次均值滤波")

    mean_filtered_point = mean_filter(mean_filtered_point,window_width)
    plt.subplot2grid((1,4),(0,3))
    plt.plot(mean_filtered_point)
    plt.grid()
    plt.title(u"3次均值滤波")

    plt.show()