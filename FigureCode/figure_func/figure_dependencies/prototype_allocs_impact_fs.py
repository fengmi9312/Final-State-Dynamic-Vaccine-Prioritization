# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 01:39:12 2025

@author: fengm
"""



import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting
import seaborn as sns
from matplotlib.ticker import ScalarFormatter
from matplotlib.transforms import offset_copy
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
    im = ax.pcolormesh(np.arange(W+1)-0.5, np.arange(H+1)-0.5, data * 100, cmap = trunc, shading='auto', vmin = 0, vmax = 0.35)
    ax.hlines(np.arange(H + 1) - 0.5, xmin = -0.5, xmax = W - 0.5, color="tab:gray", linestyle = '--', linewidth=0.5)
    ax.set_ylim(H-0.5, -0.5)
    age_groups = ['0–9', '10–19', '20–29', '30–39', '40–49', '50–59', '60–69', '70+']
    plt.yticks(np.arange(H), age_groups, fontsize = 6)
    return ax, im


def draw(anal_data, **kwargs):
    ####################################################
    param = kwargs.pop('param', 'lower')
    r0_limit = kwargs.pop('r0_limit', None)
    vac_dur = kwargs.pop('vac_dur', 60)
    ####################################################
    scale_prop = 12
    grid_attrs = [[{'pos': (0, 0), 'size': (14, 5)}, {'pos': (22, 0), 'size': (14, 5)},
                   {'pos': (0, 6), 'size': (14, 14)}, {'pos': (22, 6), 'size': (14, 14)}, 
                   {'pos': (0, 26), 'size': (36, 6)}],
                  
                  [{'pos': (0, 40), 'size': (14, 5)}, {'pos': (22, 40), 'size': (14, 5)},
                   {'pos': (0, 46), 'size': (14, 14)}, {'pos': (22, 46), 'size': (14, 14)}, 
                   {'pos': (0, 66), 'size': (36, 6)}],
                  
                  [{'pos': (50, 0), 'size': (14, 5)}, {'pos': (72, 0), 'size': (14, 5)},
                   {'pos': (50, 6), 'size': (14, 14)}, {'pos': (72, 6), 'size': (14, 14)}, 
                   {'pos': (50, 26), 'size': (36, 6)}],
                  
                  [{'pos': (50, 40), 'size': (14, 5)}, {'pos': (72, 40), 'size': (14, 5)},
                   {'pos': (50, 46), 'size': (14, 14)}, {'pos': (72, 46), 'size': (14, 14)}, 
                   {'pos': (50, 66), 'size': (36, 6)}],
                 
                 [{'pos': (100, 0), 'size': (14, 5)}, {'pos': (122, 0), 'size': (14, 5)},
                  {'pos': (100, 6), 'size': (14, 14)}, {'pos': (122, 6), 'size': (14, 14)}, 
                  {'pos': (100, 26), 'size': (36, 6)}],
                 
                 [{'pos': (100, 40), 'size': (14, 5)}, {'pos': (122, 40), 'size': (14, 5)},
                  {'pos': (100, 46), 'size': (14, 14)}, {'pos': (122, 46), 'size': (14, 14)}, 
                  {'pos': (100, 66), 'size': (36, 6)}],
                  
                  [{'pos': (138, 6), 'size': (1, 14)}, {'pos': (138, 46), 'size': (1, 14)}], 
                  [{'pos': (138, 26), 'size': (1, 6)}, {'pos': (138, 66), 'size': (1, 6)}]]
    margin_attr = {'top': 5, 'bottom': 3, 'left': 6, 'right': 7}
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.6
    label_fontsize = 9
    tick_fontsize = 6
    text_fontsize = 16
    ####################################################
    age_groups = ['0–9', '10–19', '20–29', '30–39', '40–49', '50–59', '60–69', '70+']
    cmaps = ['cividis', 'viridis', 'cividis', 'viridis']
    sttgs = ['FS-DVP', 'TS-DVP']
    value_names = ['Reduced Final State', 'Reduced Transient State', 'Reduced Final State', 'Reduced Transient State']
    r0_values = [1.4, 2.5]
    target_names = ['Cumulative Infections', 'Deaths', 'YLL']
    effs = ['Direct Effects', 'Indirect Effects']
    sttg = 'min'
    for target_idx, target in enumerate(['c', 'd', 'y']):
        for r0_idx in range(2):
            for eff_idx in range(2):
                ax = axes[target_idx * 2 + r0_idx][2 + eff_idx]
                plt.sca(ax)
                mat_data = anal_data['impact_to_dysttg'][f'{sttg}_{target}_{r0_idx}'].values
                mat_max = np.max(mat_data)
                if eff_idx == 0: mat_res = anal_data['impact_to_dysttg'][f'dir_{sttg}_{target}_{r0_idx}'].values / mat_max
                else: mat_res = (mat_data - anal_data['impact_to_dysttg'][f'dir_{sttg}_{target}_{r0_idx}'].values) / mat_max
                im = plt.imshow(mat_res, origin='lower', cmap = 'Oranges', vmin=0, vmax=1)
                figure_setting.set_spine_linewidth(ax, 1)
                plt.xticks(np.arange(len(age_groups)), age_groups, rotation = -90, fontsize = tick_fontsize)
                plt.yticks(np.arange(len(age_groups)), age_groups, fontsize = tick_fontsize)
                figure_setting.set_xylabel(ax, 'Vaccinated Group', 'Affected Group', fontsize = label_fontsize, xlabel_coords = -0.22, ylabel_coords = -0.22)
                
                if target_idx == 0 and eff_idx == 0: 
                    cbar = fig.colorbar(im, cax=axes[-2][r0_idx])
                    cbar.set_label('Normalized Impact', rotation=270, labelpad=12, fontsize = label_fontsize)
                    cbar.ax.yaxis.set_label_position('right')
                #if target_idx == 0 and eff_idx == 0: ax.text(-0.43, 0.4, f'$R_0 = {r0_values[r0_idx]}$', fontsize = 12, transform = ax.transAxes, ha = 'center', va = 'bottom', rotation = 90)
                
                
                ax = axes[target_idx * 2 + r0_idx][eff_idx]
                plt.sca(ax)
                tot_arr_data = (mat_data / mat_max).sum(axis = 0)
                arr_data =  mat_res.sum(axis = 0)
                plt.bar(np.arange(len(arr_data)), arr_data, width = 0.95, color = 'tab:orange')
                figure_setting.set_spine_linewidth(ax, 1)
                plt.xlim(-0.5, 7.5)
                figure_setting.remove_spines(ax, ['top', 'right'])
                ax.set_xticklabels([])
                ax.spines['left'].set_position(('axes', -0.03))
                if r0_idx == 1:
                    plt.ylim(0, 1.02)
                    ax.spines['left'].set_bounds(0, 1)
                    ax.set_yticks([0, 1], [0, 1], fontsize = tick_fontsize * 0.9)
                else:
                    y_lim = int(np.max(tot_arr_data) * 10) + 1
                    y_lim = (y_lim + 1) / 10 if y_lim % 2 == 1 else y_lim / 10
                    plt.ylim(0, y_lim * 1.02)
                    ax.spines['left'].set_bounds(0, y_lim)
                    ax.set_yticks([0, y_lim], [0, y_lim], fontsize = tick_fontsize * 0.9)
                if r0_idx == 0 and eff_idx == 0: ax.text(18 / 14, 1.6, target_names[target_idx], fontsize = 12, transform = ax.transAxes, ha = 'center', va = 'bottom')
                ax.text(0.5, 1.1, f'{effs[eff_idx]} ($R_0 = {r0_values[r0_idx]}$)', fontsize = 10, transform = ax.transAxes, ha = 'center', va = 'bottom')
                
            ax = axes[target_idx * 2 + r0_idx][4]
            plt.sca(ax)
            res = anal_data['allocs_dysttg_from_time'][f'alloc_{sttg}_{target}_{r0_idx * 33 + 9}']
            ax, im = pcolor_heatmap(ax, res)
            figure_setting.set_xylabel(ax, 'Time (d)', 'Age Group', fontsize = label_fontsize, xlabel_coords = -0.24, ylabel_coords = -0.1)
            plt.xticks(np.arange(0, 31, 10), np.arange(0, 31, 10), fontsize = tick_fontsize)
            # plt.yticks(np.arange(0, 36, 35) / 10000, np.arange(0, 36, 35) / 100, fontsize = tick_fontsize)
            # plt.ylim(0, res.sum(axis = 0).max())
            # if target_idx == 2 and r0_idx == 1: ax.legend(loc = 'center left', fontsize = 9, bbox_to_anchor = (1.01, 2.5), labelspacing = 0.3)
            ax.text(0.05, 1.02, f'$R_0 = {r0_values[r0_idx]}$', fontsize = 10, transform = ax.transAxes, ha = 'center', va = 'bottom')
            if target_idx == 0: 
                cbar = fig.colorbar(im, cax=axes[-1][r0_idx])
                cbar.set_label('Allocation (%)', rotation=270, labelpad=12, fontsize = label_fontsize)
                cbar.ax.yaxis.set_label_position('right')
                cbar.set_ticks(np.arange(2) * 0.35)
                # if idx == 0 and eff_idx == 0: ax.text(0.5, 1.05, f'$R_0 = {r0_values[r0_idx]}$', fontsize = 12, transform = ax.transAxes, ha = 'center', va = 'bottom')
                # if r0_idx == 0 and idx == 0 and eff_idx == 0: ax.text(1.2, 1.6, target_names[target_idx], fontsize = 14, transform = ax.transAxes, ha = 'center', va = 'bottom')
    return fig, axes
    