# -*- coding: utf-8 -*-
"""
Created on Thu May  8 15:54:53 2025

@author: fengm
"""



import matplotlib.pyplot as plt
import numpy as np
from .figure_dependencies import figure_setting, prototype_dist

def draw(anal_data):
    fig, axes = prototype_dist.draw(anal_data, file_idx = 4)
    ax = axes[0][0]
    plt.sca(ax)
    ax.set_ylim(0.14 / 20, 0.14)
    ax.spines['left'].set_bounds(0, 0.14)
    plt.yticks(np.arange(0, 15, 7) / 100, np.arange(0, 15, 7))
    ax.spines['bottom'].set_bounds(0, 7)
    figure_setting.set_xylabel(ax, 'Age Group', 'Cumulative Infections (%)', fontsize = 9, xlabel_coords = -0.09, ylabel_coords = -0.06)
    ax.legend(loc = 'lower left', fontsize = 8, bbox_to_anchor = (0.1, 0.05), labelspacing=0.5)
    return fig, axes