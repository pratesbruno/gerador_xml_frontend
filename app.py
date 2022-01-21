import streamlit as st
from PIL import Image
from io import StringIO
import requests


st.set_page_config(layout="wide")
col1, col2, col3 = st.columns((3,1,1))

image = Image.open('beep_logo.png')
col3.image(image, caption='Beep Saúde')

col1.markdown(
'''
# Gerador XML versão TISS
''')

col1.markdown(
'''
## Instruções

Faça o upload do arquivo .csv, preencha com as informações necessárias (operadora e tipo de produto) e clique no botão para gerar o XML.
''')

col1.markdown(
'''
### Faça upload do arquivo .csv
''')

arquivo_carregado = col1.file_uploader("Escolha um arquivo", type=['csv'])
try:
     arquivo_lido = arquivo_carregado.read()
     s=str(arquivo_lido,'utf-8')
     data = StringIO(s)
     col1.write(type(data))
     
except:
     col1.write('Nenhum arquivo carregado até o momento.')

col1.markdown(
'''
### Escolha a operadora
''')

operadora_escolhida = col1.selectbox(
     'Escolha a operadora',
     ('amil_one_rj', 'amil_one_sp', 'amil_rj', 'amil_sp', 'bradesco',
      'bradesco_operadora', 'bradesco_operadora_sp', 'bradesco_sp', 'camarj',
      'careplus', 'cassi', 'fio_saude', 'mediservice_rj', 'mediservice_sp',
      'omint_df', 'omint_pr', 'omint_rj', 'omint_sp', 'vale'))

col1.markdown(
'''
### Escolha o tipo de produto (exames ou vacinas)
''')

tipo_produto_escolhido = col1.selectbox(
     'Escolha o tipo de produto',
     ('exames','vacinas'))

nome_do_arquivo=f'{operadora_escolhida}_{tipo_produto_escolhido}.csv'

col1.markdown(
'''
### Clique no botão abaixo para gerar o(s) XML(s)
''')


def gerar_xml():
     
     api_endpoint = 'http://localhost:8000/gerar_xml'
     

     payload={'tipo_input': 'csv',
     'operadora': operadora_escolhida,
     'seq_transacao': '20220119199',
     'tipo_produto': tipo_produto_escolhido}

     files=[
     ('file',('file_name',arquivo_carregado.getbuffer(),'text/csv'))
     ]

     headers = {}

     response = requests.request("POST", api_endpoint, headers=headers, data=payload, files=files)

     col1.write(response.text)

col1.button('Gerar XML', on_click=gerar_xml)


# Different ways to use the API

if arquivo_carregado:
    st.download_button(label='Download CSV', data=s, mime='text/csv',
                       file_name=f'{nome_do_arquivo}')