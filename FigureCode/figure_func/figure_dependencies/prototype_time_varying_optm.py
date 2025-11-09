# -*- coding: utf-8 -*-
"""
Created on Sat May 31 00:56:24 2025

@author: fengm
"""

import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting

def draw(anal_data, **kwargs):
    ####################################################
    target = kwargs.pop('target', 'c')
    file_idx = kwargs.pop('file_idx', 0)
    ####################################################
    scale_prop = 6
    grid_attrs = [[{'pos': (0, 0), 'size': (40, 25)}]]
    margin_attr = {'top': 3, 'bottom': 6, 'left': 8, 'right': 27}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 12
    tick_fontsize = 8
    ####################################################
    ax = axes[0][0]
    plt.sca(ax)
    res = anal_data['time_varying_optm']
    colors = ['black', '#DCBF63', '#3C6C7F','#DA655D']
    labels = ['No Vaccination', '1 Round', '2 Rounds', '3 Rounds']
    prdt_labels = [None, 'Final Size after 1 Round', 'Final Size after 2 Rounds', 'Final Size after 3 Rounds']
    linestyles = [(0, (2, 1)), (0, (3, 1, 1, 1)), (0, (4, 1)), '-']
    vac_points = [3000, 6000, 9000]
    for i in range(4):
        plt.plot(res['target_curve']['time_line'], res['target_curve'][f'{target}_{i}'], color = colors[i], linestyle = linestyles[i], linewidth = 1.5, label = labels[i])
        if i != 0:
            plt.axhline(res['vac_prdt'][f'{target}_{i - 1}'][0], linestyle = ':', color = colors[i], linewidth = 1,)#plt.hlines(res['vac_prdt'][f'{target}_{i - 1}'], vac_points[i - 1] / 100, 200, linestyle = ':', color = colors[i], linewidth = 2)
            # plt.arrow(vac_points[i - 1] / 100, res['target_curve'][f'{target}_{i}'][vac_points[i - 1]], 0, res['vac_prdt'][f'{target}_{i - 1}'][0] - res['target_curve'][f'{target}_{i}'][vac_points[i - 1]], 
            #           head_width=10, head_length=20, fc=colors[i], ec=colors[i], length_includes_head=True)
            # plt.plot([vac_points[i - 1] / 100, vac_points[i - 1] / 100], [res['target_curve'][f'{target}_{i}'][vac_points[i - 1]], res['vac_prdt'][f'{target}_{i - 1}'][0]],
            #          marker='>', color=colors[i], label=anno_labels[i], markevery=[-1])
            
            
            ax.annotate('', xy=(vac_points[i - 1] / 100, res['vac_prdt'][f'{target}_{i - 1}'][0]), xytext=(vac_points[i - 1] / 100, 
                        res['target_curve'][f'{target}_{i}'][vac_points[i - 1]]), ha='center', va='top', arrowprops=dict(color=colors[i], arrowstyle='->', shrinkB=0, linestyle = '-', linewidth = 1))
    figure_setting.set_xylabel(ax, 'Time (d)', 'Fraction', fontsize = label_fontsize, xlabel_coords = -0.12, ylabel_coords = -0.10)
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)
    figure_setting.remove_spines(ax, ['top', 'right'])
    return fig, axes
    