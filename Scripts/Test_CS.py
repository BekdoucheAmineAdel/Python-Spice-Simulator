#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 11:51:18 2023

@author: bekdouche
"""

from Netlist_Reader import Read
import Circuit_Solver

network, N, nodes = Read('/home/bekdouche/Projects/Programming/Spice Simulator/Scripts/filter.netlist')

output = Circuit_Solver.Solve(network, N, nodes)

print(output)