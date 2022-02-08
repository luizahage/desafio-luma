#!/usr/bin/env python
# coding: utf-8

# ### Pontos de Interesse por GPS - Integração REST API

# In[10]:


import pyodbc

# Conexão com o Banco de Dados:

data = ("Driver={SQL Server};"
            "Server=DESKTOP-K9NVNOF;"
            "Database=POIS;"
            "UID=SystemUser;"
            "PWD=iDC%P#Nr6uLhLgnKKTuNJ72&aY5pwRWmoEoJ;")


connection = pyodbc.connect(data)
print('Conexão Bem sucedida')


# In[23]:


from math import sqrt 

class Poi:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        
    def __str__(self):
        return '{} (x = {}, y = {})'.format(self.name, self.x, self.y)
        
        
    def calc_distance(self, x, y):
        return sqrt(((x - self.x)**2) + ((y - self.y)**2))

class GenericJsonEncoder(JSONEncoder):
        def default(self, obj):
            return obj.__dict__
    
# def format_poi(poi):
#     return '{} (x = {}, y = {})'.format(poi['name'], poi['x'], poi['y'])

# def create_poi(name, x, y):
#     return {'name': name, 'x': x, 'y': y}

#def calc_distance(xa, ya, xb, yb):
#        return sqrt(((xa - xb)**2) + ((ya - yb)**2))   
        
def insert_pois(connection, pois):
    cursor = connection.cursor()
    
    if not isinstance(pois, list):
        pois = [pois]
    
    for poi in pois:
        cursor.execute("INSERT INTO POI (NAME, X, Y) VALUES (?, ?, ?)", (poi.name, poi.x, poi.y))
#        cursor.execute("INSERT INTO POI (NAME, X, Y) VALUES (?, ?, ?)", (poi['name'], poi['x'], poi['y']))

    cursor.commit()
    cursor.close()

def get_pois(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM POI") 
    rows = cursor.fetchall()
    pois = []
    for id_, name, x, y in rows:
#        pois.append({'name': name, 'x': x, 'y': y})
        pois.append(Poi(name, x, y))
    cursor.close()
    
    return pois


# In[ ]:


from flask import Flask
from flask import request
import json

app = Flask(__name__)

@app.route('/poi', methods = ['GET', 'POST'] )
def poi():
    if request.method == 'GET':
    #    return json.dumps(get_pois(connection))
        return json.dumps(get_pois(connection), cls = GenericJsonEncoder)
    elif request.method == 'POST':
        poi = Poi(request.form['name'], request.form['x'], request.form['y'])
        insert_pois(connection, poi)
        return 'Criado com sucesso!'
    

app.run()


# In[36]:


# Inserindo os pontos de interesse e cadastrando esses pontos no Banco de Dados:

print('Insira as informações dos pontos de interesse que deseja cadastrar.')

while True:    
    name = str(input('Insira o nome do ponto de interesse. Para cancelar o resgitro de um novo ponto, basta apertar enter com a caixa vazia:'))
    if name == '':
        break        
    
    try:
        x = int(input('Insira a coordenada X do ponto de interesse:'))
        if x < 0:
            print('Coordenada X inválida!')
            continue
        
        y = int(input('Insira a coordenada Y do ponto de interesse:'))
        if y < 0:
            print('Coordenada Y inválida!')
            continue
                     
        insert_pois(connection, Poi(name, x, y))
#        insert_pois(connection, create_poi(name, x, y))
#    except Exception as error:
    except:
#        print(error)
        print('Valor digitado inválido!')
        
# Capturando os pontos cadastrados no Banco de Dados para uso posterior:

print(get_pois(connection))        


# In[64]:


# Listando os pontos de interesse:

for poi in get_pois(connection):
    print('* {}\n'.format(poi))

# for poi in get_pois(connection):
#     print('* {}\n'.format(format_poi(poi)))


# In[65]:


# Inserindo o ponto de referência e a distância máxima:

reference_point = {}

print('Insira as informações do ponto de referência.')
reference_point['x'] = (int(input('Insira a coordenada X do ponto de referência:')))
reference_point['y'] = (int(input('Insira a coordenada Y do ponto de referência:')))
reference_point['max_distance'] = (int(input('Insira a distância maxima (em metros) do ponto de referência:')))
print(reference_point)


# In[69]:


# Calculando as distância entre pontos e listando os pontos de interesse por proximidade:

dict_distance = {}

for poi in get_pois(connection):
    distance = poi.calc_distance(reference_point['x'], reference_point['y'])
#   distance = calc_distance(reference_point['x'], reference_point['y'], poi['x'], poi['y']) 
    if distance <= reference_point['max_distance']:
        print(poi.name)
#        print(poi['name'])
        dict_distance[distance] = poi
#        dict_distance[distance] = poi['name']    


# In[74]:


# Calculando as distância entre pontos e listando os pontos de interesse por proximidade (em ordem crescente):

i = 1 
for key in sorted(dict_distance.keys()) :
    print('{}. {} - distância: {:.2f} metros'.format(i, dict_distance[key].name, key))
#    print('{}. {} - distância: {:.2f} metros'.format(i, dict_distance[key], key))    
    i += 1

