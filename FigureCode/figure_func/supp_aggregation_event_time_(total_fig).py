if __name__ == '__main__':
    import os
    import sys
    root_level = 2
    code_root = os.path.dirname(os.path.abspath(__file__))
    for i in range(root_level): code_root = os.path.dirname(code_root)
    sys.path.append(code_root)

from Dependencies.CodeDependencies import basic_params, func
import numpy as np
from scipy.special import gamma

def get_mean_from_weibull(alpha, beta):
    return beta * gamma(1 + 1.0 / alpha)

def get_beta_from_weibull(alpha, mean_value):
    return mean_value / gamma(1 + 1.0 / alpha)

def get_sum_of_rem(srv_rem_prev, srv_rem_next):
    srv_rem_prev_len = np.where(srv_rem_prev <= 0)[0][0] if np.any(srv_rem_prev <= 0) else len(srv_rem_prev)
    dist_rem_prev = -np.diff(srv_rem_prev[:srv_rem_prev_len])
    srv_rem_next_len = np.where(srv_rem_next <= 0)[0][0] if np.any(srv_rem_next <= 0) else len(srv_rem_next)
    dist_rem_next = -np.diff(srv_rem_next[:srv_rem_next_len])
    dist_sum = np.append(0, np.convolve(dist_rem_prev, dist_rem_next))
    srv_rem_sum = 1 - np.append(0, np.cumsum(dist_sum))
    srv_rem_sum_len = np.where(srv_rem_sum <= 0)[0][0] if np.any(srv_rem_sum <= 0) else len(srv_rem_sum)
    return srv_rem_sum[:srv_rem_sum_len]

def get_cum(srv_inf, srv_rem):
    srv_inf_len = np.where(srv_inf <= 0)[0][0] if np.any(srv_inf <= 0) else len(srv_inf)
    srv_rem_len = np.where(srv_rem <= 0)[0][0] if np.any(srv_rem <= 0) else len(srv_rem)
    cum_len = min(srv_inf_len - 1, srv_rem_len)
    haz_inf = 1 - srv_inf[1:srv_inf_len] / srv_inf[:srv_inf_len - 1]
    haz_cum = haz_inf[:cum_len] * srv_rem[:cum_len]
    return haz_cum

def get_sum_of_cum(cum_prev, srv_rem_prev, cum_next):
    tmp0 = cum_prev
    dist_rem_prev = - np.diff(srv_rem_prev)
    tmp1 = np.append(0, np.convolve(dist_rem_prev, cum_next))
    tot_len = max(len(tmp0), len(tmp1))
    if len(tmp0) < tot_len: tmp0 = np.append(tmp0, np.zeros(tot_len - len(tmp0)))
    if len(tmp1) < tot_len: tmp1 = np.append(tmp1, np.zeros(tot_len - len(tmp1)))
    return tmp0 + tmp1
    
def arr_sum(a, b, alpha, beta):
    a_tmp, b_tmp = a, b
    tot_len = max(len(a_tmp), len(b_tmp))
    if len(a_tmp) < tot_len: a_tmp = np.append(a_tmp, np.zeros(tot_len - len(a_tmp)))
    if len(b_tmp) < tot_len: b_tmp = np.append(b_tmp, np.zeros(tot_len - len(b_tmp)))
    return alpha * a_tmp + beta * b_tmp

