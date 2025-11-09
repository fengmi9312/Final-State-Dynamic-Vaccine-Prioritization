# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 01:39:12 2025

@author: fengm
"""



import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting
import seaborn as sns
from matplotlib.ticker import ScalarFormatter
from matplotlib.transforms import offset_copy

def draw(anal_data, **kwargs):
    ####################################################
    param = kwargs.pop('param', 'lower')
    r0_limit = kwargs.pop('r0_limit', None)
    vac_dur = kwargs.pop('vac_dur', 60)
    ####################################################
    scale_prop = 12
    grid_attrs = [
                  [{'pos': (2, 0), 'size': (14, 5)}, {'pos': (20, 0), 'size': (14, 5)}, {'pos': (2, 25), 'size': (14, 5)}, {'pos': (20, 25), 'size': (14, 5)}, {'pos': (2, 50), 'size': (14, 5)}, {'pos': (20, 50), 'size': (14, 5)}],
                  [{'pos': (2, 6), 'size': (14, 14)}, {'pos': (20, 6), 'size': (14, 14)}, {'pos': (2, 31), 'size': (14, 14)}, {'pos': (20, 31), 'size': (14, 14)}, {'pos': (2, 56), 'size': (14, 14)}, {'pos': (20, 56), 'size': (14, 14)}],
                  
                  [{'pos': (52, 0), 'size': (14, 5)}, {'pos': (70, 0), 'size': (14, 5)}, {'pos': (52, 25), 'size': (14, 5)}, {'pos': (70, 25), 'size': (14, 5)}, {'pos': (52, 50), 'size': (14, 5)}, {'pos': (70, 50), 'size': (14, 5)}],
                  [{'pos': (52, 6), 'size': (14, 14)}, {'pos': (70, 6), 'size': (14, 14)}, {'pos': (52, 31), 'size': (14, 14)}, {'pos': (70, 31), 'size': (14, 14)}, {'pos': (52, 56), 'size': (14, 14)}, {'pos': (70, 56), 'size': (14, 14)}],
                  
                  [{'pos': (102, 0), 'size': (14, 5)}, {'pos': (120, 0), 'size': (14, 5)}, {'pos': (102, 25), 'size': (14, 5)}, {'pos': (120, 25), 'size': (14, 5)}, {'pos': (102, 50), 'size': (14, 5)}, {'pos': (120, 50), 'size': (14, 5)}],
                  [{'pos': (102, 6), 'size': (14, 14)}, {'pos': (120, 6), 'size': (14, 14)}, {'pos': (102, 31), 'size': (14, 14)}, {'pos': (120, 31), 'size': (14, 14)}, {'pos': (102, 56), 'size': (14, 14)}, {'pos': (120, 56), 'size': (14, 14)}],
                  [{'pos': (136, 15), 'size': (1, 40)}]]
    margin_attr = {'top': 5, 'bottom': 5, 'left': 10, 'right': 5}
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.6
    label_fontsize = 9
    tick_fontsize = 7
    text_fontsize = 16
    ####################################################
    age_groups = ['0–9', '10–19', '20–29', '30–39', '40–49', '50–59', '60–69', '70+']
    cmaps = ['cividis', 'viridis', 'cividis', 'viridis']
    sttgs = ['FS-DVP', 'TS-DVP']
    value_names = ['Reduced Final State', 'Reduced Transient State', 'Reduced Final State', 'Reduced Transient State']
    r0_values = [1.4, 2.5]
    target_names = ['Cumulative Infections', 'Deaths', 'YLL']
    effs = ['Direct Effects', 'Indirect Effects']
    for target_idx, target in enumerate(['c', 'd', 'y']):
        for r0_idx in range(2):
            for idx, sttg in enumerate(['min', 'gmin']):
                for eff_idx in range(2) if sttg == 'min' else range(1):
                    ax = axes[target_idx * 2 + 1][(idx * 2 + eff_idx) * 2 + r0_idx]
                    plt.sca(ax)
                    mat_data = anal_data['impact_to_dysttg'][f'{sttg}_{target}_{r0_idx}'].values.T
                    print(np.any(mat_data > 1) or np.any(mat_data < 0))
                    mat_max = np.max(mat_data)
                    if sttg == 'min':
                        if eff_idx == 0: mat_res = anal_data['impact_to_dysttg'][f'dir_{sttg}_{target}_{r0_idx}'].values.T / mat_max
                        else: mat_res = (mat_data - anal_data['impact_to_dysttg'][f'dir_{sttg}_{target}_{r0_idx}'].values.T) / mat_max
                    else:
                        mat_res = mat_data / mat_max
                    im = plt.imshow(mat_res, origin='lower', cmap = 'Reds', vmin=0, vmax=1)
                    figure_setting.set_spine_linewidth(ax, 1)
                    if idx == 1: plt.xticks(np.arange(len(age_groups)), age_groups, rotation = -90, fontsize = tick_fontsize)
                    else: ax.set_xticklabels([])
                    if r0_idx == 0: plt.yticks(np.arange(len(age_groups)), age_groups, fontsize = tick_fontsize)
                    else: ax.set_yticklabels([])
                    if r0_idx == 0 and idx == 1: figure_setting.set_xylabel(ax, 'Vaccinated Group', 'Affected Group', fontsize = label_fontsize, xlabel_coords = -0.26, ylabel_coords = -0.26)
                    elif r0_idx == 0: figure_setting.set_xylabel(ax, '', 'Affected Group', fontsize = label_fontsize, xlabel_coords = -0.26, ylabel_coords = -0.26)
                    elif idx == 1: figure_setting.set_xylabel(ax, 'Vaccinated Group', '', fontsize = label_fontsize, xlabel_coords = -0.26, ylabel_coords = -0.26)
                    else: figure_setting.set_xylabel(ax, '', '', fontsize = label_fontsize, xlabel_coords = -0.26, ylabel_coords = -0.26)
                    #ax.text(0, 1.3, titles[r0_idx * 2 + idx], fontsize = 13, transform = ax.transAxes, ha = 'left', va = 'bottom')
                    if target_idx == 0 and r0_idx == 0 and idx == 0 and eff_idx == 0: cbar = fig.colorbar(im, cax=axes[-1][0])
                    cbar.set_label('Normalized Impact', rotation=270, labelpad=12, fontsize = label_fontsize)
                    cbar.ax.yaxis.set_label_position('right')
                    
                    if target_idx == 0 and r0_idx == 0: ax.text(-0.5, 16 / 15, f'{sttgs[idx]}', fontsize = 11, transform = ax.transAxes, ha = 'center', va = 'center')
                    if target_idx == 0 and r0_idx == 0: ax.text(-0.5, 14.5 / 15, f'({effs[eff_idx]})', fontsize = 9, transform = ax.transAxes, ha = 'center', va = 'center')
                    # fmt = ScalarFormatter(useMathText=True)  
                    # fmt.set_powerlimits((0, 0))              
                    # fmt.set_scientific(True)
                    # cbar.formatter = fmt
                    # cbar.update_ticks()  
                    # off = cbar.ax.yaxis.get_offset_text()
                    # off.set_ha('left')
                    # off.set_transform(offset_copy(off.get_transform(), fig=plt.gcf(), x=0, y=0, units='points'))
        
                    ax = axes[target_idx * 2][(idx * 2 + eff_idx) * 2 + r0_idx]
                    plt.sca(ax)
                    tot_arr_data = (mat_data / mat_max).sum(axis = 0)
                    arr_data =  mat_res.sum(axis = 0)
                    plt.bar(np.arange(len(arr_data)), arr_data, width = 0.95, color = 'tab:red')
                    figure_setting.set_spine_linewidth(ax, 1)
                    plt.xlim(-0.5, 7.5)
                    #plt.ylim(0, 1)
                    figure_setting.remove_spines(ax, ['top', 'right'])
                    ax.set_xticklabels([])
                    ax.spines['left'].set_position(('axes', -0.03))
                    if idx == 1:
                        plt.ylim(0, 1.02)
                        ax.spines['left'].set_bounds(0, 1)
                        ax.set_yticks([0, 1], [0, 1], fontsize = tick_fontsize * 0.9)
                    else:
                        y_lim = int(np.max(tot_arr_data) * 10) + 1
                        y_lim = (y_lim + 1) / 10 if y_lim % 2 == 1 else y_lim / 10
                        plt.ylim(0, y_lim * 1.02)
                        ax.spines['left'].set_bounds(0, y_lim)
                        ax.set_yticks([0, y_lim], [0, y_lim], fontsize = tick_fontsize * 0.9)
                        
                    if idx == 0 and eff_idx == 0: ax.text(0.5, 1.05, f'$R_0 = {r0_values[r0_idx]}$', fontsize = 12, transform = ax.transAxes, ha = 'center', va = 'bottom')
                    if r0_idx == 0 and idx == 0 and eff_idx == 0: ax.text(1.2, 1.6, target_names[target_idx], fontsize = 14, transform = ax.transAxes, ha = 'center', va = 'bottom')
    return fig, axes
    