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
from matplotlib.ticker import ScalarFormatter



def draw(anal_data, **kwargs):
    target = kwargs.pop('target', 'c')
    ####################################################
    scale_prop = 9
    grid_attrs = [[{'pos': (0, 0), 'size': (36, 30)}, {'pos': (50, 0), 'size': (36, 30)}, {'pos': (100, 0), 'size': (36, 30)}]]
    margin_attr = {'top': 3, 'bottom': 6, 'left': 7, 'right': 7}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 12
    tick_fontsize = 9
    ####################################################
    target_names = ['Cumulative infections', 'Deaths', 'YLL']
    ylabels = ['Cumulative infections (%)', 'Deaths (%)', 'YLL (%)']
    colors = ['tab:orange', 'k', 'tab:blue']
    selected_widx = [0, 1, 2, 4, 8, 16, 32]
    
    for target_idx, target in enumerate(['c', 'd', 'y']):
        ax = axes[0][target_idx]
        plt.sca(ax)
        res = anal_data['dist_alloc_from_dysttg_for_const']['prdts'][target]
        plt.plot(np.arange(41) / 20, res * 100, color = 'tab:blue', marker = 'D', label = 'Final epidemic burden')
        if target_idx == 0: plt.legend(loc='lower left',bbox_to_anchor=(0.25, 0.5),frameon=False)
        ax_r = ax.twinx()
        pnlt = anal_data['dist_alloc_from_dysttg_for_const']['pnlt'][target]
        ax_r.plot(np.arange(41) / 20, pnlt, color='tab:red', marker='o', linestyle='--', label = 'Average switching penalty')
        if target_idx == 0: plt.legend(loc='lower left',bbox_to_anchor=(0.25, 0.4),frameon=False)
        ax.text(0.02, 1.01, target_names[target_idx], fontsize = 13, transform = ax.transAxes, ha = 'left', va = 'bottom')
        ax_r.set_ylabel('Average switching penalty', fontsize=label_fontsize)
        formatter = ScalarFormatter(useMathText=True)
        formatter.set_scientific(True)
        formatter.set_powerlimits((0, 0))
        ax_r.yaxis.set_major_formatter(formatter)
        ax_r.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        offset_text = ax_r.yaxis.get_offset_text()
        offset_text.set_x(1.0)
        offset_text.set_ha('left')
        figure_setting.set_xylabel(ax, r'$\lambda_{{\mathrm{{reg}}}}$', ylabels[target_idx], fontsize = label_fontsize, xlabel_coords = -0.1, ylabel_coords = -0.13 if target == 'd' else -0.1)
        for i in selected_widx: plt.axvline(i / 20, linestyle = ':', color = 'tab:gray', linewidth = 1, alpha = 0.75)
    return fig, axes