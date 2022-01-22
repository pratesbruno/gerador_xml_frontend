import streamlit as st
from PIL import Image
from io import StringIO
import requests
import json

st.set_page_config(layout="wide")
col1, col2, col3 = st.columns((3,1,1))
conteudo_xml= None

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

nome_do_arquivo=f'{operadora_escolhida}_{tipo_produto_escolhido}.xml'

col1.markdown(
'''
### Clique no botão abaixo para gerar o(s) XML(s)
''')


def gerar_xml():
     
     if arquivo_carregado:
          api_endpoint = 'http://localhost:8000/gerar_xml'

          payload={'tipo_input': 'csv',
          'operadora': operadora_escolhida,
          'seq_transacao': '20220119199',
          'tipo_produto': tipo_produto_escolhido}

          files=[
          ('file',('file_name',arquivo_carregado.getbuffer(),'text/csv'))
          ]

          headers = {}

          resposta = requests.request("POST", api_endpoint, headers=headers, data=payload, files=files)

          dict_resposta = json.loads((resposta.text))

          col1.write(dict_resposta['mensagem'])

          conteudo_xml = dict_resposta['conteudo_xml']

          conteudo_namespace = dict_resposta['xml_com_namespaces']

          col1.download_button(label='Download XML', data=conteudo_namespace, mime='xml',
                         file_name=f'{nome_do_arquivo}')

     else:
          col1.write("Nenhum arquivo csv escolhido. Por favor, escolha um arquivo primeiro.")

col1.button('Gerar XML', on_click=gerar_xml)

