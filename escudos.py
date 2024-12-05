import requests
from bs4 import BeautifulSoup
import os

# URL de la página de LaLiga con los equipos
url = 'https://www.laliga.com/laliga-santander'

# Hacer la solicitud a la página web
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Crear una carpeta para guardar los escudos
if not os.path.exists('escudos'):
    os.makedirs('escudos')

# Encontrar todos los equipos y sus escudos
equipos = soup.find_all('div', class_='team')

for equipo in equipos:
    nombre = equipo.find('span', class_='name').text.strip()
    escudo_tag = equipo.find('img')
    if escudo_tag:
        escudo_url = escudo_tag['src']
        # Descargar el escudo
        escudo_response = requests.get(escudo_url)
        with open(f'escudos/{nombre}.png', 'wb') as f:
            f.write(escudo_response.content)
        print(f'Escudo de {nombre} descargado.')
    else:
        print(f'No se encontró escudo para {nombre}.')

print('Todos los escudos han sido descargados.')
