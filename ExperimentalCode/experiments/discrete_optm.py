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


def get_mean_from_weibull(alpha, beta):
    return beta * gamma(1 + 1.0 / alpha)

def get_beta_from_weibull(alpha, mean_value):
    return mean_value / gamma(1 + 1.0 / alpha)


def from_allocs_to_coefs(allocs, switch_info, populations):
    alloc_idx = 0
    coefs = []
    for info_idx, (group_idxs, switch_point) in enumerate(switch_info):
        group_num = len(group_idxs) - 1
        if group_num <= 0: continue
        allocs_tmp = []
        while alloc_idx < switch_point:
            allocs_tmp.append(allocs[alloc_idx][group_idxs])
            alloc_idx += 1
        tot_alloc_tmp = np.array(allocs_tmp).sum(axis = 0) / np.array(allocs_tmp).sum()
        for coef in tot_alloc_tmp[:-1]: coefs.append(coef)
    return np.array(coefs)

def from_coefs_to_allocs(coefs, daily_vac, switch_info, populations):
    allocs = []
    alloc_idx = 0
    coef_divs = [0]
    for info_idx, (group_idxs, switch_point) in enumerate(switch_info):
        group_num = len(group_idxs) - 1
        coef_divs.append(coef_divs[-1] + group_num)
        if group_num > 0: 
            coef = coefs[coef_divs[info_idx]:coef_divs[info_idx + 1]]
            coef = np.append(coef, 1 - coef.sum())
        else: coef = np.ones(1)
        alloc = np.zeros(len(populations))
        alloc[group_idxs] = daily_vac * coef / populations[group_idxs]
        while alloc_idx < switch_point:
            allocs.append(alloc)
            alloc_idx += 1
    return np.array(allocs)
    
def discrete_vaccination(coefs, daily_vac, switch_info, model_non, target = None):
    allocs = from_coefs_to_allocs(coefs, daily_vac, switch_info, model_non.get_populations())
    time_mark = model_non.get_current_time_int()
    for alloc in allocs:
        model_non.add_vaccination(alloc)
        for vac_idx in range(model_non.get_day_div()):
            model_non.spread_once()
    if target is None:
        return None
    else:
        target_res = model_non.calc_prdt_target(target = target)
        model_non.return_back(time_mark, remain_v = False)
        return target_res
    
def optimize_coef(init_coefs, daily_vac, switch_info, model_non, target = None):
    coef_coef = []
    coef_divs = [0]
    for info_idx, (group_idxs, switch_point) in enumerate(switch_info):
        group_num = len(group_idxs) - 1
        coef_divs.append(coef_divs[-1] + group_num)
        if group_num > 0: 
            tmp = np.zeros(len(init_coefs))
            tmp[coef_divs[info_idx]:coef_divs[info_idx + 1]] = np.ones(group_num)
            coef_coef.append(tmp)
    
    linear_constraint = LinearConstraint(np.array(coef_coef), np.zeros(len(coef_coef)), np.ones(len(coef_coef)))
    constraint = [linear_constraint,]
    bound = Bounds(np.zeros(len(init_coefs)), np.ones(len(init_coefs)))
    init_params = init_coefs
    while True:
        res = minimize(discrete_vaccination, init_coefs, method='SLSQP', jac = None, args = (daily_vac, switch_info, model_non, target),
                       constraints = constraint, bounds = bound, tol = 1e-16,
                       options={'disp': False, 'maxiter':2000})
        if res.success:
            print('Successful Optimization!')
            break
        else:
            print('Unsuccessful Optimization, optimize again...')
            init_params = np.random.rand() * init_coefs
    return res
    
    
    
    
    
    

