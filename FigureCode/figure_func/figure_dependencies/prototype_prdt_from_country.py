# -*- coding: utf-8 -*-
"""
Created on Fri May  9 00:48:13 2025

@author: fengm
"""


import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting
import pandas as pd
import seaborn as sns
import itertools
from Dependencies.CodeDependencies import  basic_params, param_data_loader

def draw(anal_data, **kwargs):
    ####################################################
    target = kwargs.pop('target', 'c')
    ####################################################
    scale_prop = 9
    grid_attrs = [[{'pos': (0, 0), 'size': (185, 30)}]]
    margin_attr = {'top': 2, 'bottom': 5, 'left': 9, 'right': 14}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    label_fontsize = 15
    tick_fontsize = 12
    ####################################################
    ax = axes[0][0]
    sttgs = {'zero_vac': 'No Vaccine', 'min': 'FS-DVP'}
    def prepare_data(data_dict):
        mean_res = {country: np.mean([data_dict[f'dist_alloc_from_{basic_params.country_abbr[country]}']['r0'][str(i)][0] for i in range(1000)]) for country in basic_params.country_abbr.keys()}
        r0_res = {}
        ageing_res = {}
        sorted_countries = sorted(mean_res, key=mean_res.get, reverse=False)
        #for decountry in [-3, -2, -1]: del sorted_countries[decountry]
        country_data = param_data_loader.load_all_data(basic_params.country_abbr.keys(), basic_params.group_div)
        target_coef = {}
        for country in sorted_countries:
            target_coef[country] = {'c': country_data[country]['populations'], 'd': country_data[country]['populations'] * country_data[country]['ifrs'], 'y': country_data[country]['populations'] * country_data[country]['ifrs'] * country_data[country]['ylls'], }
            r0_res[country] = [data_dict[f'dist_alloc_from_{basic_params.country_abbr[country]}']['r0'][str(i)][0] for i in range(1000)]
            ageing_res[country] = country_data[country]['populations'][6:].sum() / country_data[country]['populations'].sum()
        rows = []
        vac_mssg = [r'$\theta = 0.14\%$', r'$\theta = 0.35\%$']
        for country, sttg in itertools.product(sorted_countries, sttgs.keys()):
            sheet_name_tmp = f"dist_{sttg}{f'_{target}' if sttg == 'min' else ''}"
            for idx in range(1) if sttg == 'zero_vac' else range(1,2):
                if sttg != 'zero_vac': sheet_name = f'{sheet_name_tmp}_{idx}'
                else: sheet_name = sheet_name_tmp
                for i in range(1000):
                    rows.append({'Country': country, 'Strategy': sttgs[sttg] if sttg == 'zero_vac' else f'{sttgs[sttg]}, {vac_mssg[idx]}', 'Fraction': data_dict[f'dist_alloc_from_{basic_params.country_abbr[country]}'][sheet_name][str(i)].to_numpy() @ target_coef[country][target]})
        return pd.DataFrame(rows), r0_res, ageing_res, sorted_countries
    
    plt.sca(ax)
    df, r0_arr, ageing_arr, country_arr = prepare_data(anal_data)
    sns.despine(bottom=True, left=True)
    edge_width = 1.2
    sns.boxplot(data=df, y="Fraction", x="Country", hue="Strategy", width=.25, gap = 0.2, palette=sns.color_palette("deep")[0:4:3], fill=False, flierprops={'markersize': 1.5, 'markeredgewidth': edge_width},
                boxprops={'linewidth': edge_width}, whiskerprops={'linewidth': edge_width}, capprops={'linewidth': edge_width}, medianprops={'linewidth': edge_width})
    ax.yaxis.grid(True)
    figure_setting.set_xylabel(ax, '', 'Fraction', fontsize = label_fontsize, xlabel_coords = -0.1, ylabel_coords = -0.025)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)
    sns.despine(trim=True, bottom=True)
    if target == 'c':
        ax_twin = ax.twinx()
        plt.sca(ax_twin)
        mean_res = np.array([np.mean(r0_arr[country]) for country in country_arr])
        lower_res = np.array([sorted(r0_arr[country], reverse = False)[50] for country in country_arr])
        upper_res = np.array([sorted(r0_arr[country], reverse = True)[50] for country in country_arr])
        ax_twin.errorbar(np.arange(len(mean_res)), mean_res, yerr=[mean_res - lower_res, upper_res - mean_res], markersize = 9, linewidth = 2, capthick = 2,
                         fmt='D', linestyle = '-', color = 'black', capsize = 6, markeredgewidth = 1, markeredgecolor = 'white', label = r'Basic Reproduction Number ($R_0$)')
        ax_twin.spines['top'].set_visible(False)
        ax_twin.spines['bottom'].set_visible(False)
        ax_twin.spines['left'].set_visible(False)
        ax_twin.set_yticks(np.arange(1, 6), np.arange(1, 6))
        twin_bounds = (1, 5)
        plt.ylabel(r'$R_0$', fontsize = label_fontsize)
        plt.legend(loc = 'lower right', fontsize = 12)
    elif target == 'd':
        ax_twin = ax.twinx()
        plt.sca(ax_twin)
        ageing_res = np.array([ageing_arr[country] for country in country_arr])
        plt.plot(np.arange(len(ageing_res)), ageing_res, marker = 'X', color = 'tab:gray', markersize = 12, linewidth = 2, 
                 linestyle = '-', markeredgewidth = 1, markeredgecolor = 'white', zorder = 1, label = 'Population Ageing')
        ax_twin.spines['top'].set_visible(False)
        ax_twin.spines['bottom'].set_visible(False)
        ax_twin.spines['left'].set_visible(False)
        ax_twin.set_yticks(np.arange(1, 5) / 10, np.arange(1, 5) * 10)
        twin_bounds = (0.1, 0.4)
        plt.ylabel('Population Ageing (%)', fontsize = label_fontsize)
        plt.legend(loc = 'upper right', fontsize = 12)
    else: pass
    if target == 'c' or target == 'd':
        main_ylims = ax.get_ylim()
        main_bounds = ax.spines['left'].get_bounds()
        lower_ylim = twin_bounds[0] + (main_ylims[0] - main_bounds[0]) * (twin_bounds[1] - twin_bounds[0]) / (main_bounds[1] - main_bounds[0])
        upper_ylim = twin_bounds[1] + (main_ylims[1] - main_bounds[1]) * (twin_bounds[1] - twin_bounds[0]) / (main_bounds[1] - main_bounds[0])
        ax_twin.set_ylim(lower_ylim, upper_ylim)
        ax_twin.spines['right'].set_bounds(twin_bounds[0], twin_bounds[1])
    
    return fig, axes
