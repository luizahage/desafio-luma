#!/usr/bin/env python
# coding: utf-8

# ### Pontos de Interesse por GPS

# In[10]:


# Inserindo os pontos de interesse:

pois = {}
    
print('Insira as informações dos pontos de interesse que deseja cadastrar.')
    
name = str(input('Insira o nome do ponto de interesse. Para cancelar o resgitro de um novo ponto, basta apertar enter com a caixa vazia:'))
x = int(input('Insira a coordenada X do ponto de interesse:'))
y = int(input('Insira a coordenada Y do ponto de interesse:'))
    
# Permitindo que a pessoa pare de inserir os pontos de interesse, quando quiser:

while name != '':
    pois[name] = [x, y]
    name = str(input('Insira o nome do ponto de interesse. Para cancelar o resgitro de um novo ponto, basta apertar enter com a caixa vazia:'))
    if name != '':
        x = int(input('Insira a coordenada X do ponto de interesse:'))
        y = int(input('Insira a coordenada Y do ponto de interesse:'))

print(pois)


# In[11]:


# Listando os pontos de interesse:

for name_poi, coord in pois.items():
    print('{} (x = {}, y = {})'.format(name_poi, coord[0],coord[1]))


# In[12]:


# Inserindo o ponto de referência e a distância máxima:

pontoreferencia = []

print('Insira as informações do ponto de referência.')
pontoreferencia.append(int(input('Insira a coordenada X do ponto de referência:')))
pontoreferencia.append(int(input('Insira a coordenada Y do ponto de referência:')))
pontoreferencia.append(int(input('Insira a distância maxima (em metros) do ponto de referência:')))
print(pontoreferencia)


# In[13]:


#print(pois.items())
#print(list(pois.keys())[0])


# In[19]:


from math import sqrt

# Calculando as distância entre pontos e listando os pontos de interesse por proximidade:

for name_poi, coord in pois.items():
    dist = sqrt(((pontoreferencia[0] - coord[0])**2) + ((pontoreferencia[1] - coord[1])**2))
    if dist <= pontoreferencia[2]:
        print(name_poi)


# In[26]:


from math import sqrt

# Calculando as distância entre pontos e listando os pontos de interesse por proximidade (em ordem crescente):

dict_dist = {}

for name_poi, coord in pois.items():
    dist = sqrt(((pontoreferencia[0] - coord[0])**2) + ((pontoreferencia[1] - coord[1])**2))
    if dist <= pontoreferencia[2]:
        dict_dist[dist] = name_poi
#print(dict_dist)

i = 1 
for key in sorted(dict_dist.keys()) :
    print('{}. {} - distância: {:.2f} metros'.format(i, dict_dist[key], key))
    i += 1

