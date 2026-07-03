#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 14:49:42 2025

@author: mifeng
"""



from .figure_dependencies import prototype_risk_index

def draw(anal_data):
    fig, axes = prototype_risk_index.draw(anal_data)
    return fig, axes