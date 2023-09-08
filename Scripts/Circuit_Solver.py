#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 10:39:26 2023

@author: bekdouche
"""

from sympy import Symbol, ImmutableSparseMatrix, parsing

s = Symbol('s')

def Get_CS(l,item):
    for i in l:
        if item == i[0]+i[1] :
            return i
    raise ValueError("The list doesn't contain the desired item please check your input")



def Convert_value(value):
    if value[0] == '=':
        output = parsing.parse_expr(value[1:], evaluate = False)
    else:
        try:
            output = float(value)
        except ValueError:
            output = Symbol(value)
    return output

def Solve(network, N, nodes):
    
    # 
    LHS = []
    LHS_row = []
    LHS_col = []
    RHS = []
    RHS_indices = []
    current_names = [] 
    
    # 
    for component in network:
        component_type = component[0]

        if component_type == 'R':
            
            N1 = nodes[component[2]]
            N2 = nodes[component[3]]
            value = Convert_value(component[4])

            if (N1 == 0) or (N2 == 0): # if grounded...
                # diagonal term
                LHS.append(1.0 / value)
                LHS_row.append(max([N1, N2]) - 1)
                LHS_col.append(max([N1, N2]) - 1)

            else:                      # if not grounded...
                # N- N- term
                LHS.append(1.0 / value)
                LHS_row.append(N1 - 1)
                LHS_col.append(N1 - 1)

                # N+ N+ term
                LHS.append(1.0 / value)
                LHS_row.append(N2 - 1)
                LHS_col.append(N2 - 1)

                # N+ N- term
                LHS.append(-1.0 / value)
                LHS_row.append(N1 - 1)
                LHS_col.append(N2 - 1)

                # N- N+ term
                LHS.append(-1.0 / value)
                LHS_row.append(N2 - 1)
                LHS_col.append(N1 - 1)
                
        elif component_type == 'C':
            
            N1 = nodes[component[2]]
            N2 = nodes[component[3]]
            value = Convert_value(component[4])*s

            if (N1 == 0) or (N2 == 0): # if grounded...
                # diagonal term
                LHS.append(value)
                LHS_row.append(max([N1, N2]) - 1)
                LHS_col.append(max([N1, N2]) - 1)

            else:                      # if not grounded...
                # N- N- term
                LHS.append(value)
                LHS_row.append(N1 - 1)
                LHS_col.append(N1 - 1)

                # N+ N+ term
                LHS.append(value)
                LHS_row.append(N2 - 1)
                LHS_col.append(N2 - 1)

                # N+ N- term
                LHS.append(-value)
                LHS_row.append(N1 - 1)
                LHS_col.append(N2 - 1)

                # N- N+ term
                LHS.append(-value)
                LHS_row.append(N2 - 1)
                LHS_col.append(N1 - 1)
        
        if component_type == 'L':
            
            N1 = nodes[component[2]]
            N2 = nodes[component[3]]
            value = Convert_value(component[4])*s

            if (N1 == 0) or (N2 == 0): # if grounded...
                # diagonal term
                LHS.append(1.0 / value)
                LHS_row.append(max([N1, N2]) - 1)
                LHS_col.append(max([N1, N2]) - 1)
            else:                      # if not grounded...
                # N- N- term
                LHS.append(1.0 / value)
                LHS_row.append(N1 - 1)
                LHS_col.append(N1 - 1)

                # N+ N+ term
                LHS.append(1.0 / value)
                LHS_row.append(N2 - 1)
                LHS_col.append(N2 - 1)

                # N+ N- term
                LHS.append(-1.0 / value)
                LHS_row.append(N1 - 1)
                LHS_col.append(N2 - 1)

                # N- N+ term
                LHS.append(-1.0 / value)
                LHS_row.append(N2 - 1)
                LHS_col.append(N1 - 1)
                
                
        elif component_type == 'I':
            
            N1 = nodes[component[2]]
            N2 = nodes[component[3]]
            value = Convert_value(component[4])

            if (N1 == 0) or (N2 == 0): # if grounded...
                # diagonal term
                RHS.append(value)
                RHS_indices.append(max([N1, N2]) - 1)

            else:                      # if not grounded...
                # N- term
                RHS.append(value)
                RHS_indices.append(N1 - 1)

                # N+ term
                RHS.append(value)
                RHS_indices.append(N2 - 1)
        
        elif component_type == 'V':
            
            N1 = nodes[component[2]]
            N2 = nodes[component[3]]
            value = Convert_value(component[4])
            K = len(network)+component[5]
            RHS.append(value)
            RHS_indices.append(K - 1)
            current_names.append('V_'+component[1])
            
            if N1 == 0: # if N+ grounded...
                LHS.append(-1.0)
                LHS_row.append(N2 - 1)
                LHS_col.append(K-1)
                LHS.append(-1.0)
                LHS_row.append(K-1)
                LHS_col.append(N2 - 1)
            elif N2 == 0: # if N- grounded...
                LHS.append(1.0)
                LHS_row.append(N1 - 1)
                LHS_col.append(K-1)
                LHS.append(1.0)
                LHS_row.append(K-1)
                LHS_col.append(N1 - 1)
            else:                      # if not grounded...
                # N- K term
                LHS.append(-1.0)
                LHS_row.append(N2 - 1)
                LHS_col.append(K-1)

                # N+ K term
                LHS.append(1.0)
                LHS_row.append(N1 - 1)
                LHS_col.append(K-1)

                # K N- term
                LHS.append(-1.0)
                LHS_row.append(K-1)
                LHS_col.append(N2 - 1)

                # K N+ term
                LHS.append(1.0)
                LHS_row.append(K-1)
                LHS_col.append(N1 - 1)
        
        elif component_type == 'E':
            
            N1 = nodes[component[2]]
            N2 = nodes[component[3]]
            NC1 = nodes[component[4]]
            NC2 = nodes[component[5]]
            value = Convert_value(component[6])
            K = len(network)+component[7]
            current_names.append('E_'+component[1])
            
            if N1 == 0: # if N+ grounded...
                LHS.append(-1.0)
                LHS_row.append(N2 - 1)
                LHS_col.append(K-1)
                LHS.append(-1.0)
                LHS_row.append(K-1)
                LHS_col.append(N2 - 1)
            elif N2 == 0: # if N- grounded...
                LHS.append(1.0)
                LHS_row.append(N1 - 1)
                LHS_col.append(K-1)
                LHS.append(1.0)
                LHS_row.append(K-1)
                LHS_col.append(N1 - 1)
            else:                      # if not grounded...
                # N- K term
                LHS.append(-1.0)
                LHS_row.append(N2 - 1)
                LHS_col.append(K-1)

                # N+ K term
                LHS.append(1.0)
                LHS_row.append(N1 - 1)
                LHS_col.append(K - 1)

                # K N- term
                LHS.append(-1.0)
                LHS_row.append(K - 1)
                LHS_col.append(N2 - 1)

                # K N+ term
                LHS.append(1.0)
                LHS_row.append(K - 1)
                LHS_col.append(N1 - 1)
                
            if NC1 == 0: # if NC+ grounded...
                LHS.append(value)
                LHS_row.append(K - 1)
                LHS_col.append(NC2 - 1)
            elif NC2 == 0: # if N2 grounded...
                LHS.append(-value)
                LHS_row.append(K - 1)
                LHS_col.append(NC1 - 1)
            else:         # if not grounded...
                # K NC- term
                LHS.append(value)
                LHS_row.append(K - 1)
                LHS_col.append(N2 - 1)

                # K NC+ term
                LHS.append(-value)
                LHS_row.append(K - 1)
                LHS_col.append(N1 - 1)
                
        elif component_type == 'G':
            
            N1 = nodes[component[2]]
            N2 = nodes[component[3]]
            NC1 = nodes[component[4]]
            NC2 = nodes[component[5]]
            value = Convert_value(component[6])
            
            if (N1 != 0) & (NC1 != 0):
                LHS.append(value)
                LHS_row.append(N1 - 1)
                LHS_col.append(NC1 - 1)
            if (N2 != 0) & (NC2 != 0):
                LHS.append(value)
                LHS_row.append(N2 - 1)
                LHS_col.append(NC2 - 1)
            if (N1 != 0) & (NC2 != 0):
                LHS.append(-value)
                LHS_row.append(N1 - 1)
                LHS_col.append(NC2 - 1)
            if (N2 != 0) & (NC1 != 0):
                LHS.append(-value)
                LHS_row.append(N2 - 1)
                LHS_col.append(NC1 - 1)
                
        elif component_type == 'F':
                    
            N1 = nodes[component[2]]
            N2 = nodes[component[3]]
            ctrlName = component[4]
            value = Convert_value(component[5])
            vCtrl = Get_CS(network, ctrlName)
            K = len(network)+vCtrl[-1]
            
            if N1 == 0: # if NC+ grounded...
                LHS.append(-value)
                LHS_row.append(N2 - 1)
                LHS_col.append(K - 1)
            elif N2 == 0: # if N2 grounded...
                LHS.append(value)
                LHS_row.append(N1 - 1)
                LHS_col.append(K - 1)
            else:         # if not grounded...
                # N- K term
                LHS.append(-value)
                LHS_row.append(N2 - 1)
                LHS_col.append(K - 1)
            
                # N+ K term
                LHS.append(value)
                LHS_row.append(N1 - 1)
                LHS_col.append(K - 1)
        elif component_type == 'H':
                    
            N1 = nodes[component[2]]
            N2 = nodes[component[3]]
            ctrlName = component[4]
            value = Convert_value(component[5])
            H = len(network)+component[6]
            vCtrl = Get_CS(network, ctrlName)
            K = len(network)+vCtrl[-1]
            
            LHS.append(-value)
            LHS_row.append(H - 1)
            LHS_col.append(K - 1)
            
            if N1 == 0: # if NC+ grounded...
                LHS.append(-1)
                LHS_row.append(N2 - 1)
                LHS_col.append(H - 1)
                LHS.append(-1)
                LHS_row.append(H - 1)
                LHS_col.append(N2 - 1)
            elif N2 == 0: # if N2 grounded...
                LHS.append(1)
                LHS_row.append(N1 - 1)
                LHS_col.append(K - 1)
                LHS.append(1)
                LHS_row.append(H - 1)
                LHS_col.append(N1 - 1)
            else:         # if not grounded...
                # N- H term
                LHS.append(-1)
                LHS_row.append(N2 - 1)
                LHS_col.append(K - 1)
                # H N-
                LHS.append(-1)
                LHS_row.append(H - 1)
                LHS_col.append(N2 - 1)
                # N+ H term
                LHS.append(1)
                LHS_row.append(N1 - 1)
                LHS_col.append(K - 1)
                # H N+ term
                LHS.append(1)
                LHS_row.append(H - 1)
                LHS_col.append(N1 - 1)
    

    LHS_dict = {}
    for i in range(len(LHS)):
        try:
            LHS_dict[(LHS_row[i],LHS_col[i])] += LHS[i]
        except KeyError:
            LHS_dict[(LHS_row[i],LHS_col[i])] = LHS[i]
    
    RHS_dict = {}
    for i in range(len(RHS)):
        try:
            RHS_dict[(RHS_indices[i],0)] += RHS[i]
        except KeyError:
            RHS_dict[(RHS_indices[i],0)] = RHS[i]
    
    # print('RHS_dict:\n',RHS_dict)
    # print('RHS_dict:\n',RHS_dict)
    
    LHS_sparse = ImmutableSparseMatrix(N, N, LHS_dict)
    RHS_sparse = ImmutableSparseMatrix(N, 1, RHS_dict)
      
    # print('LHS:\n',LHS_sparse)
    # print('RHS:\n',RHS_sparse)
    
    solution = LHS_sparse.LUsolve(RHS_sparse)
    
    output = {}
    user_nodes = []
   
    for node in nodes:
        if node != 'gnd' and node != '0': 
            user_nodes.append(node)
    
    for i in range(len(user_nodes)+len(current_names)):
        try:
            output['V_'+user_nodes[i]] = solution[i]
        except:
            output['I_'+current_names[i-len(user_nodes)]] = solution[i]
    return output
