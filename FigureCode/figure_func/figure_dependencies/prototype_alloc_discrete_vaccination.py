#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 15:51:55 2025

@author: mifeng
"""



import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting
import seaborn as sns
from matplotlib.ticker import ScalarFormatter
from matplotlib.transforms import offset_copy
import matplotlib.colors as mcolors
from Dependencies.CodeDependencies import basic_params, param_data_loader

def pcolor_heatmap(ax, results):
    base = plt.colormaps['seismic']
    trunc = mcolors.LinearSegmentedColormap.from_list('top_half', base(np.linspace(0.5, 1, 256)))

    data = np.array(list(results.values)) * param_data_loader.load_all_data(['United States'], basic_params.group_div)['United States']['populations'][:,None]
    H, W = data.shape
    im = ax.pcolormesh(np.arange(W+1)-0.5, np.arange(H+1)-0.5, data * 100, cmap = trunc, shading='auto', vmin = 0, vmax = 0.35)
    ax.hlines(np.arange(H + 1) - 0.5, xmin = -0.5, xmax = W - 0.5, color="tab:gray", linestyle = '--', linewidth=0.5)
    ax.set_ylim(H-0.5, -0.5)
    age_groups = ['0–9', '10–19', '20–29', '30–39', '40–49', '50–59', '60–69', '70+']
    plt.yticks(np.arange(H), age_groups, fontsize = 9)
    return ax, im


def draw(anal_data, **kwargs):
    ####################################################
    sttg = kwargs.pop('sttg', 'allocs_min_c')
    ####################################################
    scale_prop = 12
    grid_attrs = [[{'pos': (0, 0), 'size': (36, 16)}], [{'pos': (38, 0), 'size': (1, 16)},]]
    margin_attr = {'top': 3, 'bottom': 4, 'left': 6, 'right': 6}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    label_fontsize = 10
    tick_fontsize = 9
    text_fontsize = 12
    ####################################################
    sttgs_formats = {'allocs_min_c': 'FS-DVP', 'mean_allocs_min_c':'Piecewise Constant', 'optm_allocs_min_c': 'Optimized Piecewise Constant'}
    
    ax = axes[0][0]
    plt.sca(ax)
    res = anal_data['discrete_optm'][sttg]
    ax, im = pcolor_heatmap(ax, res)
    figure_setting.set_xylabel(ax, 'Time (d)', 'Age Group', fontsize = label_fontsize, xlabel_coords = -0.12, ylabel_coords = -0.12)
    plt.xticks(np.arange(0, 61, 20), np.arange(0, 61, 20), fontsize = tick_fontsize)
    ax.text(0.01, 1.02, sttgs_formats[sttg], fontsize = text_fontsize, transform = ax.transAxes, ha = 'left', va = 'bottom')
    
    cbar = fig.colorbar(im, cax=axes[1][0])
    cbar.ax.tick_params(labelsize=tick_fontsize)
    cbar.set_label('Allocation (%)', rotation=270, labelpad=12, fontsize = label_fontsize)
    cbar.ax.yaxis.set_label_position('right')
    cbar.set_ticks(np.arange(6) * 0.07)
    return fig, axes
    