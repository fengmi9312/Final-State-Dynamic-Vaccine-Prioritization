# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 12:59:25 2025

@author: MIFENG
"""


import os
import sys
folder_level = 1
code_root = os.path.dirname(os.path.abspath(__file__))
for idx in range(folder_level): code_root = os.path.dirname(code_root)
sys.path.append(code_root)
from Dependencies.FrameDependencies import expr_data_loader, file_writer
import AnalysisCode.analysis_func as af
import importlib
from Dependencies.CodeDependencies import basic_params

import pandas as pd
from Dependencies.FrameDependencies import name_principle
from concurrent.futures import ThreadPoolExecutor, as_completed


def _load_one_file(task_name, file_idx):
    file_path = name_principle.analysis_file(task_name, file_idx)
    try:
        data = pd.read_excel(file_path, index_col=0, sheet_name=None)
        return str(file_idx), data, None
    except Exception as e:
        return str(file_idx), None, e


def load_certain_edatax(expr_name, expr_param, file_amount, max_workers=8):
    task_name = name_principle.get_task_name(expr_name, expr_param)
    res = {task_name: {}}
    errors = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(_load_one_file, task_name, file_idx)
            for file_idx in range(file_amount)
        ]

        for future in as_completed(futures):
            file_idx_str, data, err = future.result()
            if err is None:
                res[task_name][file_idx_str] = data
            else:
                errors[file_idx_str] = err

    if errors:
        for file_idx_str, err in errors.items():
            print(f'Failed to import {task_name}[{file_idx_str}]: {err}')
        raise RuntimeError(f'{len(errors)} files failed to import.')

    res[task_name] = {
        str(file_idx): res[task_name][str(file_idx)]
        for file_idx in range(file_amount)
    }

    print(task_name + ' imported')
    return res





edata = {}
# countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea', 'Italy', 'Singapore']
# country_idx = 65

# task_dict = {'optm_from_country': {}, 'optm_from_country_add': {}}
# for country in countries[country_idx * 2:country_idx * 2 + 2]:
#     task_dict['optm_from_country'].update({country: 40})
#     task_dict['optm_from_country_add'].update({country: 40})

# additional_task_dict = task_dict
# for expr_name, task_item in additional_task_dict.items():
#     for expr_param, file_amount in task_item.items():
#         edata.update(expr_data_loader.load_certain_edata(expr_name, expr_param, file_amount))


# anal_data = {}
# anal_list = []
# for key in task_dict['optm_from_country'].keys():
#     anal_list.append(f'dist_alloc_from_{basic_params.country_abbr[key]}')

# importlib.reload(af)
# additional_anal_list = anal_list
# for anal_name in additional_anal_list:
#     anal_data.update({anal_name: getattr(af, f'get_{anal_name}').analyze(edata)})

# for key, item in anal_data.items():
#     file_path = os.path.join(code_root, 'AnalysisData', f'Data_{key}.xlsx')
#     file_writer.write_to_file(item, file_path)

task_dict = {'optm_from_dysttg': {'lower':120}, 'optm_from_equity_r0': {'param': 40}}

additional_task_dict = {'optm_from_dysttg_for_sens': {'v14_d14':120, 'v56_d14':120, 'v35_d7':120, 'v35_d21':120}}
additional_task_dict = {'optm_from_dysttg_for_const': {'lower':41}}
for expr_name, task_item in additional_task_dict.items():
    for expr_param, file_amount in task_item.items():
        edata.update(expr_data_loader.load_certain_edata(expr_name, expr_param, file_amount))


anal_data = {}
anal_list = ['dist_alloc_from_dysttg_for_const']


importlib.reload(af)
additional_anal_list = anal_list
for anal_name in additional_anal_list:
    anal_data.update({anal_name: getattr(af, f'get_{anal_name}').analyze(edata)})



for key, item in anal_data.items():
    file_path = os.path.join(code_root, 'AnalysisData', f'Data_{key}.xlsx')
    file_writer.write_to_file(item, file_path)

# import matplotlib.pyplot as plt
# import matplotlib.colors as mcolors
# import numpy as np
# def pcolor_heatmap(ax, results):
#     base = plt.colormaps['seismic']
#     trunc = mcolors.LinearSegmentedColormap.from_list('top_half', base(np.linspace(0.5, 1, 256)))

#     data = np.array(list(results.values))
#     H, W = data.shape
#     im = ax.pcolormesh(np.arange(W+1)-0.5, np.arange(H+1)-0.5, data * 100, cmap = trunc, shading='auto')
#     ax.hlines(np.arange(H + 1) - 0.5, xmin = -0.5, xmax = W - 0.5, color="tab:gray", linestyle = '--', linewidth=0.5)
#     ax.set_ylim(H-0.5, -0.5)
#     age_groups = ['0–9', '10–19', '20–29', '30–39', '40–49', '50–59', '60–69', '70+']
#     plt.yticks(np.arange(H), age_groups, fontsize = 8)
#     return ax, im

# target = 'c'
# plt.plot(anal_data['dist_alloc_from_dysttg_for_const']['prdts'][target])

# for i in range(10):
#     plt.figure()
#     pcolor_heatmap(plt.gca(), anal_data['dist_alloc_from_dysttg_for_const'][f'alloc_min_{target}_{i*4}'])

# for sttg in sttgs:
#     plt.plot(anal_data['ipeak_from_dysttg'][f'example_{sttg}']['res'], label = sttg)
# plt.legend()



# res = analysis_func.prdt_with_param.analyze(edata)

# colors = {'under_20': 'tab:green', '20-49': 'tab:blue', '20+': 'tab:orange', '60+': 'tab:gray', 'all_ages':'tab:brown', 'zero_vac': 'black', 'min': 'tab:red'}
# fig, axes = plt.subplots(4, 3)
# for ax_arr_idx, expr_param in enumerate(['r0', 'daily_vac', 'vac_dur', 'delay']):
#     ax_arr = axes[ax_arr_idx]
#     for ax_idx, target in enumerate(['c', 'd', 'y']):
#         ax = ax_arr[ax_idx]
#         plt.sca(ax)
#         for sttg in ['under_20', '20-49', '20+', '60+', 'all_ages', 'min']:
#             if sttg == 'min': rsttg = f'{sttg}_{target}'
#             else: rsttg = sttg
#             plt.plot(res[expr_param][expr_param], res[expr_param][f'prdt_{rsttg}_{target}'], color = colors[sttg], 
#                      linestyle = '-' if sttg == 'min' else '--')
#         if expr_param == 'r0': 
#             plt.xscale('log')
        
    
    
    

# res = analysis_func.comparison_example.analyze(edata)
# import matplotlib.pyplot as plt
# optm_targets = ['c', 'd', 'y']
# empirical_sttgs = ['under_20', '20-49', '20+', '60+', 'all_ages', 'zero_vac']
# sttgs = ['no_vac'] + empirical_sttgs + [f'min_{optm_target}' for optm_target in optm_targets] + [f'min_dis_{optm_target}' for optm_target in optm_targets]
# for target in ['c', 'd', 'y']:
#     plt.figure()
#     for sttg in sttgs:
#         plt.plot(res[f'curve_{sttg}']['time_line'], res[f'curve_{sttg}'][f'curve_{target}'], linestyle = '-' if sttg.split('_')[-1] == target else '--', label = sttg)
#     plt.legend()
        
# sttg = 'min_c'
# plt.figure()
# ys = np.array([res[f'effr_{sttg}_c'][str(i * 100)] for i in range(120)]).T
# colors = ['tab:red', 'tab:green', 'tab:blue', 'tab:orange', 'tab:pink', 'tab:brown', 'tab:gray', 'black']
# for i in range(8):
#     plt.plot(ys[i], color = colors[i])
            
            


# import matplotlib.pyplot as plt
# import numpy as np
# def survey(ax, results, category_names):
#     labels = list(results.keys())
#     data = np.array(list(results.values()))
#     data_cum = data.cumsum(axis=1)
#     category_colors = plt.colormaps['RdYlGn'](
#         np.linspace(0.15, 0.85, data.shape[1]))

#     ax.invert_yaxis()
#     ax.xaxis.set_visible(False)
#     ax.set_xlim(0, np.sum(data, axis=1).max())

#     for i, (colname, color) in enumerate(zip(category_names, category_colors)):
#         widths = data[:, i]
#         starts = data_cum[:, i] - widths
#         rects = ax.barh(labels, widths, left=starts, height=0.5,
#                         label=colname, color=color)

#         r, g, b, _ = color
#         text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
#         # ax.bar_label(rects, label_type='center', color=text_color)
#     ax.legend(ncols=len(category_names), bbox_to_anchor=(0, 1),
#               loc='lower left', fontsize='small')

#     return ax








# edata = {}
# expr_name, expr_param = 'optm_from_example', 'param'
# edata.update(load_one_certain_edata(expr_name, expr_param, [3]))
# res = analysis_func.comparison_example.analyze(edata)


# for idx, sttg in enumerate(['min_steady_c', 'min_steady_d', 'min_steady_y']):
#     fig, ax  = plt.subplots(1, 1)
#     plt.sca(ax)
#     survey(ax, res[f'alloc_{sttg}'], [str(i) for i in range(8)])