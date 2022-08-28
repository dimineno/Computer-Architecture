#!/usr/bin/python3

import matplotlib.pyplot as plt

BenchCPIs = [ 'speclibm_' + str(i)  for i in range(13)]
BenchCPIs.extend(['specbzip_' + str(i)  for i in range(16)]) 
BenchCPIs.extend(['specsjeng_' + str(i)  for i in range(12)])
BenchCPIs.extend(['specmcf_' + str(i)  for i in range(14)])     
BenchCPIs.extend(['spechmmer_' + str(i)  for i in range(13)])        


CPIs =[3.114930,1.752845,3.087360,3.087360,3.082420 ,3.081454,3.079779,3.075328,3.075328,3.075328,2.283224,1.809287,1.752845,1.654755,1.764253,1.725648,1.725587,1.725587,1.690684,1.657080,1.615417,1.741313,1.727934,1.672335,1.671640,1.669988,1.705180,1.655485,8.731224        ,3.446290, 8.729778, 8.730028, 8.729588	,8.728178,8.727299,8.730076,8.729650,8.729650,5.993796,4.439235,3.446290,3.021039,1.248496,1.841442,1.208460,  1.208222,    1.203915	,   1.199678	,1.126087,1.167262	,1.166788	,1.133901,1.111803,1.103812,1.114758	,1.841442,6.997622, 6.893103, 6.893103,6.893103,6.878964,6.878964,6.878964,5.573137	,4.862183,4.628369	,4.669199	,5.724630	,3.015211]		

	 

LibmCPI = CPIs[0:13]
bzipCPI = CPIs[13:29]
sjengCPI = CPIs[29:41]
mcfCPI = CPIs[41:55]
hmmerCPI = CPIs[55:66]

"""
dictCPI = {} 
for key in BenchCPIs: 
    for value in CPIs: 
        dictCPI[key] = value 
        CPIs.remove(value) 
        break
"""
    
#print(str(dictCPI))

# Cost function using lamba func

# 16,16,16,1,1,1,64
parametersLibm = [[1,1,32,1,1,2,1],[1,4,32,1,1,2,1],[4,4,32,1,1,2,1],
             [4,8,32,1,1,2,1],[8,8,32,1,1,2,1],[8,8,64,1,1,2,1],
             [8,8,128,1,1,2,1],[8,8,128,2,2,4,1],[8,8,128,4,4,4,1],
             [8,8,128,8,8,8,1],[8,8,128,8,8,8,2],[8,8,128,8,8,8,4],[4,4,64,8,8,8,4]]
             
             
parametersbzip = [[2,2,32,1,1,2,1],[4,2,32,1,1,2,1],[4,4,32,1,1,2,1],[4,8,32,1,1,2,1],[8,8,32,1,1,2,1],[8,8,64,1,1,2,1],[8,8,128,1,1,2,1],
             [2,2,32,2,2,2,1],[2,2,32,4,4,2,1],[8,8,32,4,4,2,1],[8,8,32,4,4,4,1],[8,8,32,4,4,8,1],[8,8,32,1,1,1,1],
             [8,8,32,1,1,1,2],[8,8,32,4,4,4,2],[8,8,32,4,4,4,4]]
             
             
parametersjeng =[[2,4 ,32 ,1 ,1 ,2 ,1],[4 ,4 ,32, 1 ,1 ,2 ,1],[4 ,8, 32, 1, 1 ,2, 1],[8 ,8, 32, 1, 1 ,2, 1],[8 ,8 ,64, 1 ,1 ,2 ,1],[8,8 ,64 ,1, 1, 2, 1],
             [8 ,8 ,128, 2, 2 ,2 ,1],[8 ,8 ,128,4 ,4 ,4 ,1],[8, 8, 128, 8, 8 ,8 ,1],[8, 8 , 128,8 ,8 ,8 ,2],[8 ,8 ,128,8 ,8 ,8 ,4],[4,4,128 ,8 ,8 ,8 ,4]]

parametersmcf = [[2,4,32, 1 ,1 ,2, 1],[4 ,4 ,32, 1, 1, 2, 1],[8, 4, 32, 1 ,1 ,2, 1],[8, 8, 32, 1, 1, 2, 1],
                 [8, 8, 64, 1, 1, 2, 1],[8, 8, 128, 1 ,1, 2 ,1],[8 ,8, 128, 2, 2, 2, 1 ],
                 [8,8,32,4,4,4,1],[8,8,32,8,8,8,1],[8,8,32,8,8,8,1],[8,8,32,4,4,4,2],[8,8,32,4,4,4,4],
                 [8,8,32,8,8,8,4],[4,4,16,8,8,8,4]]

parametershmmer = [[8,4,128,1,1,2,1],
                   [8,8,128,1,1,2,1],[8,8,128,1,1,2,1],[8,8,32,1,1,2,1],
                   [8,8,32,2,2,2,1],[8,8,32,4,4,4,1],[8,8,32,8,8,8,1],[8,8,32,8,8,8,2],[8,8,32,8,8,8,4],
                   [8,8,32,4,4,4,8],[4,4,32,4,4,4,8]]




c = lambda x1,x2,x3,x4,x5,x6,x7 : 2.6*x1 + 2.6*x2 + x3 + 2.6*x4 + 2.6*x5 + x6 + 0*x7
costsLibm = []
costsbzip = []
costsjeng = []
costsmcf = []
costshmmer = []

for x in parametersLibm:
    
    costsLibm.append(c(x[0],x[1],x[2],x[3],x[4],x[5],x[6]))
    
for x in parametersbzip:
    
    costsbzip.append(c(x[0],x[1],x[2],x[3],x[4],x[5],x[6]))
    
for x in parametersjeng:
    
    costsjeng.append(c(x[0],x[1],x[2],x[3],x[4],x[5],x[6]))
    
for x in parametersmcf:
    
    costsmcf.append(c(x[0],x[1],x[2],x[3],x[4],x[5],x[6]))
    
for x in parametershmmer:
    
    costshmmer.append(c(x[0],x[1],x[2],x[3],x[4],x[5],x[6]))
    

    
plt.figure(figsize=(10,6))  
plt.scatter(costsjeng,sjengCPI,c = 'r', label = 'Sjeng')
plt.scatter(costsLibm,LibmCPI, c = 'b', label = 'Libm')
plt.scatter(costsbzip,bzipCPI, c = 'g', label = 'Bzip' )
plt.scatter(costshmmer,hmmerCPI, c = 'k', label = 'Hmmer')
plt.scatter(costsmcf,mcfCPI,c ='y',label= 'Mcf')
plt.ylabel('CPI')
plt.xlabel('Cost in units(u)')
plt.legend()

plt.show()
