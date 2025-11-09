# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 17:48:46 2025

@author: fengm
"""


import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting

def find_cross(x, y, z):
    diff = y - z
    sign_change = np.where(np.diff(np.sign(diff)) != 0)[0]
    cross_points = []
    for i in sign_change:
        x1, x2 = x[i], x[i+1]
        y1, y2 = diff[i], diff[i+1]
        x_cross = x1 - y1 * (x2 - x1) / (y2 - y1)
        cross_points.append(x_cross)
    return cross_points


def draw(anal_data, **kwargs):
    ####################################################
    param = kwargs.pop('param', 'lower')
    r0_limit = kwargs.pop('r0_limit', None)
    vac_dur = kwargs.pop('vac_dur', 60)
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
    sttgs = ['zero_vac', 'under_20', '20-49', '20+', '60+', 'all_ages', 'min', 'gmin']
    colors = ['black', 'tab:green', 'tab:blue', 'tab:orange', 'tab:gray', 'tab:purple', 'tab:red', 'tab:blue', 'tab:orange', 'tab:green']
    linestyles = [(0, (2, 1)), (0, (1, 1)), (0, (3, 1)), (0, (3, 1, 1, 1)), (0, (5, 1)), (0, (5, 1, 1, 1)), '-', '-', '-', '-']
    linewidths = [2.5, 1.2, 1.2, 1.2, 1.2, 1.2, 2.5, 2.5, 2.5, 2.5]
    zorders = [1, 2, 3, 4, 5, 6, 10, 9, 8, 7]
    labels = ['No Vaccine', 'Under 20', '20–49', '20+', '60+', 'All Ages', 'FS-DVP', 'TS-DVP']
    # adata = anal_data['prdt_from_dysttg'][f'{param}_r0']
    xlabel = r'$R_0$'
    mark_text = {'c': 'Cumulative Infections', 'd': 'Deaths', 'y': 'YLL'}
    vlines = [1.5, 2.1, 3.5]
    r0_arr = anal_data['prdt_from_dysttg'][f'{param}_r0']['r0'] if r0_limit is None else anal_data['prdt_from_dysttg'][f'{param}_r0']['r0'][:r0_limit]
    
    for idx, target in enumerate(['c', 'd', 'y']):
        ax = axes[0][idx]
        plt.sca(ax)
        for sttg_idx, sttg_key in enumerate(sttgs):
            sttg = f'{sttg_key}_{target}' if sttg_key in ['min', 'gmin', 'mmin', 'mgmin'] else sttg_key
            sttg_res = anal_data['prdt_from_dysttg'][f'{param}_{sttg}_{target}']
            res = np.array([sttg_res[str(i)][vac_dur - 1] for i in range(120)])
            if r0_limit is None: plt.plot(r0_arr, res, color = colors[sttg_idx], label = labels[sttg_idx], linewidth = linewidths[sttg_idx], linestyle = linestyles[sttg_idx], zorder = zorders[sttg_idx])
            else: plt.plot(r0_arr, res[:r0_limit], color = colors[sttg_idx], label = labels[sttg_idx], linewidth = linewidths[sttg_idx], linestyle = linestyles[sttg_idx], zorder = zorders[sttg_idx])
            figure_setting.set_xylabel(ax, xlabel, 'Fraction', fontsize = label_fontsize, xlabel_coords = -0.08, ylabel_coords = -0.08)
            figure_setting.set_spine_linewidth(ax, spine_linewidth)
            figure_setting.set_tick_fontsize(ax, tick_fontsize)
        if target == 'y' and r0_limit is None:
            sttg_min_res = anal_data['prdt_from_dysttg'][f'{param}_min_{target}_{target}']
            sttg_gmin_res = anal_data['prdt_from_dysttg'][f'{param}_gmin_{target}_{target}']
            cross_points = find_cross(r0_arr, np.array([sttg_min_res[str(i)][vac_dur - 1] for i in range(120)]), np.array([sttg_gmin_res[str(i)][vac_dur - 1] for i in range(120)]))
            print(cross_points)
            plt.axvspan(cross_points[0], cross_points[1], color = 'tab:gray', alpha = 0.2, linewidth = 0)
        ax.text(0.02, 0.98, f'{mark_text[target]}', fontsize = text_fontsize, transform = ax.transAxes, ha = 'left', va = 'top')
        if idx == 0 and r0_limit is None: 
            for i in range(3): plt.axvline(vlines[i], linestyle = (0, (5, 1)), color = 'tab:gray', alpha = 0.75, linewidth = 1)
        
    return fig, axes
    