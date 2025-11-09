# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 15:56:54 2025

@author: fengm
"""


from Dependencies.FrameDependencies import name_principle
import itertools
import pandas as pd



def analyze(edata):
    expr_name = 'optm_from_changing_example'
    expr_param = 'param'
    task_name = name_principle.get_task_name(expr_name, expr_param)
    anal_data = {}
    optm_targets = ['c', 'd', 'y']
    empirical_sttgs = ['under_20', '20-49', '20+', '60+', 'all_ages', 'zero_vac']
    sttgs = empirical_sttgs + [f'min_{optm_target}' for optm_target in optm_targets]
    for file_idx, r0_idx in itertools.product(range(2), range(2)):
        expr_data = edata[task_name][str(file_idx)]
        for sttg, curve_target in itertools.product(sttgs, ['s', 'i', 'r', 'c', 'd', 'y']):
            anal_sheet_name = f'curve_{sttg}_{file_idx}_{r0_idx}'
            expr_sheet_name = f'{sttg}_{r0_idx}'
            if curve_target == 's': anal_data[anal_sheet_name] = {'time_line': expr_data[expr_sheet_name]['time_line']}
            if not ((sttg.split('_')[0] == 'min') and sttg.split('_')[-1] != curve_target):
                anal_data[anal_sheet_name][f'curve_{curve_target}'] = expr_data[expr_sheet_name][f'curve_{curve_target}']
            if curve_target == 'y': anal_data[anal_sheet_name] = pd.DataFrame(anal_data[anal_sheet_name])
            
            if sttg[:3] == 'min':
                anal_sheet_name = f'alloc_{sttg}_{file_idx}_{r0_idx}'
                expr_sheet_name = f'alloc_{sttg}_{r0_idx}'
                anal_data[anal_sheet_name] = {}
                last_idx = expr_data[expr_sheet_name].columns[-1]
                for i in range(int(last_idx) + 1):
                    anal_data[anal_sheet_name][str(i)] = expr_data[expr_sheet_name][str(i)]
                anal_data[anal_sheet_name] = pd.DataFrame(anal_data[anal_sheet_name])
    return {sheet_name: pd.DataFrame(item) for sheet_name, item in anal_data.items()}
