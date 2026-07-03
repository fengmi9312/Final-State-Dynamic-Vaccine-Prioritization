# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 13:46:14 2022

@author: 20481756
"""


import numpy as np
from scipy.optimize import minimize, LinearConstraint, Bounds
from . import func
from copy import deepcopy

class sir_delta:
    
    def __init__(self, i0, populations, contacts, k,
                 srv_inf, srv_rem,
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
        if srv_inf[0] != 1 or srv_rem[0] != 1: print('srv error!')
        self.__actl_inf_len = np.where(srv_inf <= 0)[0][0] if np.any(srv_inf <= 0) else len(srv_inf)
        self.__actl_rem_len = np.where(srv_rem <= 0)[0][0] if np.any(srv_rem <= 0) else len(srv_rem)
        self.__cum_len = min(self.__actl_inf_len - 1, self.__actl_rem_len)
        self.__haz_inf = 1 - srv_inf[1:self.__actl_inf_len] / srv_inf[:self.__actl_inf_len - 1]
        self.__srv_rem = deepcopy(srv_rem[:self.__actl_rem_len])
        self.__haz_cum = self.__haz_inf[:self.__cum_len] * self.__srv_rem[:self.__cum_len]
        self.__inf_m = 1 / (np.diff(1 - srv_inf) * np.arange(len(srv_inf) - 1) * step).sum()
        self.__rem_m = 1 / (np.diff(1 - srv_rem) * np.arange(len(srv_rem) - 1) * step).sum()
        
        
        
        self.__delay = deepcopy(delay)
        self.__eta = deepcopy(eta)
        
        self.__totmat = self.__contacts * self.__populations[None, :] * self.__k  
        self.__step = deepcopy(step)
        self.__time0 = deepcopy(time)
        self.__period_len = deepcopy(period_len)
        self.__lambda_eff = np.log(1 / (1 - self.__haz_cum).prod())
        self.__lambda_arr = np.log(1 / np.array([(1 - self.__haz_cum[i:] / self.__srv_rem[i]).prod() for i in range(self.__cum_len)]))
        self.return_to_init()
        
    def return_to_init(self):
        self.__time_line = [self.__time0,]
        self.__current_time_int = 0
        self.__time_int = 0
        
        self.__sv = np.zeros((self.__period_len, self.__group_amount))
        self.__i_in = np.zeros((self.__period_len, self.__group_amount))
        self.__i = np.zeros((self.__period_len, self.__group_amount))
        self.__r = np.zeros((self.__period_len, self.__group_amount))
        self.__c = np.zeros((self.__period_len, self.__group_amount))
        self.__d = np.zeros((self.__period_len, self.__group_amount))
        self.__y = np.zeros((self.__period_len, self.__group_amount))
        self.__p = np.zeros((self.__period_len, self.__group_amount))
        self.__u = np.zeros((self.__period_len, self.__group_amount))
        self.__s = np.zeros((self.__period_len, self.__group_amount))
        
        self.__sv_tot = np.zeros(self.__period_len)
        self.__i_in_tot = np.zeros(self.__period_len)
        self.__i_tot = np.zeros(self.__period_len)
        self.__r_tot = np.zeros(self.__period_len)
        self.__c_tot = np.zeros(self.__period_len)
        self.__d_tot = np.zeros(self.__period_len)
        self.__y_tot = np.zeros(self.__period_len)
        self.__p_tot = np.zeros(self.__period_len)
        self.__u_tot = np.zeros(self.__period_len)
        self.__s_tot = np.zeros(self.__period_len)
        
        self.__sv[0] = 1 - self.__i0
        self.__i_in[0] = self.__i0
        self.__i[0] = self.__i0
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
        self.__i_in = np.append(self.__i_in, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        self.__i = np.append(self.__i, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        self.__r = np.append(self.__r, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        self.__c = np.append(self.__c, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        self.__d = np.append(self.__d, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        self.__y = np.append(self.__y, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        self.__u = np.append(self.__u, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        self.__p = np.append(self.__p, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        self.__s = np.append(self.__s, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        
        self.__j = np.append(self.__j, np.zeros((self.__period_len, self.__group_amount)), axis = 0)
        
        self.__sv_tot = np.append(self.__sv_tot, np.zeros(self.__period_len))
        self.__i_in_tot = np.append(self.__i_in_tot, np.zeros(self.__period_len))
        self.__i_tot = np.append(self.__i_tot, np.zeros(self.__period_len))
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
        actl_len = self.__cum_len
        return func.mulf(self.__totmat, self.__haz_cum[:func.get_tail(self.__time_int, actl_len)] \
            @ self.__i_in[self.__time_int:func.get_head(self.__time_int, actl_len):-1])
       
    
    def __calc_tot(self):
        self.__i_in_tot[self.__time_int] = self.__i_in[self.__time_int] @ self.__populations
        self.__sv_tot[self.__time_int] = self.__sv[self.__time_int] @ self.__populations
        self.__i_tot[self.__time_int] = self.__i[self.__time_int] @ self.__populations
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
        
    def add_time_course_vaccination(self, vac_alloc = None, vac_dur = 1, vac_gap = 1):
        remaining_vac = 0
        for i in range(vac_dur):
            remaining_vac += self.add_vaccination(vac_alloc / vac_dur)
            for j in range(vac_gap):
                self.spread_once()
        return remaining_vac
                
                
#here    
    def spread_once(self):
        if self.__time_int == self.__current_len - 1: self.__expand_len()
        actl_len = self.__actl_rem_len
        sv_out_tmp = self.__sv[self.__time_int] * self.__j[self.__time_int]
        u_out_tmp = self.__u[self.__time_int] * self.__j[self.__time_int]
        i_in_tmp = sv_out_tmp + u_out_tmp
        self.__i_in[self.__time_int + 1] = i_in_tmp
        self.__c[self.__time_int + 1] = self.__c[self.__time_int] + i_in_tmp
        self.__sv[self.__time_int + 1] = self.__sv[self.__time_int] - sv_out_tmp
        self.__u[self.__time_int + 1] = self.__u[self.__time_int] - u_out_tmp
        self.__i[self.__time_int + 1] = self.__srv_rem[:func.get_tail(self.__time_int + 1,actl_len)] @ self.__i_in[self.__time_int + 1:func.get_head(self.__time_int + 1,actl_len):-1]
        self.__r[self.__time_int + 1] = self.__c[self.__time_int + 1] - self.__i[self.__time_int + 1]
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
    def calc_trans_grad(self, vac_alloc):
        if self.__time_int < self.__delay:
            return None
        return np.diag((- self.__get_eff() * self.__eta) * self.__j[self.__time_int])
    
    def calc_trans_grad_target(self, target = 'c', **kwargs):
        if target == 'c':
            return self.calc_trans_grad(**kwargs) @ self.__populations
        elif target == 'd':
            return self.calc_trans_grad(**kwargs) @ (self.__populations * self.__ifrs)
        elif target == 'y':
            return self.calc_trans_grad(**kwargs) @ (self.__populations * self.__ifrs * self.__ylls)
        else:
            return None
    
    def calc_steady_grad(self, vac_alloc, non_mar_prdt = True, gtol = 1e-6):
        _vac_alloc = np.minimum(vac_alloc, self.__s[self.__current_time_int]) * self.__eta * self.__get_eff()
        lams = self.calc_lams(non_mar_prdt = non_mar_prdt)
        pos = self.__time_int
        rt= self.__r[pos]
        svu_tmp = self.__sv[pos] + self.__u[pos] - _vac_alloc
        totmat_tmp = self.__contacts * self.__populations[None, :] * self.__k  
        lam, mem_eff = lams['lambda_eff'], lams['memory_eff']
        c_arr = self.calc_vac_prdt(vac_alloc, prdt_type = 'steady' if non_mar_prdt else 'mar')
        c_grad_tmp = np.ones([self.__group_amount, self.__group_amount])
        while True:
            c_grad = - np.eye(self.__group_amount) \
            + np.eye(self.__group_amount) * np.exp(- totmat_tmp@(lam*(c_arr - rt) + mem_eff))[:,None] \
            + (totmat_tmp * (svu_tmp * lam * np.exp(- totmat_tmp@(lam*(c_arr - rt) + mem_eff)))[:,None]) @ c_grad_tmp
            if np.all(abs(c_grad-c_grad_tmp) <= abs(c_grad_tmp) * (np.ones([self.__group_amount, self.__group_amount])*gtol)): break
            else: c_grad_tmp = c_grad
        return c_grad * (self.__eta * self.__get_eff())[None, :]
        
    
    def calc_vac_prdt_grad_dis(self, vac_alloc, step = 0.001):
        prdt = self.calc_vac_prdt(vac_alloc)
        return np.array([(self.calc_vac_prdt(vac_alloc + np.eye(self.__group_amount)[i] * step) - prdt) / step for i in range(self.__group_amount)]).T
    
    
    def calc_steady_grad_target(self, target = 'c', **kwargs):
        if target == 'c':
            return self.__populations @ self.calc_steady_grad(**kwargs)
        elif target == 'd':
            return (self.__populations * self.__ifrs) @ self.calc_steady_grad(**kwargs)
        elif target == 'y':
            return (self.__populations * self.__ifrs * self.__ylls) @ self.calc_steady_grad(**kwargs)
        else:
            return None
        
    def calc_reduction_eff_target(self, target = 'c', vac_avail = None):
        if vac_avail is None or vac_avail == 0:
            zero_alloc = np.zeros(self.__group_amount)
            grad = self.calc_steady_grad_target(target = target, vac_alloc = zero_alloc, non_mar_prdt = True)
            # norm_pop = self.__populations / np.linalg.norm(self.__populations)
            # return - (grad - grad @ norm_pop * norm_pop) / self.__populations
            return - grad / self.__populations
        else:
            return - (np.array([self.calc_vac_prdt_target(np.eye(1, self.__group_amount, i)[0] * min(1, vac_avail / self.__populations[i]), target = target) for i in range(self.__group_amount)]) - self.calc_vac_prdt_target(vac_alloc = np.zeros(self.__group_amount), target = target)) / vac_avail
        
        
        
        
    
    def optimize_continual_vac_alloc(self, vac_avail, target = 'c', prdt_type = 'steady'):
        zero_alloc = np.zeros(self.__group_amount)
        if prdt_type == 'steady': grad = self.calc_steady_grad_target(target = target, vac_alloc = zero_alloc, non_mar_prdt = True)
        elif prdt_type == 'trans': grad = self.calc_trans_grad_target(target = target, vac_alloc = zero_alloc)
        elif prdt_type == 'mar': grad = self.calc_steady_grad_target(target = target, vac_alloc = zero_alloc, non_mar_prdt = None)
        else: grad = None
        dir_grad = - grad / self.__populations
        return self.order_alloc(vac_avail, func.order_index(dir_grad))[0]

    def calc_lams(self, delay_prdt = True, non_mar_prdt = True):
        if not non_mar_prdt: return {'lambda_eff': self.__inf_m / self.__rem_m, 'memory_eff': 0}
        res = {'lambda_eff': None, 'memory_eff': None}
        cum_len = self.__cum_len
        pos = self.__time_int if delay_prdt else self.__current_time_int
        res["lambda_eff"] = self.__lambda_eff
        res["memory_eff"] = (self.__lambda_arr[:func.get_tail(pos, cum_len)][:,None] * (self.__i_in[pos:func.get_head(pos, cum_len):-1] * self.__srv_rem[:func.get_tail(pos, cum_len)][:,None])).sum(axis = 0) - res["lambda_eff"] * self.__i[pos]
        return res
    
    def calc_prdt(self, prdt_type = 'steady', delay_prdt = True, ctol = 1e-10, trans_delay = 0, init_c = None):
        if prdt_type == 'steady' or prdt_type == 'mar':
            lams = self.calc_lams(delay_prdt = delay_prdt, non_mar_prdt = (prdt_type == 'steady'))
            pos = self.__time_int if delay_prdt else self.__current_time_int
            rt= self.__r[pos]
            c_tmp = self.__c[pos] if init_c is None else init_c
            tot_tmp = 1 - self.__p[pos]
            svu_tmp = self.__sv[pos] + self.__u[pos]
            lam, mem_eff = lams['lambda_eff'], lams['memory_eff']
            while True:
                c_trans_arr = tot_tmp - svu_tmp * np.exp(-self.__totmat@(lam*(c_tmp - rt) + mem_eff))
                if np.all(abs(c_trans_arr-c_tmp) <= abs(c_tmp) * (np.ones(self.__group_amount)*ctol)): break
                else: c_tmp = c_trans_arr
            return c_trans_arr 
        elif prdt_type == 'trans':
            c_time_int = self.get_current_time_int()
            for i in range(trans_delay): self.spread_once()
            c_arr = self.__c[self.__time_int]
            self.return_back(c_time_int)
            return c_arr
        else: return None

    def calc_vac_prdt(self, vac_alloc, prdt_type = 'steady', ctol = 1e-10, trans_delay = 0, init_c = None):
        if prdt_type == 'steady' or prdt_type == 'mar':
            _vac_alloc = np.minimum(vac_alloc, self.__s[self.__current_time_int]) * self.__eta * self.__get_eff()
            lams = self.calc_lams(non_mar_prdt = (prdt_type == 'steady'))
            pos = self.__time_int
            c_tmp = self.__c[pos] if init_c is None else init_c
            rt= self.__r[pos]
            tot_tmp = 1 - self.__p[pos] - _vac_alloc
            svu_tmp = self.__sv[pos] + self.__u[pos] - _vac_alloc
            totmat_tmp = self.__contacts * self.__populations[None, :] * self.__k  
            lam, mem_eff = lams['lambda_eff'], lams['memory_eff']
            while True:
                c_trans_arr = tot_tmp - svu_tmp * np.exp(- totmat_tmp@(lam*(c_tmp - rt) + mem_eff))
                if np.all(abs(c_trans_arr-c_tmp) <= abs(c_tmp) * (np.ones(self.__group_amount)*ctol)): break
                else: c_tmp = c_trans_arr
            return c_trans_arr    
        elif prdt_type == 'trans':
            c_time_int = self.get_current_time_int()
            self.add_vaccination(vac_alloc)
            for i in range(trans_delay): self.spread_once()
            c_arr = self.__c[self.__time_int]
            self.return_back(c_time_int)
            return c_arr
        else: return None
        

    def calc_prdt_target(self, target = 'c', **kwargs):
        kwargs.pop('get_p', None)
        if target == 'c':
            return self.calc_prdt(**kwargs) @ self.__populations
        elif target == 'd':
            return self.calc_prdt(**kwargs) @ (self.__populations * self.__ifrs)
        elif target == 'y':
            return self.calc_prdt(**kwargs) @ (self.__populations * self.__ifrs * self.__ylls)
        else:
            return None
        
    def calc_vac_prdt_target(self, vac_alloc, target = 'c', **kwargs):
        kwargs.pop('get_p', None)
        if target == 'c':
            return self.calc_vac_prdt(vac_alloc, **kwargs) @ self.__populations
        elif target == 'd':
            return self.calc_vac_prdt(vac_alloc, **kwargs) @ (self.__populations * self.__ifrs)
        elif target == 'y':
            return self.calc_vac_prdt(vac_alloc, **kwargs) @ (self.__populations * self.__ifrs * self.__ylls)
        else:
            return None

    def optimize_vac_alloc(self, vac_avail, target = 'c', init_strategy = None, tol = 1e-16,
                           disp = True, get_prdt = False, minimize_kwargs = {}, **kwargs):
        if vac_avail <= 0 or self.__s_tot[self.__current_time_int] == 0:
            if get_prdt: return {'target': self.calc_vac_prdt_target(np.zeros(self.__group_amount), target = target), 
                    'alloc': np.zeros(self.__group_amount)}
            else: return np.zeros(self.__group_amount)
        elif vac_avail >= self.__s_tot[self.__current_time_int]:
            if get_prdt: return {'target': self.calc_vac_prdt_target(self.__s[self.__current_time_int], target = target), 
                    'alloc': self.__s[self.__current_time_int]}
            else: return self.__s[self.__current_time_int]
        else: pass
        np.random.seed(0)
        get_res = lambda vac_alloc: self.calc_vac_prdt_target(vac_alloc, target, **kwargs)
        linear_constraint = LinearConstraint(deepcopy(self.__populations), np.array([vac_avail]), np.array([vac_avail]))
        constraint = [linear_constraint,]
        bound = Bounds(np.zeros(self.__group_amount), deepcopy(self.__s[self.__current_time_int]))
        
        init_strategies = [init_strategy] if init_strategy is not None else []
        dgr_arr = self.__contacts.sum(axis = 1)
        dgr = vac_avail * dgr_arr / dgr_arr.sum()
        init_strategies.append(np.minimum(self.__s[self.__current_time_int],  dgr / self.__populations))
        if target == 'c': dgr_arr = np.ones(self.__group_amount)
        elif target == 'd': dgr_arr = self.__ifrs 
        elif target == 'y': dgr_arr = self.__ifrs * self.__ylls 
        dgr = vac_avail * dgr_arr / dgr_arr.sum()
        init_strategies.append(np.minimum(self.__s[self.__current_time_int],  dgr / self.__populations))
        res_list = []
        for basic_init_alloc in init_strategies:
            init_alloc = basic_init_alloc
            while True:
                res = minimize(get_res, init_alloc, method='SLSQP', jac = None,
                               constraints = constraint, bounds = bound, tol = tol,
                               options={'disp': False, 'maxiter':2000}, **minimize_kwargs)
                if res.success:
                    if disp: print('Successful Optimization!')
                    break
                else:
                    if disp: print('Unsuccessful Optimization, optimize again...')
                    init_alloc = np.random.rand() * basic_init_alloc
            res_list.append({'target': res.fun, 'alloc': res.x})
        min_index = min(range(len(res_list)), key=lambda i: res_list[i]['target'])
        if get_prdt: return res_list[min_index]
        else: return res_list[min_index]['alloc']
    
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
    
    def get_i_in(self):
        return self.__i_in[:self.__current_time_int + 1]
    
    def get_sv(self):
        return self.__sv[:self.__current_time_int + 1]
    
    def get_i(self):
        return self.__i[:self.__current_time_int + 1]
    
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
    
    def get_i_in_tot(self):
        return self.__i_in_tot[:self.__current_time_int + 1]
    
    def get_sv_tot(self):
        return self.__sv_tot[:self.__current_time_int + 1]
    
    def get_i_tot(self):
        return self.__i_tot[:self.__current_time_int + 1]
    
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
        if target == 'i_in':
            return self.get_i_in_tot()
        elif target == 's':
            return self.get_s_tot()
        elif target == 'i':
            return self.get_i_tot()
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
        if target == 'i_in':
            return self.getc_i_in()
        elif target == 's':
            return self.getc_s()
        elif target == 'i':
            return self.getc_i()
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
        if target == 'i_in':
            return self.__i_in[pos]
        elif target == 's':
            return self.__s[pos]
        elif target == 'i':
            return self.__i[pos]
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
    
    def getc_i_in(self):
        return self.__i_in[self.__current_time_int]
    
    def getc_sv(self):
        return self.__sv[self.__current_time_int]
    
    def getc_i(self):
        return self.__i[self.__current_time_int]
    
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
    
    
    def getc_i_in_tot(self):
        return self.__i_in_tot[self.__current_time_int]
    
    def getc_sv_tot(self):
        return self.__sv_tot[self.__current_time_int]
    
    def getc_i_tot(self):
        return self.__i_tot[self.__current_time_int]
    
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
        if target == 'i_in':
            return self.getc_i_in_tot()
        elif target == 's':
            return self.getc_s_tot()
        elif target == 'i':
            return self.getc_i_tot()
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



def get_steady_state(_k, _populations, _contacts, _lam, _i = 0, _r = 0, ctol = 1e-6):
    group_amount = len(_populations)
    if type(_lam) == np.ndarray:
        rlam = _lam[None, :]
    else:
        rlam = _lam
    
    c_tmp = np.ones(group_amount)
    _totmat_lam = _contacts * _populations[None, :] * _k * rlam
    while True:
        c_tmp_tmp = 1 - (1 - _r - _i) * np.exp(-_totmat_lam@(c_tmp  - _r))
        if np.all(abs(c_tmp_tmp-c_tmp) <= abs(c_tmp) * ctol):
            break
        else:
            c_tmp = c_tmp_tmp
    return c_tmp_tmp
        
        
def get_k_from_steady(_steady, _populations, _contacts, _lam, _i = 0, _r = 0, ctol = 1e-6, ktol = 1e-6):
    x0 = 1.0 / (_lam * np.linalg.eig(_contacts * _populations[None, :])[0].max())
    while True:
        res = func.binary_search(lambda x: get_steady_state(x, _populations, _contacts, _lam, _i, _r, ctol) @ _populations, _steady, x0, 2 * x0, lbound = 0, tol = ktol)
        if res['success']:
            return res['x']

        
        
        
        
        
        
        
        
        
        
    
    
    
    