# -*- coding: utf-8 -*-
"""
Created on Wed May 28 15:26:25 2025

@author: MIFENG
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.patches as patches
from matplotlib.transforms import blended_transform_factory
from .figure_dependencies import prototype_allocs, figure_setting

def draw(anal_data):
    target, file_idx = 'd', 6
    fig, axes = prototype_allocs.draw(anal_data, target = target, file_idx = file_idx)
    
    ax = axes[0][0]
    plt.sca(ax)
    plt.xlim(-3.5, 143.5)
    plt.xticks(np.arange(0, 141, 70), np.arange(0, 141, 70))
    figure_setting.set_xylabel(ax, '', 'Allocation (%)', fontsize = 12, xlabel_coords = -0.15, ylabel_coords = -0.10)
    ax.text(0, 1.04, r'$R_0 = 2.0, \theta = 0.35\%$', fontsize = 10, transform = ax.transAxes, ha = 'left', va = 'bottom')
    #ax.legend(ncols=1, bbox_to_anchor=(1.01, 0.5), loc='center left', fontsize=8)
    
    center_x_list = [31.5, 62.5, 81.5]
    center_y, width, height = 0.5, 2.4, 1.1
    for idx, center_x in enumerate(center_x_list):
        ax.add_patch(patches.Rectangle((center_x - width / 2, center_y - height / 2), width, height, edgecolor='black', facecolor='none', linestyle = '--', alpha = 0.6, clip_on = False, transform = blended_transform_factory(ax.transData,ax.transAxes)))
        # ax.text(center_x + [0, -3.5, 3.5, 0][idx], 1.05, 'Switch', fontsize = 8, transform = blended_transform_factory(ax.transData,ax.transAxes), ha = 'center', va = 'bottom')
    ax.add_patch(patches.Rectangle((91.5 - width / 2, center_y - height / 2), 37.4, height, edgecolor='black', facecolor='none', linestyle = ':', linewidth = 1.5, alpha = 0.6, clip_on = False, transform = blended_transform_factory(ax.transData,ax.transAxes)))
    ax.text(110, 1.08, 'Disorder', fontsize = 10, transform = blended_transform_factory(ax.transData,ax.transAxes), ha = 'center', va = 'bottom')
    
    axes[-1][0].set_yticks(np.arange(6) * 0.07)
    
    ax = axes[0][1]
    plt.sca(ax)
    for line_idx, line in enumerate(ax.get_lines()):
        if line_idx not in [4,5,6,7]: 
            line.set_linestyle('--')
            line.set_linewidth(1)
        else:  line.set_linewidth(2)
    
    plt.xlim(-3.5, 143.5)
    ax.spines['bottom'].set_bounds(0, 140)
    ax.spines['left'].set_bounds(0, 0.05)
    plt.yticks(np.arange(0, 6, 1) / 100, np.arange(0, 6, 1) / 100)
    plt.xticks(np.arange(0, 141, 70), np.arange(0, 141, 70))
    values = anal_data['allocs_from_time'][f'effr_min_{target}_{target}_{file_idx}'].values
    for idx, center_x in enumerate(center_x_list):
        ax.annotate('', xy=(center_x, (values[[7, 6, 5][idx]][int(center_x)] + values[[7, 6, 5][idx]][int(center_x) + [0, 0, 1][idx]]) / 2), xytext=(center_x, 0.0565), ha='center', va='top', arrowprops=dict(facecolor='black', arrowstyle='->', shrinkB=7, linestyle = '--', alpha = 0.6), fontsize = 8)
    
    # values = anal_data['allocs_from_time'][f'effr_min_{target}_{target}_{file_idx}'].values
    # x_left, x_right = 128, 131
    # y_lower = values[1][int(x_right)] + (x_right - int(x_right)) * (values[1][int(x_right) + 1] - values[1][int(x_right)])
    # y_upper = values[1][int(x_left)] + (x_left - int(x_left)) * (values[1][int(x_left) + 1] - values[1][int(x_left)])
    # axins = ax.inset_axes([0.7, 0.6, 0.25, 0.35], xlim=(x_left, x_right), ylim=(y_lower, y_upper), xticklabels=[], yticklabels=[])
    # sttg_formats = [['tab:green', '-', '0–9'], ['tab:red', '-', '10–19'], ['tab:blue', '-', '20–29'], ['tab:orange', '-', '30–39'], 
    #                 ['tab:purple', '-', '40–49'], ['tab:pink', '-', '50–59'], ['tab:gray', '-', '60–69'], ['black', '-', '70+']]
    # for age_idx in range(8): axins.plot(np.arange(len(values[age_idx])), values[age_idx], color = sns.color_palette()[age_idx], linestyle = sttg_formats[age_idx][1], label = sttg_formats[age_idx][2], linewidth = 1.5)
    # ax.indicate_inset_zoom(axins, edgecolor="black")
    ax.legend(loc = 'center left', fontsize = 9, bbox_to_anchor = (1.01, 0.5), labelspacing=0.3)
    return fig, axes