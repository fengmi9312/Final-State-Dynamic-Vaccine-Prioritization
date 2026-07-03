# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 21:55:04 2025

@author: fengm
"""



import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting
import seaborn as sns
from matplotlib.colors import TwoSlopeNorm

def draw(anal_data, **kwargs):
    ####################################################
    ####################################################
    scale_prop = 12
    grid_attrs =  [[{'pos': (0, 0), 'size': (42, 30)}, {'pos': (50, 0), 'size': (42, 30)}, {'pos': (100, 0), 'size': (42, 30)}]]
    margin_attr = {'top': 3, 'bottom': 5, 'left': 6, 'right': 4}
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    label_fontsize = 12
    tick_fontsize = 10
    text_fontsize = 14
    ####################################################
    
    res = anal_data['prdt_from_equity_r0']
    cbar_tick_info = [(60, 30), (40, 20), (30, 15)]
    for dur_idx, vac_deadline in enumerate([29, 59, 89]):
        ax = axes[0][dur_idx]
        plt.sca(ax)
        zero_vac = res[f'zero_vac_{vac_deadline}'].values.T
        min_d = res[f'min_d_{vac_deadline}'].values.T
        gmin_d = res[f'gmin_d_{vac_deadline}'].values.T
        im_res = (gmin_d - min_d) / zero_vac
        vmax = np.nanmax(im_res)
        vmin = np.nanmin(im_res)
        abs_max = max(abs(vmin), abs(vmax))
        norm = TwoSlopeNorm(vmin=-abs_max, vcenter=0, vmax=abs_max)
        im = plt.imshow(im_res, cmap = 'RdBu_r', norm = norm)
        ctick_labels = np.arange(-cbar_tick_info[dur_idx][0], cbar_tick_info[dur_idx][0] + cbar_tick_info[dur_idx][1], cbar_tick_info[dur_idx][1])
        cbar = plt.colorbar(im, label = 'Relative Gain (%)', ticks = ctick_labels / 100)
        cbar.set_ticklabels([str(i) for i in ctick_labels])
        plt.gca().invert_yaxis()
        plt.yticks(np.arange(0, 40, 13), ['0', '1/3', '2/3', '1'], fontsize = tick_fontsize)
        plt.ylabel(r'Weight Heterogeneity $h$', fontsize = label_fontsize)
        plt.xticks(np.arange(0, 40, 13), 1 + (1 + np.arange(0, 40, 13)) / 10, fontsize = tick_fontsize)
        plt.xlabel(r'Basic Reproduction Number $R_0$', fontsize = label_fontsize)
        ax.text(0.02, 1.02, f"$T_{{\\mathrm{{vac}}}} = {vac_deadline + 1}$", fontsize = text_fontsize, transform = ax.transAxes, ha = 'left', va = 'bottom')
    return fig, axes
    