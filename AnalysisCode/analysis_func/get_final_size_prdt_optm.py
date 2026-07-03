# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 02:04:00 2025

@author: fengm
"""



from Dependencies.FrameDependencies import name_principle
import pandas as pd
from Dependencies.CodeDependencies import  basic_params, param_data_loader
from itertools import product
from .analysis_dependencies import duplicate_expr_file

def analyze(edata):
    return duplicate_expr_file.analyze(edata, 'final_size_prdt_optm', 'param', 0)