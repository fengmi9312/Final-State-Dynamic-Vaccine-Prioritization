# -*- coding: utf-8 -*-
"""
Created on Wed May  7 12:10:09 2025

@author: fengm
"""

import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import prototype_prdt_from_param, figure_setting

def draw(anal_data):
    fig, axes = prototype_prdt_from_param.draw(anal_data, param = 'r0')
    yticks = [np.arange(0, 101, 25), np.arange(0, 26, 5) / 10, np.arange(0, 31, 10)]
    axin_yticks = [np.arange(0, 41, 20), np.arange(0, 7, 2) / 10, np.arange(0, 11, 5)]
    ylabels = ['Cumulative Infections (%)', 'Deaths (%)', 'YLL per Capita']
    for idx in range(3):
        ax = axes[0][idx]
        plt.sca(ax)
        if idx != 2:
            plt.yticks(yticks[idx] / 100, yticks[idx])
        else:
            plt.yticks(yticks[idx] / 100, yticks[idx] / 100)
        plt.xticks(np.arange(1,6), np.arange(1,6))
        figure_setting.set_xylabel(ax, r'Basic Reproduction Number $R_0$',  ylabels[idx], fontsize = 16, xlabel_coords = -0.1, ylabel_coords = -0.075)
        if idx == 0: ax.legend(loc = 'lower left', fontsize = 9, bbox_to_anchor = (0.72, 0.55), labelspacing=0.3)
        axin_list = [child for child in ax.get_children() if isinstance(child, plt.Axes) and child is not ax]
        axin = axin_list[0]
        if idx != 2:
            axin.set_yticks(axin_yticks[idx] / 100, axin_yticks[idx])
            figure_setting.set_xylabel(axin, r'Basic Reproduction Number $R_0$', ylabels[idx], fontsize = 10, xlabel_coords = -0.16, ylabel_coords = -0.16)
        else:
            axin.set_yticks(axin_yticks[idx] / 100, axin_yticks[idx] / 100)
            figure_setting.set_xylabel(axin, r'Basic Reproduction Number $R_0$', ylabels[idx], fontsize = 10, xlabel_coords = -0.16, ylabel_coords = -0.2)
        if idx == 1:
            trans_point = 6
            plt.axvline(np.exp(trans_point * 0.075), linestyle = '--', color = 'black', linewidth = 1)
            # plt.axvspan(xmin = np.exp(0) , xmax = np.exp(trans_point * 0.075), color = 'tab:gray', alpha = 0.15, linewidth = 0)
            # plt.axvspan(xmin = np.exp(trans_point * 0.075) , xmax = np.exp(39 * 0.075), color = 'tab:green', alpha = 0.15, linewidth = 0)
            
            axin.axvline(np.exp(trans_point * 0.075), linestyle = '--', color = 'black', linewidth = 1)
            # axin.axvspan(xmin = np.exp(0) , xmax = np.exp(trans_point * 0.075), color = 'tab:red', alpha = 0.15, linewidth = 0)
            # axin.axvspan(xmin = np.exp(trans_point * 0.075) , xmax = np.exp(39 * 0.075), color = 'tab:blue', alpha = 0.15, linewidth = 0)
    return fig, axes
