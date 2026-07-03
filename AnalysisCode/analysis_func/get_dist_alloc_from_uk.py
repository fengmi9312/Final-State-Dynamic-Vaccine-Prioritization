# -*- coding: utf-8 -*-
"""
Created on Wed May  7 21:05:48 2025

@author: fengm
"""


from .analysis_dependencies import dist_alloc_from_country

def analyze(edata):
    import os
    full_path = __file__
    file_name = os.path.basename(full_path)
    name_without_extension, _ = os.path.splitext(file_name)
    ab_country = {'us': 'United States', 'uk': 'United Kingdom', 'fr': 'France', 'de': 'Germany', 'es': 'Spain', 'jp': 'Japan', 'il': 'Israel', 'at': 'Austria', 'ie': 'Ireland', 'kr': 'South Korea', 'it': 'Italy', 'sg': 'Singapore'}
    return dist_alloc_from_country.analyze(edata, ab_country[name_without_extension.split('_')[-1]])