import streamlit as st
from PIL import Image
from io import StringIO, BytesIO
from datetime import datetime
import requests
import json
import zipfile

# Cria o layout básico da pagina
st.set_page_config(layout="wide")
col1, col2, col3 = st.columns((3,1,1))

# Define os diferentes modulos do site
modulos = ["Gerar XMLs", "Gerar guias PDF", "Buscar senha Bradesco", "Baixar infos metabase"]

# Inclui sidebar
seletor_modulo = st.sidebar.selectbox("O que você deseja fazer?", (modulos[0], modulos[1], modulos[2], modulos[3]))


# Inclúi logo da Beep no canto superior direito
image = Image.open('beep_logo.png')
col3.image(image, caption='Beep Saúde')

if seletor_modulo == modulos[0]:
     col1.markdown('# Gerador XML versão TISS')

     col1.markdown(
     '''
     ## Instruções
     Faça o upload do arquivo .csv, preencha com as informações necessárias (operadora e tipo de produto) e clique no botão para gerar o XML.
     ''')

     col1.markdown('### Faça upload do arquivo .csv')

     # Cria o file_uploader, onde o usuário pode subir um arquivo .csv
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

     if tipo_produto_escolhido == 'exames':
          tipo_produto = 'lab'
          codigo_tipo_produto = '1'
     elif tipo_produto_escolhido == 'vacinas':
          tipo_produto = 'vac'
          codigo_tipo_produto = '2'


     col1.markdown(
     '''
     ### Clique no botão abaixo para gerar o(s) XML(s)
     ''')


     def gerar_xml():
          # Gera arquivo(s) XML a partir do csv selecionado e cria um botão de download para baixá-lo(s)

          data_registro_transacao = datetime.now().strftime("%Y%m%d")

          if arquivo_carregado:

               # Dados para chamar a API
               api_endpoint = 'https://gerador-xml-api-6doupywhkq-ew.a.run.app/gerar_xml'

               payload={'tipo_input': 'csv',
               'operadora': operadora_escolhida,
               'seq_transacao': f'{data_registro_transacao}{codigo_tipo_produto}01', # Pensar em como não repetir
               'tipo_produto': tipo_produto}

               files=[('file',('file_name',arquivo_carregado.getbuffer(),'text/csv'))]
               headers = {}

               # Chama a API que gera o(s) arquivo(s) XML
               resposta = requests.request("POST", api_endpoint, headers=headers, data=payload, files=files)
               dict_resposta = json.loads((resposta.text))

               # Captura informações geradas pela API
               mensagem = dict_resposta.get('mensagem')
               arquivos_xml = dict_resposta.get('arquivos_xml')
               num_guias = dict_resposta.get('num_guias')
               numero_arquivos_xml = dict_resposta.get('numero_arquivos_xml')
               valor_total = dict_resposta.get('valor_total_arquivos')
               lista_sequencial_transacao = dict_resposta.get('lista_sequencial_transacao')
               erro = dict_resposta.get('error')

               # Exibe mensagem de sucesso/erro da API
               col1.write(mensagem)
               
               # Checa se a API funcionou corretamente (verificando se ela retornou arquivos XML). Caso positivo, cria o botao para baixar os XML.
               if arquivos_xml:
                    # Exibe infos da geração do XML
                    if numero_arquivos_xml == 1:
                         infos = "Foi gerado 1 arquivo xml, referente a "
                    else:
                         infos = f"Foram gerados {numero_arquivos_xml} arquivos xml, referentes a "
                    
                    valor_total_formato_real = '{:,.2f}'.format(float(valor_total)).replace('.','aux').replace(',','.').replace('aux',',')
                    infos = infos + f"{num_guias} guias distintas e um total de R$ {valor_total_formato_real}."
                    
                    col1.write(infos)

                    # Cria um botão de download para baixar o(s) arquivo(s) XML
                    # Caso tenha mais de 1 arquivo XML, gera um ZIP. Caso contrário, gera apenas um arquivo XML
                    if len(arquivos_xml) > 1:
                         zip_buffer = BytesIO()
                         with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                              for i in range(len(arquivos_xml)):
                                   nome_arquivo = f'{operadora_escolhida}_{data_registro_transacao}_{tipo_produto}_{i+1}.xml'
                                   conteudo_arquivo = arquivos_xml[i]
                                   zip_file.writestr(nome_arquivo, conteudo_arquivo)
                         
                         col1.download_button(label='Download XML (zip)', data=zip_buffer.getvalue(), mime='application/zip',
                                        file_name=f'{operadora_escolhida}_{data_registro_transacao}_{tipo_produto}_zip.zip')

                    else:
                         col1.download_button(label='Download XML', data=arquivos_xml[0], mime='xml',
                                        file_name=f'{operadora_escolhida}_{data_registro_transacao}_{tipo_produto}_1.xml')

               # Caso a api nao tenha retornado arquivos XML, é porque ela falhou. Nesse caso, mostra a mensagem de erro.
               else:
                    col1.write(f'Mensagem de erro: {erro}')

          # Caso não tenha nenhum arquivo csv carregado, exibe uma mensagem de erro.
          else:
               col1.write("Nenhum arquivo csv escolhido. Por favor, escolha um arquivo primeiro.")

     col1.button('Gerar XML', on_click=gerar_xml)

elif seletor_modulo == modulos[1]:
     col1.markdown('# Gerador de guias formato PDF')
     col1.write("Funcionalidade ainda não implementada")

elif seletor_modulo == modulos[2]:
     col1.markdown('# Buscar senha Bradesco')
     col1.write("Funcionalidade ainda não implementada")     

elif seletor_modulo == modulos[3]:
     col1.markdown('# Consultar informações de faturamento')
     col1.write("Funcionalidade ainda não implementada")