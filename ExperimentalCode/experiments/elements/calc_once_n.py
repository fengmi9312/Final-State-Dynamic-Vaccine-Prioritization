# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 15:19:50 2024

@author: fengm
"""

import numpy as np
from copy import deepcopy
from Dependencies.CodeDependencies.model import sir_delta
from Dependencies.CodeDependencies import func, basic_params

def simulate(calc_params, r0 = 2, vac_eff = 0.95, daily_vac = 1e-2, vac_start = 30, vac_dur = None, 
             delay = 1400, k_val = None,
             get_curve = False, get_effr = False, get_empirical = True, get_trans = False, optm_targets = ['c', 'd', 'y'], prdt_targets = ['c', 'd', 'y'], optm_disp = False):
    if k_val is None:
        k_val = r0 / (np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0]) * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
    calc_params_delta = deepcopy(calc_params)
    calc_params_delta['k'] = k_val
    calc_params_delta['eta'] = vac_eff
    calc_params_delta['delay'] = delay
    res_data = {}
    #tols = {'c': 1e-16, 'd': 1e-18, 'y': 1e-17}
    empirical_sttgs = ['no_vac', 'under_20', '20-49', '20+', '60+', 'all_ages', 'zero_vac'] if get_empirical else ['zero_vac']
    sttgs = empirical_sttgs + [f'min_{optm_target}' for optm_target in optm_targets]
    if get_trans: sttgs += [f'tmin_{optm_target}' for optm_target in optm_targets]
    for sttg in sttgs:
        calc_once = sir_delta(**calc_params_delta)
        alloc_key = f'alloc_{sttg}'
        dist_key = f'dist_{sttg}'
        effr_key = f'effr_{sttg}'
        if get_curve: 
            curve_key = f'curve_{sttg}'
            res_data[curve_key] = {}
            for target in prdt_targets: res_data[curve_key][f'prdt_{target}'] = []
        for i in range(vac_start * calc_once.get_day_div()):
            if get_curve:    
                for target in prdt_targets: res_data[curve_key][f'prdt_{target}'].append(calc_once.calc_prdt_target(target = target))
            calc_once.spread_once()
        print(f'Implement Strategy: {sttg}')
        if sttg != 'no_vac':
            res_data[alloc_key] = {}
            res_data[dist_key] = {}
            if get_effr:
                for target in prdt_targets: res_data[f'{effr_key}_{target}'] = {}
            day_idx = 0
            while True:
                if vac_dur is not None: 
                    if day_idx >= vac_dur: break
                else:
                    if sttg == 'zero_vac':
                        if day_idx >= 120: break
                    else: 
                        if calc_once.getc_x_tot('s') == 0:  break
                
                if sttg.split('_')[0] == 'min': alloc = calc_once.optimize_vac_alloc(daily_vac, target = sttg.split('_')[-1], disp = optm_disp, tol = 1e-18)
                elif sttg.split('_')[0] == 'tmin': alloc = calc_once.optimize_vac_alloc(daily_vac, target = sttg.split('_')[-1], disp = optm_disp, prdt_type = 'trans', trans_delay = 1)
                else: alloc = calc_once.empirical_alloc(daily_vac, sttg)
                res_data[alloc_key][str(day_idx)] = alloc
                res_data[dist_key][str(day_idx)] = calc_once.calc_vac_prdt(alloc)
                calc_once.add_vaccination(alloc)
                for target in prdt_targets: res_data[f'{effr_key}_{target}'][str(day_idx)] = calc_once.calc_reduction_eff_target(target = target, vac_avail = None)
                for vac_idx in range(calc_once.get_day_div()):
                    if get_curve: 
                        for target in prdt_targets: res_data[curve_key][f'prdt_{target}'].append(calc_once.calc_prdt_target(target = target))
                    calc_once.spread_once()
                day_idx += 1
        if get_curve:    
            for target in prdt_targets: res_data[curve_key][f'prdt_{target}'].append(calc_once.calc_prdt_target(target = target))
            vmark = calc_once.get_current_time_int()
            while True:
                calc_once.spread_once()
                c_time_int = calc_once.get_current_time_int()
                for target in prdt_targets: res_data[curve_key][f'prdt_{target}'].append(calc_once.calc_prdt_target(target = target))
                if c_time_int > 100 and calc_once.get_c_tot()[-1] - calc_once.get_c_tot()[-100] < 1e-5 and c_time_int >= vmark + 2 * calc_params_delta['delay'] + 1: break
            res_data[curve_key]['time_line'] = calc_once.get_time_line()
            for target in basic_params.all_targets: res_data[curve_key][f'curve_{target}'] = calc_once.get_x_tot(target) 
            for target in prdt_targets: res_data[curve_key][f'prdt_{target}'] = np.array(res_data[curve_key][f'prdt_{target}'])
    return res_data



    
    



















    
    
    
    
    
    
    
    
    
    
    
    