# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 20:26:24 2025

@author: fengm
"""


from Dependencies.FrameDependencies import name_principle

def analyze(edata, expr_name, expr_param, file_idx):
    return edata[name_principle.get_task_name(expr_name, expr_param)][str(file_idx)]