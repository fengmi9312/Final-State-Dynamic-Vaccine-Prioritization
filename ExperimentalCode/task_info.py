# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 21:42:01 2024

@author: fengm
"""


info = {'optm_from_example': {'param': 12}, 'optm_from_example_comp': {'param': 5}, 'optm_from_country_example': {'param': 12}, 
        'optm_from_param': {'r0': 120, 'daily_vac': 40, 'delay': 40, 'vac_eff': 40},  
        'optm_from_comp': {'lower': 120, 'higher': 120, 'equal': 120}, 
        'optm_from_dysttg': {'lower': 120, 'equal': 120}, 
        'optm_from_compact_dysttg': {'lower': 121}, 
        'optm_from_dysttg_example': {'lower': 1, 'equal': 3}, 
        'optm_from_equity': {'param': 40}, 'optm_from_equity_r0': {'param': 40}, 'optm_from_compact_equity_r0': {'param': 41},
        'optm_from_ratio': {'param': 41}, 
        'optm_from_country': {'United States': 40, 'United Kingdom': 40, 'France': 40, 'Germany': 40, 'Spain': 40, 'Japan': 40, 'Israel': 40, 'Austria': 40, 'Ireland': 40, 'South Korea': 40, 'Italy': 40, 'Singapore': 40},
        'time_varying_optm': {'param': 1},
        'equivalence_simu': {'param': 1},
        'final_size_prdt_optm': {'param': 1},
        'optm_from_changing_example': {'param': 2},
        'discrete_optm': {'param': 1},
        'state_aggregation_alpha': {'param': 1}}       

def check_info(func_name, task_param):
    if func_name not in info:
        return False
    else:
        if task_param not in info[func_name]: return False
        else: return True
        
def get_file_amount(func_name, task_param):
    return info[func_name][task_param]