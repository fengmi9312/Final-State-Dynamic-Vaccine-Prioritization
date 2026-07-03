
from Dependencies.FrameDependencies import name_principle
import pandas as pd
from Dependencies.CodeDependencies import  basic_params, param_data_loader, func
from itertools import product
from copy import deepcopy
from scipy.special import gamma
from Dependencies.CodeDependencies.model import sir_delta
import numpy as np

def allocation_switching_penalty(x, y, normalize=True):
    x = np.asarray(x, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()

    if x.shape != y.shape:
        raise ValueError(f"x and y must have the same shape, got {x.shape} and {y.shape}")

    if normalize:
        sx, sy = x.sum(), y.sum()
        if sx < 0 or sy < 0:
            raise ValueError("Allocation vectors must have positive sums.")
        if sx > 0: x = x / sx
        elif sx == 0: pass
        else: raise ValueError("Allocation vectors must have positive sums.")
        if sy > 0: y = y / sy
        elif sy == 0: pass
        else: raise ValueError("Allocation vectors must have positive sums.")

    return 0.5 * np.sum((x - y) ** 2)


def mean_allocation_switching_penalty(arr, normalize=True):
    """
    Compute the average switching penalty between consecutive allocation vectors.

    Parameters
    ----------
    arr : array-like, shape (T, n)
        Time series of allocation vectors.
    normalize : bool
        Whether to normalize each allocation vector before computing pairwise penalties.

    Returns
    -------
    float
        Average switching penalty over T-1 transitions.
    """
    arr = np.asarray(arr, dtype=float)

    if arr.ndim != 2:
        raise ValueError(f"arr must be a 2D array with shape (T, n), got shape {arr.shape}")

    if arr.shape[0] < 2:
        return 0.0

    penalties = [
        allocation_switching_penalty(arr[t], arr[t + 1], normalize=normalize)
        for t in range(arr.shape[0] - 1)
    ]

    return float(np.mean(penalties))

def get_beta_from_weibull(alpha, mean_value):
    return mean_value / gamma(1 + 1.0 / alpha)

def analyze(edata):
    expr_name = 'optm_from_dysttg_for_const'
    expr_param = 'lower'
    # if expr_param in ['lower', 'higher']:
    #     alpha_inf, alpha_rem = {'lower': (1.5, 2.5), 'higher': (2.5, 1.5)}[expr_param]
    #     mean_inf, mean_rem = 5, 7
    #     beta_inf = get_beta_from_weibull(alpha_inf, mean_inf)
    #     beta_rem = get_beta_from_weibull(alpha_rem, mean_rem)
    # elif expr_param == 'equal':
    #     alpha_inf, alpha_rem, beta_inf, beta_rem = 2.826, 2.826, 5.665, 5.665
    file_idx = 0
    task_name = name_principle.get_task_name(expr_name, expr_param)
    countries = ['United States']
    country_data = param_data_loader.load_all_data(countries, basic_params.group_div)
    pop_coef = {'c': country_data['United States']['populations'], 
                'd': country_data['United States']['populations'] * country_data['United States']['ifrs'], 
                'y': country_data['United States']['populations'] * country_data['United States']['ifrs'] * country_data['United States']['ylls']}
    anal_data = {'prdts': {}, 'pnlt': {}}
    optm_targets = ['c', 'd', 'y']
    vac_len = 140
    
    # calc_params = deepcopy(basic_params.calc_params)
    # calc_params.update({key: country_data['United States'][key] for key in ['populations', 'ifrs', 'ylls']})
    # calc_params['contacts'] = np.sum([country_data['United States']['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    # calc_params['eta'] = 0.95
    # calc_params['delay'] = 1400
    for file_idx in range(41):
        expr_data = edata[task_name][str(file_idx)]
        
        # calc_params['srv_inf'] = func.srv_weibull(alpha_inf, expr_data['params']['beta_inf'][0], basic_params.srv_length, 1 / basic_params.day_div)
        # calc_params['srv_rem'] = func.srv_weibull(alpha_rem, expr_data['params']['beta_rem'][0], basic_params.srv_length, 1 / basic_params.day_div)
        # calc_params['k'] = expr_data['params']['k'][0]
        # calc_non = sir_delta(**calc_params)
        
        for optm_target in optm_targets:
            # fval = calc_non.calc_prdt_target(target = optm_target)
            sttg = f'min_{optm_target}'
            anal_sheet_name = f'alloc_{sttg}_{file_idx}'
            expr_sheet_name = f'allocs_{sttg}'
            anal_data[anal_sheet_name] = {}
            last_idx = int(expr_data[expr_sheet_name].columns[-1])
            allocs = []
            for i in range(min(vac_len, last_idx + 1)):
                anal_data[anal_sheet_name][str(i)] = expr_data[expr_sheet_name][str(i)].to_numpy() * country_data['United States']['populations']
                allocs.append(anal_data[anal_sheet_name][str(i)])
            if file_idx == 0:
                anal_data['prdts'][optm_target] = []
                anal_data['pnlt'][optm_target] = []
            anal_data['prdts'][optm_target].append(expr_data[f'prdts_{sttg}'][str(min(vac_len - 1, last_idx))].to_numpy() @ pop_coef[optm_target])
            anal_data['pnlt'][optm_target].append(mean_allocation_switching_penalty(allocs))
    return {sheet_name: pd.DataFrame(item) for sheet_name, item in anal_data.items()}






















