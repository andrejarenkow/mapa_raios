import plotly.express as px
import requests
import pandas as pd

# Função para obter dados de uma API e retornar um DataFrame
def get_data_for_hour(hour):
    url = f"https://data.metsul.com/raios.php?hora={hour}"
    response = requests.get(url)
    geojson_data = response.json()

    features = geojson_data['features']
    rows = []

    for feature in features:
      try:
        coordinates = feature['geometry']['coordinates']
        datahora = feature['geometry']['datahora']
        row = {
            'longitude': float(coordinates[0]),
            'latitude': float(coordinates[1]),
            'timestamp': datahora['timestamp'],
            'data': datahora['data'],
            'hora': datahora['hora'],
            'min': datahora['min'],
            'horario': datahora['horario']
        }
        rows.append(row)
      except:
        pass

    return pd.DataFrame(rows)

# Lista de horas para as quais queremos obter os dados
hours = [10, 20, 30, 40, 50, 60]

# Obter dados para todas as horas e combinar em um único DataFrame
all_data = pd.DataFrame()
for hour in hours:
    df = get_data_for_hour(hour)
    all_data = pd.concat([all_data, df], ignore_index=True)



# Plotar o mapa com Plotly Express
fig = px.scatter_mapbox(all_data.sort_values('horario'),
                        lat="latitude",
                        lon="longitude",
                        hover_name="timestamp",  # Ajuste de acordo com a coluna que deseja exibir ao passar o mouse
                        hover_data=["data", "horario"],  # Ajuste de acordo com os dados que deseja exibir
                        zoom=5,
                        center = {'lat':-31,'lon':-52},
                        animation_frame="horario",
                        height=800,
                        width=1000)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)
