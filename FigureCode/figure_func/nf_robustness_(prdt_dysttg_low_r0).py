# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 16:00:17 2025

@author: fengm
"""


import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import prototype_prdt_from_dysttg, figure_setting
from matplotlib.patches import FancyBboxPatch
from matplotlib.transforms import Bbox

def draw(anal_data):
    fig, axes = prototype_prdt_from_dysttg.draw(anal_data, param = 'lower', r0_limit = 55, vac_dur = 30)
    yticks = [np.arange(0, 71, 35), np.arange(0, 13, 4) / 10, np.arange(0, 17, 4)]
    for idx in range(3):
        ax = axes[0][idx]
        plt.sca(ax)
        if idx != 2:
            plt.yticks(yticks[idx] / 100, yticks[idx])
            figure_setting.set_xylabel(ax, r'Basic Reproduction Number $R_0$', ['Cumulative Infections (%)', 'Deaths (%)'][idx], fontsize = 16, xlabel_coords = -0.1, ylabel_coords = -0.075)
        else:
            plt.yticks(yticks[idx] / 100, yticks[idx] / 100)
            figure_setting.set_xylabel(ax, r'Basic Reproduction Number $R_0$', 'YLL per Capita', fontsize = 16, xlabel_coords = -0.1, ylabel_coords = -0.09)
        if idx == 0: 
            lines  = ax.get_lines()
            labels = [l.get_label() for l in lines]  
            for i, l in enumerate(lines):
                if i >= 6:
                    l.set_label('_nolegend_')
            leg1 = ax.legend(ncol=1, loc='upper left', bbox_to_anchor=(0.49, 0.5), frameon=False)
            ax.add_artist(leg1)     
            for l, lab in zip(lines, labels):
                l.set_label(lab)
            for i, l in enumerate(lines):
                if i < 6:
                    l.set_label('_nolegend_')       
            leg2 = ax.legend(ncol=1, loc='upper left', bbox_to_anchor=(0.75, 0.5), frameon=False)
            
            #ax.legend(loc = 'lower left', fontsize = 9, bbox_to_anchor = (0.6, 0.05), labelspacing=0.3, ncol = 2)
        plt.xticks(np.arange(1, 20, 9) / 10 + 1, np.arange(1, 20, 9) / 10 + 1)
        for i in range(2): plt.axvline(1.4 + i * 1.1, linestyle = '-.', color = 'tab:gray', linewidth = 1, alpha = 0.75)
    return fig, axes