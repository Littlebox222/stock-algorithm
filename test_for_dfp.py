#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as ny
import pandas as pd
import tushare as ts

class KLine():
    def __init__(self,data_value):
        self.date = ""
        self.open = data_value.open
        self.high = data_value.high
        self.close = data_value.close
        self.low = data_value.low
        self.volume = data_value.volume
        self.price_change = data_value.price_change
        self.p_change = data_value.p_change
        self.ma5 = data_value.ma5
        self.ma10 = data_value.ma10
        self.ma20 = data_value.ma20
        self.v_ma5 = data_value.v_ma5
        self.v_ma10 = data_value.v_ma10
        self.v_ma20 = data_value.v_ma20
        self.turnover = data_value.turnover
        

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

    def is_big_volume(self):
        if self.volume > self.v_ma5 :
            return 1
        return 0

def get_data():
    data = ts.get_hist_data('600511', start="2017-12-11", end="2018-03-12")
    return data

IS_DEBUG = 1

if __name__ == '__main__':

    data = get_data()

    k_lines = []

    for i in range(0,len(data.index)) :
        k_line = KLine(data.loc[data.index[len(data.index)-1-i]])
        k_line.date = data.index[len(data.index)-1-i]
        k_lines.append(k_line)

    for i in range(0,len(k_lines)-1) :
        
        if not k_lines[i].is_high_up() :
            if IS_DEBUG : print k_lines[i].date, "not is_high_up"
            continue
        if not k_lines[i].is_big_volume() :
            if IS_DEBUG : print k_lines[i].date, "not is_big_volume"
            continue
        if not k_lines[i+1].is_star() :
            if IS_DEBUG : print k_lines[i].date, "t+1 not is_star"
            continue
        if not k_lines[i].volume > k_lines[i+1].volume :
            if IS_DEBUG : print k_lines[i].date, "volume not greater"
            continue

        print "------------ niubility ----------->>>", k_lines[i].date