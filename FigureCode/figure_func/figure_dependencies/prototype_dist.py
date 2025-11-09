# -*- coding: utf-8 -*-
"""
Created on Thu May  1 13:49:30 2025

@author: fengm
"""

import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting
import seaborn as sns

from math import pi
import pandas as pd
 

def draw(anal_data, **kwargs):
    ####################################################
    target = kwargs.pop('target', 'c')
    file_idx = kwargs.pop('file_idx', 0)
    ####################################################
    scale_prop = 12
    grid_attrs = [[{'pos': (0, 0), 'size': (25, 20)}]]
    margin_attr = {'top': 2, 'bottom': 4, 'left': 3, 'right': 3}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 9
    tick_fontsize = 7
    ####################################################
    ax = axes[0][0]
    plt.sca(ax)
    res = anal_data['allocs_from_time']
    sttgs = ['zero_vac', 'under_20', '20-49', '20+', '60+', 'all_ages', 'min']
    colors = ['black', 'tab:green', 'tab:blue', 'tab:orange', 'tab:gray', 'tab:purple', 'tab:red']
    linestyles = ['-', '-', '-', '-', '-', '-', '-']
    markers = ['o', '^', 'p', 's', 'D', 'h', 'X']
    labels = ['No Vaccine', 'Under 20', '20–49', '20+', '60+', 'All Ages', 'Optimal']
    age_groups = ['0–9','10–19','20–29','30–39','40–49','50–59','60–69','70+']
    for idx, sttg in enumerate(sttgs):
        if sttg != 'min': res_key = f'dist_{sttg}_{target}_{file_idx}'
        else: res_key = f'dist_{sttg}_{target}_{target}_{file_idx}'
        last_idx = res[res_key].columns[-1]
        plt.plot(age_groups, res[res_key][last_idx], linewidth = 1.2, linestyle = linestyles[idx], label = labels[idx], color = colors[idx], marker = markers[idx], markersize = 8, markeredgewidth = 0.6, markeredgecolor = 'white', markerfacecolor = colors[idx])
    figure_setting.set_xylabel(ax, 'Age Group', 'Fraction', fontsize = label_fontsize, xlabel_coords = -0.12, ylabel_coords = -0.10)
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)
    figure_setting.remove_spines(ax, ['top', 'right'])
    return fig, axes
    