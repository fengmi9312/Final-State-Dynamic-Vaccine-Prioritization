# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 16:17:57 2025

@author: fengm
"""



from Dependencies.FrameDependencies import name_principle
import itertools
import pandas as pd





def analyze(edata):
    expr_name = 'optm_from_dysttg_example'
    file_idx_dict = {'lower': 1, 'equal': 3}
    anal_data = {}
    optm_targets = ['c', 'd', 'y']
    empirical_sttgs = ['under_20', '20-49', '20+', '60+', 'all_ages', 'zero_vac', 'contact_first', 'ifr_first', 'yll_first']
    sttgs = empirical_sttgs + empirical_sttgs + [f'min_{optm_target}' for optm_target in optm_targets] + empirical_sttgs + [f'gmin_{optm_target}' for optm_target in optm_targets]
    sttgs += empirical_sttgs + [f'mmin_{optm_target}' for optm_target in optm_targets] + empirical_sttgs + [f'mgmin_{optm_target}' for optm_target in optm_targets]
    for expr_param in ['lower', 'equal']:
        task_name = name_principle.get_task_name(expr_name, expr_param)
        for file_idx in range(file_idx_dict[expr_param]):
            expr_data = edata[task_name][str(file_idx)]
            for sttg, curve_target in itertools.product(sttgs, ['s', 'i', 'r', 'c', 'd', 'y']):
                anal_sheet_name = f'curve_{sttg}_{expr_param}_{file_idx}'
                expr_sheet_name = f'res_{sttg}'
                if curve_target == 's': anal_data[anal_sheet_name] = {'time_line': expr_data[expr_sheet_name]['time_line']}
                if not ((sttg.split('_')[0] == 'min' or sttg.split('_')[0] == 'tmin') and sttg.split('_')[-1] != curve_target):
                    anal_data[anal_sheet_name][f'curve_{curve_target}'] = expr_data[expr_sheet_name][f'curve_{curve_target}']
                if curve_target == 'y': anal_data[anal_sheet_name] = pd.DataFrame(anal_data[anal_sheet_name])
    return {sheet_name: pd.DataFrame(item) for sheet_name, item in anal_data.items()}