"""
WEEK 2

- Assumes you've pip installed requirements file (pip install -r requirements.txt)
- Also need to download English trained pipeline https://spacy.io/models/en#en_core_web_sm. This can be done using
    `python -m spacy download en_core_web_sm` which downloads the model as another pip package essentially.
"""
from PyPDF2 import PdfReader
import spacy
from spacy import displacy

# Assumes this model is already downloaded
nlp = spacy.load("en_core_web_sm")

def read_pdf(pdf_file_location):
    reader = PdfReader(pdf_file_location)
    full_text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            full_text += page_text + "\n"
    return full_text

def pdf_entity_extractor(pdf_file_location, display_file_location: str = None) -> dict[str, list[str]]:
    """
    Return a dictionary of entities from a pdf. Optionally display entities via displacy.
    :param pdf_file_location: file location of the pdf to analyze.
    :param display_file_location: whether to display sentence with entities
    :return: dictionary of entities. Should be formmated like so:
        {
            "entity_label": ["list", "of", "entities"],
            ...
        }

        For example,

        {
            "ORG": ["USU", "BYU"],
            ...
        }

    """

    full_text = read_pdf(pdf_file_location)
    #This is the document
    doc = nlp(full_text)

    #Build Entity Dictionary
    entities: dict[str, set[str]] = {}
    for ent in doc.ents:
        entities.setdefault(ent.label_, set()).add(ent.text)

    entity_dict: dict[str, list[str]] = {
        label: sorted(list(vals)) for label, vals in entities.items()
    }

    if display_file_location:
        html = displacy.render(doc, style="ent", page=True)
        with open(display_file_location, "w", encoding="utf-8") as f:
            f.write(html)

    return entity_dict

def token_analyzer(text: str, display_file_location: str = None) -> dict:
    """
    Given a text string, split into tokens and return for each token:
        - the lemmatized version of each token,
        - the part of speech,
        - the shape,
        - whether alpha characters are present in the token
        - whether the token is a stop word

    :param text: sentence string to analyze.
    :param display_file_location: whether to display dependencies and pos
    :return: dictionary of tokens, formatted like this:
        {
            'token A': {
                'lemma': 'token A lemma',
                'pos': 'token A pos',
                'shape': 'token A shape',
                ...
            },
            'token B': {
                ...
            }
        }
    """
    full_text = read_pdf(text)
    doc = nlp(full_text)

    token_info: dict[str, dict[str, object]] = {}
    for token in doc:
        token_info[token.text] = {
            "lemma": token.lemma_,
            "pos": token.pos_,
            "shape": token.shape_,
            "is_alpha": token.is_alpha,
            "is_stop": token.is_stop
        }

    # Optional displaCy dependency visualization
    if display_file_location:
        html = displacy.render(doc, style="dep", page=True)
        with open(display_file_location, "w", encoding="utf-8") as f:
            f.write(html)

    return token_info



def remove_stop_words(text: str) -> str:
    """
    Remove stop words: https://spacy.io/usage/linguistic-features#language-data
    :param text: original sentence, text
    :return: same string, but without stop words
    """
    full_text = read_pdf(text)
    print(full_text)
    doc = nlp(full_text)
    final_text = ""
    for token in doc:
        if not token.is_stop:
            final_text += token.text + " "
    return final_text


def lemmatizer(text: str) -> str:
    """
    Lemmatize sentence.
    :param text: original sentence, text to lemmatize
    :return: lemmatized text
    """
    nlp = spacy.load("en_core_web_sm")
    full_text = read_pdf(text)
    doc = nlp(full_text)
    lemmas = ""

    # Print each token and its lemma
    for token in doc:
        lemmas += token.lemma_ + " "
    return lemmas



def create_character_tokenizer(training_text: str, text_to_tokenize: str) -> list[int]:
    """
    Given a training text corpus and the text to tokenize, first find a character level tokenization from the training
    text apply to the text to tokenize.

    For example:
    create_character_tokenizer('abcd', 'acb') -> [0,2,1]

    :param training_text: larger corpus of text to find a character level tokenization from.
    :param text_to_tokenize: text to tokenize using found character level tokenization.
    :return: list of the tokens.
    """

    # create an ordered mapping of char -> index based on first occurrence in training_text
    char_to_index: dict[str, int] = {}
    for ch in training_text:
        if ch not in char_to_index:
            char_to_index[ch] = len(char_to_index)

    # map each character in text_to_tokenize to its index
    # if a character is not in the vocabulary, raise an error (or handle as desired)
    encoded: list[int] = []
    for ch in text_to_tokenize:
        if ch not in char_to_index and ch != ' ':
            raise ValueError(f"Character '{ch}' not found in training vocabulary.")
        encoded.append(char_to_index[ch])

    return encoded

if __name__=="__main__":
    file_path = "stat_5810_6810_fall_2025_syllabus.pdf"

    entities = pdf_entity_extractor(
        file_path,
        display_file_location="entities.html"
    )
    tokens = token_analyzer(file_path, display_file_location="tokens.html")
    #print(entities)
    #print(tokens)
    #print(lemmatizer(file_path))
    #print(remove_stop_words(file_path))
    #print(create_character_tokenizer('abcdefghijklmnopqrstuvwxyz', 'hellohowareyoutoday'))
