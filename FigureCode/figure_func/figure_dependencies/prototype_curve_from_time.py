# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 17:24:59 2025

@author: MIFENG
"""

import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting

def draw(anal_data, **kwargs):
    ####################################################
    target = kwargs.pop('target', 'c')
    file_idx = kwargs.pop('file_idx', 0)
    changing_example = kwargs.pop('changing_example', False)
    r0_idx = kwargs.pop('r0_idx', None)
    ####################################################
    scale_prop = 12
    grid_attrs = [[{'pos': (0, 0), 'size': (30, 25)}]]
    margin_attr = {'top': 2, 'bottom': 6, 'left': 6, 'right': 8}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 12
    tick_fontsize = 10
    ####################################################
    sttg_formats = {'zero_vac': ['black', (0, (2, 1)), 'No Vaccine'], 'under_20': ['tab:green', (0, (1, 1)), 'Under 20'], '20-49': ['tab:blue', (0, (3, 1)), '20–49'], 
                    '20+': ['tab:orange', (0, (3, 1, 1, 1)), '20+'], '60+': ['tab:gray', (0, (5, 1)), '60+'], 'all_ages': ['tab:purple', (0, (5, 1, 1, 1)), 'All Ages'], 
                    'min': ['tab:red', '-', 'FS-DVP']}
    ax = axes[0][0]
    plt.sca(ax)
    res = anal_data['comparison_example'] if not changing_example else anal_data['changing_example']
    for sttg in sttg_formats.keys():
        if sttg == 'min' or sttg == 'tmin': rsttg = f'{sttg}_{target}'
        else: rsttg = sttg
        curve_key = f'curve_{rsttg}_{file_idx}' if not changing_example else f'curve_{rsttg}_{file_idx}_{r0_idx}'
        plt.plot(res[curve_key]['time_line'], res[curve_key][f'curve_{target}'], 
                 color = sttg_formats[sttg][0], linestyle = sttg_formats[sttg][1], label = sttg_formats[sttg][2], linewidth = 2)
    
    figure_setting.set_xylabel(ax, 'Time (d)', 'Fraction', fontsize = label_fontsize, xlabel_coords = -0.12, ylabel_coords = -0.10)
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)
    figure_setting.remove_spines(ax, ['top', 'right'])
    return fig, axes
    