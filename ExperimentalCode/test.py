# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 11:06:16 2025

@author: MIFENG
"""


import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(code_root)
import numpy as np
from copy import deepcopy
from Dependencies.CodeDependencies.model import sir_delta
from Dependencies.CodeDependencies import func, basic_params, param_data_loader

countries = ['United States']
country_data = param_data_loader.load_all_data(countries, basic_params.group_div)
calc_params = deepcopy(basic_params.calc_params)
calc_params.update({key: country_data['United States'][key] for key in ['populations', 'ifrs', 'ylls']})
calc_params['contacts'] = np.sum([country_data['United States']['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
srv_gen = func.srv_weibull(2.826, 5.665, basic_params.srv_length, basic_params.step)
calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
r0 = 2
k_val = r0 / (np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0]) * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
calc_params['k'] = k_val
calc_params['eta'] = 0.95
calc_params['delay'] = 400
calc_params['i0'] = np.eye(8)[1]
steady_c = func.get_steady_state(k_val, calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), _i = calc_params['i0']) @ calc_params['populations']
init_c = calc_params['i0'] @ calc_params['populations']

res = []
for i in range(10):
    calc_params['i0'] = np.ones(8) * 0.01
    calc_params['i0'][1] = i / 100 + 9 / 10
    calc_once = sir_delta(**calc_params)
    print(calc_params['populations'] @ calc_once.calc_steady_grad(np.zeros(8)))
    print(calc_params['populations'] @ calc_once.calc_vac_prdt_grad_dis(np.zeros(8)))
    print('   ')
    
import matplotlib.pyplot as plt
plt.plot(res)