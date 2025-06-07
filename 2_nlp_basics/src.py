"""
WEEK 2

- First download English trained pipeline https://spacy.io/models/en#en_core_web_sm.
    This can be done using `python -m spacy download en_core_web_sm` which downloads the model as another pip package essentially.
"""
import logging

import spacy
from spacy import displacy


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Assumes this model is already downloaded
nlp = spacy.load("en_core_web_sm")


def doc_analyzer(sentence: str, display: bool = False) -> dict:
    """
    Return list of entities in a sentence. Optionally display entities via displacy.
    :param sentence: sentence string to analyze.
    :param display: whether to display sentence with entities
    :return: dictionary of entities and noun chunks (if any)
    """



def token_analyzer(sentence: str, display: bool = False) -> None:
    """
    Given a sentence display the following:
        - text, lemma_, part-of-speech tags
    :param sentence: sentence string to analyze.
    :param display: whether to display dependencies and pos
    :return:
    """



def remove_stop_words(sentence: str) -> str:
    """
    Remove stop words: https://spacy.io/usage/linguistic-features#language-data
    :param sentence: original sentence
    :return: string without stop words
    """



def lemmatizer(sentence: str) -> str:
    """
    Lemmatize sentence.
    :param sentence: original sentence to lemmatize
    :return: lemmatized sentence
    """


