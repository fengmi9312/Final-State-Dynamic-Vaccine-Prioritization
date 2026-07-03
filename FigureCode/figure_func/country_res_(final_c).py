# -*- coding: utf-8 -*-
"""
Created on Fri May  9 01:12:52 2025

@author: fengm
"""


import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import prototype_prdt_from_country, figure_setting

def draw(anal_data):
    fig, axes = prototype_prdt_from_country.draw(anal_data, target = 'c')
    ax = axes[0][0]
    plt.sca(ax)
    ax.set_yticks(np.arange(0, 101, 25) / 100, np.arange(0, 101, 25))
    figure_setting.set_xylabel(ax, '', 'Cumulative Infections (%)', fontsize = 15, xlabel_coords = -0.1, ylabel_coords = -0.025)
    plt.legend(loc = 'upper left', fontsize = 12)
    return fig, axes