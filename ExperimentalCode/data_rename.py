# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 20:12:47 2024

@author: fengm
"""
xxx
import os
import numpy as np
for file_idx in :
    current_name = f"Data_optm_from_comp_({expr_param})[{file_idx}].xlsx"
    new_name = f"Data_optm_from_comp_({expr_param})[{file_idx-3}].xlsx"
    current_path = os.path.join(folder_path, current_name)
    new_path = os.path.join(folder_path, new_name)
    try:
        os.rename(current_path, new_path)
        print("File renamed successfully.")
    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print("Permission denied to rename the file.")
    except Exception as e:
        print("An error occurred:", e)
print(expr_param)