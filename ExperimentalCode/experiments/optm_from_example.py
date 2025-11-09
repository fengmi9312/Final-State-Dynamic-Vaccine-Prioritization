# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 01:11:31 2025

@author: fengm
"""


from Dependencies.CodeDependencies import basic_params, func, param_data_loader
from copy import deepcopy
import numpy as np
import pandas as pd
from .elements import calc_once, calc_once_n


def execute(expt_param, file_idx):
    countries = ['United States']
    country_data = param_data_loader.load_all_data(countries, basic_params.group_div)
    calc_params = deepcopy(basic_params.calc_params)
    calc_params.update({key: country_data['United States'][key] for key in ['populations', 'ifrs', 'ylls']})
    calc_params['contacts'] = np.sum([country_data['United States']['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    #calc_params['ifrs'] =  calc_params['ifrs'] + 0.5 * (calc_params['ifrs'].mean() - calc_params['ifrs'])
    srv_gen = func.srv_weibull(2.826, 5.665, basic_params.srv_length, 1 / basic_params.day_div)
    calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
    delay = 1400
    daily_vac, r0, vac_dur = [[0.35 / 100, 1.5, 200], [0.14 / 100, 1.5, 200], [0.07 / 100, 1.5, 200], 
                              [0.35 / 100, 2.5, 80], [0.14 / 100, 2.5, 80], [0.07 / 100, 2.5, 80], 
                              [0.35 / 100, 2, 140], [0.14 / 100, 2, 140], [0.07 / 100, 2, 140],
                              [0.35 / 100, 1.5, 60], [0.35 / 100, 2, 60], [0.35 / 100, 2.5, 60]][file_idx]
    res = calc_once.simulate(calc_params, r0 = r0, get_curve = True, get_effr= True, get_trans = True, vac_start = 30, daily_vac = daily_vac, vac_dur = vac_dur, delay = delay, tols = {'c': 1e-16, 'd': 1e-16, 'y': 1e-18})
    return {sheet_name: pd.DataFrame(sheet_data) for sheet_name, sheet_data in res.items()}


# from scipy.stats import pearsonr
# import matplotlib.pyplot as plt
# for target in ['c']:
#     fig, axes = plt.subplots(2, 2, figsize = (12, 12))
#     for ax_idx, ax in enumerate(axes[0]):
#         ctype = ['curve', 'prdt'][ax_idx]
#         plt.sca(ax)
#         colors = {'no_vac': 'black', 'all_ages': 'tab:brown', 'under_20': 'tab:gray', 
#                   '20-49': 'tab:pink', '20+': 'tab:orange', '60+': 'tab:purple'}
#         for sttg in colors.keys():
#             plt.plot(res[f'curve_{sttg}']['time_line'], res[f'curve_{sttg}'][f'{ctype}_{target}'], color = colors[sttg])
#         colors = {'steady':'tab:blue'}
#         linestyles = {'trans': '-', 'mar': '--', 'steady':':'}
#         for sttg in colors.keys():
#             plt.plot(res[f'curve_min_{sttg}_{target}']['time_line'], 
#                       res[f'curve_min_{sttg}_{target}'][f'{ctype}_{target}'], 
#                       color = colors[sttg], linestyle = linestyles[sttg])
            
#     for ax_idx, ax in enumerate(axes[1]):
#         plt.sca(ax)
#         sttg = ['20-49', f'min_steady_{target}'][ax_idx]
#         ys = np.array([res[f'effr_{sttg}_{target}'][str(i)] for i in range(vac_dur)]).T
#         colors = ['tab:blue', 'tab:red', 'tab:green', 'tab:orange', 'tab:gray', 'tab:purple', 'tab:pink', 'black']
#         for i in range(8): plt.plot(np.arange(vac_dur) * 0.01, ys[i], color = colors[i])
        
    
    
    
    
    
    
    