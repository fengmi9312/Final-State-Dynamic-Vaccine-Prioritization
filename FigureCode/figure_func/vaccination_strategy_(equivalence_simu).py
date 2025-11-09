# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 22:56:24 2025

@author: fengm
"""



import matplotlib.pyplot as plt
import numpy as np
from .figure_dependencies import prototype_equivalence_simu
from .figure_dependencies import figure_setting

def draw(anal_data):
    fig, axes = prototype_equivalence_simu.draw(anal_data)
    ax = axes[0][0]
    plt.sca(ax)
    leg = plt.legend(loc = 'lower right', fontsize = 7.5)
    for legline in leg.get_lines():
        legline.set_linewidth(1)
    xlim = 80
    ax.set_xlim(- xlim / 20, xlim)
    ax.spines['bottom'].set_bounds(0, xlim)
    ax.set_ylim(- 0.75 / 40, 0.75)
    ax.spines['left'].set_bounds(0, 0.75)
    plt.xticks(np.arange(0, xlim + 1, 20), np.arange(0, xlim + 1, 20))
    plt.yticks(np.arange(0, 76, 25) / 100, np.arange(0, 76, 25))
    figure_setting.set_xylabel(ax, 'Time (d)', 'Cumulative Infections (%)', fontsize = 11.5, xlabel_coords = -0.125, ylabel_coords = -0.12)
    return fig, axes
    