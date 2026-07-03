#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 12:02:09 2025

@author: mifeng
"""


if __name__ == '__main__':
    import os
    import sys
    root_level = 2
    code_root = os.path.dirname(os.path.abspath(__file__))
    for i in range(root_level): code_root = os.path.dirname(code_root)
    sys.path.append(code_root)
    from elements import metapopulation_simulation as ms
else:
    from .elements import metapopulation_simulation as ms

from Dependencies.CodeDependencies import basic_params, func, param_data_loader
from copy import deepcopy
import numpy as np
import pandas as pd
from scipy.special import gamma

def get_mean_from_weibull(alpha, beta):
    return beta * gamma(1 + 1.0 / alpha)

def get_beta_from_weibull(alpha, mean_value):
    return mean_value / gamma(1 + 1.0 / alpha)

def execute(expr_param, file_idx):
    countries = ['United States']
    country_data = param_data_loader.load_all_data(countries, basic_params.group_div)
    params = deepcopy(basic_params.calc_params)
    params.update({key: country_data['United States'][key] for key in ['populations', 'ifrs', 'ylls']})
    params['contacts'] = np.sum([country_data['United States']['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    simu_structure_params = {'node_amount':12000, 'group_amount': 8, 'populations':params['populations'], 
                             'contacts': params['contacts'], 'ifrs': params['ifrs'], 'ylls': params['ylls'], 'k': 1, 'step': 1 / params['day_div'], 'time': 0}
    
    alpha_inf, alpha_rem = 1.5, 2.5
    mean_inf, mean_rem = 5, 7
    beta_inf = get_beta_from_weibull(alpha_inf, mean_inf)
    beta_rem = get_beta_from_weibull(alpha_rem, mean_rem)
    
    srv_inf = func.srv_weibull(alpha_inf, beta_inf, basic_params.srv_length, 1 / basic_params.day_div)
    srv_rem = func.srv_weibull(alpha_rem, beta_rem, basic_params.srv_length, 1 / basic_params.day_div)
    eigen_max = np.max(np.linalg.eig(params['populations'][None, :] * params['contacts'])[0])
    lambda_eff = func.lambda_eff_weibull(alpha_inf, beta_inf, alpha_rem, beta_rem)
    lambda_max = eigen_max * lambda_eff
    print(lambda_max)
    simu_structure_params['k'] =  2 / lambda_max
    simu_vaccination_params = {'delay': 1400, 'eta': 0.95}
    res = {}
    for seed_idx in range(100):
        print(seed_idx)
        simu_once = ms.simu(**simu_structure_params)
        simu_once.set_generator_seed(seed_idx)
        simu_once.set_spreading_func('weibull', 'weibull')
        simu_once.set_total_spreading_params([alpha_inf, beta_inf], [alpha_rem, beta_rem])
        simu_once.set_amount_seeds(np.ones(8) * 15, 0)
        res.update({f'time_line_{seed_idx}': [simu_once.get_time()], f'c_{seed_idx}': [simu_once.get_x_amount('c')]})
        for i in range(10000):
            simu_once.spread_once()
            res[f'time_line_{seed_idx}'].append(simu_once.get_time())
            res[f'c_{seed_idx}'].append(simu_once.get_x_amount('c'))
            
        simu_once = ms.simu(**simu_structure_params)
        simu_once.set_generator_seed(seed_idx)
        simu_once.set_spreading_func('weibull', 'weibull')
        simu_once.set_total_spreading_params([alpha_inf, beta_inf], [alpha_rem, beta_rem])
        simu_once.set_amount_seeds(np.ones(8) * 15, 0)
        res.update({f'equiv_time_line_{seed_idx}': [simu_once.get_time()], f'equiv_c_{seed_idx}': [simu_once.get_x_amount('c')]})
        
        for i in range(2000):
            simu_once.spread_once()
            res[f'equiv_time_line_{seed_idx}'].append(simu_once.get_time())
            res[f'equiv_c_{seed_idx}'].append(simu_once.get_x_amount('c'))
            
        current_time = simu_once.get_time()
        inf_list = []
        rem_list = []
        for group_idx, group_size in enumerate(simu_once.get_population_amounts()):
            inf_list.append([])
            rem_list.append([])
            for node_idx in range(group_size):
                node_state = simu_once.get_node_state(group_idx, node_idx)
                if node_state == 'i': 
                    tau = current_time - simu_once.get_node_trans_time(group_idx, node_idx)
                    inf_list[-1].append([1, 1 / func.lambda_eff_inc_weibull(alpha_inf, beta_inf, alpha_rem, beta_rem, tau)])
                else:
                    inf_list[-1].append([1, 1 / lambda_eff])
                rem_list[-1].append([1, 1])
                    
        simu_once.set_spreading_func('weibull', 'weibull')
        simu_once.set_detailed_spreading_params(inf_list, rem_list)
        
        for group_idx, group_size in enumerate(simu_once.get_population_amounts()):
            for node_idx in range(group_size):
                simu_once.reset_trans_time()
                simu_once.reset_rem_time()
        
        for i in range(8000):
            simu_once.spread_once()
            res[f'equiv_time_line_{seed_idx}'].append(simu_once.get_time())
            res[f'equiv_c_{seed_idx}'].append(simu_once.get_x_amount('c'))
            
            
        
    return res

if __name__ == '__main__':
    res = execute(None, None)
    import matplotlib.pyplot as plt
    for seed_idx in range(100):
        plt.plot(res[f'time_line_{seed_idx}'], res[f'c_{seed_idx}'], linewidth = 0.1, color = 'tab:red')
        plt.plot(res[f'equiv_time_line_{seed_idx}'], res[f'equiv_c_{seed_idx}'], linewidth = 0.1, color = 'tab:blue')