def draw(anal_data):

    asym_prob = 0.1

    exp_alpha_rem = 2.5
    exp_mean_rem = 4
    exp_beta_rem = get_beta_from_weibull(exp_alpha_rem, exp_mean_rem)
    asym_alpha_inf, asym_alpha_rem = 1.5, 2.5
    asym_mean_inf, asym_mean_rem = 5, 6
    asym_beta_inf = get_beta_from_weibull(asym_alpha_inf, asym_mean_inf)
    asym_beta_rem = get_beta_from_weibull(asym_alpha_rem, asym_mean_rem)
    presym_alpha_inf, presym_alpha_rem = 1.6, 2.4
    presym_mean_inf, presym_mean_rem = 2, 3
    presym_beta_inf = get_beta_from_weibull(presym_alpha_inf, presym_mean_inf)
    presym_beta_rem = get_beta_from_weibull(presym_alpha_rem, presym_mean_rem)
    sym_alpha_inf, sym_alpha_rem = 2, 3
    sym_mean_inf, sym_mean_rem = 3, 4
    sym_beta_inf = get_beta_from_weibull(sym_alpha_inf, sym_mean_inf)
    sym_beta_rem = get_beta_from_weibull(sym_alpha_rem, sym_mean_rem)

    exp_srv_rem = func.srv_weibull(exp_alpha_rem, exp_beta_rem, basic_params.srv_length, 1 / basic_params.day_div)
    exp_cum = np.zeros(len(exp_srv_rem))
    asym_srv_inf = func.srv_weibull(asym_alpha_inf, asym_beta_inf, basic_params.srv_length, 1 / basic_params.day_div)
    asym_srv_rem = func.srv_weibull(asym_alpha_rem, asym_beta_rem, basic_params.srv_length, 1 / basic_params.day_div)
    asym_cum = get_cum(asym_srv_inf, asym_srv_rem)
    presym_srv_inf = func.srv_weibull(presym_alpha_inf, presym_beta_inf, basic_params.srv_length, 1 / basic_params.day_div)
    presym_srv_rem = func.srv_weibull(presym_alpha_rem, presym_beta_rem, basic_params.srv_length, 1 / basic_params.day_div)
    presym_cum = get_cum(presym_srv_inf, presym_srv_rem)
    sym_srv_inf = func.srv_weibull(sym_alpha_inf, sym_beta_inf, basic_params.srv_length, 1 / basic_params.day_div)
    sym_srv_rem = func.srv_weibull(sym_alpha_rem, sym_beta_rem, basic_params.srv_length, 1 / basic_params.day_div)
    sym_cum = get_cum(sym_srv_inf, sym_srv_rem)


    tot_srv_rem = get_sum_of_rem(exp_srv_rem, arr_sum(asym_srv_rem, get_sum_of_rem(presym_srv_rem, sym_srv_rem), asym_prob, 1 - asym_prob))
    tot_haz_cum = get_sum_of_cum(exp_cum, exp_srv_rem, arr_sum(asym_cum, get_sum_of_cum(presym_cum, presym_srv_rem, sym_cum), asym_prob, 1 - asym_prob))
    tot_len = min(len(tot_srv_rem), len(tot_haz_cum))
    tot_srv_rem, tot_haz_cum = tot_srv_rem[:tot_len], tot_haz_cum[:tot_len]
    tot_haz_inf = tot_haz_cum / tot_srv_rem
    tot_srv_inf = np.cumprod(1 - np.append(0, tot_haz_inf))
    
    
        ####################################################
    # Draw event-time distributions for Fig. 1d validation
    ####################################################
    import matplotlib.pyplot as plt
    from .figure_dependencies import figure_setting
    plt.rcParams.update({
    'mathtext.fontset': 'stix',})
    scale_prop = 6
    
    grid_attrs = [
        [{'pos': (0, 0), 'size': (36, 24)}, {'pos': (50, 0), 'size': (36, 24)}, {'pos': (0, 36), 'size': (36, 24)}, {'pos': (50, 36), 'size': (36, 24)}],
        [{'pos': (110, 0), 'size': (72, 60)}], 
        [{'pos': (0, 80), 'size': (36, 24)}, {'pos': (50, 80), 'size': (36, 24)}, {'pos': (0, 116), 'size': (36, 24)}, {'pos': (50, 116), 'size': (36, 24)}],
        [{'pos': (110, 80), 'size': (72, 60)}],
    ]
    
    margin_attr = {'top': 4, 'bottom': 14, 'left': 16, 'right': 9}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 12
    tick_fontsize = 9
    title_fontsize = 11
    legend_fontsize = 10
    max_tau = 30
    dt = 1 / basic_params.day_div
    ####################################################
    
    def get_event_time_dist_from_srv(srv):
        """
        Convert survival function Psi(tau) to event-time distribution psi(tau).
        Continuous form: psi(tau) = -d Psi(tau) / d tau.
        Discrete approximation: psi_i = [Psi_i - Psi_{i+1}] / dt.
        """
        srv = np.asarray(srv, dtype=float)
        psi = -np.diff(srv) / dt
        psi[psi < 0] = 0
        tau = np.arange(len(psi)) * dt
        return tau, psi
    
    def trim_by_time(tau, y, max_tau=max_tau):
        tau = np.asarray(tau)
        y = np.asarray(y)
        idx = tau <= max_tau
        return tau[idx], y[idx]
    
    def format_ax(ax, xlabel=False, ylabel=False, xlabel_coords=-0.2, ylabel_coords=-0.2, tick_fontsize = tick_fontsize, label_fontsize = label_fontsize):
        for spine in ax.spines.values():
            spine.set_linewidth(spine_linewidth)
        ax.tick_params(axis='both', labelsize=tick_fontsize, width=spine_linewidth)
        figure_setting.set_xylabel(
            ax,
            r'Infection age $\tau$ (d)' if xlabel else '',
            r'Event-time density' if ylabel else '',
            fontsize=label_fontsize,
            xlabel_coords = xlabel_coords,
            ylabel_coords = ylabel_coords
        )
    
    # --------------------------------------------------
    # Detailed model: infection event-time distributions
    # --------------------------------------------------
    tau_asym_inf, psi_asym_inf = get_event_time_dist_from_srv(asym_srv_inf)
    tau_presym_inf, psi_presym_inf = get_event_time_dist_from_srv(presym_srv_inf)
    tau_sym_inf, psi_sym_inf = get_event_time_dist_from_srv(sym_srv_inf)
    
    tau_exp_inf = np.arange(len(exp_srv_rem) - 1) * dt
    psi_exp_inf = np.zeros_like(tau_exp_inf)
    
    detailed_inf_data = [
        (tau_exp_inf,    psi_exp_inf,    r'$\psi^{\mathrm{exp}}_{\mathrm{inf}}(\tau)$',     'Exposed infection'),
        (tau_asym_inf,   psi_asym_inf,   r'$\psi^{\mathrm{asym}}_{\mathrm{inf}}(\tau)$',    'Asymptomatic infection'),
        (tau_presym_inf, psi_presym_inf, r'$\psi^{\mathrm{presym}}_{\mathrm{inf}}(\tau)$',  'Presymptomatic infection'),
        (tau_sym_inf,    psi_sym_inf,    r'$\psi^{\mathrm{sym}}_{\mathrm{inf}}(\tau)$',     'Symptomatic infection')
    ]
    
    for col_idx, (tau, psi, label, title) in enumerate(detailed_inf_data):
        ax = axes[0][col_idx]
        plt.sca(ax)
        tau_plot, psi_plot = trim_by_time(tau, psi)
        ax.plot(tau_plot, psi_plot, color='tab:red', linewidth=2, label=label)
        ax.set_title(title, fontsize=title_fontsize)
        ax.legend(loc='upper right', fontsize=legend_fontsize, frameon=False)
        format_ax(ax, col_idx in [2, 3], col_idx in [0, 2], ylabel_coords= -0.25 if col_idx == 0 else -0.15)
        ax.set_xlim(0, max_tau)
    
    # --------------------------------------------------
    # Detailed model: exit event-time distributions
    # --------------------------------------------------
    tau_exp_exit, psi_exp_exit = get_event_time_dist_from_srv(exp_srv_rem)
    tau_asym_exit, psi_asym_exit = get_event_time_dist_from_srv(asym_srv_rem)
    tau_presym_exit, psi_presym_exit = get_event_time_dist_from_srv(presym_srv_rem)
    tau_sym_exit, psi_sym_exit = get_event_time_dist_from_srv(sym_srv_rem)
    
    detailed_exit_data = [
        (tau_exp_exit,    psi_exp_exit,    r'$\psi^{\mathrm{exp}}_{\mathrm{exit}}(\tau)$',     'Exposed exit'),
        (tau_asym_exit,   psi_asym_exit,   r'$\psi^{\mathrm{asym}}_{\mathrm{exit}}(\tau)$',    'Asymptomatic exit'),
        (tau_presym_exit, psi_presym_exit, r'$\psi^{\mathrm{presym}}_{\mathrm{exit}}(\tau)$',  'Presymptomatic exit'),
        (tau_sym_exit,    psi_sym_exit,    r'$\psi^{\mathrm{sym}}_{\mathrm{exit}}(\tau)$',     'Symptomatic exit')
    ]
    
    for col_idx, (tau, psi, label, title) in enumerate(detailed_exit_data):
        ax = axes[2][col_idx]
        plt.sca(ax)
        tau_plot, psi_plot = trim_by_time(tau, psi)
        ax.plot(tau_plot, psi_plot, color='tab:blue', linewidth=2, label=label)
        ax.set_title(title, fontsize=title_fontsize)
        ax.legend(loc='upper right', fontsize=legend_fontsize, frameon=False)
        format_ax(ax, col_idx in [2, 3], col_idx in [0, 2])
        ax.set_xlim(0, max_tau)
    
    # --------------------------------------------------
    # Aggregated general model: derived distributions
    # --------------------------------------------------
    tau_tot_inf, psi_tot_inf = get_event_time_dist_from_srv(tot_srv_inf)
    tau_tot_rem, psi_tot_rem = get_event_time_dist_from_srv(tot_srv_rem)
    
    aggregated_data = [
        (tau_tot_inf, psi_tot_inf, r'$\psi_{\mathrm{inf}}(\tau)$', 'Aggregated infection'),
        (tau_tot_rem, psi_tot_rem, r'$\psi_{\mathrm{rem}}(\tau)$', 'Aggregated removal')
    ]
    
    for col_idx, (tau, psi, label, title) in enumerate(aggregated_data):
        ax = axes[1 + 2 * col_idx][0]
        plt.sca(ax)
        tau_plot, psi_plot = trim_by_time(tau, psi)
        ax.plot(tau_plot, psi_plot, color=['tab:orange', 'tab:green'][col_idx], linewidth=2, label=label)
        ax.set_title(title, fontsize=title_fontsize * 1.2)
        ax.legend(loc='upper right', fontsize=legend_fontsize * 1.5, frameon=False)
        format_ax(ax, True, True, xlabel_coords=-0.1, ylabel_coords=-0.12, tick_fontsize = 1.2 * tick_fontsize, label_fontsize=1.2 * label_fontsize)
        ax.set_xlim(0, max_tau)
    
    
    
    return fig, axes
        
        
        