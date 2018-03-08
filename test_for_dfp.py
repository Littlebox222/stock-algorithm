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

    def is_up(self):
        if self.close > self.open :
            return 1
        return 0

    def is_high_up(self):
        if not self.is_up() :
            return 0
        if (self.close - self.open)/self.open > 0.03 :
            return 1
        return 0

    def is_star(self):
        if self.is_up() and abs(self.open - self.close)/self.open < 0.005 :
            return 1
        elif not self.is_up() and abs(self.open - self.close)/self.close < 0.005 :
            return 1
        return 0

    def is_big_volume(self, mean_volume):
        if self.volume > mean_volume :
            return 1
        return 0

def get_data():
    data = ts.get_k_data('002049', start="2017-12-11", end="2018-03-08")
    return data


if __name__ == '__main__':

    data = get_data()
    k_lines = []

    for i in range(0,len(data.values)) :
        k_lines.append(KLine(data.values[i]))

    sum_volume = 0
    for i in range(0,len(k_lines)) :
        sum_volume += k_lines[i].volume
    mean_volume = sum_volume/len(k_lines)

    for i in range(0,len(k_lines)-1) :
        if      k_lines[i].is_high_up() \
            and k_lines[i].is_big_volume(mean_volume) \
            and k_lines[i+1].is_star() \
            and k_lines[i].volume > k_lines[i+1].volume \
            and k_lines[i].close >= k_lines[i+1].close \
            and k_lines[i].close >= k_lines[i+1].open :
            #再加一个判断：十字星的最低点高于5日均线

            print k_lines[i].date