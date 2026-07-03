# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 12:39:05 2025

@author: MIFENG
"""



from Dependencies.CodeDependencies import basic_params, func, param_data_loader
from copy import deepcopy
import numpy as np
import pandas as pd
from .elements import calc_once

def execute(expr_param, file_idx):
    countries = ['United States']
    country_data = param_data_loader.load_all_data(countries, basic_params.group_div)
    calc_params = deepcopy(basic_params.calc_params)
    calc_params.update({key: country_data['United States'][key] for key in ['populations', 'ifrs', 'ylls']})
    calc_params['contacts'] = np.sum([country_data['United States']['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    srv_gen = func.srv_weibull(2.826, 5.665, basic_params.srv_length, 1 / basic_params.day_div)
    calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
    daily_vac = 0.35 / 100
    r0 = 2
    delay = 1400
    vac_eff = 0.95
    if expr_param == 'r0': r0 = 1.1 + file_idx * 0.1 / 3 #np.exp(file_idx * 0.075)
    elif expr_param == 'daily_vac': daily_vac = (0.11 + file_idx * 0.01) / 100
    elif expr_param == 'vac_eff': vac_eff = 0.22 + file_idx * 0.02
    else: pass
    res = calc_once.simulate(calc_params, r0 = r0, get_curve = False, get_grad = True, get_effr = True, vac_start = 30, daily_vac = daily_vac, delay = delay, vac_eff = vac_eff)
    return {sheet_name: pd.DataFrame(sheet_data) for sheet_name, sheet_data in res.items()}
