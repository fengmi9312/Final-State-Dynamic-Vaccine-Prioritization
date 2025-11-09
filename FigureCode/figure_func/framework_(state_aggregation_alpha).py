# -*- coding: utf-8 -*-
"""
Created on Sun Aug  3 15:37:54 2025

@author: fengm
"""




import matplotlib.pyplot as plt
import numpy as np
from .figure_dependencies import prototype_curve_from_state_aggregation
from .figure_dependencies import figure_setting

def draw(anal_data):
    fig, axes = prototype_curve_from_state_aggregation.draw(anal_data)
    for i in range(2):
        for j in range(3):
            ax = axes[i][j]
            plt.sca(ax)
            
            xlim, xgap = 200, 100
            ax.set_xlim(- xlim / 20, xlim)
            ax.spines['bottom'].set_bounds(0, xlim)
            plt.xticks(np.arange(0, xlim + 1, xgap), np.arange(0, xlim + 1, xgap))
            
            ylim, ygap, yprop = [(70, 35, 100), (6, 3, 100), (10, 5, 1000)][j]
            basic_yprop = 100
            ax.set_ylim(- (ylim / yprop) / 40, ylim / yprop)
            ax.spines['left'].set_bounds(0, ylim / yprop)
            if yprop != basic_yprop: plt.yticks(np.arange(0, ylim + 1, ygap) / yprop, np.arange(0, (ylim + 1) / (yprop / basic_yprop), ygap / (yprop / basic_yprop)))
            else: plt.yticks(np.arange(0, ylim + 1, ygap) / yprop, np.arange(0, ylim + 1, ygap))
            figure_setting.set_tick_fontsize(ax, 8)
            figure_setting.set_xylabel(ax, 'Time (d)', ['Cumulative Infections (%)', 'Symptomatics (%)', 'Deaths (%)'][j], fontsize = 7.5, xlabel_coords = -0.2, ylabel_coords = [-0.17, -0.13, -0.2][j])
            if (i, j) == (0, 0): plt.legend(loc = 'lower right', fontsize = 5)
    
    
    # ax = axes[1][0]
    # plt.sca(ax)
    # plt.xticks(np.arange(0, 101, 25) / 100, np.arange(0, 101, 25))
    # figure_setting.set_xylabel(ax, 'Cumulative Infections\n(% of age group)', 'Age Group', fontsize = 7, xlabel_coords = -0.16, ylabel_coords = -0.45)
    # plt.legend(loc = 'lower right', fontsize = 3.5)
    return fig, axes
    