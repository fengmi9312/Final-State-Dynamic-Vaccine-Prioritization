# -*- coding: utf-8 -*-
"""
Created on Sun Jul  6 15:16:47 2025

@author: fengm
"""


import matplotlib.pyplot as plt
import numpy as np
from .figure_dependencies import prototype_contacts_from_country
from .figure_dependencies import figure_setting

def draw(anal_data):
    fig, axes = prototype_contacts_from_country.draw(anal_data)
    return fig, axes