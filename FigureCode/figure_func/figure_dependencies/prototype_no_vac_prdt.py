# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 02:10:33 2025

@author: fengm
"""



import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting
from Dependencies.CodeDependencies import  basic_params, param_data_loader

def draw(anal_data, **kwargs):
    ####################################################
    target = kwargs.pop('target', 'c')
    file_idx = kwargs.pop('file_idx', 0)
    changing_example = kwargs.pop('changing_example', False)
    r0_idx = kwargs.pop('r0_idx', None)
    ####################################################
    scale_prop = 5.5
    grid_attrs = [[{'pos': (0, 0), 'size': (30, 25)}], [{'pos': (40, 0), 'size': (15, 23)}]]
    margin_attr = {'top': 2, 'bottom': 6, 'left': 7, 'right': 5}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1
    label_fontsize = 6
    tick_fontsize = 6
    ####################################################
    country_data = param_data_loader.load_all_data(['United States'], basic_params.group_div)['United States']
    ax = axes[0][0]
    plt.sca(ax)
    res = anal_data['final_size_prdt_optm']
    prdt = res['no_vac_prdt'].values @ country_data['populations']
    c_res = res['no_vac_dist'].values @ country_data['populations']
    plt.plot(np.arange(len(c_res)) * 0.01, c_res, color = '#DA655D', linestyle = '-', label = 'Time Evolution', linewidth = 1.5)
    plt.axhline(c_res[-1], color = 'tab:gray', linestyle = '--', label = 'Final Cumulative Infections', linewidth = 1)
    #plt.plot(np.arange(len(prdt)) * 0.01, prdt, color = 'tab:red', linestyle = '', label = 'Prediction', marker = 'x', markevery = 1000)
    prdt_gap, prdt_num = 1000, 8
    for i in range(prdt_num):
        x_point, c_point, c_prdt = i * prdt_gap / 100, c_res[i * prdt_gap], prdt[i * prdt_gap]
        #plt.scatter([x_point], [c_point], marker = '+')
        plt.scatter([x_point], [c_prdt], marker = 'x', color = '#34A29F', label = 'Final-state Prediction' if i == 0 else None, s = 30, linewidths=1.2, zorder = 10)
    #     plt.plot([x_point, x_point], [c_point, c_prdt], color = 'tab:blue', linestyle = '-', label = 'Time Evolution', linewidth = 2)
    
    figure_setting.set_xylabel(ax, 'Time (d)', 'Fraction', fontsize = label_fontsize, xlabel_coords = -0.12, ylabel_coords = -0.10)
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)
    figure_setting.remove_spines(ax, ['top', 'right'])
    
    age_groups = ['0–9','10–19','20–29','30–39','40–49','50–59','60–69','70+']
    colors = ['#DA655D', '#34A29F']
    labels = ['Final State', 'Prediction']
    ax = axes[1][0]
    plt.sca(ax)
    for idx, data_type in enumerate(['dist', 'prdt']):
        dist_res = res[f'no_vac_{data_type}'].values[-1] if data_type == 'dist' else res[f'no_vac_{data_type}'].values[4000]
        plt.barh(np.arange(8) - 0.2 + idx * 0.4, dist_res, color = colors[idx], edgecolor = 'black', linewidth = 1, height = 0.45, label = labels[idx])
        plt.yticks(np.arange(8), age_groups)
        figure_setting.set_xylabel(ax, 'Cumulative Infections (%)', 'Age Group', fontsize = 4.5, xlabel_coords = -0.35, ylabel_coords = -0.14)
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
    ax.invert_yaxis()
    return fig, axes
    