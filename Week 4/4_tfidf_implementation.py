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

def tf_idf(corpus: list[str], smoothed: bool = False) -> np.array:
    pass