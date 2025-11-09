# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 00:19:57 2025

@author: fengm
"""




import matplotlib.pyplot as plt
import numpy as np
from .figure_dependencies import prototype_sttg_rank_change
from matplotlib.transforms import blended_transform_factory


def draw(anal_data):
    fig, axes = prototype_sttg_rank_change.draw(anal_data, target = 'c', file_idx = 0)
    y_ranges = [np.arange(0, 76, 15), np.arange(0, 101, 25) / 100, np.arange(0, 17, 4) / 100]
    y_scales = [100, 100, 1]
    titles = ['Cumulative Infections', 'Deaths', 'YLL per Capita']
    for i in range(3):
        ax = axes[0][i]
        plt.sca(ax)
        y_range = y_ranges[i]
        y_scale = y_scales[i]
        ax.hlines(y_range / y_scale, 0.02, 0.98, alpha=0.2, lw=0.5, color="0.35", zorder=0)
        for y in y_range:
            ax.scatter(0.5, y / y_scale, s = 1200, color= 'white')
            ax.text(0.5, y / y_scale, f"{y}{'%' if i == 0 or i == 1 else ''}", size = 10, color="tab:gray",alpha=0.6, va="center", ha="center")
        if i == 0: ax.legend(ncols=1, bbox_to_anchor=(-0.01, 0.8), loc='center right', fontsize=8, labelspacing=1)
        plt.title(titles[i], fontsize = 12, color="black", weight="bold", alpha=0.8)
        plt.text(0, -0.01, r'Constant $R_0$', size=10, color="black", alpha=0.8, ha="center", va = 'top', transform = blended_transform_factory(ax.transData, ax.transAxes))
        plt.text(1, -0.01, R'Varied $R_0$', size=10, color="black", alpha=0.8, ha="center", va = 'top', transform = blended_transform_factory(ax.transData, ax.transAxes))
    return fig, axes
    