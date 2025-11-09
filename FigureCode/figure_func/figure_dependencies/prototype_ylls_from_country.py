# -*- coding: utf-8 -*-
"""
Created on Sun Jul  6 15:53:26 2025

@author: fengm
"""



import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting
import seaborn as sns
from Dependencies.CodeDependencies import  basic_params, param_data_loader
import pandas as pd

def draw(anal_data, **kwargs):
    target = kwargs.pop('target', 'c')
    ####################################################
    scale_prop = 9
    grid_attrs = [[{'pos': (0, 0), 'size': (40, 30)}, {'pos': (55, 0), 'size': (40, 30)}, {'pos': (110, 0), 'size': (40, 30)}, {'pos': (165, 0), 'size': (40, 30)},
                   {'pos': (0, 44), 'size': (40, 30)}, {'pos': (55, 44), 'size': (40, 30)}, {'pos': (110, 44), 'size': (40, 30)}, {'pos': (165, 44), 'size': (40, 30)},
                   {'pos': (0, 88), 'size': (40, 30)}, {'pos': (55, 88), 'size': (40, 30)}, {'pos': (110, 88), 'size': (40, 30)}, {'pos': (165, 88), 'size': (40, 30)}]]
    margin_attr = {'top': 4, 'bottom': 8, 'left': 7, 'right': 11}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 12
    tick_fontsize = 9
    ####################################################
    
    sorted_countries = ['Ireland', 'Japan', 'United Kingdom', 'Singapore', 'France', 'Italy', 'Germany', 'United States', 'Spain', 'Austria', 'Israel', 'South Korea']
    country_data = param_data_loader.load_all_data(basic_params.country_abbr.keys(), basic_params.group_div)
    age_groups = ['0–9', '10–19', '20–29', '30–39', '40–49', '50–59', '60–69', '70+']
    for idx, country in enumerate(sorted_countries):
        ax = axes[0][idx]
        plt.sca(ax)
        plt.bar(np.arange(len(age_groups)), country_data[country]['ylls'] * country_data[country]['ifrs'], color = 'tab:orange', edgecolor = 'black', linewidth = 1.5)
        plt.xticks(np.arange(len(age_groups)), age_groups, fontsize = tick_fontsize, rotation = -90)
        plt.xlabel('Age Group', fontsize = label_fontsize)
        plt.ylabel('Population (%)', fontsize = label_fontsize)
        ax.text(0.5, 1, country, fontsize = 13, transform = ax.transAxes, ha = 'center', va = 'center')
        figure_setting.set_xylabel(ax, 'Age Group', 'Expected YLL per Capita', label_fontsize, xlabel_coords = -0.2, ylabel_coords = -0.12)
        figure_setting.set_spine_linewidth(ax, 1.5)
        figure_setting.remove_spines(ax, ['top', 'right'])
        ax.set_xlim(-0.5, 7.5)
        ax.set_ylim(0, 1.2)
        ax.spines['bottom'].set_bounds(-0.4, 7.4)
        ax.spines['left'].set_bounds(0, 1.2)
        plt.yticks(np.arange(0, 13, 4) / 10, np.arange(0, 13, 4) / 10)
    return fig, axes