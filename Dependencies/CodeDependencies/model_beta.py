# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 13:46:14 2022

@author: 20481756
"""


import numpy as np
from scipy.optimize import minimize, LinearConstraint, Bounds
from . import func
from copy import deepcopy

class epidemic_model:
    
    def __init__(self, i0, populations, contacts, k,
                 exp_srv_rem,
                 sym_srv_inf, sym_srv_rem,
                 ifrs, ylls,
                 day_div = 100, time = 0, period_len = 1000,
                 delay = 14, eta = 1):
        step = 1 / day_div
        self.__day_div = day_div
        self.__populations = np.array(populations)
        self.__contacts = np.array(contacts)
        
        self.__k = np.array(k)
        self.__group_amount = len(self.__populations)
        
        self.__i0 = np.array(i0)
        self.__ifrs = np.array(ifrs)
        self.__ylls = np.array(ylls)
        
        if exp_srv_rem[0] != 1: print('srv error!')
        self.__exp_actl_rem_len = np.where(exp_srv_rem <= 0)[0][0] if np.any(exp_srv_rem <= 0) else len(exp_srv_rem)
        self.__exp_srv_rem = deepcopy(exp_srv_rem[:self.__exp_actl_rem_len])
        self.__exp_dist_rem = - np.diff(self.__exp_srv_rem)
        
        if sym_srv_inf[0] != 1 or sym_srv_rem[0] != 1: print('srv error!')
        self.__sym_actl_inf_len = np.where(sym_srv_inf <= 0)[0][0] if np.any(sym_srv_inf <= 0) else len(sym_srv_inf)
        self.__sym_actl_rem_len = np.where(sym_srv_rem <= 0)[0][0] if np.any(sym_srv_rem <= 0) else len(sym_srv_rem)
        self.__sym_cum_len = min(self.__sym_actl_inf_len - 1, self.__sym_actl_rem_len)
        self.__sym_haz_inf = 1 - sym_srv_inf[1:self.__sym_actl_inf_len] / sym_srv_inf[:self.__sym_actl_inf_len - 1]
        self.__sym_srv_rem = deepcopy(sym_srv_rem[:self.__sym_actl_rem_len])
        self.__sym_haz_cum = self.__sym_haz_inf[:self.__sym_cum_len] * self.__sym_srv_rem[:self.__sym_cum_len]
        self.__sym_dist_rem = - np.diff(self.__sym_srv_rem)
        
        self.__delay = deepcopy(delay)
        self.__eta = deepcopy(eta)
        
        self.__totmat = self.__contacts * self.__populations[None, :] * self.__k  
        self.__step = deepcopy(step)
        self.__time0 = deepcopy(time)
        self.__period_len = deepcopy(period_len)
        self.return_to_init()
        
    def return_to_init(self):
        self.__time_line = [self.__time0,]
        self.__current_time_int = 0
        self.__time_int = 0
        
        self.__sv = np.zeros((self.__period_len, self.__group_amount))
        self.__exp_in = np.zeros((self.__period_len, self.__group_amount))
        self.__exp = np.zeros((self.__period_len, self.__group_amount))
        self.__sym_in = np.zeros((self.__period_len, self.__group_amount))
        self.__sym = np.zeros((self.__period_len, self.__group_amount))
        self.__r = np.zeros((self.__period_len, self.__group_amount))
        self.__c = np.zeros((self.__period_len, self.__group_amount))
        self.__d = np.zeros((self.__period_len, self.__group_amount))
        self.__y = np.zeros((self.__period_len, self.__group_amount))
        self.__p = np.zeros((self.__period_len, self.__group_amount))
        self.__u = np.zeros((self.__period_len, self.__group_amount))
        self.__s = np.zeros((self.__period_len, self.__group_amount))
        
        self.__sv_tot = np.zeros(self.__period_len)
        self.__exp_in_tot = np.zeros(self.__period_len)
        self.__exp_tot = np.zeros(self.__period_len)
        self.__sym_in_tot = np.zeros(self.__period_len)
        self.__sym_tot = np.zeros(self.__period_len)
        self.__r_tot = np.zeros(self.__period_len)
        self.__c_tot = np.zeros(self.__period_len)
        self.__d_tot = np.zeros(self.__period_len)
        self.__y_tot = np.zeros(self.__period_len)
        self.__p_tot = np.zeros(self.__period_len)
        self.__u_tot = np.zeros(self.__period_len)
        self.__s_tot = np.zeros(self.__period_len)
        
        self.__sv[0] = 1 - self.__i0
        self.__exp_in[0] = self.__i0
        self.__exp[0] = self.__i0
        self.__sym_in[0] = np.zeros(self.__group_amount)
        self.__sym[0] = np.zeros(self.__group_amount)
        self.__r[0] = np.zeros(self.__group_amount)
        self.__c[0] = self.__i0
        self.__d[0] = self.__r[0] * self.__ifrs
        self.__y[0] = self.__r[0] * self.__ifrs * self.__ylls
        self.__u[0] = np.zeros(self.__group_amount)
        self.__p[0] = np.zeros(self.__group_amount)
        
        self.__j = np.zeros((self.__period_len, self.__group_amount))
        self.__j[0] = self.__calc_inf()
        self.__calc_tot()
        
        self.__s[0] = 1 - self.__i0
        self.__s_tot[0] = self.__s[self.__current_time_int] @ self.__populations
        self.__current_len = self.__period_len
        for i in range(self.__delay):
            self.spread_once()
     
    def return_back(self, c_time_int, remain_v = False):
        time_int_add = 0 if remain_v else -1
        if c_time_int + time_int_add == -1:
            self.return_to_init()
        else:
            self.__time_int = c_time_int + self.__delay + time_int_add
            self.__current_time_int = c_time_int + time_int_add
            self.__time_line = self.__time_line[:self.__current_time_int + 1]
            if remain_v == False:
                self.spread_once()      
                
    def __expand_len(self):
        self.__sv = np.append(self.__sv, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        self.__exp_in = np.append(self.__exp_in, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        self.__exp = np.append(self.__exp, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        self.__sym_in = np.append(self.__sym_in, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        self.__sym = np.append(self.__sym, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        self.__r = np.append(self.__r, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        self.__c = np.append(self.__c, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        self.__d = np.append(self.__d, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        self.__y = np.append(self.__y, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        self.__u = np.append(self.__u, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        self.__p = np.append(self.__p, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        self.__s = np.append(self.__s, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        
        self.__j = np.append(self.__j, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        
        self.__sv_tot = np.append(self.__sv_tot, np.zeros(self.__period_len))
        self.__exp_in_tot = np.append(self.__exp_in_tot, np.zeros(self.__period_len))
        self.__exp_tot = np.append(self.__exp_tot, np.zeros(self.__period_len))
        self.__sym_in_tot = np.append(self.__sym_in_tot, np.zeros(self.__period_len))
        self.__sym_tot = np.append(self.__sym_tot, np.zeros(self.__period_len))
        self.__r_tot = np.append(self.__r_tot, np.zeros(self.__period_len))
        self.__c_tot = np.append(self.__c_tot, np.zeros(self.__period_len))
        self.__d_tot = np.append(self.__d_tot, np.zeros(self.__period_len))
        self.__y_tot = np.append(self.__y_tot, np.zeros(self.__period_len))
        self.__u_tot = np.append(self.__u_tot, np.zeros(self.__period_len))
        self.__p_tot = np.append(self.__p_tot, np.zeros(self.__period_len))
        self.__s_tot = np.append(self.__s_tot, np.zeros(self.__period_len))
        
        self.__current_len = self.__current_len + self.__period_len

        
# the following functions calculate the spreading
###############################################################################            
        
    def __calc_inf(self):
        return func.mulf(self.__totmat, 
                         self.__sym_haz_cum[:func.get_tail(self.__time_int, self.__sym_cum_len)] @ self.__sym_in[self.__time_int:func.get_head(self.__time_int, self.__sym_cum_len):-1])
       
    
    def __calc_tot(self):
        self.__exp_in_tot[self.__time_int] = self.__exp_in[self.__time_int] @ self.__populations
        self.__sym_in_tot[self.__time_int] = self.__sym_in[self.__time_int] @ self.__populations
        self.__sv_tot[self.__time_int] = self.__sv[self.__time_int] @ self.__populations
        self.__exp_tot[self.__time_int] = self.__exp[self.__time_int] @ self.__populations
        self.__sym_tot[self.__time_int] = self.__sym[self.__time_int] @ self.__populations
        self.__r_tot[self.__time_int] = self.__r[self.__time_int] @ self.__populations
        self.__c_tot[self.__time_int] = self.__c[self.__time_int] @ self.__populations
        self.__d_tot[self.__time_int] = self.__d[self.__time_int] @ self.__populations
        self.__y_tot[self.__time_int] = self.__y[self.__time_int] @ self.__populations
        self.__u_tot[self.__time_int] = self.__u[self.__time_int] @ self.__populations
        self.__p_tot[self.__time_int] = self.__p[self.__time_int] @ self.__populations
        if self.__time_int >= self.__delay:
            self.__s_tot[self.__current_time_int] = self.__s[self.__current_time_int] @ self.__populations

    def __get_eff(self):
        nonzero_idx = (self.__s[self.__current_time_int] != 0)
        _eff = np.zeros(self.__group_amount)
        _eff[nonzero_idx] = self.__sv[self.__time_int][nonzero_idx] / self.__s[self.__current_time_int][nonzero_idx]
        return _eff
    
    
    def add_vaccination(self, vac_alloc):
        remaining_vac = 0
        vac_alloc_tmp = deepcopy(vac_alloc)
        if self.__time_int >= self.__delay:
            larger_idx = (vac_alloc_tmp > self.__s[self.__current_time_int])
            remaining_vac = (vac_alloc_tmp[larger_idx] - self.__s[self.__current_time_int][larger_idx]) @ self.__populations[larger_idx]
            vac_alloc_tmp[larger_idx] = self.__s[self.__current_time_int][larger_idx]
            sv_dec = vac_alloc_tmp * self.__get_eff()
            p_inc = sv_dec * self.__eta
            u_inc = sv_dec * (1 - self.__eta)
            self.__p[self.__time_int] = self.__p[self.__time_int] + p_inc
            self.__sv[self.__time_int] = self.__sv[self.__time_int] - sv_dec
            self.__u[self.__time_int] = self.__u[self.__time_int] + u_inc
            self.__s[self.__current_time_int] = self.__s[self.__current_time_int] - vac_alloc_tmp
            self.__p_tot[self.__time_int] = self.__p[self.__time_int] @ self.__populations
            self.__sv_tot[self.__time_int] = self.__sv[self.__time_int] @ self.__populations
            self.__u_tot[self.__time_int] = self.__u[self.__time_int] @ self.__populations
            self.__s_tot[self.__current_time_int] = self.__s[self.__current_time_int] @ self.__populations
        return remaining_vac
        
    def spread_once(self):
        if self.__time_int == self.__current_len - 1: self.__expand_len()
        sv_out_tmp = self.__sv[self.__time_int] * self.__j[self.__time_int]
        u_out_tmp = self.__u[self.__time_int] * self.__j[self.__time_int]
        exp_in_tmp = sv_out_tmp + u_out_tmp
        self.__exp_in[self.__time_int + 1] = exp_in_tmp
        self.__sym_in[self.__time_int + 1] = self.__exp_dist_rem[:func.get_tail(self.__time_int,self.__exp_actl_rem_len-1)] @ self.__exp_in[self.__time_int:func.get_head(self.__time_int,self.__exp_actl_rem_len-1):-1]
        self.__r[self.__time_int + 1] = self.__r[self.__time_int] + self.__sym_dist_rem[:func.get_tail(self.__time_int,self.__sym_actl_rem_len-1)] @ self.__sym_in[self.__time_int:func.get_head(self.__time_int,self.__sym_actl_rem_len-1):-1]
        self.__c[self.__time_int + 1] = self.__c[self.__time_int] + exp_in_tmp
        self.__sv[self.__time_int + 1] = self.__sv[self.__time_int] - sv_out_tmp
        self.__u[self.__time_int + 1] = self.__u[self.__time_int] - u_out_tmp
        self.__exp[self.__time_int + 1] = self.__exp_srv_rem[:func.get_tail(self.__time_int + 1,self.__exp_actl_rem_len)] @ self.__exp_in[self.__time_int + 1:func.get_head(self.__time_int + 1,self.__exp_actl_rem_len):-1]
        self.__sym[self.__time_int + 1] = self.__sym_srv_rem[:func.get_tail(self.__time_int + 1,self.__sym_actl_rem_len)] @ self.__sym_in[self.__time_int + 1:func.get_head(self.__time_int + 1,self.__sym_actl_rem_len):-1]
        self.__d[self.__time_int + 1] = self.__r[self.__time_int + 1] * self.__ifrs
        self.__y[self.__time_int + 1] = self.__r[self.__time_int + 1] * self.__ifrs * self.__ylls
        self.__p[self.__time_int + 1] = self.__p[self.__time_int]
        if self.__time_int >= self.__delay:
            self.__s[self.__current_time_int + 1] = self.__s[self.__current_time_int] - self.__s[self.__current_time_int] * self.__j[self.__current_time_int]
            self.__current_time_int = self.__current_time_int + 1
            self.__time_line.append(self.__time_line[-1] + self.__step)
        self.__time_int = self.__time_int + 1
        self.__j[self.__time_int] = self.__calc_inf()
        self.__calc_tot()
        
  
###############################################################################    

    
# the following functions are for the prediction of steady state    
#############################################################################
   
    
    def order_alloc(self, vac_avail, group_order):
        remaining_amount = vac_avail
        alloc = np.zeros(self.__group_amount)
        s_arr = self.getc_s()
        for groups in group_order:
            if s_arr[groups] @ self.__populations[groups] == 0:
                proportion = np.zeros(len(groups))
            else:
                proportion = (s_arr[groups] * self.__populations[groups]) / (s_arr[groups] @ self.__populations[groups])
            alloc[groups] = proportion * min(remaining_amount, s_arr[groups] @ self.__populations[groups]) / self.__populations[groups]
            remaining_amount = remaining_amount - (alloc[groups] @ self.__populations[groups]).sum()
        return alloc, remaining_amount
    
    
    def empirical_alloc(self, vac_avail, sttg):
        if sttg == 'all_ages': group_order = [np.arange(self.__group_amount)]
        elif sttg == 'old_first': group_order = [[i] for i in np.arange(self.__group_amount)[::-1]]
        elif sttg == 'young_first': group_order = [[i] for i in np.arange(self.__group_amount)]
        elif sttg == 'contact_first': 
            m_arr = self.__contacts.sum(axis = 1)
            group_order = func.order_index(m_arr)
        elif sttg == 'ifr_first': 
            m_arr = self.__ifrs
            group_order = func.order_index(m_arr)
        elif sttg == 'yll_first': 
            m_arr = self.__ifrs * self.__ylls
            group_order = func.order_index(m_arr)
        elif sttg == 'under_20': 
            group_order = [[0, 1], [2, 3, 4, 5, 6, 7]]
        elif sttg == '20-49': 
            group_order = [[2, 3, 4], [0, 1, 5, 6, 7]]
        elif sttg == '20+': 
            group_order = [[2, 3, 4, 5, 6, 7], [0, 1]]
        elif sttg == '60+': 
            group_order = [[6, 7], [0, 1, 2, 3, 4, 5]]
        elif sttg == 'zero_vac':
            return np.zeros(self.__group_amount)
        return self.order_alloc(vac_avail, group_order)[0]
    
###############################################################################


# the following functions return the details of the situations
###############################################################################
    
    def set_eta(self, eta):
        self.__eta = eta
        
    def set_param_m(self, inf_m, rem_m):
        self.__inf_m = inf_m
        self.__rem_m = rem_m
        
    def set_k(self, k):
        self.__k = k
        self.__totmat = self.__contacts * self.__populations[None, :] * self.__k  
    
    def get_populations(self):
        return self.__populations
    
    def get_contacts(self):
        return self.__contacts
    
    def get_lockdown(self):
        return self.__lockdown
    
    def get_ifrs(self):
        return self.__ifrs
    
    def get_ylls(self):
        return self.__ylls
    
    def get_delay(self):
        return self.__delay
    
    def get_day_div(self):
        return self.__day_div
    
    def get_step(self):
        return self.__step
    
    def get_eta(self):
        return self.__eta
    
    def get_time_line(self):
        return self.__time_line
    
    def get_time(self):
        return self.__time_line[-1]
    
    def get_current_time_int(self):
        return self.__current_time_int
    
    def get_lambda_eff(self):
        return self.__lambda_eff
    
    def get_lambda_arr(self):
        return self.__lambda_arr
    
    def get_exp_in(self):
        return self.__exp_in[:self.__current_time_int + 1]
    
    def get_sym_in(self):
        return self.__sym_in[:self.__current_time_int + 1]
    
    def get_sv(self):
        return self.__sv[:self.__current_time_int + 1]
    
    def get_exp(self):
        return self.__exp[:self.__current_time_int + 1]
    
    def get_sym(self):
        return self.__sym[:self.__current_time_int + 1]
    
    def get_r(self):
        return self.__r[:self.__current_time_int + 1]
    
    def get_c(self):
        return self.__c[:self.__current_time_int + 1]
    
    def get_d(self):
        return self.__d[:self.__current_time_int + 1]
    
    def get_y(self):
        return self.__y[:self.__current_time_int + 1]
    
    def get_p(self):
        return self.__p[:self.__current_time_int + 1]
    
    def get_s(self):
        return self.__s[:self.__current_time_int + 1]
    
    def get_v(self):
        return self.__sv[:self.__current_time_int + 1] - self.__s[:self.__current_time_int + 1] + self.__u[:self.__current_time_int + 1]
    
    def get_exp_in_tot(self):
        return self.__exp_in_tot[:self.__current_time_int + 1]
    
    def get_sym_in_tot(self):
        return self.__sym_in_tot[:self.__current_time_int + 1]
    
    def get_sv_tot(self):
        return self.__sv_tot[:self.__current_time_int + 1]
    
    def get_exp_tot(self):
        return self.__exp_tot[:self.__current_time_int + 1]
    
    def get_sym_tot(self):
        return self.__sym_tot[:self.__current_time_int + 1]
    
    def get_r_tot(self):
        return self.__r_tot[:self.__current_time_int + 1]
    
    def get_c_tot(self):
        return self.__c_tot[:self.__current_time_int + 1]
    
    def get_d_tot(self):
        return self.__d_tot[:self.__current_time_int + 1]
    
    def get_y_tot(self):
        return self.__y_tot[:self.__current_time_int + 1]
    
    def get_p_tot(self):
        return self.__p_tot[:self.__current_time_int + 1]
    
    def get_s_tot(self):
        return self.__s_tot[:self.__current_time_int + 1]
    
    def get_v_tot(self):
        return self.__sv_tot[:self.__current_time_int + 1] - self.__s_tot[:self.__current_time_int + 1] + self.__u_tot[:self.__current_time_int + 1]
    
    def get_x_tot(self, target):
        if target == 'exp_in':
            return self.get_exp_in_tot()
        elif target == 'sym_in':
            return self.get_sym_in_tot()
        elif target == 's':
            return self.get_s_tot()
        elif target == 'exp':
            return self.get_exp_tot()
        elif target == 'sym':
            return self.get_sym_tot()
        elif target == 'r':
            return self.get_r_tot()
        elif target == 'c':
            return self.get_c_tot()
        elif target == 'd':
            return self.get_d_tot()
        elif target == 'y':
            return self.get_y_tot()
        elif target == 'p':
            return self.get_p_tot()
        elif target == 'v':
            return self.get_v_tot()
        else:
            return None
        
    def getc_x(self, target):
        if target == 'exp_in':
            return self.getc_exp_in()
        elif target == 'sym_in':
            return self.getc_sym_in()
        elif target == 's':
            return self.getc_s()
        elif target == 'exp':
            return self.getc_exp()
        elif target == 'sym':
            return self.getc_sym()
        elif target == 'r':
            return self.getc_r()
        elif target == 'c':
            return self.getc_c()
        elif target == 'd':
            return self.getc_d()
        elif target == 'y':
            return self.getc_y()
        elif target == 'p':
            return self.getc_p()
        elif target == 'v':
            return self.getc_v()
        else:
            return None
         
    def __getx_x(self, target, pos):
        if target == 'exp_in':
            return self.__exp_in[pos]
        elif target == 'sym_in':
            return self.__sym_in[pos]
        elif target == 's':
            return self.__s[pos]
        elif target == 'exp':
            return self.__exp[pos]
        elif target == 'sym':
            return self.__sym[pos]
        elif target == 'r':
            return self.__r[pos]
        elif target == 'c':
            return self.__c[pos]
        elif target == 'd':
            return self.__d[pos]
        elif target == 'y':
            return self.__y[pos]
        elif target == 'p':
            return self.__p[pos]
        elif target == 'v':
            return self.__sv[pos] - self.__s[pos] + self.__u[pos]
        else:
            return None
    
    def getc_exp_in(self):
        return self.__exp_in[self.__current_time_int]
    
    def getc_sym_in(self):
        return self.__sym_in[self.__current_time_int]
    
    def getc_sv(self):
        return self.__sv[self.__current_time_int]
    
    def getc_exp(self):
        return self.__exp[self.__current_time_int]
    
    def getc_sym(self):
        return self.__sym[self.__current_time_int]
    
    def getc_r(self):
        return self.__r[self.__current_time_int]
    
    def getc_c(self):
        return self.__c[self.__current_time_int]
    
    def getc_d(self):
        return self.__d[self.__current_time_int]
    
    def getc_y(self):
        return self.__y[self.__current_time_int]
    
    def getc_p(self):
        return self.__p[self.__current_time_int]
    
    def getc_s(self):
        return self.__s[self.__current_time_int]
    
    def getc_v(self):
        return self.__sv[self.__current_time_int] - self.__s[self.__current_time_int] + self.__u[self.__current_time_int]
    
    
    def getc_exp_in_tot(self):
        return self.__exp_in_tot[self.__current_time_int]
    
    def getc_sym_in_tot(self):
        return self.__sym_in_tot[self.__current_time_int]
    
    def getc_sv_tot(self):
        return self.__sv_tot[self.__current_time_int]
    
    def getc_exp_tot(self):
        return self.__exp_tot[self.__current_time_int]
    
    def getc_sym_tot(self):
        return self.__sym_tot[self.__current_time_int]
    
    def getc_r_tot(self):
        return self.__r_tot[self.__current_time_int]
    
    def getc_c_tot(self):
        return self.__c_tot[self.__current_time_int]
    
    def getc_d_tot(self):
        return self.__d_tot[self.__current_time_int]
    
    def getc_y_tot(self):
        return self.__y_tot[self.__current_time_int]
    
    def getc_p_tot(self):
        return self.__p_tot[self.__current_time_int]
    
    def getc_s_tot(self):
        return self.__s_tot[self.__current_time_int]
    
    def getc_v_tot(self):
        return self.__sv_tot[self.__current_time_int] - self.__s_tot[self.__current_time_int] + self.__u_tot[self.__current_time_int]
    
    def getc_x_tot(self, target):
        if target == 'exp_in':
            return self.getc_exp_in_tot()
        elif target == 'sym_in':
            return self.getc_sym_in_tot()
        elif target == 's':
            return self.getc_s_tot()
        elif target == 'exp':
            return self.getc_exp_tot()
        elif target == 'sym':
            return self.getc_sym_tot()
        elif target == 'r':
            return self.getc_r_tot()
        elif target == 'c':
            return self.getc_c_tot()
        elif target == 'd':
            return self.getc_d_tot()
        elif target == 'y':
            return self.getc_y_tot()
        elif target == 'p':
            return self.getc_p_tot()
        elif target == 'v':
            return self.getc_v_tot()
        else:
            return None


        
        
        
        
        
        
        
        
    
    
    
    