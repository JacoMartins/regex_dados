import PyPDF2
import re
import json


def extract_text_from_pdf(pdf_file: str) -> [str]:
    with open(pdf_file, 'rb') as pdf:
        reader = PyPDF2.PdfReader(pdf, strict=False)
        pdf_text = []

        for page in range(31, len(reader.pages)):
            content = reader.pages[page].extract_text()
            pdf_text.append(content)

        return pdf_text


def extract_info(text):
    pattern = r"CONSELHO NACIONAL DE TRÂNSITO \nMANUAL BRASILEIRO DE FISCALIZAÇÃO DE TRÂNSITO – MBFT \nFICHA DE FISCALIZAÇÃOTipificação Resumida: (.*?)Código do Enquadramento: (.*?)Amparo Legal: (.*?)Tipificação do Enquadramento: (.*?)Gravidade: (.*?)Penalidade: (.*?)Medida Administrativa: (.*?)Pode Configurar Crime de \nTrânsito: (.*?)Infrator: (.*?)Competência: (.*?)Pontuação: (.*?)Constatação da Infração: (.*?)"

    matches = re.findall(
        pattern,
        text,
        re.DOTALL
    )

    # Convert matches to a list of dictionaries

    print(matches[0])

    info_list = [
        {
            "Tipificação": match[0].replace('\n', ''),
            "Código Enquadramento": match[1].replace('\n', ''),
            "Amparo": match[2].replace('\n', ''),
            "Gravidade": match[4].replace('\n', ''),
            "Infrator": match[8].replace('\n', ''),
            "Pontuação": match[10].replace('\n', '')
        }
        for match in matches
    ]

    return info_list

if __name__ == '__main__':
    pdf_text = "".join(extract_text_from_pdf('mbdt.pdf'))

    # with open('multas.txt', 'w', encoding="utf-8") as txt_file:
    #     txt_file.write(pdf_text)

    result_list = extract_info(pdf_text)

    # Convert the list of dictionaries to JSON
    result_json = json.dumps(result_list, indent=2, ensure_ascii=False)

    with open('multas.json', 'a', encoding="utf-8") as json_file:
        json_file.write(result_json)
