# -*- coding: utf-8 -*-
"""
Created on Wed May 28 16:33:19 2025

@author: MIFENG
"""



import matplotlib.pyplot as plt
import numpy as np
from .figure_dependencies import prototype_curve_from_time
from .figure_dependencies import figure_setting

def draw(anal_data):
    fig, axes = prototype_curve_from_time.draw(anal_data, target = 'd', file_idx = 6)
    ax = axes[0][0]
    plt.sca(ax)
    plt.legend(loc = 'center left')
    ax.text(0.02, 0.9, 'Objective: Deaths', fontsize = 10, transform = ax.transAxes, ha = 'left', va = 'top')
    ax.text(0.02, 0.98, r'$R_0 = 2.0, \theta = 0.35\%$', fontsize = 12, transform = ax.transAxes, ha = 'left', va = 'top')
    xlim = 200
    ax.set_xlim(- xlim / 20, xlim)
    ax.spines['bottom'].set_bounds(0, xlim)
    ax.set_ylim(- 0.012 / 40, 0.012)
    ax.spines['left'].set_bounds(0, 0.012)
    plt.xticks(np.arange(0, xlim + 1, 50), np.arange(0, xlim + 1, 50))
    figure_setting.set_xylabel(ax, 'Time (d)', 'Deaths (%)', fontsize = 12, xlabel_coords = -0.12, ylabel_coords = -0.10)
    plt.yticks(np.arange(0, 13, 4) / 1000, np.arange(0, 13, 4) / 10)
    plt.axvspan(xmin = 30 , xmax = 30 + 140, color='gray', alpha = 0.15, linewidth = 0)
    return fig, axes
    