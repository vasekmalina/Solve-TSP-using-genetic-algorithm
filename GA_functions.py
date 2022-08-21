# -*- coding: utf-8 -*-

import numpy as np
import copy as cp
import math


def loss_function (po, dm):
    distance = [0]*len (po)
    
    for h in range (len (po)):
        for i in range (len (po[0])-1): 
            distance [h] = distance [h] + dm[po[h,i], po[h,i+1]] 
        distance [h] = distance [h] + dm[po[h,i+1], po[h,0]]
            
    return distance


def selection_function (pop_size, selection, size_matrix_pop, quality, pop_old):
    
    selection_size = math.ceil(pop_size*selection)
    odd = pop_size % 2
    
    pop_new = np.zeros (size_matrix_pop, dtype=int)
    
    for i in range (selection_size):
        ind_min=quality.index(min(quality))
        pop_new[i] = pop_old[ind_min]
        quality[ind_min] = np.inf
        
    return (pop_new, odd, selection_size)
  
def Mutation (pop_new, mutation):  
    for i in range (len(pop_new)):
            for j in range (len(pop_new[0])):
                 mutation_chance=np.random.random_sample()
                 if mutation_chance < mutation:
                     temp = pop_new [i,j]
                     change = np.random.randint (0 , (len (pop_new [0])-1))
                     pop_new [i,j] = pop_new [i,change]
                     pop_new [i,change]=temp
                    
    return pop_new