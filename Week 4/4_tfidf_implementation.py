"""
WEEK 4 Assignment

Code up two version of tf-idf:

1. Version 1: what I've been calling "traditional" (in your function implementation below when "smoothed" is False).
In scikit-learn this would be: TfidfVectorizer(norm=None, smooth_idf=False)

2. Version 2: what I've been calling "smoothed" (in your function implementation below when "smoothed" is True).
In scikit-learn this would be: TfidfVectorizer(norm=None)

Don't worry about implementing normalization for this assignment.

The output of the function should match the output of the scikit-learn version. So in particular, if we have
the following corpus:

corpus = [
    'This is the first document.',
    'This document is the second document.',
    'And this is the third one.',
    'Is this the first USU document?',
]

Then your version should equal the scikit-learn implementation (should be helpful for testing):

tf_idf(corpus) = TfidfVectorizer(norm=None, smooth_idf=False).fit_transform(corpus).toarray()

and

tf_idf(corpus, smoothed=True) = TfidfVectorizer(norm=None).fit_transform(corpus).toarray()
"""

import numpy as np
import math
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import re


def tf_idf(corpus: list[str], smoothed: bool = False) -> np.ndarray:

    #Tokenize and build vocabulary
    #Doing this step so that it looks the same as scikitlearn
    token_pattern = re.compile(r"(?u)\b\w\w+\b")
    tokenized = [token_pattern.findall(doc.lower()) for doc in corpus]
    vocab = sorted(set(word for doc in tokenized for word in doc))
    V, N = len(vocab), len(tokenized)

    #Compute term-frequency matrix
    tf = np.zeros((N, V), dtype=float)
    for i, doc in enumerate(tokenized):
        counts = Counter(doc)
        for j, term in enumerate(vocab):
            tf[i, j] = counts[term]

    #Compute IDF vector
    df = np.array([(sum(term in doc for doc in tokenized)) for term in vocab])
    if smoothed:
        idf = np.log((1 + N) / (1 + df)) + 1
    else:
        idf = np.log(N / df) + 1

    #Multiply TF by IDF
    return tf * idf


corpus = [
    'This is the first document.',
    'This document is the second document.',
    'And this is the third one.',
    'Is this the first USU document?',
]
# --- My implementation ---
my_unsmoothed = tf_idf(corpus, smoothed=False)
my_smoothed   = tf_idf(corpus, smoothed=True)

# --- scikit-learn reference ---
sk_unsmoothed = TfidfVectorizer(norm=None, smooth_idf=False).fit_transform(corpus).toarray()
sk_smoothed   = TfidfVectorizer(norm=None).fit_transform(corpus).toarray()

# Check for equality (allowing tiny floating-point tolerance)
print("Traditional match:",
      np.allclose(my_unsmoothed, sk_unsmoothed, atol=1e-8))
print("Smoothed match:",
      np.allclose(my_smoothed, sk_smoothed, atol=1e-8))