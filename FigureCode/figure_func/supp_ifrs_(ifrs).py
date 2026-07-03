# -*- coding: utf-8 -*-
"""
Created on Sun Jul  6 19:57:20 2025

@author: fengm
"""


import matplotlib.pyplot as plt
import numpy as np
from .figure_dependencies import prototype_ifrs
from .figure_dependencies import figure_setting

def draw(anal_data):
    fig, axes = prototype_ifrs.draw(anal_data)
    return fig, axes