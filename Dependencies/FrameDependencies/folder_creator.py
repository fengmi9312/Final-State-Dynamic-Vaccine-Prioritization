# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 12:45:09 2025

@author: MIFENG
"""


from filelock import FileLock
import os

def create_folder(folder_path):
    lock = FileLock(folder_path + '.lock')
    with lock:
        os.makedirs(folder_path, exist_ok=True)
    return None