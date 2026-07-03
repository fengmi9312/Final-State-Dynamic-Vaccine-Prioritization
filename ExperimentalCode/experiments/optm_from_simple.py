# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 14:51:03 2025

@author: fengm
"""

if __name__ == '__main__':
    import os
    import sys
    root_level = 2
    code_root = os.path.dirname(os.path.abspath(__file__))
    for i in range(root_level): code_root = os.path.dirname(code_root)
    sys.path.append(code_root)


import numpy as np
from copy import deepcopy
from Dependencies.CodeDependencies.model import sir_delta
from Dependencies.CodeDependencies import func, basic_params, param_data_loader
import pandas as pd
from scipy.special import gamma

def simple_optm_alloc(self, vac_avail, target):
    group_order = func.order_index(self.calc_reduction_eff_target(target = target))
    return self.order_alloc(vac_avail, group_order)[0]

def simple_daily_optm_alloc(self, vac_avail, target):
    vac_allocs = []
    c_time_int = self.get_current_time_int()
    for vac_idx in range(self.get_day_div()):
        vac_alloc = self.simple_optm_alloc(vac_avail / self.get_day_div(), target)
        vac_allocs.append(vac_alloc)
        self.add_vaccination(vac_alloc)
        self.spread_once()
    self.return_back(c_time_int, remain_v = False)
    return np.array(vac_allocs).sum(axis = 0)

sir_delta.simple_optm_alloc = simple_optm_alloc
sir_delta.simple_daily_optm_alloc = simple_daily_optm_alloc

def get_mean_from_weibull(alpha, beta):
    return beta * gamma(1 + 1.0 / alpha)

def get_beta_from_weibull(alpha, mean_value):
    return mean_value / gamma(1 + 1.0 / alpha)


def execute(expr_param, file_idx):
    if expr_param != 'param': return None
    countries = ['United States']
    country_data = param_data_loader.load_all_data(countries, basic_params.group_div)
    calc_params = deepcopy(basic_params.calc_params)
    calc_params.update({key: country_data['United States'][key] for key in ['populations', 'ifrs', 'ylls']})
    calc_params['contacts'] = np.sum([country_data['United States']['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    alpha_inf, alpha_rem = 1.5, 2.5
    mean_inf, mean_rem = 5, 7
    beta_inf = get_beta_from_weibull(alpha_inf, mean_inf)
    beta_rem = get_beta_from_weibull(alpha_rem, mean_rem)
    eigen_max = np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0])
    
    daily_vac = 0.35 / 100
    calc_params['eta'] = 0.95
    calc_params['delay'] = 1400
    vac_onset = 30
    
    r0 = 1.1 + file_idx * 0.1 / 3
    
    
    calc_params['srv_inf'] = func.srv_weibull(alpha_inf, beta_inf, basic_params.srv_length, 1 / basic_params.day_div)
    calc_params['srv_rem'] = func.srv_weibull(alpha_rem, beta_rem, basic_params.srv_length, 1 / basic_params.day_div)
    lambda_max = eigen_max * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem'])
    calc_params['k'] =  r0 / lambda_max
    optm_targets = ['c']
    sttgs = [f'min_{optm_target}' for optm_target in optm_targets]
    sttgs += [f'simp_{optm_target}' for optm_target in optm_targets] + [f'dsimp_{optm_target}' for optm_target in optm_targets]
    res = {}
    for sttg in sttgs:
        print(sttg)
        res[f'allocs_{sttg}'] = {}
        res[f'prdts_{sttg}'] = {}
        calc_non = sir_delta(**calc_params)
        for i in range(vac_onset * basic_params.day_div):
            calc_non.spread_once()
        day_idx = 0
        while True:
            if calc_non.getc_x_tot('s') == 0:  break
            target = sttg.split('_')[-1]
            if sttg.split('_')[0] in ['min', 'dsimp']:
                if sttg.split('_')[0] == 'min': alloc = calc_non.optimize_vac_alloc(daily_vac, target = sttg.split('_')[-1], disp = False, prdt_type = 'non_mar', target_type = 'steady')
                else: alloc = calc_non.simple_daily_optm_alloc(daily_vac, target)
                res[f'allocs_{sttg}'][str(day_idx)] = alloc
                res[f'prdts_{sttg}'][str(day_idx)] = calc_non.calc_vac_prdt(alloc)
                calc_non.add_vaccination(alloc)
                for vac_idx in range(calc_non.get_day_div()):
                    calc_non.spread_once()
                day_idx += 1
            elif sttg.split('_')[0] == 'simp':
                allocs = []
                for vac_idx in range(calc_non.get_day_div()):
                    alloc = calc_non.simple_optm_alloc(daily_vac / calc_non.get_day_div(), target)
                    allocs.append(alloc)
                    calc_non.add_vaccination(alloc)
                    calc_non.spread_once()
                res[f'allocs_{sttg}'][str(day_idx)] = np.array(allocs).sum(axis = 0)
                res[f'prdts_{sttg}'][str(day_idx)] = calc_non.calc_prdt()
                day_idx += 1
            else: pass
    return {sheet_name: pd.DataFrame(sheet_data) for sheet_name, sheet_data in res.items()} 

if __name__ == '__main__':
    res = execute('param', 12)