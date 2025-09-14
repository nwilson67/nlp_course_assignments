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
    reader = PdfReader(pdf_file_location)
    full_text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            full_text += page_text + "\n"

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
    doc = nlp(text)

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



def lemmatizer(text: str) -> str:
    """
    Lemmatize sentence.
    :param text: original sentence, text to lemmatize
    :return: lemmatized text
    """



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

if __name__=="__main__":
    pdf_entity_extractor("stat_5810_6810_fall_2025_syllabus.pdf")

    entities = pdf_entity_extractor(
        "stat_5810_6810_fall_2025_syllabus.pdf",
        display_file_location="entities.html"
    )
    tokens = token_analyzer("stat_5810_6810_fall_2025_syllabus.pdf", display_file_location="tokens.html")
    #print(entities)
    print(tokens)
