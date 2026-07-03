# -*- coding: utf-8 -*-
"""
Created on Sun Aug  3 15:37:24 2025

@author: fengm
"""



import matplotlib.pyplot as plt
from . import figure_setting


def draw(anal_data, **kwargs):
    ####################################################
    ####################################################
    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (14, 10)}, {'pos': (21, 0), 'size': (14, 10)}, {'pos': (42, 0), 'size': (14, 10)}],
                  [{'pos': (0, 15), 'size': (14, 10)}, {'pos': (21, 15), 'size': (14, 10)}, {'pos': (42, 15), 'size': (14, 10)}]]
    margin_attr = {'top': 2, 'bottom': 4, 'left': 4, 'right': 2}
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.2
    label_fontsize = 16
    tick_fontsize = 12
    text_fontsize = 16
    ####################################################
    
    
    res = anal_data['state_aggregation_alpha'] 
    
    for vac_idx, vac in enumerate(['', '_vac']):
        for idx, target in enumerate(['c', 'sym', 'd']):
            ax = axes[vac_idx][idx]
            plt.sca(ax)
            key = f'non_mar_alpha{vac}'
            plt.plot(res[key]['time_line'], res[key][target], linestyle = '-', color = '#34A29F', label = 'Detailed Model' if vac_idx == 0 and idx == 0 else None)
            key = f'non_mar{vac}'
            plt.plot(res[key]['time_line'], res[key][target], linestyle = '', marker = 'x', markevery = 1000, color = '#DA655D', label = 'General Model' if vac_idx == 0 and idx == 0 else None)
            
            figure_setting.set_xylabel(ax, 'Time (d)', 'Fraction', fontsize = label_fontsize, xlabel_coords = -0.12, ylabel_coords = -0.10)
            figure_setting.set_spine_linewidth(ax, spine_linewidth)
            figure_setting.set_tick_fontsize(ax, tick_fontsize)
            figure_setting.remove_spines(ax, ['top', 'right'])
            if vac_idx == 1:
                plt.axvline(60, linestyle = (0, (3, 1, 1, 1)), color = 'tab:gray', alpha = 0.8, linewidth = 0.8)
                plt.axvline(70, linestyle = ':', color = 'tab:gray', alpha = 0.8, linewidth = 0.8)
    return fig, axes
    