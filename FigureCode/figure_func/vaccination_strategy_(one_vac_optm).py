# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 19:12:51 2025

@author: fengm
"""




import matplotlib.pyplot as plt
import numpy as np
from .figure_dependencies import prototype_one_vac_optm
from .figure_dependencies import figure_setting

def draw(anal_data):
    fig, axes = prototype_one_vac_optm.draw(anal_data)
    ax = axes[0][0]
    plt.sca(ax)
    leg = plt.legend(loc = 'upper left', fontsize = 5, handlelength=3.5)
    
    xlim = 100
    ax.set_xlim(- xlim / 20, xlim)
    ax.spines['bottom'].set_bounds(0, xlim)
    ax.set_ylim(- 0.75 / 40, 0.75)
    ax.spines['left'].set_bounds(0, 0.75)
    plt.xticks(np.arange(0, xlim + 1, 25), np.arange(0, xlim + 1, 25))
    plt.yticks(np.arange(0, 76, 25) / 100, np.arange(0, 76, 25))
    figure_setting.set_xylabel(ax, 'Time (d)', 'Cumulative Infections (%)', fontsize = 7.5, xlabel_coords = -0.125, ylabel_coords = -0.13)
    
    
    ax = axes[1][0]
    plt.sca(ax)
    plt.xticks(np.arange(0, 13, 4) / 100, np.arange(0, 13, 4))
    figure_setting.set_xylabel(ax, 'Allocation (%)', 'Age Group', fontsize = 7, xlabel_coords = -0.13, ylabel_coords = -0.45)
    return fig, axes
    