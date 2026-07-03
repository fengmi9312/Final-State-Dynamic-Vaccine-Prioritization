# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 22:58:38 2025

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
    scale_prop = 8
    grid_attrs = [[{'pos': (0, 0), 'size': (30, 25)}]]
    margin_attr = {'top': 2, 'bottom': 6, 'left': 7, 'right': 2}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 13.5
    tick_fontsize = 10
    ####################################################
    ax = axes[0][0]
    plt.sca(ax)
    res = anal_data['equivalence_simu']
    colors = ['#DA655D', '#34A29F']
    labels = ['Non-Markovian', 'Markovian Equivalence']
    for idx, pre_x in enumerate(['', 'equiv_']):
        for i in range(100):
            if i == 0: plt.plot(res[f'{pre_x}time_line_{i}'], res[f'{pre_x}c_{i}'] / 12000, linewidth = 0.1, color = colors[idx], zorder = 2 - idx, label = labels[idx])
            else: plt.plot(res[f'{pre_x}time_line_{i}'], res[f'{pre_x}c_{i}'] / 12000, linewidth = 0.1, color = colors[idx], zorder = 2 - idx)
    plt.axvline(20, linestyle = '--', color = 'tab:gray', linewidth = 1)
    figure_setting.set_xylabel(ax, 'Time (d)', 'Cumulative Infections', fontsize = label_fontsize, xlabel_coords = -0.125, ylabel_coords = -0.12)
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)
    figure_setting.remove_spines(ax, ['top', 'right'])
    return fig, axes
    