# -*- coding: utf-8 -*-
"""
Created on Sun May 11 14:21:29 2025

@author: fengm
"""


import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import prototype_allocs_from_country, figure_setting

def draw(anal_data):
    fig, axes = prototype_allocs_from_country.draw(anal_data, target = 'd')
    # fig, axes = prototype_allocs_from_country.draw(anal_data, target = 'd')
    # fig, axes = prototype_allocs_from_country.draw(anal_data, target = 'y')
    # ax = axes[0][0]
    # ax.set_yticks(np.arange(0, 16, 5) / 100, np.arange(0, 16, 5))
    # figure_setting.set_xylabel(ax, '', 'Fraction (%)', fontsize = 12, xlabel_coords = -0.1, ylabel_coords = -0.021)
    return fig, axes