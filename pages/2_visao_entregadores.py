
# Tentar usar esse comando no terminal para encontrar a pasta
# "/Users/derekaugusto/Desktop/comunidadeDS/Repos/ftc_python/dataset/visao_empresa.py"


#No terminal / pip install streamlit-folium
#No terminal / pip install folium

#Libraries
from haversine import haversine

import pandas as pd

import plotly.express as px

import plotly.graph_objects as go

import streamlit as st

from PIL import Image

from streamlit_folium import folium_static

import folium

import datetime

st.set_page_config( page_title = 'Visão Entregadores', page_icon='🚚', layout='wide')


# ---------------------------------
#Funções
#---------------------------------

def top_delivers(df1, top_asc):
    df2 = (df1.loc[:,['Delivery_person_ID','City','Time_taken(min)']]
                .groupby(['City','Delivery_person_ID'])
                .mean()
                .sort_values(['City','Time_taken(min)'], ascending = top_asc).reset_index())

    df_aux01 = df2.loc[df2['City'] == 'Metropolitian',:].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban',:].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban',:].head(10)
    df3 = pd.concat( [df_aux01, df_aux02, df_aux03]).reset_index(drop=True)

    return df3

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

#================================================



#=========================================
# Barra lateral
#================================================
st.header('Marketplace - Visão Entregadores')

#image_path='/Users/derekaugusto/Desktop/comunidadeDS/Repos/ftc_python/dataset/Logo.png'
image = Image.open('logo.png')
st.sidebar.image( image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown('---')

#st.sidebar.markdown('##  Selecione uma data limite')
#date_slider = st.sidebar.slider ('Até qual valor?', value=pd.datetime(2022,4,13), min_value=pd.datetime(2022,2,11), max_value=pd.datetime(2022,4,6), format='DD-MM-YYYY')
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

with tab1:
    with st.container():
        st.title('Overall')

        col1,col2,col3,col4 = st.columns(4, gap='large')
        with col1:
           
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Maior idade', maior_idade)

        with col2:
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Menor idade', menor_idade)

        with col3:
            melhor_condicao = df1.loc[:,'Vehicle_condition'].max()
            col3.metric('A melhor condição de veiculo é: ', melhor_condicao)


        with col4:
            pior_condicao = df1.loc[:,'Vehicle_condition'].min()
            col4.metric('A pior condição do veiculo é: ', pior_condicao)
    with st.container():
        st.markdown("""---""")
        st.title('Avaliações')

        col1,col2= st.columns(2)
        with col1:
            st.markdown('##### Avaliação média por entregador')
            df_avg_ratings_per_delivery = (df1.loc[:,['Delivery_person_ID','Delivery_person_Ratings']]
                                                .groupby('Delivery_person_ID')
                                                .mean()
                                                .round(2)
                                                .reset_index())
            st.dataframe(df_avg_ratings_per_delivery)

        with col2:
            st.markdown('##### Avaliação média por trânsito')
            df_avg_ratings_per_traffic = (df1.loc[:,['Delivery_person_Ratings','Road_traffic_density']]
                                                .groupby('Road_traffic_density')
                                                .agg({'Delivery_person_Ratings' : ['mean','std']}))

                            #renome da coluna
            df_avg_ratings_per_traffic.columns = ['delivery_mean','delivery_std']

            #reset index
            df_avg_ratings_per_traffic = df_avg_ratings_per_traffic.reset_index()

            st.dataframe(df_avg_ratings_per_traffic)


            st.markdown('##### Avaliação média por Clima')
            df_avg_ratings_per_conditions = (df1.loc[:,['Delivery_person_Ratings','Weatherconditions']]
                                                    .groupby('Weatherconditions')
                                                    .agg({'Delivery_person_Ratings' : ['mean','std']}))

            #renome da coluna
            df_avg_ratings_per_conditions.columns = ['delivery_mean','delivery_std']

            #reset index
            df_avg_ratings_per_conditions = df_avg_ratings_per_conditions.reset_index()

            st.dataframe(df_avg_ratings_per_conditions)

    with st.container():
        st.markdown("""---""")
        st.title('Velocidade de Entrega')

        col1,col2 = st.columns(2)

        with col1:
            st.subheader('Top Entregadores mais rápidos')
            df3 = top_delivers(df1, top_asc=True)
            st.dataframe(df3)
          

        with col2:
            st.markdown('##### Top Entregadores mais Lentos')
            df3 = top_delivers(df1, top_asc=False)
            st.dataframe(df3)
