import sqlite3 as sql
from os.path import dirname, join
import datetime
import numpy as np
import pandas.io.sql as psql
import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import column, layout
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput
from bokeh.plotting import figure
from bokeh.sampledata.movies_data import movie_path

# DATA
movies = pd.read_csv('/mnt/hdd/Personal/Documentos/MSc/Lawtechs/viagens_portal/data/dadosbrutos.csv', sep=';')

# Transform into numeric (float) for the plots
movies['valormultas']= movies['valormultas'].str.replace(',', '').astype(float)
movies['valortarifacomercial']= movies['valortarifacomercial'].str.replace(',', '').astype(float)
movies['valortarifagoverno']= movies['valortarifagoverno'].str.replace(',', '').astype(float)
movies['valortarifaembarque']= movies['valortarifaembarque'].str.replace(',', '').astype(float)
movies['valorreembolso']= movies['valorreembolso'].str.replace(',', '').astype(float)
movies['valorbilhete']= movies['valorbilhete'].str.replace(',', '').astype(float)
movies['diferencatarifa']= movies['diferencatarifa'].str.replace(',', '').astype(float)

# Transform clolumns that are not numeric into numeric for plots
movies['classetarifarianumerica'] = movies['classetarifaria'].astype('category').cat.codes
movies['companhiaaereanumerica'] = movies['companhiaaerea'].astype('category').cat.codes
movies['noshownumerico'] = movies['noshow'].astype('category').cat.codes
movies['remarcadonumerico'] = movies['remarcado'].astype('category').cat.codes
movies['situacaobilhetenumerico'] = movies['situacaobilhete'].astype('category').cat.codes


viagens = movies[['codigoorgaosuperior', 'nomeorgaosuperior', 'codigoorgaosolicitante', \
                 'nomeorgaosolicitante', 'dataembarque', 'valortarifacomercial', 'companhiaaerea', \
                 'classetarifaria', 'noshow',  'remarcado', 'valorreembolso', 'situacaobilhete', \
                 'classetarifarianumerica', 'companhiaaereanumerica', 'noshownumerico', \
                 'remarcadonumerico', 'situacaobilhetenumerico']]

l = ['nomeorgaosuperior', 'nomeorgaosolicitante', 'companhiaaerea', 'noshow', 'remarcado', 'situacaobilhete']
# l = ['situacaobilhete']
for i in range(0, len(l)):
    v = viagens[l[i]]
    v = v.to_list()
    v1=[]

    for j in range(0, len(v)):
        a = str(v[j])
        v1.append(a.strip())

    v2 = np.unique(v1)
    s = '/mnt/hdd/Personal/Documentos/MSc/Lawtechs/viagens_portal/viagens/'+l[i]+'.txt'
    f = open(s, 'w')
    for i in range(0, len(v2)):
        f.write(str(v2[i]) + ';')

    f.close()


axis_map = {
    "Orgão Superior": "codigoorgaosuperior",
    "Orgão Solicitante": "codigoorgaosolicitante",
    "Valor Tarifa (reais)": "valortarifacomercial",
    "Companhia Aerea": "companhiaaereanumerica",
    "Classe Tarifaria (numero)": "classetarifarianumerica",
    "No Show": "noshownumerico",
    "Remarcado": "remarcadonumerico",
    "Valor do Reembolso": "valorreembolso",
    "Situação do Bilhete (numero)": "situacaobilhetenumerico"

}


desc = Div(text=open(join(dirname(__file__), "description.html")).read(), sizing_mode="stretch_width")

# Create Input controls
min_year = Slider(title="Ano Inicial", start=2017, end=2019, value=2017, step=1)
max_year = Slider(title="Ano Final", start=2017, end=2019, value=2019, step=1)

nomeorg = Select(title="Nome Orgão", value="All",
               options=open(join(dirname(__file__), '../viagens/nomeorgaosuperior.txt')).read().split(sep=';'))

aerea = Select(title="Nome Orgão", value="All",
               options=open(join(dirname(__file__), '../viagens/companhiaaerea.txt')).read().split(sep=';'))

orgsolicitante = Select(title="Orgão Solicitante", value="All",
               options=open(join(dirname(__file__), '../viagens/nomeorgaosolicitante.txt')).read().split(sep=';'))

noshow = Select(title="NoShow", value="All",
               options=open(join(dirname(__file__), '../viagens/noshow.txt')).read().split(sep=';'))

remarc = Select(title="Viagem Remarcada", value="All",
               options=open(join(dirname(__file__), '../viagens/remarcado.txt')).read().split(sep=';'))

bilhete = Select(title="Sitaução do Bilhete", value="All",
               options=open(join(dirname(__file__), '../viagens/situacaobilhete.txt')).read().split(sep=';'))

