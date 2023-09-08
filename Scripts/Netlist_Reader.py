#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 10:06:31 2023

@author: bekdouche
"""


def Read(netlist):
    """
    

    Parameters
    ----------
    netlist : a file containing the description of the netlist (file_name.netlist)

    Returns
    -------
    Network : List of component, their postion in the circuit and crucial informations about them

    """
    
    # check if the file is of type netlist
    file_type = netlist.split('.')[1]
    if file_type != 'netlist':
        raise ValueError('File must be of type netlist make sure that you have changed the extension of your file to .netlist')
    
    # open the file and start the reading process
    f = open(netlist)
    
    nodes = {}
    nodes_counter = 1
    nodes_temporary_list = []
    
    network = []    
    N = 0 #Dimension
    for line in f:
        data = line.split()
        component_description = []
        
        
        component_type =   data[0][0].upper()
        component_id   =   data[0][1:].upper()
        component_Np   =   data[1]
        component_Nm   =   data[2]
        component_description.extend((component_type, component_id, component_Np, component_Nm))
        nodes_temporary_list.extend((component_Np, component_Nm))
        
        
        if len(data) == 4:
            component_value   =   data[3]
            component_description.append(component_value)
            
        elif len(data) == 5:
            component_controller   =   data[3]
            component_value        =   data[4]
            component_description.extend((component_controller, component_value))
            
        elif len(data) == 6:
            component_NCp    =   data[3]
            component_NCm    =   data[4]
            component_value  =   data[5]
            component_description.extend((component_NCp, component_NCm, component_controller, component_value))
            nodes_temporary_list.extend((component_NCp, component_NCm))
        
        
        if data[0][0] in ('H'):
            component_description.append(N)# H
            N += 1
            
        if data[0][0] in ('V','E'):
            component_description.append(N)# K
            N += 1
        # Componet = (type, id, N+, N-, NC+(not always), NC-(not always), Vname(not always), value, H(not always), K(not always))
        network.append(component_description)
    
    N += len(network)-1 # Dimension
    
    # Converts nodes into numerical reference
    for node in nodes_temporary_list:
        if node not in nodes.keys():
            if node.lower() == 'gnd' or node == '0':
                nodes[node] = 0
            else:
                nodes[node] = nodes_counter
                nodes_counter += 1
                
    return network, N, nodes