def execute(expr_param, file_idx):
    if expr_param != 'param' or file_idx != 0: return None
    countries = ['United States']
    country_data = param_data_loader.load_all_data(countries, basic_params.group_div)
    calc_params = deepcopy(basic_params.calc_params)
    calc_params.update({key: country_data['United States'][key] for key in ['populations', 'ifrs', 'ylls']})
    calc_params['contacts'] = np.sum([country_data['United States']['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    alpha_inf, alpha_rem = 1.5, 2.5
    mean_inf, mean_rem = 5, 7
    beta_inf = get_beta_from_weibull(alpha_inf, mean_inf)
    beta_rem = get_beta_from_weibull(alpha_rem, mean_rem)
    eigen_max = np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0])
    
    daily_vac = 0.35 / 100
    calc_params['eta'] = 0.95
    calc_params['delay'] = 1400
    vac_onset = 40
    r0 = 2.1
    
    calc_params['srv_inf'] = func.srv_weibull(alpha_inf, beta_inf, basic_params.srv_length, 1 / basic_params.day_div)
    calc_params['srv_rem'] = func.srv_weibull(alpha_rem, beta_rem, basic_params.srv_length, 1 / basic_params.day_div)
    lambda_max = eigen_max * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem'])
    calc_params['k'] =  r0 / lambda_max
    sttgs = ['under_20', '20-49', '20+', '60+', 'all_ages', 'zero_vac', 'min_c', 'min_d', 'min_y']
    
    sttgs = ['no_vac', 'min_c']
    switch_info_dict = {'c': [([1], 13), ([1, 3], 34), ([1, 3, 4], 39), ([1, 2, 3, 4], 60)]}
    init_coefs_dict = {'c': None, 'd': None, 'y': None}
    res = {}
    for sttg in sttgs:
        print(sttg)
        calc_non = sir_delta(**calc_params)
        for i in range(vac_onset * basic_params.day_div):
            calc_non.spread_once()
        if sttg != 'no_vac':
            if sttg.split('_')[0] == 'min':
                optm_target = sttg.split('_')[-1]
            res[f'allocs_{sttg}'] = {}
            day_idx = 0
            while day_idx < 60:
                if sttg.split('_')[0] == 'min': alloc = calc_non.optimize_vac_alloc(daily_vac, target = optm_target, disp = False, prdt_type = 'non_mar', target_type = 'steady')
                else: alloc = calc_non.empirical_alloc(daily_vac, sttg)
                res[f'allocs_{sttg}'][str(day_idx)] = alloc
                calc_non.add_vaccination(alloc)
                for vac_idx in range(calc_non.get_day_div()):
                    calc_non.spread_once()
                day_idx += 1
        while calc_non.getc_x_tot('i') > 1e-6:
            calc_non.spread_once()
        res[f'curves_{sttg}'] = {'time_line': calc_non.get_time_line()}
        for res_target in ['s', 'i', 'r', 'c', 'd', 'y']:
            res[f'curves_{sttg}'][res_target] = calc_non.get_x_tot(res_target)
            
        if sttg != 'no_vac' and sttg.split('_')[0] == 'min':
            calc_non = sir_delta(**calc_params)
            for i in range(vac_onset * basic_params.day_div):
                calc_non.spread_once()
            
            idx = 0
            #coef_divs = [0]
            
            init_coefs_dict[optm_target] = []
            for info_idx, (group_idxs, switch_point) in enumerate(switch_info_dict[optm_target]):
                group_num = len(group_idxs) - 1
                # coef_divs.append(coef_divs[-1] + group_num)
                
                allocs_tmp = []
                while idx < switch_point:
                    allocs_tmp.append(res[f'allocs_{sttg}'][str(idx)][group_idxs])
                    idx += 1
                if group_num > 0: 
                    tot_alloc_tmp = np.array(allocs_tmp).sum(axis = 0) / np.array(allocs_tmp).sum()
                    for coef in tot_alloc_tmp[:-1]: init_coefs_dict[optm_target].append(coef)
            init_coefs_dict[optm_target] = np.array(init_coefs_dict[optm_target])
            
            optm_coefs = optimize_coef(init_coefs_dict[optm_target], daily_vac, switch_info_dict[optm_target], calc_non, target = optm_target).x
            optm_allocs = from_coefs_to_allocs(optm_coefs, daily_vac, switch_info_dict[optm_target], calc_non.get_populations())
            res[f'optm_allocs_{sttg}'] = {}
            for i in range(len(optm_allocs)): res[f'optm_allocs_{sttg}'][str(i)] = optm_allocs[i]
            calc_non = sir_delta(**calc_params)
            for i in range(vac_onset * basic_params.day_div):
                calc_non.spread_once()
            discrete_vaccination(optm_coefs, daily_vac, switch_info_dict[optm_target], calc_non)
            while calc_non.getc_x_tot('i') > 1e-6:
                calc_non.spread_once()
            res[f'optm_curves_{sttg}'] = {'time_line': calc_non.get_time_line()}
            for res_target in ['s', 'i', 'r', 'c', 'd', 'y']:
                res[f'optm_curves_{sttg}'][res_target] = calc_non.get_x_tot(res_target)
            
            mean_coefs = init_coefs_dict[optm_target]
            mean_allocs = from_coefs_to_allocs(mean_coefs, daily_vac, switch_info_dict[optm_target], calc_non.get_populations())
            res[f'mean_allocs_{sttg}'] = {}
            for i in range(len(mean_allocs)): res[f'mean_allocs_{sttg}'][str(i)] = mean_allocs[i]
            calc_non = sir_delta(**calc_params)
            for i in range(vac_onset * basic_params.day_div):
                calc_non.spread_once()
            discrete_vaccination(mean_coefs, daily_vac, switch_info_dict[optm_target], calc_non)
            while calc_non.getc_x_tot('i') > 1e-6:
                calc_non.spread_once()
            res[f'mean_curves_{sttg}'] = {'time_line': calc_non.get_time_line()}
            for res_target in ['s', 'i', 'r', 'c', 'd', 'y']:
                res[f'mean_curves_{sttg}'][res_target] = calc_non.get_x_tot(res_target)

    return res




# countries = ['United States']
# country_data = param_data_loader.load_all_data(countries, basic_params.group_div)
# calc_params = deepcopy(basic_params.calc_params)
# calc_params.update({key: country_data['United States'][key] for key in ['populations', 'ifrs', 'ylls']})
# calc_params['contacts'] = np.sum([country_data['United States']['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)

# res = execute('param', 0)

# import matplotlib.pyplot as plt
# import matplotlib.colors as mcolors

# def pcolor_heatmap(ax, results):
#     base = plt.colormaps['seismic']
#     trunc = mcolors.LinearSegmentedColormap.from_list('top_half', base(np.linspace(0.5, 1, 256)))
#     data = results.T * 100
    
#     H, W = data.shape
#     im = ax.pcolormesh(np.arange(W+1)-0.5, np.arange(H+1)-0.5, data, cmap = trunc, shading='auto', vmin = 0, vmax = 0.35)
#     ax.hlines(np.arange(H + 1) - 0.5, xmin = -0.5, xmax = W - 0.5, color="tab:gray", linestyle = '--', linewidth=0.5)
#     ax.set_ylim(H-0.5, -0.5)
#     age_groups = ['0–9', '10–19', '20–29', '30–39', '40–49', '50–59', '60–69', '70+']
#     plt.yticks(np.arange(H), age_groups, fontsize = 6)
#     return ax, im, data

# for sttg in ['min_c']:
#     plt.figure()
#     ax, im, test = pcolor_heatmap(plt.gca(), np.array([res[f'allocs_{sttg}'][str(i)] * calc_params['populations'] for i in range(60)]))
#     plt.colorbar(im)
    
#     for x in [13, 34, 39]:
#         plt.axvline(x)
    
    # plt.figure()
    # ax, im, test = pcolor_heatmap(plt.gca(), np.array([res[f'optm_allocs_{sttg}'][str(i)] * calc_params['populations'] for i in range(60)]))
    # plt.colorbar(im)
    
    # plt.figure()
    # ax, im, test = pcolor_heatmap(plt.gca(), np.array([res[f'mean_allocs_{sttg}'][str(i)] * calc_params['populations'] for i in range(60)]))
    # plt.colorbar(im)

    # plt.figure()
    # plt.plot(res[f'curves_{sttg}']['time_line'], res[f'curves_{sttg}']['y'], color = 'tab:red')
    # plt.plot(res[f'optm_curves_{sttg}']['time_line'], res[f'optm_curves_{sttg}']['y'], color = 'tab:blue')
    # plt.plot(res[f'mean_curves_{sttg}']['time_line'], res[f'mean_curves_{sttg}']['y'], color = 'tab:green')

# plt.figure()
# sttgs = ['under_20', '20-49', '20+', '60+', 'all_ages', 'zero_vac', 'min_c', 'min_d', 'min_y']
# for sttg in sttgs:
#     plt.plot(res[sttg].get_time_line(), res[sttg].get_c_tot())

# if __name__ == '__main__':
#     total_res = [execute('lower', i) for i in [12]]



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




