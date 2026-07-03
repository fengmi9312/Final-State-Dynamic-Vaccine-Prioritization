# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 14:35:54 2025

@author: fengm
"""

import matplotlib.pyplot as plt
from . import figure_setting
import numpy as np


def draw(anal_data, **kwargs):
    ####################################################
    scale_prop = 12
    grid_attrs = [[{'pos': (0, 0), 'size': (42, 30)}, {'pos': (50, 0), 'size': (42, 30)}]]
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
    sttg_formats_list = [{'zero_vac': ['black', (0, (2, 1)), 'No Vaccine'], 'under_20': ['tab:green', (0, (1, 1)), 'Under 20'], '20-49': ['tab:blue', (0, (3, 1)), '20–49'], 
                        '20+': ['tab:orange', (0, (3, 1, 1, 1)), '20+'], '60+': ['tab:gray', (0, (5, 1)), '60+'], 'all_ages': ['tab:purple', (0, (5, 1, 1, 1)), 'All Ages'], 
                        'min_c': ['tab:red', '-', 'FS-DVP, cumulative infections']},
                         {'zero_vac': ['black', (0, (2, 1)), 'No Vaccine'], 
                        'min_c': ['tab:red', '-', 'FS-DVP, cumulative infections'], 'min_d': ['tab:green', (0, (1, 1)), 'FS-DVP, deaths'], 'min_y': ['tab:orange', (0, (3, 1, 1, 1)), 'FS-DVP, YLL'], 
                        'gmin_c': ['tab:blue', (0, (3, 1)), 'TS-DVP, cumulative infections'], 'gmin_d': ['tab:gray', (0, (5, 1)), 'TS-DVP, deaths'], 'gmin_y': ['tab:purple', (0, (5, 1, 1, 1)), 'TS-DVP, YLL']}]
    
    for i in range(2):
        sttg_formats = sttg_formats_list[i]
        ax = axes[0][i]
        plt.sca(ax)
        for sttg in sttg_formats.keys():
            res = anal_data['ipeak_from_dysttg'][sttg]['res']
            time_line = np.arange(len(res)) * 0.01
            plt.plot(time_line, res, color = sttg_formats[sttg][0], linestyle = sttg_formats[sttg][1], label = sttg_formats[sttg][2], linewidth = 2)
        figure_setting.set_xylabel(ax, 'Time (d)', 'Fraction', fontsize = label_fontsize, xlabel_coords = -0.12, ylabel_coords = -0.10)
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
        figure_setting.remove_spines(ax, ['top', 'right'])

    return fig, axes
    