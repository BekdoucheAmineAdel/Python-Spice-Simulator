#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 10:40:18 2023

@author: bekdouche
"""

import sympy
from numpy import logspace
import matplotlib as plt

def Simulate(output, simulation_type, scales, var_values, freq_range = None, timespan = None):
    plots = {}
    if simulation_type == "Bode":
        for i in range(len(scales)):
            
            plots[scale[i]] = output[scale].subs(var_values[i])
            
    return plots

def plot(plots):
    for scale in plots:
        plt.figure()
        plt.plot(plots[scale])
        plt.title(scale)
        
s = sympy.Symbol('s')
l = 5*s

sympy.plot(l)