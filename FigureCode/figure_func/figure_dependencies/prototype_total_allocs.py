# -*- coding: utf-8 -*-
"""
Created on Thu May  8 17:20:15 2025

@author: fengm
"""


import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting
import seaborn as sns



def draw(anal_data, **kwargs):
    ####################################################
    target = kwargs.pop('target', 'c')
    file_idx_0 = kwargs.pop('file_idx_0', 1)
    file_idx_1 = kwargs.pop('file_idx_1', 4)
    ####################################################
    scale_prop = 12
    grid_attrs = [[{'pos': (0, 0), 'size': (16, 12)}, {'pos': (21, 0), 'size': (16, 12)}]]
    margin_attr = {'top': 2, 'bottom': 6, 'left': 4, 'right': 2}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 10
    tick_fontsize = 9
    ####################################################
    age_groups = ['0–9', '10–19', '20–29', '30–39', '40–49', '50–59', '60–69', '70+']
    colors = ['tab:red', 'black']
    hatches= ['///', '...']
    res = anal_data['allocs_from_time']
    file_idxes = [file_idx_0, file_idx_1]
    for idx in range(2):
        ax = axes[0][idx]
        plt.sca(ax)
        plt.bar(np.arange(8), res[f'alloc_min_{target}_{file_idxes[idx]}'].values.sum(axis = 1), hatch = hatches[idx], color = 'none', edgecolor = colors[idx], linewidth = 1.5,)
        plt.xticks(np.arange(8), age_groups, rotation = 270)
        figure_setting.set_xylabel(ax, 'Age Group', 'Allocation', fontsize = label_fontsize, xlabel_coords = -0.35, ylabel_coords = -0.10)
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
    return fig, axes