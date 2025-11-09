# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 19:00:17 2025

@author: fengm
"""



import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import prototype_perf_from_dysttg_dur, figure_setting

def draw(anal_data):
    fig, axes = prototype_perf_from_dysttg_dur.draw(anal_data, param = 'lower', comp_sttg = 'mmin')
    for idx in range(3):
        ax = axes[0][idx]
        plt.sca(ax)
        if idx == 0: lower_ylim, upper_ylim, ygap, y_coef = 0, 50, 25, 100
        elif idx == 1: lower_ylim, upper_ylim, ygap, y_coef = 0, 4, 2, 100
        elif idx == 2: lower_ylim, upper_ylim, ygap, y_coef = 0, 4, 2, 1000
        else: pass
        # if idx == 0: lower_ylim, upper_ylim, ygap = 0, 75, 25
        # elif idx == 1: lower_ylim, upper_ylim, ygap = 0, 75, 25
        # elif idx == 2: lower_ylim, upper_ylim, ygap = 0, 75, 25
        # else: pass
        
        if y_coef != 100: plt.yticks(np.arange(lower_ylim, upper_ylim + 1, ygap) / y_coef, np.arange(lower_ylim, upper_ylim + 1, ygap) * 100 / y_coef)
        else: plt.yticks(np.arange(lower_ylim, upper_ylim + 1, ygap) / y_coef, np.arange(lower_ylim, upper_ylim + 1, ygap))
        ax.set_ylim(lower_ylim / y_coef - (upper_ylim - lower_ylim) / y_coef / 40, upper_ylim / y_coef)
        ax.spines['left'].set_bounds(lower_ylim / y_coef, upper_ylim / y_coef)
    return fig, axes
