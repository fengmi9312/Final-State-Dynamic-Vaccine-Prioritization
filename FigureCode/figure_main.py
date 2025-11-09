# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 17:04:41 2025

@author: MIFENG
"""


import os
import sys
folder_level = 1
code_root = os.path.dirname(os.path.abspath(__file__))
for idx in range(folder_level): code_root = os.path.dirname(code_root)
sys.path.append(code_root)
from Dependencies.CodeDependencies import func
from Dependencies.FrameDependencies.expr_data_loader import load_certain_edata
import AnalysisCode.analysis_func as af
import FigureCode.figure_func as ff
from AnalysisCode import analysis
import importlib
from Dependencies.CodeDependencies import basic_params
from string import ascii_lowercase as lc


# edata = {}

# task_dict = {'optm_from_param': {'r0': 40, 'daily_vac': 40, 'vac_eff': 40}, }

# additional_task_dict = task_dict
# for expr_name, task_item in additional_task_dict.items():
#     for expr_param, file_amount in task_item.items():
#         edata.update(load_certain_edata(expr_name, expr_param, file_amount))
        

# anal_data = {}
# importlib.reload(af)
# additional_anal_list = ['comparison_example']
# for anal_name in additional_anal_list:
#     anal_data.update({anal_name: getattr(af, f'get_{anal_name}').analyze(edata)})

# importlib.reload(ff)
# getattr(ff, 'figure_2b').draw(anal_data)

anal_data = {}
anal_list = ['allocs_from_time']
for country, country_abbr in basic_params.country_abbr.items():
    anal_list.append(f'dist_alloc_from_{country_abbr}')
anal_list = ['prdt_from_dysttg', 'allocs_dysttg_from_time']
anal_list = ['prdt_from_param', 'comparison_example', 'changing_example', 'prdt_from_dysttg']
anal_list = [f'dist_alloc_from_{basic_params.country_abbr[country]}' for country in basic_params.country_abbr.keys()]

anal_list = ['allocs_from_time', 'allocs_from_country_example']
anal_list = ['prdt_from_equity_r0', 'prdt_from_dysttg']
anal_list = ['impact_to_dysttg', 'allocs_dysttg_from_time']
anal_data.update(analysis.get_anal_data(anal_list))
save_fig = True

# fig_dict = {'supp_nf_robustness': ['prdt_dysttg_r0', 'rg_dur_grad', 'rg_dur_mar', 'rg_r0_equity_grad'], 'supp_dy_robustness': ['prdt_vac_dur', 'prdt_daily_vac', 'prdt_vac_eff'], 
#             'supp_contacts': ['contacts'], 'supp_populations': ['populations'], 'supp_ifrs': ['ifrs'], 'supp_ylls': ['ylls']}
#fig_dict = {'dy_robustness': ['curve_r25_t35', 'prdt_r0', 'curve_changing_r0', 'optm_changing_r0'], 'nf_robustness': ['prdt_dysttg_low_r0']}

fig_dict = {'obj_mechanism': ['mpb_c_r20_t35', 'mpb_d_r20_t35', 'mpb_y_r20_t35']}
fig_dict = {'country_res': ['allocs_c']}
fig_dict = {'r0_mechanism': ['mpb_c_r15_t14', 'mpb_c_r25_t14'], 'obj_mechanism': ['mpb_c_r20_t35', 'mpb_d_r20_t35', 'mpb_y_r20_t35'], 'country_res': ['allocs_c', 'allocs_d', 'allocs_y']}
fig_dict = {'supp_contacts': ['contacts']}
fig_dict = {'supp_dy_robustness': ['prdt_daily_vac', 'prdt_vac_dur', 'prdt_vac_eff']}
fig_dict = {'supp_nf_robustness': ['rg_r0_equity_grad']}
fig_dict = {'vaccination_strategy': ['illustrative_example']}

fig_dict = {'supp_discrete_vaccination': ['dy_allocs_c', 'mean_allocs_c', 'optm_allocs_c','curve_c']}
fig_dict = {'supp_nf_robustness': ['prdt_dysttg_r0', 'rg_dur_grad', 'rg_r0_equity_grad']}
fig_dict = {'nf_robustness': ['allocs_impact_fs', 'allocs_impact_ts']}

import matplotlib.pyplot as plt
importlib.reload(ff)
for fig_name, sub_name_list in fig_dict.items():
    for sub_name in sub_name_list:
        fig, _ = getattr(ff, f'{fig_name}_({sub_name})').draw(anal_data)
        if save_fig:
            fig.savefig(os.path.join(code_root, 'Figure', fig_name, f'{sub_name}.pdf'), dpi=300)
            plt.close(fig)




# import matplotlib.pyplot as plt
# from matplotlib.colors import TwoSlopeNorm
# import seaborn as sns
# import numpy as np
# for vac_deadline in [29, 59, 89, 119]:
#     plt.figure()
#     res = anal_data['prdt_from_equity']
#     zero_vac = res[f'zero_vac_{vac_deadline}'].values.T
#     min_d = res[f'min_d_{vac_deadline}'].values.T
#     gmin_d = res[f'gmin_d_{vac_deadline}'].values.T
#     im_res = (gmin_d - min_d) / (zero_vac - gmin_d)
#     vmax = np.nanmax(im_res)
#     vmin = np.nanmin(im_res)
#     abs_max = max(abs(vmin), abs(vmax))
#     norm = TwoSlopeNorm(vmin=-abs_max, vcenter=0, vmax=abs_max)
#     im = plt.imshow(im_res, cmap = sns.diverging_palette(220, 20, as_cmap=True), norm = norm)
#     plt.colorbar(im)
#     plt.gca().invert_yaxis()
#     plt.yticks(np.arange(0, 40, 13), ['0', '1/3', '2/3', '1'])
#     plt.ylabel('Equity')
#     plt.xticks(np.arange(0, 40, 13), 1 + (1 + np.arange(0, 40, 13)) / 10)
#     plt.xlabel(r'$R_0$')
    


#ff.allocs_test.draw(anal_data)
# anal_data = analysis.get_anal_data(anal_list)



# fig.savefig(os.path.join(code_root, 'Figure', f'figure4', f'figure_4a.pdf'), dpi=300)
# plt.close(fig)

# importlib.reload(ff)
# fig, _ = getattr(ff, 'figure_5b').draw(anal_data)
# fig.savefig(os.path.join(code_root, 'Figure', f'figure5', f'figure_5b.pdf'), dpi=300)
# plt.close(fig)

# importlib.reload(ff)
# fig, _ = getattr(ff, 'figure_5c').draw(anal_data)
# fig.savefig(os.path.join(code_root, 'Figure', f'figure5', f'figure_5c.pdf'), dpi=300)
# plt.close(fig)

# for target in ['c', 'd', 'y']:
#     plt.figure()
#     x = anal_data['prdt_from_param'][f'r0_min_{target}_{target}'].values
#     y = anal_data['prdt_from_param'][f'r0_gmin_{target}_{target}'].values
#     z = anal_data['prdt_from_param'][f'r0_zero_vac_{target}'].values
    
#     im = plt.imshow((z - y) / (z - x))
#     plt.colorbar(im)
#     plt.gca().invert_yaxis()








# importlib.reload(ff)

# fig, _ = getattr(ff, f'figure_4a').draw(anal_data)

# fig.savefig(os.path.join(code_root, 'Figure', 'figure1', 'figure_1f.pdf'), dpi=300)
# plt.close(fig)

# getattr(ff, f'figure_4b').draw(anal_data)
# getattr(ff, f'figure_4c').draw(anal_data)
# getattr(ff, f'figure_4xx').draw(anal_data)

# subfig_num = [None, None, 7, 6, 3, 6]
# importlib.reload(ff)
# for fig_idx in range(3, 5):
#     for idx in lc[:subfig_num[fig_idx]]:
#         fig, _ = getattr(ff, f'figure_{fig_idx}{idx}').draw(anal_data)
#         fig.savefig(os.path.join(code_root, 'Figure', f'figure{fig_idx}', f'figure_{fig_idx}{idx}.pdf'), dpi=300)
#         plt.close(fig)

# importlib.reload(ff)
# for idx in lc[:1]:
#     getattr(ff, f'figure_3{idx}').draw(anal_data)
    
    

# import numpy as np
# import matplotlib.pyplot as plt
# from . import figure_setting
# import pandas as pd
# import seaborn as sns
# import itertools
# from Dependencies.CodeDependencies import  basic_params, param_data_loader
# countries = ['Ireland', 'Japan', 'United Kingdom', 'Singapore', 'France', 'Italy', 'Germany', 'United States', 'Spain', 'Austria', 'Israel', 'South Korea']
# ys = param_data_loader.load_all_data(countries, basic_params.group_div)

# import matplotlib.pyplot as plt
# plt.figure()
# plt.plot(countries, [ys[country]['populations'][-2:].sum() / ys[country]['populations'].sum() for country in countries])
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        