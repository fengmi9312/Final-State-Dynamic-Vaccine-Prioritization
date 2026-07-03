# -*- coding: utf-8 -*-
"""
Created on Fri May 30 13:54:17 2025

@author: MIFENG
"""

# import os
# import sys
# root_level = 2
# code_root = os.path.dirname(os.path.abspath(__file__))
# for i in range(root_level): code_root = os.path.dirname(code_root)
# sys.path.append(code_root)

import numpy as np
from copy import deepcopy
from Dependencies.CodeDependencies.model import sir_delta
from Dependencies.CodeDependencies import func, basic_params, param_data_loader
import pandas as pd

def execute(expr_param, file_idx):
    if expr_param != 'param' or file_idx != 0: return None
    countries = ['United States']
    country_data = param_data_loader.load_all_data(countries, basic_params.group_div)
    calc_params = deepcopy(basic_params.calc_params)
    calc_params.update({key: country_data['United States'][key] for key in ['populations', 'ifrs', 'ylls']})
    calc_params['contacts'] = np.sum([country_data['United States']['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    srv_gen = func.srv_weibull(2.826, 5.665, basic_params.srv_length, 1 / basic_params.day_div)
    calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
    delay, r0, vac_eff = 1400, 2, 0.95
    calc_params['k'] = r0 / (np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0]) * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
    calc_params['eta'] = vac_eff
    calc_params['delay'] = delay
    res = {'params': {'populations': calc_params['populations'], 'ifrs': calc_params['ifrs'], 'ylls': calc_params['ylls']}}
    one_vac = 0.1
    vac_points = np.array([3000, 6000, 9000])
    time_int_limit = 20000
    res['vac_alloc'] = {}
    res['vac_prdt'] = {}
    res['target_curve'] = {'time_line': np.arange(time_int_limit + 1) / basic_params.day_div}
    calc_models = {}
    for target in ['c', 'd', 'y']:
        main_model = sir_delta(**calc_params)
        calc_models[target] = []
        vac_idx = 0
        for i in range(time_int_limit):
            main_model.spread_once()
            for model_idx, calc_once in enumerate(calc_models[target]):
                calc_once.spread_once()
            if i in vac_points:
                calc_models[target].append(deepcopy(main_model))
                vac_alloc = main_model.optimize_vac_alloc(one_vac, target = target)
                res['vac_alloc'][f'{target}_{vac_idx}'] = vac_alloc
                res['vac_prdt'][f'{target}_{vac_idx}'] = [main_model.calc_vac_prdt_target(vac_alloc, target)]
                main_model.add_vaccination(vac_alloc)
                vac_idx += 1
        calc_models[target].append(main_model)
        for model_idx in range(len(vac_points) + 1):
            res['target_curve'][f'{target}_{model_idx}'] = calc_models[target][model_idx].get_x_tot(target = target)
    return {sheet_name: pd.DataFrame(sheet_data) for sheet_name, sheet_data in res.items()} 







