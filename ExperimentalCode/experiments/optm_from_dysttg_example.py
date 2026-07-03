# -*- coding: utf-8 -*-
"""
Created on Sat Jun 28 20:30:59 2025

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

def fit_rem_from_data(trans_data, step, init_params, **kwargs):
    data_len = len(trans_data['daily_infection'])
    removal_data = trans_data['removal'] - trans_data['removal'][0]
    
    def curve(params):
        rem_srv = 1 - np.exp(-params[0] * np.arange(data_len) * step)
        return np.convolve(rem_srv, trans_data['daily_infection'], 'full')[:data_len]
        
    def loss_func(params):
        return ((curve(params) - removal_data)**2).sum()
    
    init_p = init_params
    while True:
        res = minimize(loss_func, init_p, **kwargs)
        if res.success: return res, curve(res.x)
        else: init_p = init_params * np.random.rand(len(init_params))

def fit_inf_from_data(trans_data, step, mu, populations, contacts, k, init_params, **kwargs):
    group_amount = len(populations)
    totmat = contacts * populations[None, :] * k  
    data_len = len(trans_data['daily_infection_arr'])
    i_in_data = trans_data['daily_infection_arr'][:-1].T
    s_data = (1 - trans_data['confirmed_arr'][:-1]).T
    c_data_target = trans_data['confirmed_arr'][1:].T
    c_data0 = trans_data['confirmed_arr'][0:1].T
    
    def curve(params):
        cum_rate = params[0] * np.exp(- mu * np.arange(data_len) * step) * step
        inf_tmp = np.array([np.convolve(cum_rate, i_in_data[i], 'full')[:data_len - 1] for i in range(group_amount)]) 
        return ((1 - ((1 - inf_tmp).reshape((group_amount, data_len - 1, 1)) ** 
               totmat.T.reshape((group_amount, 1, group_amount))).prod(axis = 0)).T * s_data).cumsum(axis = 1) + c_data0
    
    def loss_func(params):
        return ((populations @ (curve(params) - c_data_target))**2).sum()
    
    init_p = init_params
    while True:
        res = minimize(loss_func, init_p, **kwargs)
        if res.success: return res, curve(res.x)
        else: init_p = init_params * np.random.rand(len(init_params))



def get_mean_from_weibull(alpha, beta):
    return beta * gamma(1 + 1.0 / alpha)

def get_beta_from_weibull(alpha, mean_value):
    return mean_value / gamma(1 + 1.0 / alpha)


def execute(expr_param, file_idx):
    countries = ['United States']
    country_data = param_data_loader.load_all_data(countries, basic_params.group_div)
    calc_params = deepcopy(basic_params.calc_params)
    calc_params.update({key: country_data['United States'][key] for key in ['populations', 'ifrs', 'ylls']})
    calc_params['contacts'] = np.sum([country_data['United States']['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    if expr_param in ['lower', 'higher']:
        alpha_inf, alpha_rem = {'lower': (1.5, 2.5)}[expr_param]
        mean_inf, mean_rem = 5, 7
        beta_inf = get_beta_from_weibull(alpha_inf, mean_inf)
        beta_rem = get_beta_from_weibull(alpha_rem, mean_rem)
        r0 = [1.55,][file_idx]
    elif expr_param == 'equal':
        alpha_inf, alpha_rem, beta_inf, beta_rem = 2.826, 2.826, 5.665, 5.665
        r0 = [1.5, 2, 2.5][file_idx]
    else: return None
    eigen_max = np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0])
    
    daily_vac = 0.35 / 100
    calc_params['eta'] = 0.95
    calc_params['delay'] = 1400
    c_level = 0.2
    vac_onset = 30
    
    beta_coef = func.find_weibull_coef_from_g(0.14, r0, alpha_inf, alpha_rem, beta_inf, beta_rem, 160000, 1 / basic_params.day_div)
    print(beta_coef)
    calc_params['srv_inf'] = func.srv_weibull(alpha_inf, beta_inf * beta_coef, basic_params.srv_length, 1 / basic_params.day_div)
    calc_params['srv_rem'] = func.srv_weibull(alpha_rem, beta_rem * beta_coef, basic_params.srv_length, 1 / basic_params.day_div)
    lambda_max = eigen_max * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem'])
    calc_params['k'] =  r0 / lambda_max
    steady_c = calc_params['populations'] @ func.get_steady_state(calc_params['k'], calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), basic_params.i0)
    fitting_calc = sir_delta(**calc_params)
    while True:
        if fitting_calc.getc_c_tot() >= basic_params.i0 + c_level * (steady_c - basic_params.i0): break
        fitting_calc.spread_once()
    
    params_fitting = {'method': 'SLSQP', 'tol': 1e-16, 'bounds': Bounds(np.ones(1) * 0.001, np.ones(1) * np.inf)}
    rem_trans_data = {'daily_infection': fitting_calc.get_i_in_tot(), 'removal': fitting_calc.get_r_tot()}
    rem_res, rem_curve = fit_rem_from_data(rem_trans_data, 1 / basic_params.day_div, init_params = np.ones(1), **params_fitting)
    inf_trans_data = {'daily_infection_arr': fitting_calc.get_i_in(), 'confirmed_arr': fitting_calc.get_c()}
    inf_res, cum_curve = fit_inf_from_data(inf_trans_data, 1 / basic_params.day_div, 
                                            mu = rem_res.x[0], populations = calc_params['populations'], contacts = calc_params['contacts'], k = calc_params['k'],
                                            init_params = np.ones(1), **params_fitting)
    del fitting_calc
    
    calc_params['srv_inf'] = func.srv_weibull(alpha_inf, beta_inf, basic_params.srv_length, 1 / basic_params.day_div)
    calc_params['srv_rem'] = func.srv_weibull(alpha_rem, beta_rem, basic_params.srv_length, 1 / basic_params.day_div)
    lambda_max = eigen_max * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem'])
    calc_params['k'] =  r0 / lambda_max
    optm_targets = ['c', 'd', 'y']
    sttgs = ['under_20', '20-49', '20+', '60+', 'all_ages', 'zero_vac', 'contact_first', 'ifr_first', 'yll_first']
    sttgs += [f'gmin_{optm_target}' for optm_target in optm_targets] + [f'mgmin_{optm_target}' for optm_target in optm_targets]
    sttgs += [f'mmin_{optm_target}' for optm_target in optm_targets] + [f'min_{optm_target}' for optm_target in optm_targets]
    prdt_target_types = {'min': ('non_mar', 'steady'), 'gmin': ('non_mar', 'trans'), 'mmin': ('mar', 'steady'), 'mgmin': ('mar', 'trans')}
    res = {}
    for sttg in sttgs:
        print(sttg)
        calc_non = sir_delta(**calc_params)
        calc_non.set_param_m(inf_res.x[0] * beta_coef, rem_res.x[0] * beta_coef)
        for i in range(vac_onset * basic_params.day_div):
            calc_non.spread_once()
        day_idx = 0
        while True:
            if calc_non.getc_x_tot('s') == 0 or day_idx >= 50: break
            if sttg.split('_')[0] in ['min', 'gmin', 'mmin', 'mgmin']: 
                prdt_type, target_type = prdt_target_types[sttg.split('_')[0]]
                alloc = calc_non.optimize_vac_alloc(daily_vac, target = sttg.split('_')[-1], disp = False, prdt_type = prdt_type, target_type = target_type)
            else: alloc = calc_non.empirical_alloc(daily_vac, sttg)
            calc_non.add_vaccination(alloc)
            for vac_idx in range(calc_non.get_day_div()):
                calc_non.spread_once()
            day_idx += 1
        for idx in range(200):
            for i in range(calc_non.get_day_div()):
                calc_non.spread_once()
        res[f'res_{sttg}'] = {'time_line': calc_non.get_time_line()}
        for target in basic_params.all_targets: res[f'res_{sttg}'][f'curve_{target}'] = calc_non.get_x_tot(target) 
    return {sheet_name: pd.DataFrame(sheet_data) for sheet_name, sheet_data in res.items()} 















