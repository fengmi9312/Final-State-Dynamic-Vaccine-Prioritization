# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 19:23:37 2025

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
    grid_attrs = [[{'pos': (0, 0), 'size': (30, 25)}], [{'pos': (40, 0), 'size': (15, 25)}]]
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
    s_res = res['all_ages_sarr'].values @ country_data['populations']
    sttg_formats = {'no_vac': ['black', (0, (2, 1)), 'No Vaccination'], 'under_20': ['tab:green', (0, (1, 1)), 'Under 20'], '20-49': ['tab:blue', (0, (3, 1)), '20–49'], 
                    '20+': ['tab:orange', (0, (3, 1, 1, 1)), '20+'], '60+': ['tab:gray', (0, (5, 1)), '60+'], 'all_ages': ['tab:purple', (0, (5, 1, 1, 1)), 'All Ages'], 
                    'min_c': ['tab:red', '-', 'Optimal']}
    for sttg in ['no_vac', 'under_20', '20-49', '20+', '60+', 'all_ages', 'min_c']:
        c_res = res[f'{sttg}_dist'].values @ country_data['populations']
        plt.plot(np.arange(len(c_res)) * 0.01, c_res, color = sttg_formats[sttg][0], linestyle = sttg_formats[sttg][1], label = sttg_formats[sttg][2], linewidth = 1.5)
    
    vac_point = np.where(np.diff(s_res, prepend = s_res[0]) < -0.1)[0][0]
    plt.axvline(vac_point / 100, linestyle = (0, (3, 1, 1, 1)), color = 'tab:gray')
    plt.axvline(vac_point / 100 + 7, linestyle = ':', color = 'tab:gray')
    figure_setting.set_xylabel(ax, 'Time (d)', 'Fraction', fontsize = label_fontsize, xlabel_coords = -0.12, ylabel_coords = -0.10)
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)
    figure_setting.remove_spines(ax, ['top', 'right'])
    
    
    age_groups = ['0–9','10–19','20–29','30–39','40–49','50–59','60–69','70+']
    colors = ['#DA655D', '#34A29F']
    labels = ['Final State', 'Prediction']
    ax = axes[1][0]
    plt.sca(ax)
    plt.barh(np.arange(8), res['min_c_alloc']['alloc'] * country_data['populations'], color = '#DA655D', edgecolor = 'black', linewidth = 1, height = 0.9)
    plt.yticks(np.arange(8), age_groups)
    figure_setting.set_xylabel(ax, 'Allocation (%)', 'Age Group', fontsize = 4.5, xlabel_coords = -0.35, ylabel_coords = -0.14)
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)
    ax.invert_yaxis()
    
    return fig, axes
    