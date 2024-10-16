import argparse

from create_excel_table import build_excel_table
from votation_data import build_data_to_table, get_votation_data
from sections_places_br import section_places_locales

# Criar o parser
parser = argparse.ArgumentParser(description='Processar os argumentos candidate_name, city_code, file_name, election_year.')

# Adicionar argumentos
parser.add_argument('--candidate_name', type=str, required=True, help='Nome do candidato')
parser.add_argument('--city_code', type=int, required=True, help='Código da cidade')
parser.add_argument('--file_name', type=str, required=True, help='Nome do arquivo de saída da tabela de votos seção a seção')
parser.add_argument('--election_year', type=str, required=True, help='Ano da eleição')

# Parsear os argumentos da linha de comando
args = parser.parse_args()

candidate_name = args.candidate_name
city_code = args.city_code
file_name = args.file_name
election_year = args.election_year

# Acessar os valores passados para cada argumento
print(f"Nome do Candidato: {candidate_name}")
print(f"Código da Cidade: {city_code}")
print(f"Nome do Arquivo: {file_name}")
print(f"Ano da eleição: {election_year}\n")

section_place = section_places_locales[str(city_code)]

votation_data = get_votation_data(candidate_name, city_code, file_name, section_place)
votation_data_to_table = build_data_to_table(votation_data)

table_tab_title=f"Votação seções {candidate_name}"
table_title=f"Votação {candidate_name}"
file_name=f"Tabela_votacao_{election_year}_{candidate_name}"

build_excel_table(
  table_tab_title=table_tab_title,
  table_title=table_title,
  file_name=file_name,
  data=votation_data_to_table,
  data_total=["Total", "", votation_data['qtd_votes'], ""]
)
