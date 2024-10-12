import pandas as pd

from create_excel_table import build_excel_table

section_places = {
  "Curituba": {
    "sections": [7, 8, 16, 17, 61, 98, 122, 143]
  },
  "Olaria": {
    "sections": [80, 112, 113, 114, 119, 131, 148]
  },
  "Agrovila": {
    "sections": [85, 94, 100, 110, 127, 135, 120, 154, 147]
  },
  "Capim Grosso": {
    "sections": [3, 4, 5, 6, 12, 13, 14, 15, 54, 139, 151]
  },
  "Cuiabá": {
    "sections": [91, 155, 84, 111, 133]
  },
  "Canadá": {
    "sections": [99, 128]
  },
  "Delmiro": {
    "sections": [53, 56, 57, 59, 62, 64, 65, 67, 79, 82]
  },
  "Dom Juvêncio": {
    "sections": [9, 10, 11, 51, 52, 58, 63, 68, 77, 90]
  },
  "Maria Do Carmo": {
    "sections": [1, 2, 93, 95, 118, 132, 145]
  },
  "Trevo": {
    "sections": [96, 97, 101, 104, 106, 107, 108]
  },
  "João Marinho": {
    "sections": [103]
  }
}

# Ler o arquivo CSV
df = pd.read_csv('./files/1_turno_se_2024.csv', sep=";", encoding='ISO-8859-1')

year_votation = 2024
candidate_name = "Klebinho Feitosa"
city_code = "31232"

table_tab_title=f"Votação seções {candidate_name}"
table_title=f"Votação {candidate_name}"
file_name=f"Tabela_votacao_{year_votation}_{candidate_name}"

df['NM_VOTAVEL'] = df['NM_VOTAVEL'].str.strip()
df_filtrado = df[(df['CD_MUNICIPIO'] == int(city_code)) & (df['NM_VOTAVEL'].str.contains(candidate_name, case=False, na=False))]

# NR_ZONA
# NR_SECAO
# QT_VOTOS

councilior_votes_by_section_place = {}
qtd_votes = 0

for section_place in section_places:
  sections_numbers = section_places[section_place]
  councilior_votes_by_section_place[section_place] = {"sections": {}}
  
  for section_number in sections_numbers['sections']:
    votes_by_section = df_filtrado[df_filtrado['NR_SECAO'] == section_number]
    qtd_votes_by_section = votes_by_section['QT_VOTOS'].head(1).values
    qtd_votes_by_section = qtd_votes_by_section[0] if qtd_votes_by_section.size > 0 else 0
    
    councilior_votes_by_section_place[section_place]["sections"][str(section_number)] = int(qtd_votes_by_section)
    
    qtd_votes += qtd_votes_by_section

votes_data = []

for votes_by_place in councilior_votes_by_section_place:
  votes_total_in_place = 0
  vote_place_data = []
  
  votes_by_place_sections = councilior_votes_by_section_place[votes_by_place]['sections']
  for vote_place in votes_by_place_sections:
    votes = votes_by_place_sections[vote_place]
    vote_place_data.append(["", vote_place, votes, ""])
    votes_total_in_place += int(votes)
  
  votes_data.append([votes_by_place, "", "", votes_total_in_place])
  votes_data.extend(vote_place_data)

print('Votes per sections', councilior_votes_by_section_place)

build_excel_table(
  table_tab_title=table_tab_title,
  table_title=table_title,
  file_name=file_name,
  data=votes_data,
  data_total=["Total", "", qtd_votes, ""]
)
