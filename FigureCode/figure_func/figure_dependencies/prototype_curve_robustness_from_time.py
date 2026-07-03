# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 14:35:54 2025

@author: fengm
"""

import matplotlib.pyplot as plt
from . import figure_setting


def draw(anal_data, **kwargs):
    ####################################################
    robust_type = kwargs.pop('robust_type', 'dy')
    file_idx = kwargs.pop('file_idx', 0)
    ####################################################
    scale_prop = 12
    grid_attrs = [[{'pos': (0, 0), 'size': (42, 30)}, {'pos': (50, 0), 'size': (42, 30)}, {'pos': (100, 0), 'size': (42, 30)}]]
    margin_attr = {'top': 2, 'bottom': 6, 'left': 6, 'right': 4}
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.6
    label_fontsize = 16
    tick_fontsize = 12
    text_fontsize = 16
    ####################################################
    
    
    ax = axes[0][0]
    plt.sca(ax)
    if robust_type == 'dy': 
        sttg_formats = {'zero_vac': ['black', (0, (2, 1)), 'No Vaccine'], 'under_20': ['tab:green', (0, (1, 1)), 'Under 20'], '20-49': ['tab:blue', (0, (3, 1)), '20–49'], 
                        '20+': ['tab:orange', (0, (3, 1, 1, 1)), '20+'], '60+': ['tab:gray', (0, (5, 1)), '60+'], 'all_ages': ['tab:purple', (0, (5, 1, 1, 1)), 'All Ages'], 
                        'min': ['tab:red', '-', 'FS-DVP']}
        res = anal_data['comparison_example'] 
    elif robust_type == 'nf': 
        sttg_formats = {'zero_vac': ['black', (0, (2, 1)), 'No Vaccine'], 'under_20': ['tab:green', (0, (1, 1)), 'Under 20'], '20-49': ['tab:blue', (0, (3, 1)), '20–49'], 
                        '20+': ['tab:orange', (0, (3, 1, 1, 1)), '20+'], '60+': ['tab:gray', (0, (5, 1)), '60+'], 'all_ages': ['tab:purple', (0, (5, 1, 1, 1)), 'All Ages'], 
                        'min': ['tab:red', '-', 'FS-DVP']}
        res = anal_data['comparison_example_comp'] 
    else: pass
    
    for idx, target in enumerate(['c', 'd', 'y']):
        ax = axes[0][idx]
        plt.sca(ax)
        for sttg in sttg_formats.keys():
            if sttg in ['min', 'gmin', 'mmin', 'mgmin']: rsttg = f'{sttg}_{target}'
            else: rsttg = sttg
            if type(file_idx) == int: curve_key = f'curve_{rsttg}_{file_idx}'
            else: curve_key = f'curve_{rsttg}_{file_idx[idx]}'
            plt.plot(res[curve_key]['time_line'], res[curve_key][f'curve_{target}'], 
                     color = sttg_formats[sttg][0], linestyle = sttg_formats[sttg][1], label = sttg_formats[sttg][2], linewidth = 1 if sttg not in ['min', 'gmin', 'mmin', 'mgmin'] and robust_type == 'nf' else 2)
        
        figure_setting.set_xylabel(ax, 'Time (d)', 'Fraction', fontsize = label_fontsize, xlabel_coords = -0.12, ylabel_coords = -0.10)
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
        figure_setting.remove_spines(ax, ['top', 'right'])
    return fig, axes
    