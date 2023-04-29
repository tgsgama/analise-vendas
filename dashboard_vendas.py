import streamlit as st 
from streamlit_option_menu import option_menu 
import pandas as pd
import altair as alt 
import os
import datetime
from PIL import Image


# --------- Importar o dataframe
df = pd.read_excel(
    io='./datasets/relatorio_vendas.xlsx',
    engine='openpyxl',
    sheet_name='relatorio',
    usecols='A:J',
    nrows=4400
)

# ------- Declaração de Variaveis
# f_vendedor: str = ''
# f_produto: str = ''
# f_cliente: str = ''
cor_grafico = '#61a9dc'
altura_grafico = 250


def generate_dashboards(fcliente, fproduto, fvendedor):

    # ------- Tabela Quantidade vendida por produto    
    tab1_qtde_produto = df.loc[(df['Vendedor'] == fvendedor) & (df['Cliente'] == fcliente)]
    tab1_qtde_produto = tab1_qtde_produto.groupby('Produto vendido').sum().reset_index()

    # ------- Tabela Vendas e Margens
    tab2_vendas_margens = df.loc[(df['Vendedor'] == fvendedor) & (df['Produto vendido'] == fproduto) & (df['Cliente'] == fcliente)]

    # ------- Tabela Vendas por Vendedor
    tab3_vendas_vendedor = df.loc[(df['Produto vendido'] == fproduto) & (df['Cliente'] == fcliente)]
    tab3_vendas_vendedor = tab3_vendas_vendedor.groupby('Vendedor').sum().reset_index()
    tab3_vendas_vendedor = tab3_vendas_vendedor.drop(columns=['Nº pedido','Preço'])

    # ------- Tabela Vendas por Cliente
    tab4_venda_cliente = df.loc[(df['Vendedor'] == fvendedor) & (df['Produto vendido'] == fproduto)]
    tab4_venda_cliente = tab4_venda_cliente.groupby('Cliente').sum().reset_index()

    # ------- Tabela Vendas mensais
    tab5_vendas_mensais = df.loc[(df['Vendedor'] == fvendedor) & (df['Produto vendido'] == fproduto) & (df['Cliente'] == fcliente)]
    tab5_vendas_mensais['mm'] = tab5_vendas_mensais['Data'].dt.strftime('%m/%Y')


    # ------- Grafico 1.0 Quantidade vendida por produto
    graf1_qtde_produto = alt.Chart(tab1_qtde_produto).mark_bar(
        color=cor_grafico,
        cornerRadiusTopLeft=9,
        cornerRadiusTopRight=9,    
    ).encode(
        x= 'Produto vendido',
        y= 'Quantidade',
        tooltip=['Produto vendido', 'Quantidade'],     
       
    ).properties(
        height=altura_grafico,
        title='QUANTIDADE VENDIDA POR PRODUTO'
    ).configure_axis(grid=False).configure_view(strokeWidth=0)

    # mean_line = alt.Chart(tab1_qtde_produto).mark_rule(color='red').encode(y='mean(Quantidade)')

    # ------- Cria o Rotulo do grafico
    # rotulo_graf1 = graf1_qtde_produto.mark_text(
    #     dy= -8,
    #     size=17
    # ).encode(text='Quantidade')

    # ------- Grafico 1.1 Valor da Venda por produto
    graf1_valor_produto = alt.Chart(tab1_qtde_produto).mark_bar(
        color=cor_grafico,
        cornerRadiusTopLeft=9,
        cornerRadiusTopRight=9,    
    ).encode(
        x= 'Produto vendido',
        y= 'Quantidade',
        tooltip=['Produto vendido', 'Valor Pedido'],
        
    ).properties(
        height=altura_grafico,
        title='VALOR TOTAL POR PRODUTO'
    ).configure_axis(grid=False).configure_view(strokeWidth=0)

    # ------- Grafico 2 vendas por Vendedor
    graf2_vendas_vendedor = alt.Chart(tab3_vendas_vendedor).mark_arc(
        innerRadius=100,
        outerRadius=150,
    ).encode(
        theta= alt.Theta(field='Valor Pedido', type='quantitative', stack=True),
        color = alt.Color(
            field='Vendedor',
            type='nominal',
            legend=None,
        ),
        tooltip=['Vendedor', 'Valor Pedido' ]
    ).properties(
        height=500,
        width=560,
        title='VALOR VENDA POR VENDEDOR'
    )

    rot2Ve = graf2_vendas_vendedor.mark_text(radius=210, size=14).encode(text='Vendedor')
    rot2Vp = graf2_vendas_vendedor.mark_text(radius=180, size=12).encode(text='Valor Pedido')

    # ------- Grafico 4 Vendas por Cliente
    graf4_vendas_cliente = alt.Chart(tab4_venda_cliente).mark_bar(
        color=cor_grafico,
        cornerRadiusTopLeft=9,
        cornerRadiusTopRight=9,    
    ).encode(
        x= 'Cliente',
        y= 'Valor Pedido',
        tooltip=['Cliente', 'Valor Pedido']
    ).properties(
        height=altura_grafico,
        title='VENDAS POR CLIENTE'
    ).configure_axis(grid=False).configure_view(strokeWidth=0)


    # ------- Grafico 5 Vendas Mensais
    graf5_vendas_mensais = alt.Chart(tab5_vendas_mensais).mark_line(
        color=cor_grafico,
        point=True,
    ).encode(
        alt.X('monthdate(Data):T'),
        y= 'Valor Pedido:Q'
    ).properties(
        height=altura_grafico,
        title='VENDAS MENSAIS',
    ).configure_axis(grid=False).configure_view(strokeWidth=0)


    # ------- PAGINA DOS GRAFICOS
    total_vendas = round(tab2_vendas_margens['Valor Pedido'].sum(), 2)
    total_margem = round(tab2_vendas_margens['Margem Lucro'].sum(), 2)
    porc_margem = int(100*total_margem/total_vendas)

    st.header(":bar_chart: RELATÓRIO DE VENDAS")


    dst1, dst2, dst3, dst4 = st.columns([1,1,1,2.5])
    with dst1:
        st.write('**VENDAS TOTAIS:**')
        st.info(f'**R$ {total_vendas}**')
    with dst2:
        st.write('**MARGEM TOTAL:**')
        st.info(f'**R$ {total_margem}**')
    with dst3:
        st.write('**MARGEM %:**')
        st.info(f'**{porc_margem} %**')

    st.markdown('---')

    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        st.altair_chart(graf4_vendas_cliente, use_container_width=True)
        st.altair_chart(graf5_vendas_mensais, use_container_width=True)
    with col2:
        st.altair_chart(graf1_qtde_produto, use_container_width=True)
        st.altair_chart(graf1_valor_produto, use_container_width=True)
    with col3:
        st.altair_chart(graf2_vendas_vendedor+rot2Ve+rot2Vp)
    
    st.markdown('---')
