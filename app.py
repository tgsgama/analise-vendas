import streamlit as st 
from streamlit_option_menu import option_menu 
import pandas as pd
import altair as alt 
import os
import datetime
from PIL import Image
from dashboard_vendas import *

# --------- Importar o dataframe
df = pd.read_excel(
    io='./datasets/relatorio_vendas.xlsx',
    engine='openpyxl',
    sheet_name='relatorio',
    usecols='A:J',
    nrows=4400
)

# ------- Declaração de Variaveis
f_vendedor: str = ''
f_produto: str = ''
f_cliente: str = ''
cor_grafico = '#61a9dc'

altura_grafico = 250

# ------- Configuração da Pagina
st.set_page_config(
    page_title='Dashboard de Vendas',
    page_icon=':white_check_mark:',
    layout='wide', # ou wide
    initial_sidebar_state='collapsed', # expanded, collapsed ou auto
    menu_items={
        'Get help': 'https://www.fluxoea.com',
        'About': 'Desenvolvido por Fluxo Engenharia e Automação'
    }
)

# ------- Cria o sidebar
with st.sidebar:

    logo = Image.open('./assets/Aqua.png')
    st.image(logo, width=150)
    
    selected = option_menu(
        menu_title = 'Menu Principal', 
        options = ['Inicio', 'Dashboards', 'Suporte'], 
        icons=['apple', 'bar-chart', 'fan'], 
        menu_icon= 'cast', 
        default_index = 0,
        styles={
            'container': {'padding': '0!import', 'background-color': '#ffffff'},
            'icon': {'color': '#1d3557', 'font-size': '20px'},
            'nav-link': {
                'font-size': '15px',
                'text-align': 'left',
                'margin': '0px',
                '--hover-color': '#eaeef1',               
                
            },
            'nav-link-selected': {'background-color': '#dae7f0'}
            
        } 
        
    ) 


    if selected == 'Dashboards':
        
        f_vendedor = st.selectbox("Selecione o Vendedor:", options=df['Vendedor'].unique())
        f_produto = st.selectbox("Selecione o Produto:", options=df['Produto vendido'].unique())
        f_cliente = st.selectbox("Selecione o Cliente:", options=df['Cliente'].unique())
if selected == 'Dashboards':
    generate_dashboards(f_cliente, f_produto, f_vendedor)

if selected != 'Dashboards':
    st.write(selected)
