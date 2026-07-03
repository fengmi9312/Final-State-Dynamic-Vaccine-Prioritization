# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 23:54:37 2025

@author: fengm
"""

if __name__ == '__main__':
    import os
    import sys
    root_level = 2
    code_root = os.path.dirname(os.path.abspath(__file__))
    for i in range(root_level): code_root = os.path.dirname(code_root)
    sys.path.append(code_root)

from Dependencies.CodeDependencies import basic_params, func, param_data_loader
from copy import deepcopy
import numpy as np
import pandas as pd
from Dependencies.CodeDependencies.model import sir_delta
from scipy.special import gamma
from scipy.optimize import fsolve, minimize, LinearConstraint, Bounds

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
    calc_params['i0'] = 0.001
    alpha_inf, alpha_rem = 1.5, 2.5
    mean_inf, mean_rem = 5, 7
    beta_inf = get_beta_from_weibull(alpha_inf, mean_inf)
    beta_rem = get_beta_from_weibull(alpha_rem, mean_rem)
    eigen_max = np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0])
    
    one_vac = 0.3
    calc_params['eta'] = 0.95
    calc_params['delay'] = 700
    c_level = 0.05
    
    r0 = 2
    calc_params['srv_inf'] = func.srv_weibull(alpha_inf, beta_inf, basic_params.srv_length, 1 / basic_params.day_div)
    calc_params['srv_rem'] = func.srv_weibull(alpha_rem, beta_rem, basic_params.srv_length, 1 / basic_params.day_div)
    lambda_max = eigen_max * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem'])
    calc_params['k'] =  r0 / lambda_max
    steady_c = calc_params['populations'] @ func.get_steady_state(calc_params['k'], calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), basic_params.i0)
   
    sttgs = ['under_20', '20-49', '20+', '60+', 'all_ages', 'no_vac', 'min_c', 'min_d', 'min_y']
    res = {}
    group_amount = len(calc_params['populations'])
    for sttg in sttgs:
        print(sttg)
        calc_non = sir_delta(**calc_params)
        delay_prdt = False
        prdt = calc_non.calc_prdt(prdt_type = 'non_mar', delay_prdt = delay_prdt)
        res[f'{sttg}_prdt'] = {str(i): [prdt[i]] for i in range(group_amount)}
        while True:
            if calc_non.getc_c_tot() >= basic_params.i0 + c_level * (steady_c - basic_params.i0): break
            calc_non.spread_once()
            prdt = calc_non.calc_prdt(prdt_type = 'non_mar', delay_prdt = delay_prdt)
            for i in range(group_amount): res[f'{sttg}_prdt'][str(i)].append(prdt[i])
            
        if sttg[:3] == 'min':
            alloc = calc_non.optimize_vac_alloc(one_vac, target = sttg[-1], disp = False, prdt_type = 'non_mar', target_type = 'steady')
            delay_prdt = True
            prdt = calc_non.calc_vac_prdt(alloc, prdt_type = 'non_mar')
            for i in range(group_amount): res[f'{sttg}_prdt'][str(i)][-1] = prdt[i]
            calc_non.add_vaccination(alloc)
        elif sttg == 'no_vac': 
            pass
        else:
            alloc = calc_non.empirical_alloc(one_vac, sttg)
            delay_prdt = True
            prdt = calc_non.calc_vac_prdt(alloc, prdt_type = 'non_mar')
            for i in range(group_amount): res[f'{sttg}_prdt'][str(i)][-1] = prdt[i]
            calc_non.add_vaccination(alloc)
            
        for idx in range(150 * calc_params['day_div']):
            calc_non.spread_once()
            prdt = calc_non.calc_prdt(prdt_type = 'non_mar', delay_prdt = delay_prdt)
            for i in range(group_amount): res[f'{sttg}_prdt'][str(i)].append(prdt[i])
            
        
        res_c = calc_non.get_c() 
        res_s = calc_non.get_s()
        res_v = calc_non.get_v()
        res[f'{sttg}_dist'] = {}
        if sttg == 'all_ages': 
            res[f'{sttg}_sarr'] = {}
            res[f'{sttg}_varr'] = {}
        for i in range(group_amount): 
            res[f'{sttg}_dist'][str(i)] = res_c.T[i]
            if sttg == 'all_ages': 
                res[f'{sttg}_sarr'][str(i)] = res_s.T[i]
                res[f'{sttg}_varr'][str(i)] = res_v.T[i]
        if sttg[:3] == 'min': res[f'{sttg}_alloc'] = {'alloc': alloc}
    return {sheet_name: pd.DataFrame(sheet_data) for sheet_name, sheet_data in res.items()} 

if __name__ == '__main__':
    res = execute('param', 0)










