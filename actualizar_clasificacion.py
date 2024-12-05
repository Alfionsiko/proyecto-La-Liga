import requests
import pandas as pd

# Tu clave API de Football-Data.org
api_key = '712a560c01674c17bf48f9ec6cc38bf2'

# URL de la API para obtener la clasificación de la Liga Española (v4)
url = 'https://api.football-data.org/v4/competitions/PD/standings'

# Encabezados de la solicitud
headers = {
    'X-Auth-Token': api_key
}

# Hacer la solicitud a la API
response = requests.get(url, headers=headers)
data = response.json()

# Verificar la estructura de los datos
if 'standings' in data:
    standings = data['standings'][0]['table']
    teams = []

    for team in standings:
        teams.append({
            'Posición': team['position'],
            'Equipo': team['team']['name'],
            'Jugados': team['playedGames'],
            'Ganados': team['won'],
            'Empatados': team['draw'],
            'Perdidos': team['lost'],
            'Goles a Favor': team['goalsFor'],
            'Goles en Contra': team['goalsAgainst'],
            'Diferencia de Goles': team['goalDifference'],
            'Puntos': team['points']
        })

    # Crear un DataFrame de pandas
    df = pd.DataFrame(teams)

    # Guardar los datos en un archivo CSV
    df.to_csv('clasificacion_liga.csv', index=False)

    print("Archivo CSV creado con éxito")
else:
    print("Error: La clave 'standings' no se encuentra en la respuesta de la API.")
