import PyPDF2
import json

def extract_info_from_pdf(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfFileReader(file)
        
        # Initialize variables to store the information
        infringement_list = []

        # Loop through each page in the PDF
        for page_num in range(pdf_reader.numPages):
            # Get the text from the current page
            page = pdf_reader.getPage(page_num)
            text = page.extractText()

            # Extract information for each kind of infringement
            info = extract_infringement_info(text)
            if info:
                infringement_list.append(info)

    return infringement_list

def extract_infringement_info(text):
    # Define keywords to identify relevant sections
    keywords = ['Código do Enquadramento', 'Tipificação Resumida', 'Amparo Legal', 'Gravidade', 'Infrator', 'Pontuação']

    # Initialize a dictionary to store information for each kind of infringement
    infringement_info = {}

    # Loop through the keywords and extract relevant information
    for keyword in keywords:
        start_index = text.find(keyword)
        if start_index != -1:
            # Find the end of the line containing the keyword
            end_index = text.find('\n', start_index)
            
            # Extract the value after the colon
            value = text[start_index + len(keyword):end_index].strip()

            # Add the information to the dictionary
            infringement_info[keyword] = value

    # Check if all required information is present
    if all(key in infringement_info for key in keywords):
        return infringement_info
    else:
        return None

def main():
    pdf_path = 'mbdt.pdf'
    infringement_list = extract_info_from_pdf(pdf_path)

    # Convert the list of dictionaries to JSON
    json_data = json.dumps(infringement_list, indent=2)

    with open('multas.json', 'a') as json_file:
        json_file.write(json_data)

if __name__ == "__main__":
    main()
