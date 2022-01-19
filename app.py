import streamlit as st
from PIL import Image


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

uploaded_file = col1.file_uploader("Escolha um arquivo", type=['csv'])



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

col1.markdown(
'''
### Clique no botão abaixo para gerar o(s) XML(s)
''')



col1.button('Gerar XML')



# Different ways to use the API

if uploaded_file:
    st.download_button('Download CSV', uploaded_file, )