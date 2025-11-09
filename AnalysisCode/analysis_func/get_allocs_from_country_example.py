# -*- coding: utf-8 -*-
"""
Created on Tue May 27 12:47:52 2025

@author: MIFENG
"""


from Dependencies.FrameDependencies import name_principle
import pandas as pd
from Dependencies.CodeDependencies import  basic_params, param_data_loader
from itertools import product

def analyze(edata):
    expr_name = 'optm_from_country_example'
    expr_param = 'param'
    task_name = name_principle.get_task_name(expr_name, expr_param)
    countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea', 'Italy', 'Singapore']
    country_data = param_data_loader.load_all_data(countries, basic_params.group_div)
    anal_data = {}
    optm_targets = ['c', 'd', 'y']
    sttgs = [f'min_{optm_target}' for optm_target in optm_targets]
    for file_idx, country in enumerate(countries):
        expr_data = edata[task_name][str(file_idx)]
        target_coef = {'c': country_data[country]['populations'], 'd': country_data[country]['populations'] * country_data[country]['ifrs'], 'y': country_data[country]['populations'] * country_data[country]['ifrs'] * country_data[country]['ylls'], }
        for sttg in sttgs:
            anal_sheet_name = f'alloc_{sttg}_{basic_params.country_abbr[country]}'
            expr_sheet_name = f'alloc_{sttg}'
            anal_data[anal_sheet_name] = {}
            last_idx = expr_data[expr_sheet_name].columns[-1]
            for i in range(int(last_idx) + 1):
                anal_data[anal_sheet_name][str(i)] = expr_data[expr_sheet_name][str(i)].to_numpy() * country_data[country]['populations']
            anal_data[anal_sheet_name] = pd.DataFrame(anal_data[anal_sheet_name])
            
            for target, val_type in product(['c', 'd', 'y'], ['effr', 'dist']):
                anal_sheet_name = f'{val_type}_{sttg}_{target}_{basic_params.country_abbr[country]}'
                expr_sheet_name = f"{val_type}_{sttg}" if val_type == 'dist' else f"{val_type}_{sttg}_{target}"
                anal_data[anal_sheet_name] = {}
                last_idx = expr_data[expr_sheet_name].columns[-1]
                for i in range(int(last_idx) + 1):
                    if val_type == 'dist': anal_data[anal_sheet_name][str(i)] = expr_data[expr_sheet_name][str(i)] * target_coef[target]
                    else: anal_data[anal_sheet_name][str(i)] = expr_data[expr_sheet_name][str(i)]
                anal_data[anal_sheet_name] = pd.DataFrame(anal_data[anal_sheet_name])
            
    return {sheet_name: pd.DataFrame(item) for sheet_name, item in anal_data.items()}