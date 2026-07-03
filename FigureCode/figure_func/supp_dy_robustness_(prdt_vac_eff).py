# -*- coding: utf-8 -*-
"""
Created on Sun Jul  6 20:24:01 2025

@author: fengm
"""



import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import prototype_prdt_from_param, figure_setting

def draw(anal_data):
    fig, axes = prototype_prdt_from_param.draw(anal_data, param = 'vac_eff')
    yticks = [np.arange(0, 76, 25), np.arange(0, 13, 4) / 10, np.arange(0, 19, 6)]
    ylabels = ['Cumulative Infections (%)', 'Deaths (%)', 'YLL per Capita']
    for idx in range(3):
        ax = axes[0][idx]
        plt.sca(ax)
        if idx != 2:
            plt.yticks(yticks[idx] / 100, yticks[idx])
        else:
            plt.yticks(yticks[idx] / 100, yticks[idx] / 100)
        plt.xticks(np.arange(20, 101, 20) / 100, np.arange(20, 101, 20))
        figure_setting.set_xylabel(ax, r'Vaccine Efficacy $\eta$ (%)',  ylabels[idx], fontsize = 16, xlabel_coords = -0.1, ylabel_coords = -0.075 if idx != 2 else -0.09)
        if idx == 0: ax.legend(loc = 'lower left', fontsize = 12, bbox_to_anchor = (0.05, 0.05), labelspacing=0.3, handlelength=3)
    return fig, axes
