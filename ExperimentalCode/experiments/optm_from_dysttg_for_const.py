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



def allocation_switching_penalty(x, y, normalize=True):
    x = np.asarray(x, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()

    if x.shape != y.shape:
        raise ValueError(f"x and y must have the same shape, got {x.shape} and {y.shape}")

    if normalize:
        sx, sy = x.sum(), y.sum()
        if sx <= 0 or sy <= 0:
            raise ValueError("Allocation vectors must have positive sums.")
        x = x / sx
        y = y / sy

    return 0.5 * np.sum((x - y) ** 2)

def optimize_vac_alloc_with_reg(self, vac_avail, reg, target = 'c', init_strategy = None, tol = 1e-16,
                       disp = True, get_prdt = False, minimize_kwargs = {}, **kwargs):
    if vac_avail <= 0 or self._sir_delta__s_tot[self._sir_delta__current_time_int] == 0:
        if get_prdt: return {'target': self.calc_vac_prdt_target(np.zeros(self._sir_delta__group_amount), target = target), 
                'alloc': np.zeros(self._sir_delta__group_amount)}
        else: return np.zeros(self._sir_delta__group_amount)
    elif vac_avail >= self._sir_delta__s_tot[self._sir_delta__current_time_int]:
        if get_prdt: return {'target': self.calc_vac_prdt_target(self._sir_delta__s[self._sir_delta__current_time_int], target = target), 
                'alloc': self._sir_delta__s[self._sir_delta__current_time_int]}
        else: return self._sir_delta__s[self._sir_delta__current_time_int]
    else: pass
    np.random.seed(0)
    prdt_type = kwargs.pop('prdt_type', 'non_mar')
    target_type = kwargs.pop('target_type', 'steady')
    if target_type == 'trans':  return self.order_alloc(vac_avail, func.order_index(-self.calc_trans_grad_target(target = target, prdt_type = prdt_type)))[0]
    
    if reg['prev_alloc'] is None:
        get_res = lambda vac_alloc: self.calc_vac_prdt_target(vac_alloc, target, prdt_type = prdt_type, **kwargs)
    else:
        get_res = lambda vac_alloc: self.calc_vac_prdt_target(vac_alloc, target, prdt_type = prdt_type, **kwargs) + reg['weight'] *  reg['fval'] * allocation_switching_penalty(vac_alloc * self._sir_delta__populations, reg['prev_alloc'] * self._sir_delta__populations)
    linear_constraint = LinearConstraint(deepcopy(self._sir_delta__populations), np.array([vac_avail]), np.array([vac_avail]))
    constraint = [linear_constraint,]
    bound = Bounds(np.zeros(self._sir_delta__group_amount), deepcopy(self._sir_delta__s[self._sir_delta__current_time_int]))
    
    init_strategies = [init_strategy] if init_strategy is not None else []
    dgr_arr = self._sir_delta__contacts.sum(axis = 1)
    dgr = vac_avail * dgr_arr / dgr_arr.sum()
    init_strategies.append(np.minimum(self._sir_delta__s[self._sir_delta__current_time_int],  dgr / self._sir_delta__populations))
    if target == 'c': dgr_arr = np.ones(self._sir_delta__group_amount)
    elif target == 'd': dgr_arr = self._sir_delta__ifrs 
    elif target == 'y': dgr_arr = self._sir_delta__ifrs * self._sir_delta__ylls 
    dgr = vac_avail * dgr_arr / dgr_arr.sum()
    init_strategies.append(np.minimum(self._sir_delta__s[self._sir_delta__current_time_int],  dgr / self._sir_delta__populations))
    res_list = []
    for basic_init_alloc in init_strategies:
        init_alloc = basic_init_alloc
        while True:
            res = minimize(get_res, init_alloc, method='SLSQP', jac = None,
                           constraints = constraint, bounds = bound, tol = tol,
                           options={'disp': False, 'maxiter':2000}, **minimize_kwargs)
            if res.success:
                if disp: print('Successful Optimization!')
                break
            else:
                if disp: print('Unsuccessful Optimization, optimize again...')
                init_alloc = np.random.rand() * basic_init_alloc
        res_list.append({'target': res.fun, 'alloc': res.x})
    min_index = min(range(len(res_list)), key=lambda i: res_list[i]['target'])
    if get_prdt: return res_list[min_index]
    else: return res_list[min_index]['alloc']


sir_delta.optimize_vac_alloc_with_reg = optimize_vac_alloc_with_reg


def fit_rem_from_data(trans_data, step, init_params, **kwargs):
    data_len = len(trans_data['daily_infection'])
    removal_data = trans_data['removal'] - trans_data['removal'][0]
    
    def curve(params):
        rem_srv = 1 - np.exp(-params[0] * np.arange(data_len) * step)
        return np.convolve(rem_srv, trans_data['daily_infection'], 'full')[:data_len]
        
    def loss_func(params):
        return ((curve(params) - removal_data)**2).sum()
    
    init_p = init_params
    while True:
        res = minimize(loss_func, init_p, **kwargs)
        if res.success: return res, curve(res.x)
        else: init_p = init_params * np.random.rand(len(init_params))

def fit_inf_from_data(trans_data, step, mu, populations, contacts, k, init_params, **kwargs):
    group_amount = len(populations)
    totmat = contacts * populations[None, :] * k  
    data_len = len(trans_data['daily_infection_arr'])
    i_in_data = trans_data['daily_infection_arr'][:-1].T
    s_data = (1 - trans_data['confirmed_arr'][:-1]).T
    c_data_target = trans_data['confirmed_arr'][1:].T
    c_data0 = trans_data['confirmed_arr'][0:1].T
    
    def curve(params):
        cum_rate = params[0] * np.exp(- mu * np.arange(data_len) * step) * step
        inf_tmp = np.array([np.convolve(cum_rate, i_in_data[i], 'full')[:data_len - 1] for i in range(group_amount)]) 
        return ((1 - ((1 - inf_tmp).reshape((group_amount, data_len - 1, 1)) ** 
               totmat.T.reshape((group_amount, 1, group_amount))).prod(axis = 0)).T * s_data).cumsum(axis = 1) + c_data0
    
    def loss_func(params):
        return ((populations @ (curve(params) - c_data_target))**2).sum()
    
    init_p = init_params
    while True:
        res = minimize(loss_func, init_p, **kwargs)
        if res.success: return res, curve(res.x)
        else: init_p = init_params * np.random.rand(len(init_params))



def get_mean_from_weibull(alpha, beta):
    return beta * gamma(1 + 1.0 / alpha)

def get_beta_from_weibull(alpha, mean_value):
    return mean_value / gamma(1 + 1.0 / alpha)


def execute(expr_param, file_idx):
    countries = ['United States']
    country_data = param_data_loader.load_all_data(countries, basic_params.group_div)
    calc_params = deepcopy(basic_params.calc_params)
    calc_params.update({key: country_data['United States'][key] for key in ['populations', 'ifrs', 'ylls']})
    calc_params['contacts'] = np.sum([country_data['United States']['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    if expr_param in ['lower', 'higher']:
        alpha_inf, alpha_rem = {'lower': (1.5, 2.5), 'higher': (2.5, 1.5)}[expr_param]
        mean_inf, mean_rem = 5, 7
        beta_inf = get_beta_from_weibull(alpha_inf, mean_inf)
        beta_rem = get_beta_from_weibull(alpha_rem, mean_rem)
    elif expr_param == 'equal':
        alpha_inf, alpha_rem, beta_inf, beta_rem = 2.826, 2.826, 5.665, 5.665
    else: return None
    eigen_max = np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0])
    
    daily_vac = 0.35 / 100
    calc_params['eta'] = 0.95
    calc_params['delay'] = 1400
    c_level = 0.2
    vac_onset = 30
    
    r0 = 2
    beta_coef = func.find_weibull_coef_from_g(0.14, r0, alpha_inf, alpha_rem, beta_inf, beta_rem, 160000, 1 / basic_params.day_div)
    print(beta_coef)
    calc_params['srv_inf'] = func.srv_weibull(alpha_inf, beta_inf * beta_coef, basic_params.srv_length, 1 / basic_params.day_div)
    calc_params['srv_rem'] = func.srv_weibull(alpha_rem, beta_rem * beta_coef, basic_params.srv_length, 1 / basic_params.day_div)
    lambda_max = eigen_max * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem'])
    calc_params['k'] =  r0 / lambda_max
    steady_c = calc_params['populations'] @ func.get_steady_state(calc_params['k'], calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), basic_params.i0)
    fitting_calc = sir_delta(**calc_params)
    while True:
        if fitting_calc.getc_c_tot() >= basic_params.i0 + c_level * (steady_c - basic_params.i0): break
        fitting_calc.spread_once()
    
    params_fitting = {'method': 'SLSQP', 'tol': 1e-16, 'bounds': Bounds(np.ones(1) * 0.001, np.ones(1) * np.inf)}
    rem_trans_data = {'daily_infection': fitting_calc.get_i_in_tot(), 'removal': fitting_calc.get_r_tot()}
    rem_res, rem_curve = fit_rem_from_data(rem_trans_data, 1 / basic_params.day_div, init_params = np.ones(1), **params_fitting)
    inf_trans_data = {'daily_infection_arr': fitting_calc.get_i_in(), 'confirmed_arr': fitting_calc.get_c()}
    inf_res, cum_curve = fit_inf_from_data(inf_trans_data, 1 / basic_params.day_div, 
                                            mu = rem_res.x[0], populations = calc_params['populations'], contacts = calc_params['contacts'], k = calc_params['k'],
                                            init_params = np.ones(1), **params_fitting)
    del fitting_calc
    
    calc_params['srv_inf'] = func.srv_weibull(alpha_inf, beta_inf, basic_params.srv_length, 1 / basic_params.day_div)
    calc_params['srv_rem'] = func.srv_weibull(alpha_rem, beta_rem, basic_params.srv_length, 1 / basic_params.day_div)
    lambda_max = eigen_max * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem'])
    calc_params['k'] =  r0 / lambda_max
    optm_targets = ['c', 'd', 'y']
    sttgs = [f'min_{optm_target}' for optm_target in optm_targets]
    res = {'params': {'inf_rate': [inf_res.x[0] * beta_coef], 'rem_rate': [rem_res.x[0] * beta_coef], 'r0': [calc_params['k'] * eigen_max * inf_res.x[0] / rem_res.x[0]], 
                      'k': [calc_params['k']], 'beta_inf': [beta_inf], 'beta_rem': [beta_rem], }}
    prdt_target_types = {'min': ('non_mar', 'steady'), 'gmin': ('non_mar', 'trans'), 'mmin': ('mar', 'steady'), 'mgmin': ('mar', 'trans')}
    for sttg in sttgs:
        print(sttg)
        res[f'allocs_{sttg}'] = {}
        res[f'prdts_{sttg}'] = {}
        calc_non = sir_delta(**calc_params)
        reg = {'weight': file_idx / 20, 'fval': calc_non.calc_prdt_target(target = sttg.split('_')[-1]), 'prev_alloc': None}
        res['params'][sttg.split('_')[-1]] = [reg['fval'],]
        calc_non.set_param_m(res['params']['inf_rate'][0], res['params']['rem_rate'][0])
        for i in range(vac_onset * basic_params.day_div):
            calc_non.spread_once()
        day_idx = 0
        while True:
            if calc_non.getc_x_tot('s') == 0:  break 
            # if day_idx % 10 == 0: print(day_idx)
            prdt_type, target_type = prdt_target_types[sttg.split('_')[0]]
            alloc = calc_non.optimize_vac_alloc_with_reg(daily_vac, reg, target = sttg.split('_')[-1], disp = False, prdt_type = prdt_type, target_type = target_type)
            res[f'allocs_{sttg}'][str(day_idx)] = alloc
            res[f'prdts_{sttg}'][str(day_idx)] = calc_non.calc_vac_prdt(alloc)
            calc_non.add_vaccination(alloc)
            for vac_idx in range(calc_non.get_day_div()):
                calc_non.spread_once()
            day_idx += 1
            reg['prev_alloc'] = alloc
    return {sheet_name: pd.DataFrame(sheet_data) for sheet_name, sheet_data in res.items()} 



# if __name__ == '__main__':
#     total_res = [execute('lower', i) for i in [21]]



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




