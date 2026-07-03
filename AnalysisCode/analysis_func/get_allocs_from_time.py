# -*- coding: utf-8 -*-
"""
Created on Thu May  1 13:51:14 2025

@author: fengm
"""


from Dependencies.FrameDependencies import name_principle
import pandas as pd
from Dependencies.CodeDependencies import  basic_params, param_data_loader
from itertools import product

def analyze(edata):
    expr_name = 'optm_from_example'
    expr_param = 'param'
    file_idx = 0
    task_name = name_principle.get_task_name(expr_name, expr_param)
    country = 'United States'
    countries = [country]
    country_data = param_data_loader.load_all_data(countries, basic_params.group_div)
    anal_data = {}
    optm_targets = ['c', 'd', 'y']
    empirical_sttgs = ['under_20', '20-49', '20+', '60+', 'all_ages', 'zero_vac']
    sttgs = empirical_sttgs + [f'min_{optm_target}' for optm_target in optm_targets]
    target_coef = {'c': country_data[country]['populations'], 'd': country_data[country]['populations'] * country_data[country]['ifrs'], 'y': country_data[country]['populations'] * country_data[country]['ifrs'] * country_data[country]['ylls'], }
    vac_len = [200, 80, 140, 60]
    for file_idx in range(12):
        expr_data = edata[task_name][str(file_idx)]
        
        for sttg in sttgs:
            anal_sheet_name = f'alloc_{sttg}_{file_idx}'
            expr_sheet_name = f'alloc_{sttg}'
            anal_data[anal_sheet_name] = {}
            for i in range(vac_len[file_idx // 3]):
                anal_data[anal_sheet_name][str(i)] = expr_data[expr_sheet_name][str(i)].to_numpy() * country_data['United States']['populations']
            anal_data[anal_sheet_name] = pd.DataFrame(anal_data[anal_sheet_name])
            
            for target, val_type in product(['c', 'd', 'y'], ['effr', 'dist']):
                anal_sheet_name = f'{val_type}_{sttg}_{target}_{file_idx}'
                expr_sheet_name = f"{val_type}_{sttg}" if val_type == 'dist' else f"{val_type}_{sttg}_{target}"
                anal_data[anal_sheet_name] = {}
                for i in range(vac_len[file_idx // 3]):
                    if val_type == 'dist': anal_data[anal_sheet_name][str(i)] = expr_data[expr_sheet_name][str(i)] * target_coef[target]
                    else: anal_data[anal_sheet_name][str(i)] = expr_data[expr_sheet_name][str(i)]
                anal_data[anal_sheet_name] = pd.DataFrame(anal_data[anal_sheet_name])
            
    return {sheet_name: pd.DataFrame(item) for sheet_name, item in anal_data.items()}