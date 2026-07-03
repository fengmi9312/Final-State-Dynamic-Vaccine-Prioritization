# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 15:10:52 2025

@author: MIFENG
"""

from Dependencies.FrameDependencies import name_principle
import itertools
import pandas as pd





def analyze(edata):
    expr_name = 'optm_from_example'
    expr_param = 'param'
    file_idx = 0
    task_name = name_principle.get_task_name(expr_name, expr_param)
    anal_data = {}
    optm_targets = ['c', 'd', 'y']
    empirical_sttgs = ['under_20', '20-49', '20+', '60+', 'all_ages', 'zero_vac']
    sttgs = ['no_vac'] + empirical_sttgs + [f'min_{optm_target}' for optm_target in optm_targets]
    for file_idx in range(12):
        expr_data = edata[task_name][str(file_idx)]
        for sttg, curve_target in itertools.product(sttgs, ['s', 'i', 'r', 'c', 'd', 'y']):
            anal_sheet_name = f'curve_{sttg}_{file_idx}'
            expr_sheet_name = f'curve_{sttg}'
            if curve_target == 's': anal_data[anal_sheet_name] = {'time_line': expr_data[expr_sheet_name]['time_line']}
            if not ((sttg.split('_')[0] == 'min' or sttg.split('_')[0] == 'tmin') and sttg.split('_')[-1] != curve_target):
                anal_data[anal_sheet_name][f'curve_{curve_target}'] = expr_data[expr_sheet_name][f'curve_{curve_target}']
            if curve_target == 'y': anal_data[anal_sheet_name] = pd.DataFrame(anal_data[anal_sheet_name])
            
            
            # if curve_target == 's' and sttg != 'no_vac': 
            #     sheet_name = f'alloc_{sttg}'
            #     res[sheet_name] = {}
            #     for i in range(120):
            #         res[sheet_name][str(i)] = expr_data[sheet_name][str(i)].to_numpy() * country_data['United States']['populations']
            # if curve_target in ['c', 'd', 'y'] and sttg != 'no_vac':
            #     sheet_name = f'effr_{sttg}_{curve_target}'
            #     res[sheet_name] = {}
            #     for i in range(120):
            #         for j in range(100): res[sheet_name][str(i * 100 + j)] = expr_data[sheet_name][str(i * 100 + j)].to_numpy()
    return {sheet_name: pd.DataFrame(item) for sheet_name, item in anal_data.items()}