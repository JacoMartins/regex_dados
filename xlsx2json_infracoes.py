import openpyxl, json

wb = openpyxl.load_workbook('infracoes.xlsx')
sheet = wb['Infrações']

multas_json = json.loads(open('multas.json', 'r', encoding="utf-8").read())
new_json = []

def format_gravidade(gravidade):
    if gravidade == '---':
        return "Não aplicável"
    
    if 'Gravíss' in gravidade:
        return gravidade.split(" ")[0].replace('Gravíss', 'Gravíssima')
    else:
        return gravidade.split(" ")[0]

for row in range(2, sheet.max_row + 1):
    cod_enquadramento = f"{sheet['A' + str(row)].value}-{sheet['B' + str(row)].value}"
    tipificacao = sheet['C' + str(row)].value
    amparo = sheet['D' + str(row)].value
    infrator = sheet['E' + str(row)].value
    pontuacao, gravidade = sheet['F' + str(row)].value.split(' - ') if len(sheet['F' + str(row)].value.split(' - ')) == 2 else ["Não Computável", sheet['F' + str(row)].value]
    amplificador = gravidade.split(" ")[1] if len(gravidade.split(" ")) == 2 else ""
    gravidade_formatada = format_gravidade(gravidade)

    if "-" in tipificacao:
        desdobramentos = tipificacao.split(" - ")
        # if desdobramento starts with lowercase letter, split it by spaces and bring the first word. Then bring desdobramentos[0] and delete the word and all words after it. 
        for index, desdobramento in enumerate(desdobramentos):
            if desdobramento[0].islower():
                first_word = desdobramento.split(" ")[0]
                desdobramento = f"{desdobramentos[0].split(f'{first_word} ')[0]}{' ' if desdobramento[0] != '-' else ''}{desdobramento}"

            new_json.append({
                "Tipificação": desdobramento,
                "Código Enquadramento": cod_enquadramento[:-1] + str(index + 1),
                "Amparo": str(amparo),
                "Gravidade": gravidade_formatada,
                "Infrator": infrator,
                "Pontuação": pontuacao
            })
    else:
        new_json.append({
            "Tipificação": tipificacao,
            "Código Enquadramento": cod_enquadramento,
            "Amparo": str(amparo),
            "Gravidade": gravidade_formatada,
            "Infrator": infrator,
            "Pontuação": pontuacao
        })

for item in new_json:
    if item['Código Enquadramento'] not in [multa['Código Enquadramento'] for multa in multas_json]:
        multas_json.append(item)

sorted_multas_json = sorted(multas_json, key=lambda k: k['Código Enquadramento'])

with open('multas.json', 'w', encoding="utf-8") as outfile:
    json.dump(sorted_multas_json, outfile, indent=4, ensure_ascii=False)