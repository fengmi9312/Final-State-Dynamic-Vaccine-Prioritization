

import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import prototype_robustness_ipeak, figure_setting

def draw(anal_data):
    fig, axes = prototype_robustness_ipeak.draw(anal_data, robust_type = 'r0')
    yticks = [np.arange(0, 101, 25), np.arange(0, 26, 5) / 10]
    axin_yticks = [np.arange(0, 41, 20), np.arange(0, 7, 2) / 10, np.arange(0, 11, 5)]
    ylabels = ['Infection peak (%)', 'Infection peak (%)']
    ylims = [(0, 60, 15), (0, 60, 15)]
    coefs = [(0.01, 1), (0.01, 1)]
    for idx in range(2):
        ax = axes[0][idx]
        plt.sca(ax)
        plt.legend(loc = 'lower right', fontsize = 9)
        ax.text(0.02, 0.98, r'$\theta = 0.35\%$', fontsize = 15, transform = ax.transAxes, ha = 'left', va = 'top')
        x_lowerlim, x_upperlim, x_gap = 1, 5.5, 1
        ax.set_xlim(x_lowerlim - (x_upperlim - x_lowerlim) / 20, x_upperlim)
        # ax.spines['bottom'].set_bounds(x_lowerlim, x_upperlim)
        figure_setting.set_xtick_ranges(ax, 1, 5, 1)
        
        y_lowerlim, y_upperlim, y_gap = ylims[idx]
        ax.set_ylim((y_lowerlim - (y_upperlim - y_lowerlim) / 20) * coefs[idx][0], y_upperlim * coefs[idx][0])
        figure_setting.set_ytick_ranges(ax, y_lowerlim, y_upperlim, y_gap, coefs = coefs[idx])
        figure_setting.set_xylabel(ax, r'$R_0$', ylabels[idx], fontsize = 15, xlabel_coords = -0.08, ylabel_coords = -0.075)
    return fig, axes
