#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 12:57:03 2025

@author: mifeng
"""



import matplotlib.pyplot as plt
import numpy as np
from .figure_dependencies import prototype_curve_discrete_vaccination
from .figure_dependencies import figure_setting

def draw(anal_data):
    fig, axes = prototype_curve_discrete_vaccination.draw(anal_data)
    ax = axes[0][0]
    plt.sca(ax)
    leg = plt.legend(loc = 'upper left', fontsize = 8, handlelength=3.4)
    
    xlim = 160
    ax.set_xlim(- xlim / 20, xlim)
    ax.spines['bottom'].set_bounds(0, xlim)
    ax.set_ylim(- 0.75 / 40, 0.75)
    ax.spines['left'].set_bounds(0, 0.75)
    plt.xticks(np.arange(0, xlim + 1, 40), np.arange(0, xlim + 1, 40))
    plt.yticks(np.arange(0, 76, 25) / 100, np.arange(0, 76, 25))
    figure_setting.set_xylabel(ax, 'Time (d)', 'Cumulative Infections (%)', fontsize = 12, xlabel_coords = -0.125, ylabel_coords = -0.08)
    plt.axvspan(xmin = 40 , xmax = 40 + 60, color='gray', alpha = 0.15, linewidth = 0)
    return fig, axes