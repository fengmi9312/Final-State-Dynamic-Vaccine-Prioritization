# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 21:59:33 2025

@author: fengm
"""


import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import prototype_perf_from_equity_r0, figure_setting

def draw(anal_data):
    fig, axes = prototype_perf_from_equity_r0.draw(anal_data)
    return fig, axes
