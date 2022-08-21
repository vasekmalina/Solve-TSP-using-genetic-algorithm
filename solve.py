import GA_functions
import numpy as np
import copy as cp

def tsp_solve(matrix):
    distance_matrix = matrix
    mutation = 0.05
    selection = 0.3
    pop_size = 20
    epoch = 100

    size_matrix_pop = (pop_size, len(distance_matrix) )
    pop = np.zeros(size_matrix_pop,dtype='int16')

    for i in range ((pop_size)):
        pop [i] = np.random.permutation((len(distance_matrix)))

    quality = GA_functions.loss_function (pop, distance_matrix)

    pop_old = pop
    ind_min=quality.index(min(quality))
    best_quality = min(quality)
    best_way = pop_old[ind_min]
    evolution = []

    def Breeding_pmx (selection_size, pop_size, selection, pop_new, odd):  
        itr = selection_size    
        while True:
    
            for i in range (0, selection_size-1, 2):                
                    gene_1 = cp.copy(pop_new [i]) 
                    gene_2 = cp.copy(pop_new [i+1])                 
                
                    smash_1 = np.random.randint (0 , (len (pop_new [0])-2)) 
                    smash_2 = np.random.randint (smash_1+1 , len (pop_new [0]-1)) 
                    
                    temp = cp.copy(gene_1 [smash_1:smash_2])
                    gene_1 [smash_1:smash_2] = gene_2 [smash_1:smash_2]
                    gene_2 [smash_1:smash_2] = temp

                    change_1 = []
                    indx_1 = []
                    change_2 = []
                    indx_2 = []
                    
                    for j in range (smash_1,(smash_2)):
                        for k in range (len (pop_new [0])):
                            if gene_1 [j] == gene_1 [k] and j!=k:
                                change_1.append (gene_1 [k])
                                indx_1.append (k)
                                
                            if gene_2 [j] == gene_2 [k] and j!=k:
                                change_2.append (gene_2 [k])
                                indx_2.append (k)

                    for l in range (len(indx_1)):
                        gene_1[indx_1[l]]=change_2[l]
                        gene_2[indx_2[l]]=change_1[l]
                    
                    if itr+1 == pop_size:
                        
                        pop_new[itr] = gene_1
                        return pop_new 
                    
                    pop_new[itr] = gene_1
                    pop_new[itr + 1] = gene_2
                                    
                    itr += 2         
        
                    if itr >= pop_size: 
                        return pop_new
                    
                    if odd == True and itr+1 == pop_size: 
                        pop_new[itr+1] = pop_new[0]  
                        return pop_new     

    for i in range (epoch):
        (pop_new, odd, selection_size ) = GA_functions.selection_function (pop_size, selection, size_matrix_pop, quality, pop_old)
                
        pop_new = Breeding_pmx (selection_size, pop_size, selection, pop_new, odd)

        pop_new = GA_functions.Mutation (pop_new, mutation ) 
        
        quality = GA_functions.loss_function (pop_new, distance_matrix)
        
        pop_old = cp.copy(pop_new)
        ind_min=quality.index(min(quality))
        
        evolution.append (min(quality))
        

            
        if (min(quality)) < best_quality:
            best_way = pop_old[ind_min]
            best_quality = min(quality)

    return best_quality, best_way