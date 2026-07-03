# -*- coding: utf-8 -*-
"""
Created on Tue May 27 00:28:21 2025

@author: fengm
"""




from Dependencies.CodeDependencies import basic_params, func, param_data_loader
from copy import deepcopy
import numpy as np
import pandas as pd
from .elements import calc_once


def execute(expt_param, file_idx):
    if expt_param != 'param': return None
    country = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea', 'Italy', 'Singapore'][file_idx]
    country_data =  param_data_loader.load_all_data([country], basic_params.group_div)
    mean_params, _, _ = func.fit_g(country_data[country]['confirmed'][:90] / country_data[country]['total_population'], basic_params.beginning[country], get_all_params = True)
    g_val = mean_params[1]
    alpha, beta = 2.826, 5.665
    calc_params = deepcopy(basic_params.calc_params)
    calc_params.update({key: country_data[country][key] for key in ['populations', 'ifrs', 'ylls']})
    calc_params['contacts'] = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    srv_gen = func.srv_weibull(alpha, beta, basic_params.srv_length, 1 / basic_params.day_div)
    calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
    r0 = func.calc_r0(g_val, alpha, beta, basic_params.srv_length, 1 / basic_params.day_div)
    daily_vac = 0.35 / 100
    delay = 1400
    res = calc_once.simulate(calc_params, r0 = r0, get_curve = False, get_effr= True, get_empirical = False, vac_start = 30, daily_vac = daily_vac, vac_dur = None, delay = delay)
    return {sheet_name: pd.DataFrame(sheet_data) for sheet_name, sheet_data in res.items()}