# reviews = Slider(title="Minimum number of reviews", value=80, start=10, end=300, step=10)
# min_year = Slider(title="Year released", start=1940, end=2014, value=1970, step=1)
# max_year = Slider(title="End Year released", start=1940, end=2014, value=2014, step=1)
# oscars = Slider(title="Minimum number of Oscar wins", start=0, end=4, value=0, step=1)
# boxoffice = Slider(title="Dollars at Box Office (millions)", start=0, end=800, value=0, step=1)
# genre = Select(title="Genre", value="All",
#                options=open(join(dirname(__file__), 'genres.txt')).read().split())
# director = TextInput(title="Director name contains")
# cast = TextInput(title="Cast names contains")
x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="Classe Tarifaria (numero)")
y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="Valor Tarifa (reais)")

# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(x=[], y=[], nomeorgaosuperior=[], year=[], nomeorgaosolicitante=[], classetarifaria=[], valortarifacomercial=[]))

TOOLTIPS=[
    ("Orgão Superior", "@nomeorgaosuperior"),
    ("Orgão Solicitante", "@nomeorgaosolicitante"),
    ("Classe Tarifaria", "@classetarifaria"),
    ("Valor Tarifa", "@valortarifacomercial"),
    ("Situação do Bilhete", "@situacaobilhete")
]

p = figure(plot_height=600, plot_width=700, title="", toolbar_location=None, tooltips=TOOLTIPS, sizing_mode="scale_both", tools='wheel_zoom')
p.circle(x="x", y="y", source=source, size=7, line_color=None)

def createListSolicitante(selected):

    # df1 = viagens[viagens.nomeorgaosuperior==nomeorg_val]
    # print(df1)
    f = open('/mnt/hdd/Personal/Documentos/MSc/Lawtechs/viagens_portal/viagens/nomeorgaosolicitante.txt', 'r+')
    f.truncate(0)
    f.close()
    # print('Org', nomeorg_val)
    # print('select:', selected)

    v = selected['nomeorgaosolicitante']

    v = v.to_list()
    # print(v)

    v1=[]

    for j in range(0, len(v)):
        a = str(v[j])
        v1.append(a.strip())

    v2 = np.unique(v1)
    print(v2)
    s = '/mnt/hdd/Personal/Documentos/MSc/Lawtechs/viagens_portal/viagens/nomeorgaosolicitante'+'.txt'
    f = open(s, 'w')
    for i in range(0, len(v2)):
        f.write(str(v2[i]) + ';')

    f.close()
    orgsolicitante.options=open(join(dirname(__file__), '/mnt/hdd/Personal/Documentos/MSc/Lawtechs/viagens_portal/viagens/nomeorgaosolicitante.txt')).read().split(sep=';')
    # return selected

def select_movies():
    nomeorg_val = nomeorg.value
    aerea_val = aerea.value
    orgsolicitante_val = orgsolicitante.value
    noshow_val = noshow.value
    remarc_val = remarc.value
    bilhete_val = bilhete.value

    # director_val = director.value.strip()
    # cast_val = cast.value.strip()
    selected = viagens#[
        # (movies.Reviews >= reviews.value) &
        # (movies.BoxOffice >= (boxoffice.value * 1e6)) &
        # (viagens.dataembarque >= min_year.value) &
        # (viagens.dataembarque <= max_year.value)
        # (movies.Oscars >= oscars.value)
    #]
    if (nomeorg_val != "All"):
        selected = selected[selected.nomeorgaosuperior.str.contains(nomeorg_val)==True]
        createListSolicitante(selected)
    if (aerea_val != "All"):
        selected = selected[selected.companhiaaerea.str.contains(aerea_val)==True]
    if (orgsolicitante_val != "All"):
        selected = selected[selected.nomeorgaosolicitante.str.contains(orgsolicitante_val)==True]
    if (noshow_val != "All"):
        selected = selected[selected.noshow.str.contains(noshow_val)==True]
    if (remarc_val != "All"):
        selected = selected[selected.remarcado.str.contains(remarc_val)==True]
    if (bilhete_val != "All"):
        selected = selected[selected.situacaobilhete.str.contains(bilhete_val)==True]
    return selected


def update():
    df = select_movies()
    x_name = axis_map[x_axis.value]
    y_name = axis_map[y_axis.value]

    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = y_axis.value
    p.title.text = "%d viagens selected" % len(df)
    # source = ColumnDataSource(data=dict(x=[], y=[],
    # nomeorgaosuperior=[], year=[], nomeorgaosolicitante=[], classetarifaria=[], valortarifacomercial=[]))

    source.data = dict(
        x=df[x_name],
        y=df[y_name],
        nomeorgaosuperior=df["nomeorgaosuperior"],
        year=df["dataembarque"],
        nomeorgaosolicitante=df["nomeorgaosolicitante"],
        classetarifaria=df["classetarifaria"],
        valortarifacomercial=df["valortarifacomercial"]
    )

controls = [nomeorg, aerea, min_year, max_year, orgsolicitante, noshow, remarc, bilhete, x_axis, y_axis]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

inputs = column(*controls, width=320, height=1000)
inputs.sizing_mode = "fixed"
l = layout([
    [desc],
    [inputs, p],
], sizing_mode="scale_both")

update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "Viagens a Serviço do Governo"
