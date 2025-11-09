# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 16:50:53 2025

@author: fengm
"""


import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import prototype_allocs_from_dysttg, figure_setting

def draw(anal_data):
    fig, axes = prototype_allocs_from_dysttg.draw(anal_data, target = 'y')
    return fig, axes
