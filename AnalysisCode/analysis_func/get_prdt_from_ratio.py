# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 07:58:04 2025

@author: fengm
"""



from Dependencies.FrameDependencies import name_principle
import itertools
import pandas as pd
import numpy as np
from Dependencies.CodeDependencies import basic_params, param_data_loader
import scipy.special as sc

def get_ratio(alpha_inf, alpha_rem):
    return sc.gamma((alpha_inf + 1) / alpha_rem) / (sc.gamma(alpha_inf / alpha_rem) * sc.gamma(1 + 1.0 / alpha_rem))

def analyze(edata):
    vac_deadline = 30 - 1
    anal_data = {}
    expr_name = 'optm_from_ratio'
    expr_params = ['param']
    countries = ['United States']
    country_data = param_data_loader.load_all_data(countries, basic_params.group_div)['United States']
    pop_coef = {'c': country_data['populations'], 
                'd': country_data['populations'] * country_data['ifrs'], 
                'y': country_data['populations'] * country_data['ifrs'] * country_data['ylls']}
    for expr_param in expr_params:
        task_name = name_principle.get_task_name(expr_name, expr_param)
        sheet_name = 'res'
        anal_data[sheet_name] = {'ratio': get_ratio(1 + np.arange(41) * 0.05, 2)}
        for sttg, target in itertools.product(['zero_vac', 'under_20', '20-49', '20+', '60+', 'all_ages', 'min', 'gmin', 'mmin', 'mgmin'], ['c', 'd', 'y']):
            if sttg in ['min', 'gmin', 'mmin', 'mgmin']: rsttg = f'{sttg}_{target}'
            else: rsttg = sttg
            anal_data[sheet_name][f'prdt_{rsttg}_{target}'] = []
            for ratio_idx in range(41):
                last_idx = edata[task_name][str(ratio_idx)][f'prdts_{rsttg}'].columns[-1]
                anal_data[sheet_name][f'prdt_{rsttg}_{target}'].append(edata[task_name][str(ratio_idx)][f'prdts_{rsttg}'][str(vac_deadline) if vac_deadline < int(last_idx) else last_idx].to_numpy() @ pop_coef[target])
         
        for sttg, target in itertools.product(['zero_vac', 'under_20', '20-49', '20+', '60+', 'all_ages', 'min', 'gmin', 'mmin', 'mgmin'], ['c', 'd', 'y']):
            if sttg in ['min', 'gmin', 'mmin', 'mgmin']: rsttg = f'{sttg}_{target}'
            else: rsttg = sttg
            sheet_name = f'{rsttg}_{target}'
            anal_data[sheet_name] = {'ratio': np.arange(1, 121)}   
            for ratio_idx in range(41):
                anal_data[sheet_name][str(ratio_idx)] = []
                last_idx = edata[task_name][str(ratio_idx)][f'prdts_{rsttg}'].columns[-1]
                for i in range(0, 120):
                    anal_data[sheet_name][str(ratio_idx)].append(edata[task_name][str(ratio_idx)][f'prdts_{rsttg}'][str(i) if i < int(last_idx) else last_idx].to_numpy() @ pop_coef[target])
    return {sheet_name: pd.DataFrame(item) for sheet_name, item in anal_data.items()}