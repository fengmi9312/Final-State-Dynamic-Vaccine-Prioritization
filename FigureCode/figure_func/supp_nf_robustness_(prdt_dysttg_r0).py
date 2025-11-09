# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 17:53:18 2025

@author: fengm
"""


import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import prototype_prdt_from_dysttg, figure_setting

def draw(anal_data):
    fig, axes = prototype_prdt_from_dysttg.draw(anal_data, param = 'lower', vac_dur = 50)
    yticks = [np.arange(0, 101, 25), np.arange(0, 31, 10) / 10, np.arange(0, 31, 10)]
    axin_yticks = [np.arange(0, 41, 20), np.arange(0, 7, 2) / 10, np.arange(0, 11, 5)]
    for idx in range(3):
        ax = axes[0][idx]
        plt.sca(ax)
        if idx != 2:
            plt.yticks(yticks[idx] / 100, yticks[idx])
            figure_setting.set_xylabel(ax, r'Basic Reproduction Number $R_0$', ['Cumulative Infections (%)', 'Deaths (%)'][idx], fontsize = 16, xlabel_coords = -0.1, ylabel_coords = -0.075)
        else:
            plt.yticks(yticks[idx] / 100, yticks[idx] / 100)
            figure_setting.set_xylabel(ax, r'Basic Reproduction Number $R_0$', 'YLL per Capita', fontsize = 16, xlabel_coords = -0.1, ylabel_coords = -0.075)
        if idx == 0: ax.legend(loc = 'lower right', fontsize = 9, bbox_to_anchor = (0.95, 0.05), labelspacing=0.3)
        plt.xticks(np.arange(1, 6), np.arange(1, 6))
    return fig, axes
