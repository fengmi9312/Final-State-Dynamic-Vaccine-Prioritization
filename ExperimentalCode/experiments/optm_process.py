# -*- coding: utf-8 -*-
"""
Created on Mon May 12 10:18:33 2025

@author: MIFENG
"""

import os
import sys
code_root =  os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(code_root)
from Dependencies.CodeDependencies import basic_params, func, param_data_loader
from copy import deepcopy
import numpy as np
from Dependencies.CodeDependencies.model import sir_delta
import itertools
import pandas as pd

def execute(expt_param, file_idx):
    countries = ['United States']
    country_data = param_data_loader.load_all_data(countries, basic_params.group_div)
    calc_params = deepcopy(basic_params.calc_params)
    calc_params.update({key: country_data['United States'][key] for key in ['populations', 'ifrs', 'ylls']})
    calc_params['contacts'] = np.sum([country_data['United States']['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    srv_gen = func.srv_weibull(2.826, 5.665, basic_params.srv_length, 1 / basic_params.day_div)
    calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
    delay = 1400
    daily_vac, r0, vac_times, group_idxs = [[0.14 / 100, 1.5, 50, [1, 3]], [0.14 / 100, 2.5, 11, [1, 3]]][file_idx]
    vac_start = 30
    vac_eff = 0.95
    target = 'c'
    k_val = r0 / (np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0]) * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
    calc_params['k'] = k_val
    calc_params['eta'] = vac_eff
    calc_params['delay'] = delay
    calc_once = sir_delta(**calc_params)
    for i in range(vac_start * calc_once.get_day_div()): calc_once.spread_once()
    for i in range(vac_times):
        alloc = calc_once.optimize_vac_alloc(daily_vac, target = target, disp = False)
        calc_once.add_vaccination(alloc)
        for vac_idx in range(calc_once.get_day_div()):
            calc_once.spread_once()
    alloc = calc_once.optimize_vac_alloc(daily_vac, target = target, disp = False)
    group_amount = len(calc_once.get_populations())
    one_vac = np.zeros(group_amount)
    res = {'prdt': {}}
    for idx in range(group_amount): res[f'grad_{idx}'] = {}
    res['info'] = {'s_arr': calc_once.getc_s(), 'populations': calc_once.get_populations(), 'optm_alloc': alloc}
    for i, j in itertools.product(range(101), range(101)):
        one_vac[group_idxs] = np.array([i / 100, j / 100]) * daily_vac * 2.5 / calc_once.get_populations()[group_idxs]
        if j == 0: 
            res['prdt'][str(i)] = []
            for idx in range(group_amount): res[f'grad_{idx}'][str(i)] = []
        res['prdt'][str(i)].append(calc_once.calc_vac_prdt_target(one_vac, target = target))
        grad_res = calc_once.get_populations() @ calc_once.calc_steady_grad(one_vac)
        for idx in range(group_amount): res[f'grad_{idx}'][str(i)].append(grad_res[idx])
    return {sheet_name: pd.DataFrame(sheet_data) for sheet_name, sheet_data in res.items()}

res = execute(0,  1)
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
plt.sca(ax)
X, Y = np.meshgrid(np.arange(101) / 100 * (0.14 / 100) * 2.5, np.arange(101) / 100 * (0.14 / 100) * 2.5)
plt.pcolor(X, Y, res['prdt'].values.T)
X, Y = np.meshgrid(np.arange(101)[::10] / 100 * (0.14 / 100) * 2.5, np.arange(101)[::10] / 100 * (0.14 / 100) * 2.5)
U = res['grad_1'].values.T[::10, ::10]
V = res['grad_3'].values.T[::10, ::10]
ax.set_title('Arrows scale with plot width, not view')
Q = ax.quiver(X, Y, U, V, units='width')


















