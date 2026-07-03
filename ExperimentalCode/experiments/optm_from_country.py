# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 01:11:31 2025

@author: fengm
"""


import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(code_root)

from Dependencies.CodeDependencies import basic_params, func, param_data_loader
from copy import deepcopy
import numpy as np
import pandas as pd
from .elements import calc_once



import scipy.stats as stats
def get_lognormal_sample(central_value, ci_lower, ci_upper, sample_size, confidence = 0.95):
    alpha = 1 - confidence
    z_lower = stats.norm.ppf(alpha / 2)  # Z-score for 2.5th percentile
    z_upper = stats.norm.ppf(1 - alpha / 2)  # Z-score for 97.5th percentile
    sigma = (np.log(ci_upper) - np.log(ci_lower)) / (z_upper - z_lower)
    mu = np.log(central_value)
    return np.random.lognormal(mean=mu, sigma=sigma, size=sample_size)


def execute(expt_param, file_idx):
    n_samples = 25
    np.random.seed(file_idx * n_samples)
    mean_alpha, ci_lower_alpha, ci_upper_alpha = 2.826, 1.75, 4.7
    mean_beta, ci_lower_beta, ci_upper_beta = 5.665, 4.7, 6.9
    country = expt_param
    country_data =  param_data_loader.load_all_data([country], basic_params.group_div)
    mean_params, std_params, best_segment = func.fit_g(country_data[country]['confirmed'][:90] / country_data[country]['total_population'], basic_params.beginning[country], get_all_params = True)
    a_samples = np.random.normal(mean_params[0], std_params[0], n_samples)
    b_samples = np.random.normal(mean_params[1], std_params[1], n_samples)
    c_samples = np.random.normal(mean_params[2], std_params[2], n_samples)
    d_samples = np.random.normal(mean_params[3], std_params[3], n_samples)
    # import matplotlib.pyplot as plt
    # t_arr= np.arange(basic_params.beginning[country], 90)
    # plt.plot(t_arr, country_data[country]['confirmed'][basic_params.beginning[country]:90] / country_data[country]['total_population'], color = 'black')
    # plt.plot(t_arr, mean_params[0] * np.exp(mean_params[1] * (t_arr - mean_params[2])) + mean_params[3], color = 'orange')
    # plt.axvspan(xmin = best_segment[0] , xmax = best_segment[1], color='gray', alpha = 0.15, linewidth = 0)
    
    calc_params = deepcopy(basic_params.calc_params)
    calc_params.update({key: country_data[country][key] for key in ['populations', 'ifrs', 'ylls']})
    calc_params['contacts'] = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    alpha_samples = get_lognormal_sample(mean_alpha, ci_lower_alpha, ci_upper_alpha, n_samples)
    beta_samples = get_lognormal_sample(mean_beta, ci_lower_beta, ci_upper_beta, n_samples)
    res = {}
    for idx, (a, b, c, d, alpha, beta) in enumerate(zip(a_samples, b_samples, c_samples, d_samples, alpha_samples, beta_samples)):
        g_val = b
        srv_gen = func.srv_weibull(alpha, alpha, basic_params.srv_length, 1 / basic_params.day_div)
        calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
        r0 = func.calc_r0(g_val, alpha, beta, basic_params.srv_length, 1 / basic_params.day_div)
        print(r0, g_val)
        daily_vac = 0.14 / 100
        delay = 1400
        res_once = calc_once.simulate(calc_params, r0 = r0, get_curve = False, get_effr= True, get_empirical = False, vac_start = 30, daily_vac = daily_vac, vac_dur = None, delay = delay)
        res.update({f'{sheet_name}_{idx}': pd.DataFrame(sheet_data) for sheet_name, sheet_data in res_once.items()})
        res.update({f'transmission_params_{idx}': {'params': pd.Series([r0, g_val, alpha, beta, a, b, c, d, best_segment[0], best_segment[1]], 
                                                                       index = ['r0', 'growth_rate', 'alpha', 'beta', 'a', 'b', 'c', 'd', 'best_left', 'best_right'])}})
    return res


    
    