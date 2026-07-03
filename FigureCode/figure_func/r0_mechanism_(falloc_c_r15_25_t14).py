# -*- coding: utf-8 -*-
"""
Created on Thu May  8 17:27:27 2025

@author: fengm
"""



import matplotlib.pyplot as plt
import numpy as np
from .figure_dependencies import figure_setting, prototype_total_allocs

def draw(anal_data):
    fig, axes = prototype_total_allocs.draw(anal_data, file_idx_0 = 1, file_idx_1 = 4)
    ax = axes[0][0]
    plt.sca(ax)
    plt.yticks(np.arange(0, 11, 5) / 100, np.arange(0, 11, 5))
    figure_setting.set_xylabel(ax, 'Age Group', 'Allocation (%)', fontsize = 10, xlabel_coords = -0.35, ylabel_coords = -0.10)
    ax.text(0.98, 0.98, r'$R_0 = 1.5$', fontsize = 10, transform = ax.transAxes, ha = 'right', va = 'top')
    
    ax = axes[0][1]
    plt.sca(ax)
    plt.yticks(np.arange(0, 5, 2) / 100, np.arange(0, 5, 2))
    figure_setting.set_xylabel(ax, 'Age Group', 'Allocation (%)', fontsize = 10, xlabel_coords = -0.35, ylabel_coords = -0.10)
    ax.text(0.98, 0.98, r'$R_0 = 2.5$', fontsize = 10, transform = ax.transAxes, ha = 'right', va = 'top')
    return fig, axes