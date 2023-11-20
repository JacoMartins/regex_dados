import PyPDF2
import json
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

results = []

def extract_text_from_pdf(pdf_file: str) -> [str]:
    with open(pdf_file, 'rb') as pdf:
        reader = PyPDF2.PdfReader(pdf, strict=False)
        pdf_text = []

        for page in range(31, len(reader.pages)):
            content = reader.pages[page].extract_text()
            pdf_text.append(content)

        return pdf_text


wanted_word = str(input("Qual palavra você quer comparar? "))
# Sample input string
input_string = "".join(extract_text_from_pdf('mbdt.pdf'))

# Tokenization
tokens1 = word_tokenize(wanted_word)
tokens2 = word_tokenize(input_string)

# Combine tokenized words into sentences for TF-IDF
sentences = [wanted_word, input_string]

# Feature extraction using TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(sentences)

# Get feature names (words)
feature_names = list(vectorizer.get_feature_names_out())

# Compute cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

unique_words = set()

# Print the words and their TF-IDF weights for each sentence
for i, sentence in enumerate(sentences):
    print(f"\nTokens for Input String {i + 1}:")
    for j, word in enumerate(tokens1 if i == 0 else tokens2):
        word_index = feature_names.index(word) if word in feature_names else -1
        tfidf_weight = tfidf_matrix[i, word_index] if word_index != -1 else 0

        if word not in unique_words:
            results.append({
                "word": word,
                "weight": tfidf_weight
            })
            unique_words.add(word)

results.sort(key=lambda x: x['weight'], reverse=True)

with open('results.json', 'w', encoding="utf-8") as json_file:
    json_file.write(json.dumps(results, indent=2, ensure_ascii=False))
