#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 17:26:45 2023

@author: Bekdouche

@version: 
    
@Python Version:
    
@Numpy Version:

@Sympy Version:
    
@description: 

@how_to_use:
    Nodes have to be numbers
    Controllers have to be declared before the controlled source
"""

import sympy as sp

def CheckValue(s):
    """
    

    Parameters
    ----------
    x : string

    Returns
    -------
    number if x is a number
    symbolic variable if x is a variable

    """
    try:
        out = float(s)
    except ValueError:
        out = sp.Symbol(s)
    
    return out

def getCurrentID(l,Vname):
    for item in l:
        if item[0]+item[1] == Vname:
            return item[-1]
    raise ValueError(Vname + " was not found in the item list make sure its declared before the Current Controlled Sources")
    
def Bspice(netlist):
    ##################################################
    #        STAMPS & NETLIST CONFIGURATION          #
    ##################################################
    #   Resistor
    #       Rxxx N+ N- Rvalue
    #   Capacitor
    #       Cxxx N+ N- Cvalue
    #   Inductor
    #       Lxxx N+ N- Lvalue
    #   Current Source
    #       Ixxx N+ N- Ivalue
    #   Voltage Source
    #       Vxxx N+ N- Vvalue
    #   Voltage Controlled Current Source
    #       Gxxx N+ N- NC+ NC- Gvalue
    #   Voltage Controlled Voltage Source
    #       Exxx N+ N- NC+ NC- Evalue
    #   Current Controlled Current Source
    #       Fxxx N+ N- Vxxx Fvalue
    #       Vxxx NC+ NC- Vvalue
    #   Current Controlled Voltage Source
    #       Hxxx N+ N- Vxxx Hvalue
    #       Vxxx NC+ NC- Vvalue
    ##################################################
    #                NETLIST READING                 #
    ##################################################
    ##  to do
    """
        create a netlist reader
        which transforms the normale netlist string into
        an array of elements each element has everything 
        you need to know about it
    """
    p = sp.Symbol('p')
    elementsList = []
    nodes = {0}
    currentIntroduced = 0
    currentID = 0
    for component in netlist:
        temporaryElement = []
        info = component.split()
        componentType = info[0][0]
        temporaryElement.append(componentType)
        ########################################################
        #                         R                            #
        ########################################################
        if componentType == 'R':
            # ID
            temporaryElement.append(info[0][1:])
            # N+
            temporaryElement.append(int(info[1]))
            nodes.add(int(info[1]))
            # N-
            temporaryElement.append(int(info[2]))
            nodes.add(int(info[2]))
            # Value
            temporaryElement.append(CheckValue(info[3]))
        ########################################################
        #                         C                            #
        ########################################################
        elif componentType == 'C':
            # ID
            temporaryElement.append(info[0][1:])
            # N+
            temporaryElement.append(int(info[1]))
            nodes.add(int(info[1]))
            # N-
            temporaryElement.append(int(info[2]))
            nodes.add(int(info[2]))
            # Value
            temporaryElement.append(1/CheckValue(info[3])/p)
        ########################################################
        #                         L                            #
        ########################################################
        elif componentType == 'L':
            # ID
            temporaryElement.append(info[0][1:])
            # N+
            temporaryElement.append(int(info[1]))
            nodes.add(int(info[1]))
            # N-
            temporaryElement.append(int(info[2]))
            nodes.add(int(info[2]))
            # Value
            temporaryElement.append(CheckValue(info[3])*p)
        ########################################################
        #                         I                            #
        ########################################################
        elif componentType == 'I':
            # ID
            temporaryElement.append(info[0][1:])
            # N+
            temporaryElement.append(int(info[1]))
            nodes.add(int(info[1]))
            # N-
            temporaryElement.append(int(info[2]))
            nodes.add(int(info[2]))
            # Value
            temporaryElement.append(CheckValue(info[3]))
        ########################################################
        #                         V                            #
        ########################################################
        elif componentType == 'V':
            # ID
            temporaryElement.append(info[0][1:])
            # N+
            temporaryElement.append(int(info[1]))
            nodes.add(int(info[1]))
            # N-
            temporaryElement.append(int(info[2]))
            nodes.add(int(info[2]))
            # Value
            temporaryElement.append(CheckValue(info[3]))
            # Current ID
            currentID += 1
            temporaryElement.append(currentID)
            # Introduce the current in the matrix
            currentIntroduced += 1
        ########################################################
        #                       VCCS                           #
        ########################################################
        elif componentType == 'G':
            # ID
            temporaryElement.append(info[0][1:])
            # N+
            temporaryElement.append(int(info[1]))
            nodes.add(int(info[1]))
            # N-
            temporaryElement.append(int(info[2]))
            nodes.add(int(info[2]))
            # NC+
            temporaryElement.append(int(info[3]))
            nodes.add(int(info[3]))
            # NC-
            temporaryElement.append(int(info[4]))
            nodes.add(int(info[4]))
            # Value
            temporaryElement.append(CheckValue(info[5]))
        ########################################################
        #                       VCVS                           #
        ########################################################
        elif componentType == 'E':
            # ID
            temporaryElement.append(info[0][1:])
            # N+
            temporaryElement.append(int(info[1]))
            nodes.add(int(info[1]))
            # N-
            temporaryElement.append(int(info[2]))
            nodes.add(int(info[2]))
            # NC+
            temporaryElement.append(int(info[3]))
            nodes.add(int(info[3]))
            # NC-
            temporaryElement.append(int(info[4]))
            nodes.add(int(info[4]))
            # Value
            temporaryElement.append(CheckValue(info[5]))
            # Current ID
            currentID += 1
            temporaryElement.append(currentID)
            # Introduce the current in the matrix
            currentIntroduced += 1
        ########################################################
        #                       CCCS                           #
        ########################################################
        elif componentType == 'F':
            # ID
            temporaryElement.append(info[0][1:])
            # N+
            temporaryElement.append(int(info[1]))
            nodes.add(int(info[1]))
            # N-
            temporaryElement.append(int(info[2]))
            nodes.add(int(info[2]))
            # Vname
            temporaryElement.append(info[3])
            # Value
            temporaryElement.append(int(info[4]))
        ########################################################
        #                       CCVS                           #
        ########################################################
        elif componentType == 'H':
            # ID
            temporaryElement.append(info[0][1:])
            # N+
            temporaryElement.append(int(info[1]))
            nodes.add(int(info[1]))
            # N-
            temporaryElement.append(int(info[2]))
            nodes.add(int(info[2]))
            # Vname
            temporaryElement.append(info[3])
            # Value
            temporaryElement.append(int(info[4]))
            # Current ID
            currentID += 1
            temporaryElement.append(currentID)
            # Introduce the current in the matrix
            currentIntroduced += 1
        elementsList.append(temporaryElement)
    ##################################################
    #              Generating the matrixes           #
    ##################################################
    nodes.remove(0)
    N = len(nodes)+currentIntroduced
    Y = sp.zeros(N,N)
    I = sp.zeros(N,1)
    currentsName = []
    for element in elementsList:
        temporaryY = sp.zeros(N,N)
        temporaryI = sp.zeros(N,1)
        componentType = element[0]
        ########################################################
        #                         R                            #
        ########################################################
        if componentType == 'R':
            positiveNode = element[2]
            negativeNode = element[3]
            if negativeNode != 0:
                temporaryY[(negativeNode-1)*N+negativeNode-1]=1/element[-1]
            if positiveNode != 0:
                temporaryY[(positiveNode-1)*N+positiveNode-1]=1/element[-1]
        ########################################################
        #                         C                            #
        ########################################################
        elif componentType == 'C':
            positiveNode = element[2]
            negativeNode = element[3]
            if negativeNode != 0:
                temporaryY[(negativeNode-1)*N+negativeNode-1]=1/element[-1]
            if positiveNode != 0:
                temporaryY[(positiveNode-1)*N+positiveNode-1]=1/element[-1]
        ########################################################
        #                         L                            #
        ########################################################
        elif componentType == 'L':
            positiveNode = element[2]
            negativeNode = element[3]
            if negativeNode != 0:
                temporaryY[(negativeNode-1)*N+negativeNode-1]=1/element[-1]
            if positiveNode != 0:
                temporaryY[(positiveNode-1)*N+positiveNode-1]=1/element[-1]
        ########################################################
        #                         I                            #
        ########################################################
        elif componentType == 'I':
            positiveNode = element[2]
            negativeNode = element[3]
            if negativeNode != 0:
                temporaryI[negativeNode-1]=1/element[-1]
            if positiveNode != 0:
                temporaryI[positiveNode-1]=-1/element[-1]
        ########################################################
        #                         V                            #
        ########################################################
        elif componentType == 'V':
            positiveNode = element[2]
            negativeNode = element[3]
            currentNode = len(nodes)+element[-1]
            currentsName.append('V'+element[1])
            if negativeNode != 0:
                temporaryY[(currentNode-1)*N+negativeNode-1]=-1
                temporaryY[(negativeNode-1)*N+currentNode-1]=-1
            if positiveNode != 0:
                temporaryY[(currentNode-1)*N+positiveNode-1]=1
                temporaryY[(positiveNode-1)*N+currentNode-1]=1
            temporaryI[currentNode-1]=element[-2]
        ########################################################
        #                       VCCS                           #
        ########################################################
        elif componentType == 'G':
            positiveNode = element[2]
            negativeNode = element[3]
            positiveNodeC = element[4]
            negativeNodeC = element[5]
            if positiveNode != 0 and positiveNodeC != 0:
                temporaryY[(positiveNode-1)*N+positiveNodeC-1] = element[-1]
            if positiveNode != 0 and negativeNodeC != 0:
                temporaryY[(positiveNode-1)*N+negativeNodeC-1] = -element[-1]
            if negativeNode != 0 and positiveNodeC != 0:
                temporaryY[(negativeNode-1)*N+positiveNodeC-1] = -element[-1]
            if negativeNode != 0 and negativeNodeC != 0:
                temporaryY[(positiveNode-1)*N+negativeNodeC-1] = element[-1]
        # ########################################################
        # #                       VCVS                           #
        # ########################################################
        elif componentType == 'E':
            positiveNode = element[2]
            negativeNode = element[3]
            positiveNodeC = element[4]
            negativeNodeC = element[5]
            currentNode = len(nodes)+element[-1]
            currentsName.append('V'+element[1])
            if positiveNode != 0:
                temporaryY[(currentNode-1)*N+positiveNode-1] = 1
                temporaryY[(positiveNode-1)*N+currentNode-1] = 1
            if negativeNode != 0:
                temporaryY[(currentNode-1)*N+negativeNode-1] = -1
                temporaryY[(negativeNode-1)*N+currentNode-1] = -1 
            if positiveNodeC != 0:
                temporaryY[(currentNode-1)*N+positiveNodeC-1] = -element[-2]
            if negativeNodeC != 0:
                temporaryY[(currentNode-1)*N+negativeNodeC-1] = element[-2]
        ########################################################
        #                       CCCS                           #
        ########################################################
        elif componentType == 'F':
            positiveNode = element[2]
            negativeNode = element[3]
            controllerCurrentID = getCurrentID(elementsList,element[-2])
            controllerCurrentNode = len(nodes)+controllerCurrentID
            if negativeNode != 0:
                temporaryY[(negativeNode-1)*N+controllerCurrentNode-1]=-element[-1]
            if positiveNode != 0:
                temporaryY[(positiveNode-1)*N+controllerCurrentNode-1]=element[-1]
        ########################################################
        #                       CCVS                           #
        ########################################################
        elif componentType == 'H':
            positiveNode = element[2]
            negativeNode = element[3]
            controllerCurrentID = getCurrentID(elementsList,element[-3])
            controllerCurrentNode = len(nodes)+controllerCurrentID
            currentNode = len(nodes)+element[-1]
            if negativeNode != 0:
                temporaryY[(currentNode-1)*N+negativeNode-1]=-1
                temporaryY[(negativeNode-1)*N+currentNode-1]=-1
            if positiveNode != 0:
                temporaryY[(currentNode-1)*N+positiveNode-1]=1
                temporaryY[(positiveNode-1)*N+currentNode-1]=1
            temporaryY[(currentNode-1)*N+controllerCurrentNode-1]=-element[-2]
        I += temporaryI
        Y += temporaryY
    E = sp.simplify(Y.LUsolve(I))
    ##################################################
    #              Generating the output             #
    ##################################################
    names = []
    ########################################################
    #                       CCVS                           #
    #######################################################
    for node in nodes:
        names.append('V('+str(node)+')')
    for name in currentsName:
        names.append('I('+name+')')    
    
    return names,E