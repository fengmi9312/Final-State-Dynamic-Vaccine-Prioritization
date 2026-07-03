# -*- coding: utf-8 -*-
"""
Created on Sat Jun 28 21:12:50 2025

@author: fengm
"""


import matplotlib.pyplot as plt
from . import figure_setting


def draw(anal_data, **kwargs):
    ####################################################
    ####################################################
    scale_prop = 12
    grid_attrs = [[{'pos': (0, 0), 'size': (42, 30)}]]
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
    sttg_formats = {'zero_vac': ['black', '--', 'No Vaccine'], 'min': ['tab:red', '-', 'NF-DVP'], 'gmin': ['tab:blue', '-', 'NT-DVP']}
    res = anal_data['comparison_dysttg_example'] 
    
    for idx, target in enumerate(['d']):
        ax = axes[0][idx]
        plt.sca(ax)
        for sttg in sttg_formats.keys():
            if sttg in ['min', 'gmin', 'mmin', 'mgmin']: rsttg = f'{sttg}_{target}'
            else: rsttg = sttg
            curve_key = f'curve_{rsttg}_lower_0'
            plt.plot(res[curve_key]['time_line'], res[curve_key][f'curve_{target}'], 
                     color = sttg_formats[sttg][0], linestyle = sttg_formats[sttg][1], label = sttg_formats[sttg][2], 
                     linewidth = 2)
        
        figure_setting.set_xylabel(ax, 'Time (d)', 'Fraction', fontsize = label_fontsize, xlabel_coords = -0.12, ylabel_coords = -0.10)
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
        figure_setting.remove_spines(ax, ['top', 'right'])
    return fig, axes
    