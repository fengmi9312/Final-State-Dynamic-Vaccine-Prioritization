#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 13:36:58 2025

@author: mifeng
"""

if __name__ == '__main__':
    import os
    import sys
    root_level = 3
    code_root = os.path.dirname(os.path.abspath(__file__))
    for i in range(root_level): code_root = os.path.dirname(code_root)
    sys.path.append(code_root)

from Dependencies.CodeDependencies import basic_params, param_data_loader
from copy import deepcopy
import numpy as np
from . import figure_setting
import matplotlib.pyplot as plt


def draw(anal_data, **kwargs):
    ####################################################
    ####################################################
    scale_prop = 12
    grid_attrs = [[{'pos': (3, 0), 'size': (30, 15)}, {'pos': (53, 0), 'size': (30, 15)}, {'pos': (103, 0), 'size': (30, 15)}]]
    margin_attr = {'top': 3, 'bottom': 6, 'left': 7, 'right': 12}
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.6
    label_fontsize = 10
    tick_fontsize = 9
    text_fontsize = 16
    ####################################################
    countries = ['United States']
    country_data = param_data_loader.load_all_data(countries, basic_params.group_div)
    calc_params = deepcopy(basic_params.calc_params)
    calc_params.update({key: country_data['United States'][key] for key in ['populations', 'ifrs', 'ylls']})
    calc_params['contacts'] = np.sum([country_data['United States']['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    age_groups = ['0–9', '10–19', '20–29', '30–39', '40–49', '50–59', '60–69', '70+']
    target_names = ['Cumulative Infections', 'Deaths', 'YLL']
    res = {'c': calc_params['contacts'] @ calc_params['populations'],
           'd': (calc_params['contacts'] @ calc_params['populations']) * calc_params['ifrs'],
           'y': (calc_params['contacts'] @ calc_params['populations']) * calc_params['ifrs'] * calc_params['ylls']}
    for idx, target in enumerate(['c', 'd', 'y']):
        ax = axes[0][idx]
        plt.sca(ax)
        plt.bar(np.arange(len(calc_params['populations'])), res[target] / np.max(res[target]), color = '#DA655D', linewidth = 1.5, edgecolor = 'black')
        figure_setting.set_spine_linewidth(ax, 1.5)
        plt.xlim(-0.5, 7.5)
        figure_setting.remove_spines(ax, ['top', 'right'])
        plt.xticks(np.arange(len(age_groups)), age_groups, rotation = -90, fontsize = tick_fontsize)
        ax.spines['left'].set_position(('axes', -0.03))
        figure_setting.set_xylabel(ax, 'Age Group', 'Normalized Risk', fontsize = label_fontsize, xlabel_coords = -0.3, ylabel_coords = -0.15)
        plt.ylim(0, 1.02)
        ax.spines['left'].set_bounds(0, 1)
        ax.set_yticks(np.arange(3) * 0.5, np.arange(3) * 0.5, fontsize = tick_fontsize * 0.9)
        ax.text(0.5, 1.02, target_names[idx], fontsize = 14, transform = ax.transAxes, ha = 'center', va = 'bottom')
    return fig, axes