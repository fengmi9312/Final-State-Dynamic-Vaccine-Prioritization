# -*- coding: utf-8 -*-
"""
Created on Wed May  7 11:50:09 2025

@author: fengm
"""



import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting

def draw(anal_data, **kwargs):
    ####################################################
    param = kwargs.pop('param', 'r0')
    ####################################################
    scale_prop = 12
    grid_attrs = [[{'pos': (0, 0), 'size': (42, 30)}, {'pos': (50, 0), 'size': (42, 30)}, {'pos': (100, 0), 'size': (42, 30)}]]
    margin_attr = {'top': 2, 'bottom': 6, 'left': 6, 'right': 4}
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.6
    label_fontsize = 16
    tick_fontsize = 12
    text_fontsize = 16
    ####################################################
    sttgs = ['zero_vac', 'under_20', '20-49', '20+', '60+', 'all_ages', 'min']
    colors = ['black', 'tab:green', 'tab:blue', 'tab:orange', 'tab:gray', 'tab:purple', 'tab:red']
    linestyles = [(0, (2, 1)), (0, (1, 1)), (0, (3, 1)), (0, (3, 1, 1, 1)), (0, (5, 1)), (0, (5, 1, 1, 1)), '-']
    markers = ['o', '^', 'p', 's', 'D', 'h', 'X']
    labels = ['No Vaccine', 'Under 20', '20–49', '20+', '60+', 'All Ages', 'FS-DVP']
    adata = anal_data['prdt_from_param'][param]
    xlabels = {'r0': r'$R_0$', 'daily_vac': r'$theta$', 'vac_dur': 'Duration', 'delay': r'$T_{\mathrm{resp}}$', 'vac_eff': r'$\eta$'}
    mark_text = {'c': 'Cumulative Infections', 'd': 'Deaths', 'y': 'YLL'}
    
    for idx, target in enumerate(['c', 'd', 'y']):
        ax = axes[0][idx]
        plt.sca(ax)
        for sttg_idx, sttg_key in enumerate(sttgs):
            sttg = f'{sttg_key}_{target}' if sttg_key == 'min' or sttg_key == 'gmin' else sttg_key
            plt.plot(adata[param], adata[f'prdt_{sttg}_{target}'], color = colors[sttg_idx], label = labels[sttg_idx], linewidth = 2.5, linestyle = linestyles[sttg_idx])
            figure_setting.set_xylabel(ax, xlabels[param], 'Fraction', fontsize = label_fontsize, xlabel_coords = -0.08, ylabel_coords = -0.08)
            figure_setting.set_spine_linewidth(ax, spine_linewidth)
            figure_setting.set_tick_fontsize(ax, tick_fontsize)
        ax.text(0.02, 0.98, f'{mark_text[target]}', fontsize = text_fontsize, transform = ax.transAxes, ha = 'left', va = 'top')
        if param == 'r0': 
            axin = ax.inset_axes([0.58, 0.15, 0.4, 0.4])
            for sttg_idx, sttg_key in enumerate(sttgs):
                if sttg_key != 'zero_vac':
                    sttg = f'{sttg_key}_{target}' if sttg_key == 'min' or sttg_key == 'gmin' else sttg_key
                    axin.plot(adata[param], adata[f'prdt_zero_vac_{target}'] - adata[f'prdt_{sttg}_{target}'], color = colors[sttg_idx], label = labels[sttg_idx], linewidth = 2,  linestyle = linestyles[sttg_idx])
                    figure_setting.set_xylabel(axin, xlabels[param], 'Fraction', fontsize = label_fontsize * 0.75, xlabel_coords = -0.16, ylabel_coords = -0.16)
                    figure_setting.set_spine_linewidth(axin, spine_linewidth * 0.75)
                    figure_setting.set_tick_fontsize(axin, tick_fontsize * 0.75)
    return fig, axes
    