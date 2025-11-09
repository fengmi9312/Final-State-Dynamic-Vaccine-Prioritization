# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 02:07:48 2025

@author: fengm
"""



import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting

def draw(anal_data, **kwargs):
    ####################################################
    target = kwargs.pop('target', 'c')
    file_idx = kwargs.pop('file_idx', 0)
    ####################################################
    scale_prop = 12
    grid_attrs = [[{'pos': (0, 0), 'size': (30, 25)}, {'pos': (0, 33), 'size': (30, 25)}]]
    margin_attr = {'top': 2, 'bottom': 6, 'left': 6, 'right': 8}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 12
    tick_fontsize = 10
    
    linestyles = [(0, (2, 1)), (0, (1, 1)), (0, (3, 1)), (0, (3, 1, 1, 1)), (0, (5, 1)), (0, (5, 1, 1, 1)), '-']
    ####################################################
    sttg_formats = {'zero_vac': ['black', (0, (2, 1)), 'No Vaccine'], 'under_20': ['tab:green', (0, (1, 1)), 'Under 20'], '20-49': ['tab:blue', (0, (3, 1)), '20–49'], 
                    '20+': ['tab:orange', (0, (3, 1, 1, 1)), '20+'], '60+': ['tab:gray', (0, (5, 1)), '60+'], 'all_ages': ['tab:purple', (0, (5, 1, 1, 1)), 'All Ages'], 'min': ['tab:red', '-', 'FS-DVP']}
    res = anal_data['changing_example']
    for r0_idx in range(2):
        ax = axes[0][r0_idx]
        plt.sca(ax)
        for sttg in sttg_formats.keys():
            if sttg == 'min' or sttg == 'tmin': rsttg = f'{sttg}_{target}'
            else: rsttg = sttg
            curve_key = f'curve_{rsttg}_{file_idx}_{r0_idx}'
            plt.plot(res[curve_key]['time_line'], res[curve_key][f'curve_{target}'], 
                     color = sttg_formats[sttg][0], linestyle = sttg_formats[sttg][1], label = sttg_formats[sttg][2], linewidth = 2)
        
        figure_setting.set_xylabel(ax, 'Time (d)', 'Fraction', fontsize = label_fontsize, xlabel_coords = -0.12, ylabel_coords = -0.10)
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
        figure_setting.remove_spines(ax, ['top', 'right'])
    return fig, axes
    