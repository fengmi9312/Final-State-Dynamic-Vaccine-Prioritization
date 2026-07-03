# -*- coding: utf-8 -*-
"""
Created on Tue May  6 16:13:19 2025

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



def execute(expr_param, file_idx):
    if expr_param != 'param': return None
    countries = ['United States']
    country_data = param_data_loader.load_all_data(countries, basic_params.group_div)
    calc_params = deepcopy(basic_params.calc_params)
    calc_params.update({key: country_data['United States'][key] for key in ['populations', 'ylls']})
    calc_params['contacts'] = np.sum([country_data['United States']['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    srv_gen = func.srv_weibull(2.826, 5.665, basic_params.srv_length, 1 / basic_params.day_div)
    calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
    eigen_max = np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0])
    lambda_max = eigen_max * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']) 
    
    daily_vac = 0.35 / 100
    calc_params['eta'] = 0.95
    calc_params['delay'] = 1400
    vac_onset = 30
    
    
    optm_targets = ['d']
    empirical_sttgs = ['under_20', '20-49', '20+', '60+', 'all_ages', 'zero_vac']
    sttgs = empirical_sttgs + [f'min_{optm_target}' for optm_target in optm_targets] + [f'gmin_{optm_target}' for optm_target in optm_targets]
    basic_ifrs = country_data['United States']['ifrs']
    mean_ifrs = basic_ifrs.mean() * np.ones_like(basic_ifrs)
    diff_ifrs = basic_ifrs - mean_ifrs
    calc_params['ifrs'] = mean_ifrs + (file_idx / 39) * diff_ifrs
    res = {}
    for r0_idx in range(40):
        r0 = 1.1 + r0_idx * 0.1
        calc_params['k'] =  r0 / lambda_max
        print(f'Excute: r0_idx == {r0_idx}')
        for sttg in sttgs:
            print(f'Strategy: {sttg}')
            res[f'allocs_{sttg}_{r0_idx}'] = {}
            res[f'prdts_{sttg}_{r0_idx}'] = {}
            calc_non = sir_delta(**calc_params)
            for i in range(vac_onset * basic_params.day_div):
                calc_non.spread_once()
            day_idx = 0
            while True:
                if sttg == 'zero_vac':
                    if day_idx >= 120: break 
                else:
                    if calc_non.getc_x_tot('s') == 0:  break
                if sttg.split('_')[0] == 'min': alloc = calc_non.optimize_vac_alloc(daily_vac, target = sttg.split('_')[-1], disp = False)
                elif sttg.split('_')[0] == 'gmin': alloc = calc_non.optimize_vac_alloc(daily_vac, target = sttg.split('_')[-1], disp = False, prdt_type = 'grad', trans_delay = 1)
                else: alloc = calc_non.empirical_alloc(daily_vac, sttg)
                res[f'allocs_{sttg}_{r0_idx}'][str(day_idx)] = alloc
                res[f'prdts_{sttg}_{r0_idx}'][str(day_idx)] = calc_non.calc_vac_prdt(alloc)
                calc_non.add_vaccination(alloc)
                for vac_idx in range(calc_non.get_day_div()):
                    calc_non.spread_once()
                day_idx += 1
    return {sheet_name: pd.DataFrame(sheet_data) for sheet_name, sheet_data in res.items()} 



# if __name__ == '__main__':
#     total_res = [execute('param', i) for i in [10]]


# countries = ['United States']
# country_data = param_data_loader.load_all_data(countries, basic_params.group_div)
# calc_params = deepcopy(basic_params.calc_params)
# calc_params.update({key: country_data['United States'][key] for key in ['populations', 'ifrs', 'ylls']})
# calc_params['contacts'] = np.sum([country_data['United States']['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
# target = 'y'
# target_coef = {'c': calc_params['populations'], 'd': calc_params['populations'] * calc_params['ifrs'], 'y': calc_params['populations'] * calc_params['ifrs'] * calc_params['ylls']}
# for i in range(5):
#     print(total_res[i][f'prdts_mar_min_{target}'][str(90)] @ target_coef[target],
#           total_res[i][f'prdts_non_min_{target}'][str(90)] @ target_coef[target])

# print(res['prdts_mar_min_c'][str(60)] @ (calc_params['populations'] * calc_params['ifrs']))
# print(res['prdts_non_min_c'][str(60)] @ (calc_params['populations'] * calc_params['ifrs']))
# print(res['prdts_mar_gmin_c'][str(60)] @ (calc_params['populations'] * calc_params['ifrs']))
# print(res['prdts_non_gmin_c'][str(60)] @ (calc_params['populations'] * calc_params['ifrs']))




# import matplotlib.pyplot as plt
# params_fitting = {'method': 'SLSQP', 'tol': 1e-16, 'bounds': Bounds(np.ones(1) * 0.001, np.ones(1) * np.inf)}

# rem_trans_data = {'daily_infection': calc_once.get_i_in_tot(), 'removal': calc_once.get_r_tot()}
# rem_res, rem_curve = fit_rem_from_data(rem_trans_data, 1 / basic_params.day_div, init_params = np.ones(1), **params_fitting)

# plt.figure()
# plt.plot(rem_trans_data['removal'], color = 'tab:blue')
# plt.plot(rem_curve, color = 'tab:red')
# plt.title('Removel Rate Fitting')


# inf_trans_data = {'daily_infection_arr': calc_once.get_i_in(), 'confirmed_arr': calc_once.get_c()}
# inf_res, cum_curve = fit_inf_from_data(inf_trans_data, 1 / basic_params.day_div, 
#                                        mu = rem_res.x[0], populations = calc_params['populations'], contacts = calc_params['contacts'], k = calc_params['k'],
#                                        init_params = np.ones(1), **params_fitting)
# plt.figure()
# plt.plot(calc_params['populations'] @ inf_trans_data['confirmed_arr'].T, color = 'tab:blue')
# plt.plot(calc_params['populations'] @ cum_curve, color = 'tab:red')
# plt.title('Infection Rate Fitting')

# print(inf_res.x[0], rem_res.x[0], calc_params['k'] * eigen_max * inf_res.x[0] / rem_res.x[0])




