# -*- coding: utf-8 -*-
"""
Created on Sat May 31 01:02:30 2025

@author: fengm
"""


import matplotlib.pyplot as plt
import numpy as np
from .figure_dependencies import prototype_time_varying_optm
from .figure_dependencies import figure_setting

def draw(anal_data):
    fig, axes = prototype_time_varying_optm.draw(anal_data, file_idx = 0)
    ax = axes[0][0]
    plt.sca(ax)
    plt.legend(loc='center left', bbox_to_anchor=(1.01, 0.5), fontsize = 6, handlelength=3.6)
    xlim = 200
    ax.set_xlim(- xlim / 20, xlim)
    ax.spines['bottom'].set_bounds(0, xlim)
    ax.set_ylim(- 0.75 / 40, 0.75)
    ax.spines['left'].set_bounds(0, 0.75)
    plt.xticks(np.arange(0, xlim + 1, 50), np.arange(0, xlim + 1, 50))
    plt.yticks(np.arange(0, 76, 25) / 100, np.arange(0, 76, 25))
    figure_setting.set_xylabel(ax, 'Time (d)', 'Cumulative Infections (%)', fontsize = 10, xlabel_coords = -0.12, ylabel_coords = -0.10)
    return fig, axes
    