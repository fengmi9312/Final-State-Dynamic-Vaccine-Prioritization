# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 15:40:15 2025

@author: MIFENG
"""


from Dependencies.FrameDependencies import name_principle
import itertools
import pandas as pd
import numpy as np
from Dependencies.CodeDependencies import basic_params, param_data_loader

def analyze(edata):
    anal_data = {}
    expr_name = 'optm_from_param'
    expr_params = ['r0', 'daily_vac', 'vac_dur', 'vac_eff']
    countries = ['United States']
    country_data = param_data_loader.load_all_data(countries, basic_params.group_div)['United States']
    pop_coef = {'c': country_data['populations'], 
                'd': country_data['populations'] * country_data['ifrs'], 
                'y': country_data['populations'] * country_data['ifrs'] * country_data['ylls']}
    for expr_param in expr_params:
        if expr_param != 'vac_dur': task_name = name_principle.get_task_name(expr_name, expr_param)
        else: task_name = name_principle.get_task_name(expr_name, 'r0')
        sheet_name = expr_param
        anal_data[sheet_name] = {}
        if expr_param == 'r0': anal_data[sheet_name][expr_param] = 1.1 + np.arange(120) * 0.1 / 3
        elif expr_param == 'daily_vac': anal_data[sheet_name][expr_param] = (0.11 + np.arange(40) * 0.01) / 100
        elif expr_param == 'delay': anal_data[sheet_name][expr_param] = np.arange(40) * 0.5
        elif expr_param == 'vac_dur': anal_data[sheet_name][expr_param] = np.arange(120) + 1
        elif expr_param == 'vac_eff': anal_data[sheet_name][expr_param] = np.arange(40) * 0.02 + 0.22
        else: pass
        for sttg, target in itertools.product(['zero_vac', 'under_20', '20-49', '20+', '60+', 'all_ages', 'min', 'gmin'], ['c', 'd', 'y']):
            if sttg == 'min' or sttg == 'gmin': rsttg = f'{sttg}_{target}'
            else: rsttg = sttg
            anal_data[sheet_name][f'prdt_{rsttg}_{target}'] = []
            if expr_param != 'vac_dur': anal_data[f'{sheet_name}_{rsttg}_{target}'] = {}
            for i in range(120 if expr_param in ['r0', 'vac_dur'] else 40):
                if expr_param != 'vac_dur':
                    last_idx = edata[task_name][str(i)][f'dist_{rsttg}'].columns[-1]
                    anal_data[sheet_name][f'prdt_{rsttg}_{target}'].append(edata[task_name][str(i)][f'dist_{rsttg}']['60' if 60 < int(last_idx) else last_idx].to_numpy() @ pop_coef[target])
                    anal_data[f'{sheet_name}_{rsttg}_{target}'][str(i)] = []
                    for j in range(40):
                        anal_data[f'{sheet_name}_{rsttg}_{target}'][str(i)].append(edata[task_name][str(i)][f'dist_{rsttg}'][str(j * 3) if j * 3 < int(last_idx) else last_idx].to_numpy() @ pop_coef[target])
                else:
                    anal_data[sheet_name][f'prdt_{rsttg}_{target}'].append(edata[task_name]['27'][f'dist_{rsttg}'][str(i)].to_numpy() @ pop_coef[target])
                
    return {sheet_name: pd.DataFrame(item) for sheet_name, item in anal_data.items()}