# -*- coding: utf-8 -*-
"""
Created on Tue May 27 02:51:50 2025

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
    target = kwargs.pop('target', 'c')
    file_idx = kwargs.pop('file_idx', 0)
    ####################################################
    scale_prop = 9
    grid_attrs = [[{'pos': (0, 0), 'size': (39, 10)}, {'pos': (0, 15), 'size': (39, 10)}]]
    margin_attr = {'top': 3, 'bottom': 5, 'left': 7, 'right': 11}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 12
    tick_fontsize = 9
    ####################################################
    
    countries = ['United States']
    country_data = param_data_loader.load_all_data(basic_params.country_abbr.keys(), basic_params.group_div)
    res = []
    for r0_idx in range(2):
        data_tmp = anal_data['changing_example'][f'alloc_min_{target}_{file_idx}_{r0_idx}']
        data_len = data_tmp.shape[1] if data_tmp.shape[1] <= 120 else 120
        res.append(pd.DataFrame({str(i): data_tmp[str(i)] * country_data['United States']['populations'] for i in range(data_len)}))
    ####################################################
    
    sttg_formats = [['tab:green', '-', '0–9'], ['tab:red', '-', '10–19'], ['tab:blue', '-', '20–29'], ['tab:orange', '-', '30–39'], 
                    ['tab:purple', '-', '40–49'], ['tab:pink', '-', '50–59'], ['tab:gray', '-', '60–69'], ['black', '-', '70+']]
    age_groups = ['0–9', '10–19', '20–29', '30–39', '40–49', '50–59', '60–69', '70+']

    for r0_idx in range(2):
        ax = axes[0][r0_idx]
        plt.sca(ax)
        ax = dist_bar(ax, res[r0_idx], age_groups, [sns.color_palette()[age_idx] for age_idx in range(8)])
        figure_setting.set_xylabel(ax, 'Time (d)' if r0_idx == 1 else '', 'Allocation (%)', fontsize = label_fontsize, xlabel_coords = -0.28, ylabel_coords = -0.12)
        plt.xticks(np.arange(0, res[r0_idx].shape[1] + 1, 30), np.arange(0, res[r0_idx].shape[1] + 1, 30), fontsize = tick_fontsize)
        plt.yticks(np.arange(0, 36, 7) / 10000, np.arange(0, 36, 7) / 100, fontsize = tick_fontsize)
    return fig, axes