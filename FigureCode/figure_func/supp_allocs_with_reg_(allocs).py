# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 14:57:09 2026

@author: fengm
"""

import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import figure_setting
import seaborn as sns
from Dependencies.CodeDependencies import  basic_params, param_data_loader
import pandas as pd
import matplotlib.colors as mcolors

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
    grid_attrs = [[{'pos': (0, 0), 'size': (39, 10)}, {'pos': (50, 0), 'size': (39, 10)}, {'pos': (100, 0), 'size': (39, 10)}],
                  [{'pos': (0, 15), 'size': (39, 10)}, {'pos': (50, 15), 'size': (39, 10)}, {'pos': (100, 15), 'size': (39, 10)}],
                  [{'pos': (0, 30), 'size': (39, 10)}, {'pos': (50, 30), 'size': (39, 10)}, {'pos': (100, 30), 'size': (39, 10)}],
                  [{'pos': (0, 45), 'size': (39, 10)}, {'pos': (50, 45), 'size': (39, 10)}, {'pos': (100, 45), 'size': (39, 10)}],
                  [{'pos': (0, 60), 'size': (39, 10)}, {'pos': (50, 60), 'size': (39, 10)}, {'pos': (100, 60), 'size': (39, 10)}],
                  [{'pos': (0, 75), 'size': (39, 10)}, {'pos': (50, 75), 'size': (39, 10)}, {'pos': (100, 75), 'size': (39, 10)}],
                  [{'pos': (0, 90), 'size': (39, 10)}, {'pos': (50, 90), 'size': (39, 10)}, {'pos': (100, 90), 'size': (39, 10)}],
                  [{'pos': (142, 0), 'size': (1, 55)}]]
    margin_attr = {'top': 4, 'bottom': 5, 'left': 7, 'right': 7}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 12
    tick_fontsize = 9
    ####################################################
    
    
    sttg_formats = [['tab:green', '-', '0–9'], ['tab:red', '-', '10–19'], ['tab:blue', '-', '20–29'], ['tab:orange', '-', '30–39'], 
                    ['tab:purple', '-', '40–49'], ['tab:pink', '-', '50–59'], ['tab:gray', '-', '60–69'], ['black', '-', '70+']]
    age_groups = ['0–9', '10–19', '20–29', '30–39', '40–49', '50–59', '60–69', '70+']
    target_names = ['Cumulative infections', 'Deaths', 'YLL']
    
    selected_widx = [0, 1, 2, 4, 8, 16, 32]
    
    for idx, widx in enumerate(selected_widx):
        for target_idx, target in enumerate(['c', 'd', 'y']):
            ax = axes[idx][target_idx]
            plt.sca(ax)
            res = anal_data['dist_alloc_from_dysttg_for_const'][f'alloc_min_{target}_{widx}']
            ax, im = pcolor_heatmap(ax, res)
            figure_setting.set_xylabel(ax, 'Time (d)' if widx == selected_widx[-1] else '', 'Age Group', fontsize = label_fontsize, xlabel_coords = -0.28, ylabel_coords = -0.12)
            ax.text(0, 1.005, rf'$\lambda_{{\mathrm{{reg}}}}$ = {widx / 20}', fontsize = 9, transform = ax.transAxes, ha = 'left', va = 'bottom')
            if idx == 0: ax.text(0.5, 1.1, target_names[target_idx], fontsize = 13, transform = ax.transAxes, ha = 'center', va = 'bottom')
            plt.xticks(np.arange(0, res.shape[1] + 1, 30), np.arange(0, res.shape[1] + 1, 30), fontsize = tick_fontsize)
            if idx == 0 and target_idx == 0: 
                cbar = fig.colorbar(im, cax=axes[-1][0])
                cbar.set_label('Allocation (%)', rotation=270, labelpad=12, fontsize = label_fontsize)
                cbar.ax.yaxis.set_label_position('right')
                cbar.set_ticks(np.arange(6) * 0.07)
    return fig, axes