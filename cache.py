import numpy as np
import sys
import re
from numpy import array as narray


def imprimir(rows, cols):
    print "sets ", rows, "\t blocks ", cols


cache_size = int(raw_input("Tamano de cache: (max 16)"))
sets = int(raw_input("Sets: (max 4)"))
text = raw_input("arreglo: ")
rep_pol = raw_input("Reemplazo: LRU o FIFO ")
b = re.findall(r'[+-]?[0-9.]+', text)

a = np.array(b)
"""
cache_size = 8
sets = 2
a = np.array([0,3,2,5,6,0,3,2,6,9,1,2,4,10,12,13,6,3])
rep_pol = 'LRU'
"""
columns = int(cache_size)/int(sets)

mat_cache = np.ones((int(sets),int(columns),4))*-1
#print mat_cache[:,:,0]

#imprimir(sets,columns)

a_uso=0
a_ent=0
hit=0
miss = 0
comp_miss = 0
conf_miss = 0
cont = 0
i_aux = 0

cache_seq = np.char.array([",,,,,,,,," for x in range(len(a))])

for i in a:
    i = int(i)
    #a_uso=0
    #a_ent=0
    if (i >= sets):
        i_aux = i
        while( i_aux >= sets):
            i_aux -= sets
    else:
        i_aux = i
    if (i_aux <= (sets-1)):
        zero = np.where(mat_cache[i_aux,:,1] == -1)[0] #devuelve las posiciones donde hay ceros (pos valid)
        unos = np.where(mat_cache[i_aux,:,1] == 1)[0]
        valor = np.where(mat_cache[i_aux,:,0] == i)[0]
        #print len(c)
        if len(valor):#cuando encuentra un hit
            hit+=1
            cache_seq[cont] = str(mat_cache[i_aux,valor[0],0]) + str('-') + str(i)
            mat_cache[i_aux,valor[0],0] = i
            mat_cache[i_aux,valor[0],1] = 1
            mat_cache[i_aux,valor[0],2] = a_uso
            #mat_cache[i_aux,valor[0],3] = a_ent
            a_uso+=1
        elif len(zero): #en caso de que haya posiciones en cero y sea miss
            comp_miss+=1
            cache_seq[cont] = str(i)
            mat_cache[i_aux,zero[0],0] = i
            mat_cache[i_aux,zero[0],1] = 1
            mat_cache[i_aux,zero[0],2] = a_uso
            mat_cache[i_aux,zero[0],3] = a_ent
            a_uso+=1
            a_ent+=1
        else: # en caso de que sea miss y no haya posiciones en cero (Reemplazo)
            #hit+=1
            conf_miss+=1
            if rep_pol == 'LRU':
                minim = mat_cache[i_aux,:,2]
                d = minim.argsort()[:1]
                cache_seq[cont] = str(i) + str('-') + str(mat_cache[i_aux,d[0],0]) 
                mat_cache[i_aux,d[0],0] = i
                mat_cache[i_aux,d[0],1] = 1
                mat_cache[i_aux,d[0],2] = a_uso
                mat_cache[i_aux,d[0],3] = a_ent
                a_uso+=1
                a_ent+=1
            if rep_pol == 'FIFO':
                minim = mat_cache[i_aux,:,3]
                d = minim.argsort()[:1]
                cache_seq[cont] = str(i) + str('-') + str(mat_cache[i_aux,d[0],0])
                mat_cache[i_aux,d[0],0] = i
                mat_cache[i_aux,d[0],1] = 1
                mat_cache[i_aux,d[0],2] = a_uso
                mat_cache[i_aux,d[0],3] = a_ent
                a_uso+=1
                a_ent+=1
    #print i
    #cache_seq[cont] += str(i)
    cont+=1
                
print "\n\n"           
print "total cache queries ", len(a)
print "hit",hit
print "compulsory miss ",comp_miss
print "conflict miss ",conf_miss
print "total miss ", comp_miss+conf_miss
print "miss rate %.4f " % float((float(comp_miss)+float(conf_miss))*100/float(len(a))), "%"
print "hit rate %.4f" %float(100 - float((float(comp_miss)+float(conf_miss))*100/float(len(a)))), "%"
print "Cache Contents: LRU replacement policy; "
print mat_cache[:,:,0]
print "Cache Query Sequence Trace"
print cache_seq

            
 

