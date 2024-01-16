import PyPDF2
import re
import json

def extract_text_from_pdf(pdf_file: str) -> [str]:
    with open(pdf_file, 'rb') as pdf:
        reader = PyPDF2.PdfReader(pdf, strict=False)
        pdf_text = []

        for page in range(0, len(reader.pages)):
            content = reader.pages[page].extract_text()
            pdf_text.append(content)

        return pdf_text


def fix_spaces(text: str):
    removed_newlines = text.replace('\n', ' ')
    removed_spaces = re.sub(r"\s{2,}", "", removed_newlines)
    removed_spaces = removed_spaces.strip()
    
    return removed_spaces

def extract_info(text):
    pattern = r"CONSELHO NACIONAL DE TRÂNSITO(?:.*?)\nMANUAL BRASILEIRO DE FISCALIZAÇÃO DE TRÂNSITO(?:.*?)–(?:.*?)MBFT(?:.*?)\nFICHA DE FISCALIZAÇÃO(?:.*?)Tipificação Resumida:(?:\s\s|\s)(.*?)Código\s(?:do\s|de\s|d\so\s|do\s\s)?Enquadramento:(.*?)Amparo Legal:(.*?)Tipificação do Enquadramento:(.*?)Gravidade:(.*?)Penalida(?:\s)?d(?:\s)?e:(.*?)Medida Administrativa:(.*?)Pode Configurar Crime de \nTrânsito:(.*?)Infrator:(.*?)Competência(?:\s)?:(.*?)Pontuação(?:\s)?:(.*?)Constatação da Infração:(.*?)"
    remove_spaces_pattern = r"\s+"

    matches = re.findall(
        pattern,
        text,
        re.DOTALL
    )

    # Convert matches to a list of dictionaries

    print(matches[0])

    info_list = [
        {
            "Tipificação": fix_spaces(match[0][:-1]),
            "Código Enquadramento": re.sub(remove_spaces_pattern, '', match[1]).replace('-', '')[0:4] + '-' + re.sub(remove_spaces_pattern, '', match[1]).replace('-', '')[-1],
            "Amparo": fix_spaces(match[2][:-1]),
            "Gravidade": fix_spaces(match[4]),
            "Infrator": fix_spaces(match[8][:-1]),
            "Pontuação": fix_spaces(match[10].replace(' ', '') if re.match(r'[0-9]{1}', match[10]) else match[10][:-1]),
        }
        for match in matches
    ]


    return info_list

if __name__ == '__main__':
    pdf_text = "".join(extract_text_from_pdf('mbdt.pdf'))

    result_list = extract_info(pdf_text)

    # Convert the list of dictionaries to JSON
    result_json = json.dumps(result_list, indent=2, ensure_ascii=False)

    with open('multas.json', 'w', encoding="utf-8") as json_file:
        json_file.write(result_json)
