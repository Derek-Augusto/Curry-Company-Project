# "/Users/derekaugusto/Desktop/comunidadeDS/Repos/ftc_python/dataset/visao_empresa.py"


#Libraries
from haversine import haversine

import pandas as pd

import plotly.express as px

import plotly.graph_objects as go

import streamlit as st

from PIL import Image

from streamlit_folium import folium_static

import folium

import numpy as np

import datetime

st.set_page_config( page_title = 'Visão Restaurantes', page_icon='🍽️', layout='wide')


#===========================
#Funções
#===========================

def avg_std_time_on_traffic(df1):
    df_aux = (df1.loc[:,['City','Time_taken(min)','Road_traffic_density']].groupby(['City','Road_traffic_density']).agg({'Time_taken(min)' : ['mean','std']}))
    df_aux.columns = ['avg_time','std_time']
    df_aux = df_aux.reset_index()
    fig = px.sunburst(df_aux, path=['City','Road_traffic_density'], values='avg_time',
                        color='std_time', color_continuous_scale='RdBu',
                        color_continuous_midpoint=np.average(df_aux['std_time']))
    return fig


def avg_std_time_graph(df1):
    df_aux = df1.loc[:,['City','Time_taken(min)']].groupby('City').agg({'Time_taken(min)' : ['mean','std']})
    df_aux.columns = ['avg_time','std_time']
    df_aux = df_aux.reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Control',
                                x=df_aux['City'],
                                y=df_aux['avg_time'],
                                error_y=dict(type='data', array=df_aux['std_time'])))
    fig.update_layout(barmode='group')

    return fig


def avg_std_time_delivery(df1,festival, op):
        """ Está função calcula o tempo médio e o desvio padrão do tempo de entrega
        Parâmetros:
        Input: 
                - df: Dataframe com os dados necessários para o cálculo
                - op: Tipo de operação que precisa ser calculado
                    'avg_time': Calcula o tempo médio
                    'std_time': Calcula o desvio padrão do tempo
        output:
                    - df:Dataframe com 2 colunas e 1 linha. """
        cols = ['Festival', 'Time_taken(min)']
        df_aux = (df1.loc[:,cols].groupby('Festival').agg({'Time_taken(min)':['mean','std']}) )
        df_aux.columns = ['avg_time','std_time']
        df_aux = df_aux.reset_index()
        df_aux = np.round(df_aux.loc[df_aux['Festival'] == festival ,op],2)

        return df_aux


def distance(df1, fig):
    if fig == False:
        cols = ['Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']
        df1['distance'] = df1.loc[:,cols].apply(lambda x: haversine( (x['Restaurant_latitude'],x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
        avg_distance = np.round(df1['distance'].mean(),2)
        return avg_distance


    else:
        cols = ['Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']
        df1['distance'] = df1.loc[:,cols].apply(lambda x: haversine( (x['Restaurant_latitude'],x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
        avg_distance = df1.loc[:, ['City','distance']].groupby('City').mean().reset_index()
        fig = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['distance'], pull=[0,0.1,0])])

        return fig


def clean_code(df1):
          
          #Ëstá função tem a responsabilidade de limpar o dataframe
          #Tipos de limpeza:
          #1. Remoção dos dados NaN
          #2.0Mudança do tipo da coluina de dados
          #3. Remoção dos espaços
          #4. Formatação da coluna de datas
          #6.Limpeza da coluna de tempo ( remoção do texto da variavel numérica)

          #input: DataFrame
          #output: DataFrame

#Remover espaço da string
    df1.loc[:,'ID'] = df1.loc[:,'ID'].str.strip()
    df1.loc[:,'Delivery_person_ID'] = df1.loc[:,'Delivery_person_ID'].str.strip()
    df1.loc[:,'Road_traffic_density'] = df1.loc[:,'Road_traffic_density'].str.strip()
    df1.loc[:,'Type_of_order'] = df1.loc[:,'Type_of_order'].str.strip()
    df1.loc[:,'Type_of_vehicle'] = df1.loc[:,'Type_of_vehicle'].str.strip()
    df1.loc[:,'City'] = df1.loc[:,'City'].str.strip()
    df1.loc[:,'Festival'] = df1.loc[:,'Festival'].str.strip()




    #Excluir as linhas vazias
    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, : ].copy()

    linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN')
    df1 = df1.loc[linhas_selecionadas,:].copy()

    linhas_selecionadas = (df1['City'] != 'NaN')
    df1 = df1.loc[linhas_selecionadas,:].copy()

    linhas_selecionadas = (df1['Festival'] != 'NaN')
    df1 = df1.loc[linhas_selecionadas,:].copy()


    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)


    #Conversão de texto/categoria/string para numeros inteiros
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

    #Conversão de texto/categoria/string para numeros decimais
    df1['Delivery_person_Ratings'] =df1['Delivery_person_Ratings'].astype(float)

    #Conversão de texto para data
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'],format='%d-%m-%Y' )

    #Remove as linhas da coluna multiple_deliveries que tenham o conteudo igual a NaN '
    linhas_vazias = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    #Limpando a coluna de time taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min)')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return  df1

#import dataset

df = pd.read_csv ('dataset/train.csv')


df1 = clean_code(df)



#=========================================
# Barra lateral
#================================================
st.header('Marketplace - Visão Restaurantes')

#image_path='/Users/derekaugusto/Desktop/comunidadeDS/Repos/ftc_python/dataset/Logo.png'
image = Image.open('logo.png')
st.sidebar.image( image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown('---')

#st.sidebar.markdown('##  Selecione uma data limite')
#date_slider = st.sidebar.slider ('Até qual valor?', value=pd.to_datetime(2022,4,13), min_value=pd.to_datetime(2022,2,11), max_value=pd.to_datetime(2022,4,6), format='DD-MM-YYYY')
st.sidebar.markdown('##  Selecione uma data limite')
date_value = pd.Timestamp(2022, 4, 13)
date_timestamp = int(date_value.timestamp())
date_datetime = datetime.datetime.fromtimestamp(date_timestamp)
date_slider = st.sidebar.slider(
    "Até qual valor?",
    value=date_datetime,
    min_value=datetime.datetime(2022, 2, 11),
    max_value=datetime.datetime(2022, 4, 6),
    format='YYYY-MM-DD')

st.header ( date_slider)
st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
    'Quantas as condições do trânsito',
    ['Low','Medium','High','Jam'],
    default=['Low','Medium','High','Jam'] )

st.sidebar.markdown('---')
st.sidebar.markdown('### Powered by Comunidade DS')

#Filtro de datas
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas,:]


#Filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas,:]

#Filtro de climas
climatic_options = st.sidebar.multiselect(
    'Condições climáticas',
    ['conditions Sunny','conditions Stormy','conditions Sandstorms',
    'conditions Cloudy','conditions Fog','conditions Windy'],
    default=['conditions Sunny','conditions Stormy','conditions Sandstorms',
            'conditions Cloudy','conditions Fog','conditions Windy'])

linhas_selecionadas = df1['Weatherconditions'].isin(climatic_options)
df1 = df1.loc[linhas_selecionadas,:]


#================================================
# Layout Streamlit
#================================================
tab1, tab2, tab3 = st.tabs(['Visão Gerencial','_','_'])

with st.container():
    st.title("Overall Métric")

    col1,col2,col3,col4,col5,col6 = st.columns(6)
    with col1:
        delivery_unique = len(df1.loc[:,'Delivery_person_ID'].unique())
        col1.metric('Entregadores Únicos', delivery_unique)
    with col2:
        avg_distance = distance(df1, fig = False)
        col2.metric('Distância média das entregas', avg_distance)

    with col3:
        df_aux = avg_std_time_delivery(df1,'Yes', 'avg_time')
        st.markdown('Em dias de Festivais')
        col3.metric('Tempo médio de entrega',df_aux)

    with col4:
        df_aux = avg_std_time_delivery(df1, 'Yes', 'std_time')
        st.markdown('Em dias de Festivais')
        col4.metric('STD médio de entrega',df_aux)
    with col5:
        df_aux = avg_std_time_delivery(df1, 'No', 'avg_time')
        st.markdown('Em dias sem Festivais')
        col5.metric('Tempo médio de entrega',df_aux)
        
    with col6:
        df_aux = avg_std_time_delivery(df1, 'No', 'std_time')
        st.markdown('Em dias sem Festivais')
        col6.metric('STD médio de entrega',df_aux)

with st.container():
    st.markdown("""---""")
col1,col2 = st.columns(2)

with col1:
    st.title('Tempo médio de entrega por cidade')
    fig = avg_std_time_graph(df1)
    st.plotly_chart(fig)

with col2:
    st.title('Distribuição de distância')
    df_aux = (df1.loc[:,['City','Time_taken(min)','Type_of_order']].groupby(['Type_of_order','City']).agg({'Time_taken(min)' : ['mean','std']}))
    df_aux.columns = ['avg_time','std_time']
    df_aux = df_aux.reset_index()
    st.dataframe(df_aux)



with st.container():
    st.markdown("""---""")
    st.title('Distribuição do tempo')

    col1,col2,col3 = st.columns(3)
    with col1:
        fig = distance(df1,fig=True)
        st.plotly_chart(fig)

    with col2:
        st.markdown('Coluna 2')
        fig = avg_std_time_on_traffic(df1)
        st.plotly_chart(fig)


    with col3:
        st.markdown('Coluna 3 ')


    
