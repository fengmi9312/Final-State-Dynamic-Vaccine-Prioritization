# -*- coding: utf-8 -*-
"""
Created on Sat May 10 18:21:38 2025

@author: fengm
"""


import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting
import pandas as pd
import seaborn as sns
import itertools
from Dependencies.CodeDependencies import  basic_params, param_data_loader

def draw(anal_data, **kwargs):
    ####################################################
    target = kwargs.pop('target', 'c')
    ####################################################
    scale_prop = 9
    grid_attrs = [[{'pos': (0, 0), 'size': (185, 15)}]]
    margin_attr = {'top': 2, 'bottom': 5, 'left': 9, 'right': 14}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    label_fontsize = 15
    tick_fontsize = 12
    ####################################################
    ax = axes[0][0]
    sttgs = {'zero_vac': 'No Vaccine', 'min': 'Optimal'}
    def prepare_data(data_dict):
        mean_res = {country: np.mean([data_dict[f'dist_alloc_from_{basic_params.country_abbr[country]}']['r0'][str(i)][0] for i in range(1000)]) for country in basic_params.country_abbr.keys()}
        sorted_countries = sorted(mean_res, key=mean_res.get, reverse=False)
        for decountry in [-3, -2, -1]: del sorted_countries[decountry]
        country_data = param_data_loader.load_all_data(basic_params.country_abbr.keys(), basic_params.group_div)
        res = {country: {'mean': [], 'lower': [], 'upper': []} for country in sorted_countries}
        for country in sorted_countries:
            sheet_name = f'alloc_min_{target}_1'
            for age_idx in range(8):
                sorted_res = sorted([data_dict[f'dist_alloc_from_{basic_params.country_abbr[country]}'][sheet_name][str(i)].to_numpy()[age_idx] * country_data[country]['populations'][age_idx] for i in range(1000)])
                res[country]['mean'].append(np.mean(sorted_res))
                res[country]['lower'].append(sorted_res[50])
                res[country]['upper'].append(sorted_res[-50])
            res[country]['mean'] = np.array(res[country]['mean'])
            res[country]['lower'] = np.array(res[country]['lower'])
            res[country]['upper'] = np.array(res[country]['upper'])
        return sorted_countries, res
    
   
    countries, res = prepare_data(anal_data)
    colors = plt.cm.tab20.colors[1:16:2]
    ax = axes[0][0]
    plt.sca(ax)
    ax.yaxis.grid(True, linestyle = '--', alpha = 0.8, zorder = 0)
    age_groups = ['0–9', '10–19', '20–29', '30–39', '40–49', '50–59', '60–69', '70+']
    for idx, (country, country_res) in enumerate(res.items()):
        plt.bar(np.arange(8) + idx * 12, country_res['mean'], yerr = [country_res['mean'] - country_res['lower'], country_res['upper'] - country_res['mean']], color = colors, edgecolor='black', capsize = 2, width = 1, zorder = 3, label = age_groups if idx == 0 else None)
        # print( country_res['mean'].sum())
    plt.xlim(3.5 - 6, 8 * 12 + 3.5 + 6)
    ax.set_xticks(np.arange(0, 9) * 12 + 3.5, countries)
    plt.legend(loc = 'center left', bbox_to_anchor = (1.005, 0.5))
    figure_setting.set_xylabel(ax, '', 'Fraction', fontsize = label_fontsize, xlabel_coords = -0.1, ylabel_coords = -0.025)
    return fig, axes
