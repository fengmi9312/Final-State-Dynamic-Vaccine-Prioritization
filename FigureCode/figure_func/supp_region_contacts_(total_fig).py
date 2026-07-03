
import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import figure_setting
import seaborn as sns
from Dependencies.CodeDependencies import  basic_params, param_data_loader
import pandas as pd

def draw(anal_data, **kwargs):
    target = kwargs.pop('target', 'c')
    ####################################################
    scale_prop = 9
    grid_attrs = [[{'pos': (0, 0), 'size': (32, 32)}, {'pos': (55, 0), 'size': (32, 32)}, {'pos': (110, 0), 'size': (32, 32)}, {'pos': (165, 0), 'size': (32, 32)}],
                  [{'pos': (34, 0), 'size': (2, 32)}, {'pos': (89, 0), 'size': (2, 32)}, {'pos': (144, 0), 'size': (2, 32)}, {'pos': (199, 0), 'size': (2, 32)}]]
    margin_attr = {'top': 4, 'bottom': 8, 'left': 7, 'right': 11}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 12
    tick_fontsize = 9
    ####################################################
    country = 'United States'
    region_names = ['Home', 'School', 'Work', 'Other locations']
    regions = ['home', 'school', 'work', 'other_locations']
    country_data = param_data_loader.load_all_data(basic_params.country_abbr.keys(), basic_params.group_div)
    age_groups = ['0–9', '10–19', '20–29', '30–39', '40–49', '50–59', '60–69', '70+']
    for idx, region in enumerate(regions):
        ax = axes[0][idx]
        plt.sca(ax)
        im = plt.imshow(country_data[country]['contacts'][region],
                        origin = 'lower', cmap = 'Blues')
        plt.xticks(np.arange(len(age_groups)), age_groups, rotation = -90, fontsize = tick_fontsize)
        plt.yticks(np.arange(len(age_groups)), age_groups, fontsize = tick_fontsize)
        ax.text(0.5, 1.02, region_names[idx], fontsize = 13, transform = ax.transAxes, ha = 'center', va = 'bottom')
        cbar = fig.colorbar(im, cax=axes[1][idx])
        cbar.set_label('Contact Level', fontsize = 10)
        
    return fig, axes