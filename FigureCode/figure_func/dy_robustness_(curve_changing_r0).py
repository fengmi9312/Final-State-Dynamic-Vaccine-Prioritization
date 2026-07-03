# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 21:48:11 2025

@author: fengm
"""


import matplotlib.pyplot as plt
import numpy as np
from .figure_dependencies import prototype_changing_curve_from_time
from .figure_dependencies import figure_setting
from matplotlib.transforms import blended_transform_factory

def mark_duration(ax, text, x1, x2, y_arrow, y_text, gap, fontsize):
    trans = blended_transform_factory(ax.transData, ax.transAxes)
    ax.annotate('', xy=(x1, y_arrow), xycoords=trans, xytext=((x1 + x2)/2 - gap/2, y_arrow), textcoords=trans, arrowprops=dict(arrowstyle='->', lw=1.5))
    ax.annotate('', xy=(x2, y_arrow), xycoords=trans, xytext=((x1 + x2)/2 + gap/2, y_arrow), textcoords=trans, arrowprops=dict(arrowstyle='->', lw=1.5))
    ax.text((x1 + x2)/2, y_text, text, fontsize=fontsize, ha='center', va='center', transform=trans)


def draw(anal_data):
    fig, axes = prototype_changing_curve_from_time.draw(anal_data, file_idx = 0)
    ax = axes[0][0]
    plt.sca(ax)
    plt.legend(loc = 'center left')
    ax.text(0.02, 0.98, r'$R_0 = 1.5, \theta = 0.35\%$', fontsize = 12, transform = ax.transAxes, ha = 'left', va = 'top')
    xlim = 225
    ax.set_xlim(- xlim / 20, xlim)
    ax.spines['bottom'].set_bounds(0, xlim)
    ax.set_ylim(- 0.5 / 40, 0.5)
    ax.spines['left'].set_bounds(0, 0.5)
    plt.xticks(np.arange(0, xlim + 1, 75), np.arange(0, xlim + 1, 75))
    figure_setting.set_xylabel(ax, 'Time (d)', 'Cumulative Infections (%)', fontsize = 12, xlabel_coords = -0.12, ylabel_coords = -0.10)
    plt.yticks(np.arange(0, 51, 25) / 100, np.arange(0, 51, 25))
    plt.axvspan(xmin = 90 , xmax = 90 + 120, color='gray', alpha = 0.15, linewidth = 0)
    
    ax = axes[0][1]
    plt.sca(ax)
    plt.legend(loc = 'center left')
    ax.text(0.02, 0.98, r'$\theta = 0.35\%$', fontsize = 12, transform = ax.transAxes, ha = 'left', va = 'top')
    xlim = 225
    ax.set_xlim(- xlim / 20, xlim)
    ax.spines['bottom'].set_bounds(0, xlim)
    ax.set_ylim(- 0.75 / 40, 0.75)
    ax.spines['left'].set_bounds(0, 0.75)
    plt.xticks(np.arange(0, xlim + 1, 75), np.arange(0, xlim + 1, 75))
    figure_setting.set_xylabel(ax, 'Time (d)', 'Cumulative Infections (%)', fontsize = 12, xlabel_coords = -0.12, ylabel_coords = -0.10)
    plt.yticks(np.arange(0, 76, 25) / 100, np.arange(0, 76, 25))
    plt.axvspan(xmin = 90 , xmax = 90 + 120, color='gray', alpha = 0.15, linewidth = 0)
    plt.axvline(150, linestyle = '--', color = 'tab:gray')
    gap, y_text = 50, 1.03
    mark_duration(ax, r'$R_0 = 1.5$', 0, 150, y_text, y_text, gap, 12)
    mark_duration(ax, r'$R_0 = 2.3$', 150, 225, y_text, y_text, gap, 12)
    return fig, axes
    