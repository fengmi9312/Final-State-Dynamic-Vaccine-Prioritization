# -*- coding: utf-8 -*-
"""
Created on Tue May 27 02:51:50 2025

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
    grid_attrs = [[{'pos': (0, 0), 'size': (32, 32)}, {'pos': (55, 0), 'size': (32, 32)}, {'pos': (110, 0), 'size': (32, 32)}, {'pos': (165, 0), 'size': (32, 32)},
                   {'pos': (0, 44), 'size': (32, 32)}, {'pos': (55, 44), 'size': (32, 32)}, {'pos': (110, 44), 'size': (32, 32)}, {'pos': (165, 44), 'size': (32, 32)},
                   {'pos': (0, 88), 'size': (32, 32)}, {'pos': (55, 88), 'size': (32, 32)}, {'pos': (110, 88), 'size': (32, 32)}, {'pos': (165, 88), 'size': (32, 32)}],
                  [{'pos': (34, 0), 'size': (2, 32)}, {'pos': (89, 0), 'size': (2, 32)}, {'pos': (144, 0), 'size': (2, 32)}, {'pos': (199, 0), 'size': (2, 32)},
                   {'pos': (34, 44), 'size': (2, 32)}, {'pos': (89, 44), 'size': (2, 32)}, {'pos': (144, 44), 'size': (2, 32)}, {'pos': (199, 44), 'size': (2, 32)},
                   {'pos': (34, 88), 'size': (2, 32)}, {'pos': (89, 88), 'size': (2, 32)}, {'pos': (144, 88), 'size': (2, 32)}, {'pos': (199, 88), 'size': (2, 32)}]]
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
        im = plt.imshow(np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0), #vmin = 0, vmax = 1.2,
                        origin = 'lower', cmap = 'Blues')
        plt.xticks(np.arange(len(age_groups)), age_groups, rotation = -90, fontsize = tick_fontsize)
        plt.yticks(np.arange(len(age_groups)), age_groups, fontsize = tick_fontsize)
        ax.text(0.5, 1.02, country, fontsize = 13, transform = ax.transAxes, ha = 'center', va = 'bottom')
        cbar = fig.colorbar(im, cax=axes[1][idx])
        cbar.set_label('Contact Level', fontsize = 10)
        
    return fig, axes