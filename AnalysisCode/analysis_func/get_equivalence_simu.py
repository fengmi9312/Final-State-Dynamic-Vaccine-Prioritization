# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 20:31:54 2025

@author: fengm
"""


from Dependencies.FrameDependencies import name_principle
import pandas as pd
from Dependencies.CodeDependencies import  basic_params, param_data_loader
from itertools import product
from .analysis_dependencies import duplicate_expr_file

def analyze(edata):
    return duplicate_expr_file.analyze(edata, 'equivalence_simu', 'param', 0)