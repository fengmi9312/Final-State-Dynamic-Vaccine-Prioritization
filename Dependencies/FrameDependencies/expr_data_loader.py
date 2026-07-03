# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 22:51:03 2025

@author: fengm
"""

import pandas as pd
from . import name_principle

def load_certain_edata(expr_name, expr_param, file_amount):
    task_name = name_principle.get_task_name(expr_name, expr_param)
    res = {task_name: {}}
    for file_idx in range(file_amount):
        res[task_name][str(file_idx)] = pd.read_excel(name_principle.analysis_file(task_name, file_idx), index_col = 0, sheet_name = None)
    print(task_name + ' imported')
    return res

def load_edata(key_dict):
    res = {}
    for expr_name, expr_param_infos in key_dict.items():
        for expr_param, file_amount in expr_param_infos.items():
            res.update(load_certain_edata(expr_name, expr_param, file_amount))
    return res

def load_one_certain_edata(expr_name, expr_param, file_idx_list):
    task_name = name_principle.get_task_name(expr_name, expr_param)
    res = {task_name: {}}
    for file_idx in file_idx_list:
        res[task_name][str(file_idx)] = pd.read_excel(name_principle.analysis_file(task_name, file_idx), index_col = 0, sheet_name = None)
        print(task_name + ' imported')
    return res