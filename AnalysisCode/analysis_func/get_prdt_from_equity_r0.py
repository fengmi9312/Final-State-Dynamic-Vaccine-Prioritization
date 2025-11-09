# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 15:18:37 2025

@author: fengm
"""


from Dependencies.FrameDependencies import name_principle
import itertools
import pandas as pd
import numpy as np
from Dependencies.CodeDependencies import basic_params, param_data_loader

def analyze(edata):
    anal_data = {}
    expr_name = 'optm_from_equity_r0'
    expr_param = 'param'
    task_name = name_principle.get_task_name(expr_name, expr_param)
    countries = ['United States']
    country_data = param_data_loader.load_all_data(countries, basic_params.group_div)['United States']
    basic_ifrs = country_data['ifrs']
    for rsttg, vac_deadline in itertools.product(['zero_vac', 'under_20', '20-49', '20+', '60+', 'all_ages', 'contact_first', 'ifr_first', 'yll_first', 'min_d', 'gmin_d', 'mmin_d', 'mgmin_d'], [29, 59, 89, 119]):
        sheet_name = f'{rsttg}_{vac_deadline}'
        anal_data[sheet_name] = {}
        for file_idx in range(40):
            mean_ifrs = basic_ifrs.mean() * np.ones_like(basic_ifrs)
            diff_ifrs = basic_ifrs - mean_ifrs
            ifrs = mean_ifrs + (file_idx / 39) * diff_ifrs
            pop_coef = country_data['populations'] * ifrs
            anal_data[sheet_name][str(file_idx)] = []
            for r0_idx in range(40):
                last_idx = edata[task_name][str(file_idx)][f'prdts_{rsttg}_{r0_idx}'].columns[-1]
                anal_data[sheet_name][str(file_idx)].append(edata[task_name][str(file_idx)][f'prdts_{rsttg}_{r0_idx}'][str(vac_deadline) if vac_deadline < int(last_idx) else last_idx].to_numpy() @ pop_coef)
    return {sheet_name: pd.DataFrame(item) for sheet_name, item in anal_data.items()}