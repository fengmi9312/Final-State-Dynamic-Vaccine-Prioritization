# -*- coding: utf-8 -*-
"""
Created on Sun Aug  3 13:53:31 2025

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
from Dependencies.CodeDependencies.model_alpha import epidemic_model
from Dependencies.CodeDependencies.model import sir_delta
from scipy.special import gamma

def get_mean_from_weibull(alpha, beta):
    return beta * gamma(1 + 1.0 / alpha)

def get_beta_from_weibull(alpha, mean_value):
    return mean_value / gamma(1 + 1.0 / alpha)

def get_sum_of_rem(srv_rem_prev, srv_rem_next):
    srv_rem_prev_len = np.where(srv_rem_prev <= 0)[0][0] if np.any(srv_rem_prev <= 0) else len(srv_rem_prev)
    dist_rem_prev = -np.diff(srv_rem_prev[:srv_rem_prev_len])
    srv_rem_next_len = np.where(srv_rem_next <= 0)[0][0] if np.any(srv_rem_next <= 0) else len(srv_rem_next)
    dist_rem_next = -np.diff(srv_rem_next[:srv_rem_next_len])
    dist_sum = np.append(0, np.convolve(dist_rem_prev, dist_rem_next))
    srv_rem_sum = 1 - np.append(0, np.cumsum(dist_sum))
    srv_rem_sum_len = np.where(srv_rem_sum <= 0)[0][0] if np.any(srv_rem_sum <= 0) else len(srv_rem_sum)
    return srv_rem_sum[:srv_rem_sum_len]

def get_cum(srv_inf, srv_rem):
    srv_inf_len = np.where(srv_inf <= 0)[0][0] if np.any(srv_inf <= 0) else len(srv_inf)
    srv_rem_len = np.where(srv_rem <= 0)[0][0] if np.any(srv_rem <= 0) else len(srv_rem)
    cum_len = min(srv_inf_len - 1, srv_rem_len)
    haz_inf = 1 - srv_inf[1:srv_inf_len] / srv_inf[:srv_inf_len - 1]
    haz_cum = haz_inf[:cum_len] * srv_rem[:cum_len]
    return haz_cum

def get_sum_of_cum(cum_prev, srv_rem_prev, cum_next):
    tmp0 = cum_prev
    dist_rem_prev = - np.diff(srv_rem_prev)
    tmp1 = np.append(0, np.convolve(dist_rem_prev, cum_next))
    tot_len = max(len(tmp0), len(tmp1))
    if len(tmp0) < tot_len: tmp0 = np.append(tmp0, np.zeros(tot_len - len(tmp0)))
    if len(tmp1) < tot_len: tmp1 = np.append(tmp1, np.zeros(tot_len - len(tmp1)))
    return tmp0 + tmp1
    
def arr_sum(a, b, alpha, beta):
    a_tmp, b_tmp = a, b
    tot_len = max(len(a_tmp), len(b_tmp))
    if len(a_tmp) < tot_len: a_tmp = np.append(a_tmp, np.zeros(tot_len - len(a_tmp)))
    if len(b_tmp) < tot_len: b_tmp = np.append(b_tmp, np.zeros(tot_len - len(b_tmp)))
    return alpha * a_tmp + beta * b_tmp

def execute(expr_param, file_idx):
    if expr_param != 'param' and file_idx != 0: return None
    countries = ['United States']
    country_data = param_data_loader.load_all_data(countries, basic_params.group_div)
    calc_params_basic = deepcopy(basic_params.calc_params)
    calc_params_basic.update({key: country_data['United States'][key] for key in ['populations', 'ifrs', 'ylls']})
    calc_params_basic['contacts'] = np.sum([country_data['United States']['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    
    eigen_max = np.max(np.linalg.eig(calc_params_basic['populations'][None, :] * calc_params_basic['contacts'])[0])
    calc_params_basic['i0'] = 0.001
    calc_params_basic['eta'] = 0.95
    calc_params_basic['delay'] = 1000
    r0 = 2

    asym_prob = 0.1

    exp_alpha_rem = 2.5
    exp_mean_rem = 4
    exp_beta_rem = get_beta_from_weibull(exp_alpha_rem, exp_mean_rem)
    asym_alpha_inf, asym_alpha_rem = 1.5, 2.5
    asym_mean_inf, asym_mean_rem = 5, 6
    asym_beta_inf = get_beta_from_weibull(asym_alpha_inf, asym_mean_inf)
    asym_beta_rem = get_beta_from_weibull(asym_alpha_rem, asym_mean_rem)
    presym_alpha_inf, presym_alpha_rem = 1.6, 2.4
    presym_mean_inf, presym_mean_rem = 2, 3
    presym_beta_inf = get_beta_from_weibull(presym_alpha_inf, presym_mean_inf)
    presym_beta_rem = get_beta_from_weibull(presym_alpha_rem, presym_mean_rem)
    sym_alpha_inf, sym_alpha_rem = 2, 3
    sym_mean_inf, sym_mean_rem = 3, 4
    sym_beta_inf = get_beta_from_weibull(sym_alpha_inf, sym_mean_inf)
    sym_beta_rem = get_beta_from_weibull(sym_alpha_rem, sym_mean_rem)

    exp_srv_rem = func.srv_weibull(exp_alpha_rem, exp_beta_rem, basic_params.srv_length, 1 / basic_params.day_div)
    exp_cum = np.zeros(len(exp_srv_rem))
    asym_srv_inf = func.srv_weibull(asym_alpha_inf, asym_beta_inf, basic_params.srv_length, 1 / basic_params.day_div)
    asym_srv_rem = func.srv_weibull(asym_alpha_rem, asym_beta_rem, basic_params.srv_length, 1 / basic_params.day_div)
    asym_cum = get_cum(asym_srv_inf, asym_srv_rem)
    presym_srv_inf = func.srv_weibull(presym_alpha_inf, presym_beta_inf, basic_params.srv_length, 1 / basic_params.day_div)
    presym_srv_rem = func.srv_weibull(presym_alpha_rem, presym_beta_rem, basic_params.srv_length, 1 / basic_params.day_div)
    presym_cum = get_cum(presym_srv_inf, presym_srv_rem)
    sym_srv_inf = func.srv_weibull(sym_alpha_inf, sym_beta_inf, basic_params.srv_length, 1 / basic_params.day_div)
    sym_srv_rem = func.srv_weibull(sym_alpha_rem, sym_beta_rem, basic_params.srv_length, 1 / basic_params.day_div)
    sym_cum = get_cum(sym_srv_inf, sym_srv_rem)


    tot_srv_rem = get_sum_of_rem(exp_srv_rem, arr_sum(asym_srv_rem, get_sum_of_rem(presym_srv_rem, sym_srv_rem), asym_prob, 1 - asym_prob))
    tot_haz_cum = get_sum_of_cum(exp_cum, exp_srv_rem, arr_sum(asym_cum, get_sum_of_cum(presym_cum, presym_srv_rem, sym_cum), asym_prob, 1 - asym_prob))
    tot_len = min(len(tot_srv_rem), len(tot_haz_cum))
    tot_srv_rem, tot_haz_cum = tot_srv_rem[:tot_len], tot_haz_cum[:tot_len]
    tot_haz_inf = tot_haz_cum / tot_srv_rem
    tot_srv_inf = np.cumprod(1 - np.append(0, tot_haz_inf))

    lambda_eff = np.log(1 / (1 - tot_haz_cum).prod())
    lambda_max = eigen_max * lambda_eff
    calc_params_basic['k'] =  r0 / lambda_max

    calc_params_alpha = deepcopy(calc_params_basic)
    calc_params_alpha['asym_prob'] =  asym_prob
    calc_params_alpha['exp_srv_rem'] = exp_srv_rem
    calc_params_alpha['asym_srv_inf'] = asym_srv_inf
    calc_params_alpha['asym_srv_rem'] = asym_srv_rem
    calc_params_alpha['presym_srv_inf'] = presym_srv_inf
    calc_params_alpha['presym_srv_rem'] = presym_srv_rem
    calc_params_alpha['sym_srv_inf'] = sym_srv_inf
    calc_params_alpha['sym_srv_rem'] = sym_srv_rem

    calc_params= deepcopy(calc_params_basic)
    calc_params['srv_inf'] = tot_srv_inf
    calc_params['srv_rem'] = tot_srv_rem
    calc_params['ifrs'] = (1 - asym_prob) * calc_params['ifrs']
    
    res = {}
    for vac in [True, False]:
        key = f"non_mar_alpha{'_vac' if vac else ''}"
        res[key] = {}
        calc_alpha = epidemic_model(**calc_params_alpha)
        for i in range(20000):
            if vac and i == 6000:
                calc_alpha.add_vaccination(calc_alpha.empirical_alloc(0.3, 'all_ages'))
            calc_alpha.spread_once()
        res[key]['time_line'] = calc_alpha.get_time_line()
        for target in ['s', 'exp', 'asym', 'presym', 'sym', 'w', 'r', 'v', 'p', 'c', 'd', 'y']:
            res[key][target] = calc_alpha.get_x_tot(target)

    
        key = f"non_mar{'_vac' if vac else ''}"
        res[key] = {}
        calc_non = sir_delta(**calc_params)
        for i in range(20000):
            if vac and i == 6000:
                calc_non.add_vaccination(calc_non.empirical_alloc(0.3, 'all_ages'))
            calc_non.spread_once()
        res[key]['time_line'] = calc_non.get_time_line()
        for target in ['s', 'w', 'r', 'v', 'p', 'c', 'd', 'y']:
            res[key][target] = calc_non.get_x_tot(target)    
        res[key]['exp'] = np.convolve(calc_non.get_x_tot('i_in'), exp_srv_rem)[:len(res[key]['time_line'])]
        asym_in =  np.append(0, np.convolve(calc_non.get_x_tot('i_in'), - asym_prob * np.diff(exp_srv_rem)))
        res[key]['asym'] = np.convolve(asym_in, asym_srv_rem)[:len(res[key]['time_line'])]
        presym_in =  np.append(0, np.convolve(calc_non.get_x_tot('i_in'), - (1 - asym_prob) * np.diff(exp_srv_rem)))
        res[key]['presym'] = np.convolve(presym_in, presym_srv_rem)[:len(res[key]['time_line'])]
        sym_in =  np.append(0, np.convolve(presym_in, - np.diff(presym_srv_rem)))
        res[key]['sym'] = np.convolve(sym_in, sym_srv_rem)[:len(res[key]['time_line'])]
        
    return {sheet_name: pd.DataFrame(sheet_data) for sheet_name, sheet_data in res.items()} 

if __name__ == '__main__':
    res = execute('param', 0)
    import matplotlib.pyplot as plt
    plt.plot(res['non_mar_alpha']['time_line'], res['non_mar_alpha']['c'], color = 'tab:red')
    plt.plot(res['non_mar']['time_line'], res['non_mar']['c'], color = 'tab:blue', linestyle = '--')
    
    
    
    
    
    
    
    
    
    
    
    
    
    