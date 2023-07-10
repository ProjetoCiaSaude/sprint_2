'''
AQUI ESTÃO AS FUNÇÕES PARA CRIAR A TABELA DE TODOS OS USUÁRIOS NO BANCO DE DADOS
QUE É MOSTRADA NA TELA DE PACIENTE (CONSULTA)
'''

from bd import pacientes
import pandas as pd

def pacientesTable_toHTML():
    pacientes_dados = pacientes.find()
    pacientes_lista = [x for x in pacientes_dados]

    pacientes_dataframe = pd.DataFrame(pacientes_lista)

    # turn dataframe into html
    html_df = pacientes_dataframe.to_html()

    # write html to file
    text_file = open("templates/pacientes_table.html", "w", encoding="utf-8")
    text_file.write(html_df)
    text_file.close()

    