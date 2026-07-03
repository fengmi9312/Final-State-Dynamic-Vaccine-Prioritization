# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 18:55:33 2025

@author: fengm
"""


import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting
import seaborn as sns

def draw(anal_data, **kwargs):
    ####################################################
    param = kwargs.pop('param', 'lower')
    comp_sttg = kwargs.pop('comp_sttg', 'gmin')
    ####################################################
    scale_prop = 12
    grid_attrs =  [[{'pos': (0, 0), 'size': (42, 30)}, {'pos': (50, 0), 'size': (42, 30)}, {'pos': (100, 0), 'size': (42, 30)}]]
    margin_attr = {'top': 2, 'bottom': 6, 'left': 6, 'right': 4}
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.6
    label_fontsize = 16
    tick_fontsize = 12
    text_fontsize = 16
    ####################################################
    adata = anal_data['prdt_from_dysttg']
    xlabel = r'Vaccination Duration $T_{\mathrm{vac}}$'
    labels = {'c': 'Cumulative Infections', 'd': 'Deaths', 'y': 'YLL'}
    colors = {'c': sns.color_palette('deep')[3], 'd': sns.color_palette('deep')[2], 'y': sns.color_palette('deep')[0]}
    markers = {'c': 'X', 'd': 'o', 'y': 'D'}
    linestyles = {'c': '-', 'd': (0, (3, 1, 1, 1)), 'y': (0, (1, 1))}
    mark_text = [1.5, 2.1, 3.5]
    for i, r0_idx in enumerate([12, 30, 72]):
        ax = axes[0][i]
        plt.sca(ax)
        for idx, target in enumerate(['c', 'd', 'y']):
            zero_vac, optm, counterpart = adata[f'{param}_zero_vac_{target}'][str(r0_idx)], adata[f'{param}_min_{target}_{target}'][str(r0_idx)], adata[f'{param}_{comp_sttg}_{target}_{target}'][str(r0_idx)]
            res = (counterpart - optm) / zero_vac
            plt.plot(adata[f'{param}_zero_vac_{target}']['vac_dur'], res, color = colors[target], linewidth = 1.5, label= labels[target], linestyle = linestyles[target],
                     markevery = 6, marker = markers[target], markersize = 8, markeredgewidth = 1, markeredgecolor = 'white')
            figure_setting.set_xylabel(ax, xlabel, 'Relative Gain (%)', fontsize = label_fontsize, xlabel_coords = -0.08, ylabel_coords = -0.08)
            figure_setting.set_spine_linewidth(ax, spine_linewidth)
            figure_setting.set_tick_fontsize(ax, tick_fontsize)
            plt.xticks(np.arange(0, 121, 30), np.arange(0, 121, 30))
            ax.spines['bottom'].set_bounds(0, 120)
        ax.text(0.02, 1, f'$R_0 = {mark_text[i]}$', fontsize = text_fontsize, transform = ax.transAxes, ha = 'left', va = 'top')
        figure_setting.remove_spines(ax, ['top', 'right'])
        if i == 0: plt.legend()
    return fig, axes
    