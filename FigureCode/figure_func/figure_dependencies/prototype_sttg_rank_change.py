# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 23:34:45 2025

@author: fengm
"""



import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting
import seaborn as sns
from Dependencies.CodeDependencies import basic_params
import pandas as pd






def draw(anal_data, **kwargs):
    file_idx = kwargs.pop('file_idx', 0)
    ####################################################
    scale_prop = 9
    grid_attrs = [[{'pos': (0, 0), 'size': (35, 70)}, {'pos': (45, 0), 'size': (35, 70)}, {'pos': (90, 0), 'size': (35, 70)}]]
    margin_attr = {'top': 3, 'bottom': 5, 'left': 15, 'right': 5}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 12
    tick_fontsize = 9
    ####################################################
    
    sttg_formats = {'zero_vac': ['black', '--', 'o', 'No Vaccine'], 'under_20': ['tab:green', '--', '^', 'Under 20'], '20-49': ['tab:blue', '--', 'p', '20–49'], 
                    '20+': ['tab:orange', '--', 's', '20+'], '60+': ['tab:gray', '--', 'D', '60+'], 'all_ages': ['tab:purple', '--', 'h', 'All Ages'], 'min': ['tab:red', '-', 'X', 'FS-DVP']}
    solid_sttgs = {'c': ['under_20', '20-49'], 'd': ['under_20', '60+'], 'y': ['under_20', '20-49']}
    
    for idx, target in enumerate(['c', 'd', 'y']):
        ax = axes[0][idx]
        plt.sca(ax)
        plt.axvline(x=0, color='black', linestyle='--', linewidth=1) 
        plt.axvline(x=1, color='black', linestyle='--', linewidth=1)
        res = anal_data['changing_example']
        for idx, sttg in enumerate(sttg_formats.keys()):
            if sttg == 'min': rsttg = f'{sttg}_{target}'
            else: rsttg = sttg
            curve_key = f'curve_{rsttg}_{file_idx}'
            y0, y1 = res[f'{curve_key}_0'][f'curve_{target}'].to_numpy()[-1], res[f'{curve_key}_1'][f'curve_{target}'].to_numpy()[-1]
            linestyle = '-' if sttg in solid_sttgs[target] else ':'
            if sttg == 'min': linestyle = '--'
            zorder = 10 + (len(sttg_formats) - idx) if sttg in solid_sttgs[target] else 5
            if sttg == 'min': zorder = 20
            plt.plot([0, 1], [y0, y1], color = sttg_formats[sttg][0], linestyle = linestyle, linewidth = 2.5, zorder = zorder)
            plt.plot([0, 1], [y0, y1], color = sttg_formats[sttg][0], linestyle = '', label = sttg_formats[sttg][3], marker = sttg_formats[sttg][2], markersize = 10, markeredgewidth = 0.8, markeredgecolor = 'white', zorder = zorder)
            # plt.text(-0.04, y0,  f"{sttg_formats[sttg][3]}, {y0}", fontsize=8, color='black', transform = ax.transData, ha = 'right', va = 'center') 
            # plt.text(1.04, y1,  f"{sttg_formats[sttg][3]}, {y1}", fontsize=8, color='black', transform = ax.transData, ha = 'left', va = 'center') 
        # plt.xlim(0, 1)
        plt.xticks([]) # Remove y-axis
        plt.yticks([]) # Remove y-axis
        plt.box(False) # Remove the bounding box around plot
    return fig, axes