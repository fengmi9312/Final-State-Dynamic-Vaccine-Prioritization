# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 17:38:44 2025

@author: fengm
"""




import matplotlib.pyplot as plt
import numpy as np
from .figure_dependencies import prototype_vac_prdt
from .figure_dependencies import figure_setting

def draw(anal_data):
    fig, axes = prototype_vac_prdt.draw(anal_data)
    ax = axes[0][0]
    plt.sca(ax)
    #leg = plt.legend(loc = 'lower right', fontsize = 4.2)
    
    xlim = 100
    ax.set_xlim(- xlim / 20, xlim)
    ax.spines['bottom'].set_bounds(0, xlim)
    ax.set_ylim(- 1 / 40, 1.01)
    ax.spines['left'].set_bounds(0, 1)
    plt.xticks(np.arange(0, xlim + 1, 25), np.arange(0, xlim + 1, 25))
    plt.yticks(np.arange(0, 101, 25) / 100, np.arange(0, 101, 25))
    figure_setting.set_xylabel(ax, 'Time (d)', 'Cumulative Infections (%)', fontsize = 7.5, xlabel_coords = -0.125, ylabel_coords = -0.13)
    
    
    ax = axes[1][0]
    plt.sca(ax)
    plt.xticks(np.arange(0, 101, 25) / 100, np.arange(0, 101, 25))
    figure_setting.set_xylabel(ax, 'Cumulative Infections\n(% of age group)', 'Age Group', fontsize = 7, xlabel_coords = -0.16, ylabel_coords = -0.45)
    plt.legend(loc = 'lower right', fontsize = 3.5)
    return fig, axes
    