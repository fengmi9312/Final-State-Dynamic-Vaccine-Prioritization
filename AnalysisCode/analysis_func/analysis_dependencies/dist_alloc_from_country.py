# -*- coding: utf-8 -*-
"""
Created on Wed May  7 21:26:26 2025

@author: fengm
"""



from Dependencies.FrameDependencies import name_principle
import pandas as pd
import numpy as np
from itertools import product

def analyze(edata, country):
    anal_data = {'r0': {}}
    expr_names = ['optm_from_country', 'optm_from_country_add']
    sttgs = [['min_c', 'min_d', 'min_y', 'zero_vac'], ['min_c', 'min_d', 'min_y']]
    for expr_idx, expr_name in enumerate(expr_names):
        task_name = name_principle.get_task_name(expr_name, country)
        for sttg in sttgs[expr_idx]:
            dist_sttg = f'dist_{sttg}' if sttg == 'zero_vac' else f'dist_{sttg}_{expr_idx}'
            alloc_sttg = f'alloc_{sttg}' if sttg == 'zero_vac' else f'alloc_{sttg}_{expr_idx}'
            mean_alloc_sttg = f'mean_alloc_{sttg}' if sttg == 'zero_vac' else f'mean_alloc_{sttg}_{expr_idx}'
            lower_alloc_sttg = f'lower_alloc_{sttg}' if sttg == 'zero_vac' else f'lower_alloc_{sttg}_{expr_idx}'
            upper_alloc_sttg = f'upper_alloc_{sttg}' if sttg == 'zero_vac' else f'upper_alloc_{sttg}_{expr_idx}'
            anal_data[dist_sttg] = {}
            anal_data[alloc_sttg] = {}
            anal_data[mean_alloc_sttg] = {}
            anal_data[lower_alloc_sttg] = {}
            anal_data[upper_alloc_sttg] = {}
            alloc_res = []
            min_len = None
            for file_idx, sample_idx in product(range(40), range(25)):
                col_name = str(file_idx * 25 + sample_idx)
                last_idx = edata[task_name][str(file_idx)][f'dist_{sttg}_{sample_idx}'].columns[-1]
                idx = '119' if int(last_idx) >= 120 else last_idx
                anal_data[dist_sttg][col_name] = edata[task_name][str(file_idx)][f'dist_{sttg}_{sample_idx}'][idx]
                alloc = np.array([edata[task_name][str(file_idx)][f'alloc_{sttg}_{sample_idx}'][str(i)].to_numpy() for i in range(int(idx) + 1)])
                anal_data[alloc_sttg][col_name] = np.sum(alloc, axis = 0)
                alloc_res.append(alloc)
                if min_len is None or len(alloc) < min_len: min_len = len(alloc)
            for file_idx, sample_idx in product(range(40), range(25)):
                col_idx = file_idx * 25 + sample_idx
                alloc_res[col_idx] = alloc_res[col_idx][:min_len]
            alloc_res = np.array(alloc_res)
            mean_alloc_res = np.mean(alloc_res, axis = 0)
            sorted_alloc_res = np.sort(alloc_res, axis = 0)
            lower_alloc_res = sorted_alloc_res[49, :, :]
            upper_alloc_res = sorted_alloc_res[950, :, :]
            for i in range(min_len):
                anal_data[mean_alloc_sttg][str(i)] = mean_alloc_res[i]
                anal_data[lower_alloc_sttg][str(i)] = lower_alloc_res[i]
                anal_data[upper_alloc_sttg][str(i)] = upper_alloc_res[i]
        if expr_idx == 0:
            for file_idx, sample_idx in product(range(40), range(25)):
                col_name = str(file_idx * 25 + sample_idx)
                anal_data['r0'][col_name] = [edata[task_name][str(file_idx)][f'transmission_params_{sample_idx}'].loc['r0', 'params']]
    return {sheet_name: pd.DataFrame(item) for sheet_name, item in anal_data.items()}