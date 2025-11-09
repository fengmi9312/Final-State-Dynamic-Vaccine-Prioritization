# -*- coding: utf-8 -*-
"""
Created on Thu May  1 13:49:30 2025

@author: fengm
"""


import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting
import seaborn as sns
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
    plt.yticks(np.arange(H), age_groups, fontsize = 8)
    return ax, im



def draw(anal_data, **kwargs):
    ####################################################
    target = kwargs.pop('target', 'c')
    file_idx = kwargs.pop('file_idx', 0)
    ####################################################
    scale_prop = 12
    grid_attrs = [[{'pos': (0, 0), 'size': (36, 12)}, {'pos': (0, 16), 'size': (36, 30)}], [{'pos': (37, 0), 'size': (1, 12)}]]
    margin_attr = {'top': 5, 'bottom': 6, 'left': 6, 'right': 7}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 12
    tick_fontsize = 10
    ####################################################
    sttg_formats = [['tab:green', '-', '0–9'], ['tab:red', '-', '10–19'], ['tab:blue', '-', '20–29'], ['tab:orange', '-', '30–39'], 
                    ['tab:purple', '-', '40–49'], ['tab:pink', '-', '50–59'], ['tab:gray', '-', '60–69'], ['black', '-', '70+']]
    
    res = anal_data['allocs_from_time']
    
    
    ax = axes[0][0]
    plt.sca(ax)
    ax, im = pcolor_heatmap(ax, res[f'alloc_min_{target}_{file_idx}'])
    figure_setting.set_xylabel(ax, '', 'Age Group', fontsize = label_fontsize, xlabel_coords = -0.15, ylabel_coords = -0.10)
    cbar = fig.colorbar(im, cax=axes[-1][0])
    cbar.set_label('Allocation (%)', rotation=270, labelpad=12, fontsize = label_fontsize)
    cbar.ax.yaxis.set_label_position('right')
    # add_rectpatch(ax, target, file_idx)
    # 
    
    ax = axes[0][1]
    plt.sca(ax)
    values = res[f'effr_min_{target}_{target}_{file_idx}'].values
    for age_idx in range(8):
        plt.plot(np.arange(len(values[age_idx])), values[age_idx], color = sns.color_palette()[age_idx], linestyle = sttg_formats[age_idx][1], label = sttg_formats[age_idx][2], linewidth = 1.5)
    # if file_idx == 2: ax.legend(loc = 'center left', fontsize = 9, bbox_to_anchor = (1.01, 0.5), labelspacing=0.3)
    figure_setting.set_xylabel(ax, 'Time (d)', 'MVB', fontsize = label_fontsize, xlabel_coords = -0.08, ylabel_coords = -0.08 if target != 'd' else -0.12)
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # if target == 'c':
    #     if file_idx < 3:
    #         plt.yticks(np.arange(0, 26, 5) / 10, np.arange(0, 26, 5) / 10)
    #         ax.spines['left'].set_bounds(0, 2.5)
    #         if file_idx == 1:
    #             ax.annotate('', xy=(49.5, (values[1][49] + values[1][50]) / 2), xytext=(49.5, 2.8), ha='center', va='top', arrowprops=dict(facecolor='black', arrowstyle='->', shrinkB=7, linestyle = '--'), fontsize = 8)
    #             ax.annotate('', xy=(75.5, (values[1][75] + values[1][80]) / 2), xytext=(75.5, 2.8), ha='center', va='top', arrowprops=dict(facecolor='black', arrowstyle='->', shrinkB=7, linestyle = '--'), fontsize = 8)
    #     else:
    #         plt.yticks(np.arange(0, 16, 5) / 10, np.arange(0, 16, 5) / 10)
    #         ax.spines['left'].set_bounds(0, 1.5)
    # elif target == 'd':
    #     if file_idx < 3:
    #         plt.yticks(np.arange(0, 33, 8) / 1000, np.arange(0, 33, 8) / 1000)
    #         ax.spines['left'].set_bounds(0, 0.032)
    #     else:
    #         plt.yticks(np.arange(0, 71, 35) / 1000, np.arange(0, 71, 35) / 1000)
    #         ax.spines['left'].set_bounds(0, 0.07)
    # elif target == 'y':
    #     if file_idx < 3:
    #         plt.yticks(np.arange(0, 7, 3) / 10, np.arange(0, 7, 3) / 10)
    #         ax.spines['left'].set_bounds(0, 0.6)
    #     else:
    #         plt.yticks(np.arange(0, 51, 25) / 100, np.arange(0, 51, 25) / 100)
    #         ax.spines['left'].set_bounds(0, 0.5)
    # else: pass
    return fig, axes
    
    