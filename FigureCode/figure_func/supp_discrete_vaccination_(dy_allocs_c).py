#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 12:57:04 2025

@author: mifeng
"""



import matplotlib.pyplot as plt
import numpy as np
from .figure_dependencies import prototype_alloc_discrete_vaccination
from .figure_dependencies import figure_setting

def draw(anal_data):
    fig, axes = prototype_alloc_discrete_vaccination.draw(anal_data)
    return fig, axes