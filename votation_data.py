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

def get_votation_data(candidate_name, city_code, file, file_sep=";", file_encoding='ISO-8859-1'):
  # Ler o arquivo CSV
  df = pd.read_csv(file, sep=file_sep, encoding=file_encoding)

  df['NM_VOTAVEL'] = df['NM_VOTAVEL'].str.strip()
  df_filtrado = df[(df['CD_MUNICIPIO'] == int(city_code)) & (df['NM_VOTAVEL'].str.contains(candidate_name, case=False, na=False))]

  candidate_votes_by_section_place = {}
  qtd_votes = 0

  for section_place in section_places:
    sections_numbers = section_places[section_place]
    candidate_votes_by_section_place[section_place] = {"sections": {}}
    
    for section_number in sections_numbers['sections']:
      votes_by_section = df_filtrado[df_filtrado['NR_SECAO'] == section_number]
      qtd_votes_by_section = votes_by_section['QT_VOTOS'].head(1).values
      qtd_votes_by_section = qtd_votes_by_section[0] if qtd_votes_by_section.size > 0 else 0
      
      candidate_votes_by_section_place[section_place]["sections"][str(section_number)] = int(qtd_votes_by_section)
      qtd_votes += qtd_votes_by_section
    
  
  return {
    'qtd_votes': qtd_votes,
    'candidate_votes_by_section_place': candidate_votes_by_section_place,
  }

def build_data_to_table(votation_data):
  candidate_votes_by_section_place = votation_data['candidate_votes_by_section_place']
  qtd_votes = votation_data['qtd_votes']
  votes_data = []

  for votes_by_place in candidate_votes_by_section_place:
    votes_total_in_place = 0
    vote_place_data = []
    
    votes_by_place_sections = candidate_votes_by_section_place[votes_by_place]['sections']
    for vote_place in votes_by_place_sections:
      votes = votes_by_place_sections[vote_place]
      vote_place_data.append(["", vote_place, votes, ""])
      votes_total_in_place += int(votes)
    
    votes_data.append([votes_by_place, "", "", votes_total_in_place])
    votes_data.extend(vote_place_data)

  print('Votes per sections', candidate_votes_by_section_place, qtd_votes)
  
  return votes_data
