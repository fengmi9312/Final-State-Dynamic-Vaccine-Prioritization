#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 13:05:19 2025

@author: mifeng
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
    sttg_formats = {'curves_no_vac': ['black', '--', 'No Vaccination'], 'curves_min_c': ['tab:red', '-', 'FS-DVP'], 
                    'mean_curves_min_c': ['tab:blue', (0, (5, 1, 1, 1)), 'Piecewise Constant'], 
                    'optm_curves_min_c': ['tab:orange', (0, (1, 1)), 'Optimized Piecewise Constant']}
    res = anal_data['discrete_optm'] 
    
    ax = axes[0][0]
    plt.sca(ax)
    for curve_key in sttg_formats.keys():
        plt.plot(res[curve_key]['time_line'], res[curve_key]['c'], 
                 color = sttg_formats[curve_key][0], linestyle = sttg_formats[curve_key][1], label = sttg_formats[curve_key][2], 
                 linewidth = 2)
    
    figure_setting.set_xylabel(ax, 'Time (d)', 'Fraction', fontsize = label_fontsize, xlabel_coords = -0.12, ylabel_coords = -0.10)
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)
    figure_setting.remove_spines(ax, ['top', 'right'])
    
    return fig, axes
    