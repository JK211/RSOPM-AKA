#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This model is to compute storage cost of Terminal and CSP
the result will be saved to excel

2021/5/20
Jerry
"""
from results_data_record import excel_write

l = []
title = ['Data_CSP', 'Data_T']
l.append(title)
for i in range(1, 12):
    m = []
    CSP_i = (80*(630000+52560*i)+80*7600000000*pow(1+0.11, i))/(1000*1000*1000)      #  GB
    T_i = (80*(630000+52560*i)+64*2400000*pow(1+0.008, i))/(1000*1000)  # MB
    m.append(CSP_i)
    m.append(T_i)
    l.append(m)

file_name = r'D:\PythonProject\FUIH\simu_results_data\Storage_Cost_new.xlsx'
excel_write.save_excel(l, file_name)
