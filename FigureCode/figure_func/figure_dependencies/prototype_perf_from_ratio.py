# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 18:55:33 2025

@author: fengm
"""

import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting

def draw(anal_data, **kwargs):
    ####################################################
    scale_prop = 12
    grid_attrs = [[{'pos': (0, 0), 'size': (42, 30)}]]
    margin_attr = {'top': 2, 'bottom': 6, 'left': 6, 'right': 4}
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.6
    label_fontsize = 16
    tick_fontsize = 12
    text_fontsize = 16
    ####################################################
    sttgs = ['zero_vac', 'under_20', '20-49', '20+', '60+', 'all_ages', 'min', 'gmin', 'mmin', 'mgmin']
    labels = {'c': 'Cumulative Infections', 'd': 'Deaths', 'y': 'YLL'}
    colors = {'c': 'tab:red', 'd': 'tab:blue', 'y': 'tab:orange'}
    linestyles = ['-', ':', ':', ':', ':', ':', '-', '-', '-', '-']
    linewidths = [2.5, 1, 1, 1, 1, 1, 2.5, 2.5, 2.5, 2.5]
    zorders = [1, 2, 3, 4, 5, 6, 10, 7, 8, 9]
    adata = anal_data['prdt_from_ratio']['res']
    xlabel = r'$R_0$'
    mark_text = {'c': 'Cumulative Infections', 'd': 'Deaths', 'y': 'YLL'}
    adata = anal_data['prdt_from_ratio']['res']
    ax = axes[0][0]
    plt.sca(ax)
    for idx, target in enumerate(['c', 'd', 'y']):
        zv, nf, nt = adata[f'prdt_zero_vac_{target}'], adata[f'prdt_min_{target}_{target}'], adata[f'prdt_mmin_{target}_{target}']
        print(zv, nf, nt)
        plt.plot(adata['ratio'], (nt - nf) / (zv - nf), color = colors[target], linewidth = 2, label= labels[target])
        figure_setting.set_xylabel(ax, xlabel, 'yyy', fontsize = label_fontsize, xlabel_coords = -0.08, ylabel_coords = -0.08)
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
        ax.text(0.02, 0.98, f'{mark_text[target]}', fontsize = text_fontsize, transform = ax.transAxes, ha = 'left', va = 'top')
        #plt.xticks(np.arange(1, 6), np.arange(1, 6))
    return fig, axes
    