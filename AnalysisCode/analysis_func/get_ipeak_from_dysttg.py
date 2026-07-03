# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 19:38:51 2025

@author: fengm
"""


from Dependencies.FrameDependencies import name_principle
import pandas as pd

def analyze(edata):
    expr_name = 'optm_from_dysttg_for_ipeak'
    expr_param = 'lower'
    file_idx = 0
    task_name = name_principle.get_task_name(expr_name, expr_param)
    anal_data = {}
    optm_targets = ['c', 'd', 'y']
    sttgs = ['under_20', '20-49', '20+', '60+', 'all_ages', 'zero_vac']
    sttgs += [f'gmin_{optm_target}' for optm_target in optm_targets] + [f'mgmin_{optm_target}' for optm_target in optm_targets]
    sttgs += [f'mmin_{optm_target}' for optm_target in optm_targets] + [f'min_{optm_target}' for optm_target in optm_targets]
    example_idx = [9, 42]
    for sttg in sttgs:
        anal_sheet_name = sttg
        expr_sheet_name = f'ipeak_{sttg}'
        anal_data[anal_sheet_name] = {'res': []}
        for e_idx in example_idx:
            anal_data[f'example_{e_idx}_{anal_sheet_name}'] = {}
        for file_idx in range(120):
            expr_data = edata[task_name][str(file_idx)]
            i_arr = expr_data[expr_sheet_name]['res'].to_numpy()
            anal_data[anal_sheet_name]['res'].append(max(i_arr))
            if file_idx in example_idx:
                anal_data[f'example_{file_idx}_{anal_sheet_name}']['res'] = i_arr
        anal_data[anal_sheet_name] = pd.DataFrame(anal_data[anal_sheet_name])
    return {sheet_name: pd.DataFrame(item) for sheet_name, item in anal_data.items()}