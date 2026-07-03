# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 01:46:18 2025

@author: fengm
"""



import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import prototype_impact_to_dysttg, figure_setting

def draw(anal_data):
    fig, axes = prototype_impact_to_dysttg.draw(anal_data, target = 'd')
    return fig, axes