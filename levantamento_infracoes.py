import json, openpyxl

workbook = openpyxl.load_workbook('tabela-infracoes.xlsx')

sheet = workbook['Infrações']

rows = []

for index, row in enumerate(sheet.iter_rows()):
    if index == 0:
        continue
    else:
        Pontuacao, GravidadeX = row[5].value.split(' - ')
        Gravidade, Multiplicador = GravidadeX.split(' ')

        row_dict = {
            "Código Enquadramento": row[0].value,
            "Desdobramento": row[1].value,
            "Tipificação": row[2].value,
            "Amparo": "Art. " + row[3].value,
            "Infrator": row[4].value,
            "Gravidade": row[5].value,
        }

        rows.append(row_dict)
            

multasbr_infracoes = []
infracoes_mbti = []

with open('multasbr_infracoes.json', 'r', encoding='utf-8') as file:
  multasbr_infracoes = json.loads(file.read())

with open('multas.json', 'r', encoding='utf-8') as file:
    infracoes_mbti = json.loads(file.read())

for infracao in infracoes_mbti:
    codigo = infracao['Código Enquadramento'].split('-')[0]
    desdobramento = infracao['Código Enquadramento'].split('-')[1]

    for multabr_infracao in multasbr_infracoes:
        if not (codigo == multabr_infracao['Código Enquadramento'] and desdobramento == multabr_infracao['Desdobramento']):
            infracoes_mbti.append({
                "Tipificação": multabr_infracao['Tipificação'],
                "Código Enquadramento": multabr_infracao['Código Enquadramento'] + '-' + multabr_infracao['Desdobramento'],
                "Amparo": "Art. " + multabr_infracao['Amparo'],
                "Gravidade": infracao['Gravidade'],
                "Infrator": infracao['Infrator'],
                "Pontuação": infracao['Pontuação'],
            })