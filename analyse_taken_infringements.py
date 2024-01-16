import json

infracoes = []
multas = {}

with open('multas.json', 'r', encoding='utf-8') as file:
  infracoes = json.loads(file.read())

for infracao in infracoes:
  multas[infracao['Tipificação']] = infracao['Código Enquadramento']

with open('multas_tipificadas.json', 'w', encoding='utf-8') as file:
  file.write(json.dumps(multas, indent=2, ensure_ascii=False))