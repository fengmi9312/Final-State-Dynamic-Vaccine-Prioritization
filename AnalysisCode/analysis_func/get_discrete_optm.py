#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 12:44:20 2025

@author: mifeng
"""



from Dependencies.FrameDependencies import name_principle
import pandas as pd
from Dependencies.CodeDependencies import  basic_params, param_data_loader
from itertools import product
from .analysis_dependencies import duplicate_expr_file

def analyze(edata):
    return duplicate_expr_file.analyze(edata, 'discrete_optm', 'param', 0)