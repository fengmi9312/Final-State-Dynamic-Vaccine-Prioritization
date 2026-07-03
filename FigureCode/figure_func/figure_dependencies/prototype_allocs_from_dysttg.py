# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 16:30:30 2025

@author: fengm
"""


import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting
import seaborn as sns
from Dependencies.CodeDependencies import  basic_params, param_data_loader
import pandas as pd

def dist_bar(ax, results, category_names, category_colors):
    
    labels = list(results.keys())
    data = np.array(list(results.values.T))
    data_cum = data.cumsum(axis=1)
    
    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        heights = data[:, i]
        starts = data_cum[:, i] - heights
        ax.bar(labels, heights, bottom=starts, width=1, label=colname, color=color, linewidth = len(data) * 0.08 / 80, edgecolor = 'white', alpha = 0.8)
    return ax




def draw(anal_data, **kwargs):
    ####################################################
    
    scale_prop = 12
    
    grid_attrs = [[{'pos': (1, 0), 'size': (36, 4)}, {'pos': (1, 6), 'size': (36, 4)}, {'pos': (1, 18), 'size': (36, 4)}, {'pos': (1, 24), 'size': (36, 4)}],
                  [{'pos': (51, 0), 'size': (36, 4)}, {'pos': (51, 6), 'size': (36, 4)}, {'pos': (51, 18), 'size': (36, 4)}, {'pos': (51, 24), 'size': (36, 4)}],
                  [{'pos': (101, 0), 'size': (36, 4)}, {'pos': (101, 6), 'size': (36, 4)}, {'pos': (101, 18), 'size': (36, 4)}, {'pos': (101, 24), 'size': (36, 4)}]]
    
    margin_attr = {'top': 4, 'bottom': 4, 'left': 6, 'right': 9}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 12
    tick_fontsize = 9
    ####################################################
    
    sttg_formats = [['tab:green', '-', '0–9'], ['tab:red', '-', '10–19'], ['tab:blue', '-', '20–29'], ['tab:orange', '-', '30–39'], 
                    ['tab:purple', '-', '40–49'], ['tab:pink', '-', '50–59'], ['tab:gray', '-', '60–69'], ['black', '-', '70+']]
    age_groups = ['0–9', '10–19', '20–29', '30–39', '40–49', '50–59', '60–69', '70+']
    targets = ['c', 'd', 'y']
    sttgs = ['min', 'gmin']
    res = anal_data['allocs_dysttg_from_time']
    sttg_names = {'min': 'FS-DVP', 'gmin': 'TS-DVP'}
    obj_names = {'c': 'Cumulative Infections', 'd': 'Deaths', 'y': 'YLL'}
    r0_values = [1.4, 2.5]
    
    for target_idx, target in enumerate(targets):
        for r0_idx_idx, r0_idx in enumerate([9, 42]):
            for sttg_idx, sttg in enumerate(sttgs):
                ax = axes[target_idx][r0_idx_idx * 2 + sttg_idx]
                plt.sca(ax)
                anal_sheet_name = f'alloc_{sttg}_{target}_{r0_idx}'
                ax = dist_bar(ax, res[anal_sheet_name], age_groups, [sns.color_palette()[age_idx] for age_idx in range(8)])
                figure_setting.set_xylabel(ax, 'Time (d)' if sttg_idx == 1 else '', '', fontsize = label_fontsize, xlabel_coords = -0.48, ylabel_coords = -0.08)
                ax.text(0, 1.01, sttg_names[sttg], fontsize = 10, transform = ax.transAxes, ha = 'left', va = 'bottom')
                if sttg_idx == 0: ax.text(0.5, 1.05, f'$R_0 = {r0_values[r0_idx_idx]}$; {obj_names[target]}', fontsize = 12, transform = ax.transAxes, ha = 'center', va = 'bottom')
                plt.xticks(np.arange(0, 31, 10), np.arange(0, 31, 10), fontsize = tick_fontsize)
                plt.yticks(np.arange(0, 36, 35) / 10000, np.arange(0, 36, 35) / 100, fontsize = tick_fontsize)
                if target_idx == 2 and r0_idx_idx == 0 and sttg_idx == 1: ax.legend(loc = 'center left', fontsize = 9, bbox_to_anchor = (1.01, -1), labelspacing = 0.3)
                if sttg_idx != 1: ax.set_xticks([])
                if sttg_idx == 1: ax.text(-0.09, 1.5, 'Allocation (%)', fontsize = label_fontsize, transform = ax.transAxes, ha = 'right', va = 'center', rotation = 90)
    return fig, axes