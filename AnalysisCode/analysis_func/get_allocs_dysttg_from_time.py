# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 19:38:51 2025

@author: fengm
"""


from Dependencies.FrameDependencies import name_principle
import pandas as pd
from Dependencies.CodeDependencies import  basic_params, param_data_loader
from itertools import product

def analyze(edata):
    expr_name = 'optm_from_dysttg'
    expr_param = 'lower'
    file_idx = 0
    task_name = name_principle.get_task_name(expr_name, expr_param)
    country = 'United States'
    countries = [country]
    country_data = param_data_loader.load_all_data(countries, basic_params.group_div)
    anal_data = {}
    optm_targets = ['c', 'd', 'y']
    sttgs = [f'min_{optm_target}' for optm_target in optm_targets] + [f'gmin_{optm_target}' for optm_target in optm_targets]
    sttgs += [f'mmin_{optm_target}' for optm_target in optm_targets] + [f'mgmin_{optm_target}' for optm_target in optm_targets]
    vac_len = 30
    for file_idx in [9, 42]:
        expr_data = edata[task_name][str(file_idx)]
        for sttg in sttgs:
            anal_sheet_name = f'alloc_{sttg}_{file_idx}'
            expr_sheet_name = f'allocs_{sttg}'
            anal_data[anal_sheet_name] = {}
            last_idx = int(expr_data[expr_sheet_name].columns[-1])
            for i in range(min(vac_len, last_idx + 1)):
                anal_data[anal_sheet_name][str(i)] = expr_data[expr_sheet_name][str(i)].to_numpy() * country_data['United States']['populations']
            anal_data[anal_sheet_name] = pd.DataFrame(anal_data[anal_sheet_name])
    return {sheet_name: pd.DataFrame(item) for sheet_name, item in anal_data.items()}