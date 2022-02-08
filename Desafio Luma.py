#!/usr/bin/env python
# coding: utf-8

# ### Pontos de Interesse por GPS - Integração Banco de Dados

# In[102]:


# Comando para fazer o ID recomeçar
#DBCC CHECKIDENT ('POI', RESEED, 0 );

# Comando para deletar um linha específica
#DELETE FROM POI WHERE NAME = 'Posto';


# In[103]:


#cursor.execute("INSERT INTO POI (NAME, X, Y) VALUES ('Lanchonete', 27, 12);")
#cursor.execute("SELECT * FROM POI;") 
#row = cursor.fetchone() 
#while row: 
#    print(row)
#    row = cursor.fetchone()
#cursor.commit()
#cursor.close()



#from math import sqrt 

#class Poi:
#    def __init__(self, name, x ,y):
#        self.name = name
#        self.x = x
#         self.y = y
#     def calc_dist(self, x, y):
#         return sqrt(((x - self.x)**2) + ((y - self.y)**2))

# poi = Poi('Lanchonete', 27, 12)

# dict_poi = {"name": 'Lanchonete', "x": 27, "y":12}

# print(dict_poi["name"])


# In[19]:


from math import sqrt 

def calc_dist(xa, ya, xb, yb):
    return sqrt(((xa - xb)**2) + ((ya - yb)**2))

def insert_multiple_pois(connection, list_pois):
    cursor = connection.cursor()
    for poi in list_pois:
        cursor.execute("INSERT INTO POI (NAME, X, Y) VALUES (?, ?, ?)", (poi['name'], poi['x'], poi['y']))
    cursor.commit()
    cursor.close()

def get_pois(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM POI") 
    row = cursor.fetchall()
    cursor.close()
    
    return row


# In[1]:


import pyodbc

# Conexão com o Banco de Dados:

data = ("Driver={SQL Server};"
            "Server=DESKTOP-K9NVNOF;"
            "Database=POIS;"
            "UID=SystemUser;"
            "PWD=iDC%P#Nr6uLhLgnKKTuNJ72&aY5pwRWmoEoJ;")


connection = pyodbc.connect(data)
print('Conexão Bem sucedida')

#cursor.execute("INSERT INTO POI (NAME, X, Y) VALUES ('Posto', 31, 18);")
#cursor.execute("SELECT * FROM POI;") 

#row1 = cursor.fetchall()
#print(row1)
#row = cursor.fetchone()
#while row: 
#    print(row)
#    row = cursor.fetchone()
#cursor.commit()
#cursor.close()


# In[10]:


# Inserindo os pontos de interesse e cadastrando esses pontos no Banco de Dados:

cursor = connection.cursor()

print('Insira as informações dos pontos de interesse que deseja cadastrar.')
    
while True:    
    name = str(input('Insira o nome do ponto de interesse. Para cancelar o resgitro de um novo ponto, basta apertar enter com a caixa vazia:'))
    if name == '':
        break        
    
    try:
        x = int(input('Insira a coordenada X do ponto de interesse:'))    
        y = int(input('Insira a coordenada Y do ponto de interesse:'))
        print(x,y)
        if x < 0:
            print('Coordenada X inválida!')
        elif y < 0:
            print('Coordenada Y inválida!')
        else:        
            cursor.execute("INSERT INTO POI (NAME, X, Y) VALUES (?, ?, ?)", (name, x, y))
            cursor.commit()
    except:
        print('Valor digitado inválido!')
        
# Capturando os pontos cadastrados no Banco de Dados para uso posterior:

cursor.execute("SELECT * FROM POI") 
row = cursor.fetchall()
print(row)        
cursor.close()


# In[11]:


# Listando os pontos de interesse:

for key, name_poi, coordx, coordy in row:
    print('{} (x = {}, y = {})'.format(name_poi, coordx,coordy))


# In[5]:


# Inserindo o ponto de referência e a distância máxima:

pontoreferencia = []

print('Insira as informações do ponto de referência.')
pontoreferencia.append(int(input('Insira a coordenada X do ponto de referência:')))
pontoreferencia.append(int(input('Insira a coordenada Y do ponto de referência:')))
pontoreferencia.append(int(input('Insira a distância maxima (em metros) do ponto de referência:')))
print(pontoreferencia)


# In[6]:


from math import sqrt

# Calculando as distância entre pontos e listando os pontos de interesse por proximidade:

for key, name_poi, coordx, coordy in row:
    dist = sqrt(((pontoreferencia[0] - coordx)**2) + ((pontoreferencia[1] - coordy)**2))
    if dist <= pontoreferencia[2]:
        print(name_poi)


# In[7]:


from math import sqrt

# Calculando as distância entre pontos e listando os pontos de interesse por proximidade (em ordem crescente):

dict_dist = {}

for key, name_poi, coordx, coordy in row:
    dist = sqrt(((pontoreferencia[0] - coordx)**2) + ((pontoreferencia[1] - coordy)**2))
    if dist <= pontoreferencia[2]:
        dict_dist[dist] = name_poi
#print(dict_dist)

i = 1 
for key in sorted(dict_dist.keys()) :
    print('{}. {} - distância: {:.2f} metros'.format(i, dict_dist[key], key))
    i += 1

