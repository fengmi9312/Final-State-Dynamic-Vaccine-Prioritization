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
import matplotlib.colors as mcolors

def dist_bar(ax, results, category_names, category_colors):
    
    labels = list(results.keys())
    data = np.array(list(results.values.T))
    data_cum = data.cumsum(axis=1)
    
    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        heights = data[:, i]
        starts = data_cum[:, i] - heights
        ax.bar(labels, heights, bottom=starts, width=1, label=colname, color=color, linewidth = len(data) * 0.08 / 80, edgecolor = 'white', alpha = 0.8)
    return ax


def pcolor_heatmap(ax, results):
    base = plt.colormaps['seismic']
    trunc = mcolors.LinearSegmentedColormap.from_list('top_half', base(np.linspace(0.5, 1, 256)))

    data = np.array(list(results.values))
    H, W = data.shape
    im = ax.pcolormesh(np.arange(W+1)-0.5, np.arange(H+1)-0.5, data * 100, cmap = trunc, shading='auto')
    ax.hlines(np.arange(H + 1) - 0.5, xmin = -0.5, xmax = W - 0.5, color="tab:gray", linestyle = '--', linewidth=0.5)
    ax.set_ylim(H-0.5, -0.5)
    age_groups = ['0–9', '10–19', '20–29', '30–39', '40–49', '50–59', '60–69', '70+']
    plt.yticks(np.arange(H), age_groups, fontsize = 6.5)
    return ax, im




def draw(anal_data, **kwargs):
    target = kwargs.pop('target', 'c')
    ####################################################
    scale_prop = 9
    grid_attrs = [[{'pos': (0, 0), 'size': (39, 10)}, {'pos': (47, 0), 'size': (39, 10)}, {'pos': (94, 0), 'size': (39, 10)}, {'pos': (139, 0), 'size': (39, 10)},
                   {'pos': (0, 15), 'size': (39, 10)}, {'pos': (47, 15), 'size': (39, 10)}, {'pos': (94, 15), 'size': (39, 10)}, {'pos': (139, 15), 'size': (39, 10)},
                   {'pos': (0, 30), 'size': (39, 10)}, {'pos': (47, 30), 'size': (39, 10)}, {'pos': (94, 30), 'size': (39, 10)}, {'pos': (139, 30), 'size': (39, 10)}],
                  [{'pos': (180, 0), 'size': (1, 40)}]]
    margin_attr = {'top': 3, 'bottom': 5, 'left': 7, 'right': 7}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 12
    tick_fontsize = 9
    ####################################################
    
    sorted_countries = ['Ireland', 'Japan', 'United Kingdom', 'Singapore', 'France', 'Italy', 'Germany', 'United States', 'Spain', 'Austria', 'Israel', 'South Korea']
    country_data = param_data_loader.load_all_data(basic_params.country_abbr.keys(), basic_params.group_div)
    res = {}
    for country in basic_params.country_abbr.keys():
        data_tmp = anal_data['allocs_from_country_example'][f'alloc_min_{target}_{basic_params.country_abbr[country]}']
        data_len = data_tmp.shape[1] if data_tmp.shape[1] <= 120 else 120
        res[country] = pd.DataFrame({str(i): data_tmp[str(i)] for i in range(data_len)})
    #res = {country: pd.DataFrame({str(i): anal_data['allocs_from_country_example'][f'alloc_min_{target}_{basic_params.country_abbr[country]}'][str(i)] for i in range(50)}) for country in basic_params.country_abbr.keys()}
    # res = {country: anal_data['allocs_from_country_example'][f'alloc_min_{target}_{basic_params.country_abbr[country]}'] for country in basic_params.country_abbr.keys()}
    ####################################################
    
    sttg_formats = [['tab:green', '-', '0–9'], ['tab:red', '-', '10–19'], ['tab:blue', '-', '20–29'], ['tab:orange', '-', '30–39'], 
                    ['tab:purple', '-', '40–49'], ['tab:pink', '-', '50–59'], ['tab:gray', '-', '60–69'], ['black', '-', '70+']]
    age_groups = ['0–9', '10–19', '20–29', '30–39', '40–49', '50–59', '60–69', '70+']

    for idx, country in enumerate(sorted_countries):
        ax = axes[0][idx]
        plt.sca(ax)
        ax, im = pcolor_heatmap(ax, res[country])
        figure_setting.set_xylabel(ax, 'Time (d)' if idx in [8, 9, 10, 11] else '', 'Age Group' if idx in [0, 4, 8] else '', fontsize = label_fontsize, xlabel_coords = -0.28, ylabel_coords = -0.12)
        ax.text(0, 1.01, country, fontsize = 12, transform = ax.transAxes, ha = 'left', va = 'bottom')
        plt.xticks(np.arange(0, res[country].shape[1] + 1, 30), np.arange(0, res[country].shape[1] + 1, 30), fontsize = tick_fontsize)
        # plt.yticks(np.arange(0, 36, 7) / 10000, np.arange(0, 36, 7) / 100, fontsize = tick_fontsize)
        if idx == 7: 
            cbar = fig.colorbar(im, cax=axes[-1][0])
            cbar.set_label('Allocation (%)', rotation=270, labelpad=12, fontsize = label_fontsize)
            cbar.ax.yaxis.set_label_position('right')
            cbar.set_ticks(np.arange(6) * 0.07)
    return fig, axes