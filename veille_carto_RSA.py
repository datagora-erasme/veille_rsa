import dash
from dash import dcc
from dash import html
import plotly.express as px
import glob
import csv
import datetime

"""Recuperation des données de CSV créés"""

filenames = glob.glob("data/agences/geocode/*.csv")

orth_taux = ["Taux de satisfaction des demandeurs d'emploi_Score APE", "Taux de satisfaction des demandeurs d'emploi"]
orth_n_demandeurs = ["Nombre de demandeurs d'emploi", "Nombre de demandeurs d'emploi (DEFM A)"]

datas = []
for filename in filenames:
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)        
        for row in csv_reader:
            data = {}
            for o1 in orth_taux:
                for o2 in orth_n_demandeurs:
                    try:
                        n_demandeurs = row[o2]
                        taux = row[o1]
                        # print("file : ", filename, "has enough data \n")
                        data["Nombre de demandeurs d'emploi"] = int(n_demandeurs)
                        data["Taux de satisfaction des demandeurs d'emploi"] = float(taux)*100
                        data["lat"] = float(row['latitude'])
                        data["long"] = float(row['longitude'])
                        year = int(filename[-6:-4])
                        month = int(filename[-9:-7])
                        day = int(filename[-12:-10])
                        data["datetime"] = datetime.datetime(year, month, day)
                        data["date"] = filename[-12:-4]
                        datas.append(data)
                    except KeyError:
                        # print("file : ", filename, "has not enough data \n")
                        pass
                    except ValueError:
                        pass

# datas est une liste de dictionnaires, chaque dico est une ligne d'un de tous les excels
datas = sorted(datas, key=lambda d: d["datetime"])      #sort datas by datetime

"""
-ne faire le test que pour la première ligne
-séparer le test de l'orthographe et le test de si il y a de la donnée (test de présence donnée à faire pour chaque ligne)?
"""


"""Création de la carto"""

fig = px.scatter_mapbox(datas, 
                        lat="lat", 
                        lon="long",
                        color="Taux de satisfaction des demandeurs d'emploi",
                        size="Nombre de demandeurs d'emploi",
                        zoom=10,
                        # color_continuous_scale="RdBu",
                        color_continuous_scale="sunset",
                        width=1200,
                        height=700,
                        opacity=0.7,
                        size_max=50,
                        labels={
                            "Taux de satisfaction des demandeurs d'emploi" : "Taux de satisfaction des demandeurs d'emploi (%)"
                            },
                        animation_frame="date",
                        range_color = [40.0, 90.0]
                        )
fig.update_layout(mapbox_style = 'carto-positron')
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

'''
mapbox_style    'carto-positron' pas mal
                'stamen-toner'
                'open-street-map'
'''

app = dash.Dash()
app.layout = html.Div(children=[
    html.Div(children=[
        html.H1(children="Nombre et satisfaction des demandeurs d'emploi (%) par agence")
        ],
        style={
            'display': 'block',
            'margin' : 'auto',
            'margin-top': '1%',
            'margin-bottom': '1%',
            'width': 'fit-content'
            })
    ,
    html.Div(children=[
        dcc.Graph(figure=fig)],
        style={
            'display': 'block',
            'margin': 'auto',
            'width': 'fit-content',
            }
        )
    ]
    )
app.run_server(debug=True, use_reloader=False)
