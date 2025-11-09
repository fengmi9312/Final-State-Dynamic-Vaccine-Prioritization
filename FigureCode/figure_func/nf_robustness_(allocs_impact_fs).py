#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 22 15:33:20 2025

@author: mifeng
"""


import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import prototype_allocs_impact_fs, figure_setting

def draw(anal_data):
    fig, axes = prototype_allocs_impact_fs.draw(anal_data, target = 'd')
    return fig, axes