# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 16:05:49 2025

@author: MIFENG
"""

import numpy as np
from copy import deepcopy
from Dependencies.CodeDependencies.model import sir_delta
from Dependencies.CodeDependencies import func, basic_params, param_data_loader
import pandas as pd

def execute(expr_param, file_idx):
    if expr_param != 'param': return None
    countries = ['United States']
    country_data = param_data_loader.load_all_data(countries, basic_params.group_div)
    calc_params = deepcopy(basic_params.calc_params)
    calc_params.update({key: country_data['United States'][key] for key in ['populations', 'ifrs', 'ylls']})
    calc_params['contacts'] = np.sum([country_data['United States']['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    srv_gen = func.srv_weibull(2.826, 5.665, basic_params.srv_length, 1 / basic_params.day_div)
    calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
    delay, vac_eff = 1400, 0.95
    r0, updated_r0 = 1.5, 2.3
    calc_params['eta'] = vac_eff
    calc_params['delay'] = delay
    res = {'params': {'populations': calc_params['populations'], 'ifrs': calc_params['ifrs'], 'ylls': calc_params['ylls']}}
    daily_vac = 0.35 / 100
    vac_dur = 120
    changing_point = [150, 90][file_idx]
    start_point = [90, 30][file_idx]
    sttgs = ['zero_vac', 'under_20', '20-49', '20+', '60+', 'all_ages'] + [f'min_{optm_target}' for optm_target in ['c', 'd', 'y']]
    res = {}
    for r0_idx in range(2):
        models = {}
        calc_params['k'] = r0 / (np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0]) * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
        main_model = sir_delta(**calc_params)
        for i in range(start_point * main_model.get_day_div()):
            main_model.spread_once()
            if r0_idx == 1 and main_model.get_current_time_int() == main_model.get_day_div() * changing_point:
                main_model.set_k(updated_r0 / (np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0]) * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem'])))
        for sttg in sttgs:
            alloc_key = f'alloc_{sttg}_{r0_idx}'
            effr_key = f'effr_{sttg}_{r0_idx}'
            res[alloc_key] = {}
            for target in ['c', 'd', 'y']: res[f'{effr_key}_{target}'] = {}
            print(sttg, r0_idx)
            models[sttg] = deepcopy(main_model)
            for day_idx in range(vac_dur):
                if sttg.split('_')[0] == 'min': alloc =  models[sttg].optimize_vac_alloc(daily_vac, target = sttg.split('_')[-1], disp = False, tol = {'c': 1e-16, 'd': 1e-16, 'y': 1e-16}[sttg.split('_')[-1]])
                else: alloc = models[sttg].empirical_alloc(daily_vac, sttg)
                res[alloc_key][str(day_idx)] = alloc
                for target in ['c', 'd', 'y']: res[f'{effr_key}_{target}'][str(day_idx)] = models[sttg].calc_reduction_eff_target(target = target, vac_avail = None)
                models[sttg].add_vaccination(alloc)
                for vac_idx in range(models[sttg].get_day_div()):
                    models[sttg].spread_once()
                    if r0_idx == 1 and models[sttg].get_current_time_int() == models[sttg].get_day_div() * changing_point:
                        models[sttg].set_k(updated_r0 / (np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0]) * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem'])))
            vmark = models[sttg].get_current_time_int()
            while True:
                models[sttg].spread_once()
                if r0_idx == 1 and models[sttg].get_current_time_int() == models[sttg].get_day_div() * changing_point:
                    models[sttg].set_k(updated_r0 / (np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0]) * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem'])))
                c_time_int =  models[sttg].get_current_time_int()
                if c_time_int > 100 and  models[sttg].get_c_tot()[-1] -  models[sttg].get_c_tot()[-100] < 1e-5 and c_time_int >= vmark + 2 * calc_params['delay'] + 1: break
            curve_key = f'{sttg}_{r0_idx}'
            res[curve_key] = {}
            res[curve_key]['time_line'] = models[sttg].get_time_line()
            for target in basic_params.all_targets: res[curve_key][f'curve_{target}'] =  models[sttg].get_x_tot(target) 
        
    return {sheet_name: pd.DataFrame(sheet_data) for sheet_name, sheet_data in res.items()} 

# res.update(execute('param', 0))

# target = 'c'
# for target in ['c', 'd', 'y']:
#     colors = {'zero_vac': 'black', 'under_20': 'tab:blue', '20-49': 'tab:green', '20+': 'tab:brown', '60+': 'tab:gray', 'all_ages': 'tab:orange', 'min_c': 'tab:red', 'min_d': 'tab:red', 'min_y': 'tab:red'}
#     import matplotlib.pyplot as plt
#     for r0_idx in [0, 2]:
#         plt.figure()
#         for sttg in ['zero_vac', 'under_20', '20-49', '20+', '60+', 'all_ages', f'min_{target}']:
#             curve_key = f'{sttg}_{r0_idx}'
#             plt.plot(res[curve_key]['time_line'], res[curve_key][f'curve_{target}'], color = colors[sttg])





















