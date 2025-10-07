# or next weeks assignment (due Oct. 6 at 11:59 pm), I'm asking for two things. Go ahead and put both of these in a notebook and create a PR in a folder such as 5_neural_nets.
#
# Create a function calculating the cosine similarity between two vectors. I'd like you to do this from first principles, meaning don't use a cosine similarity function from another package. Look to numpy or scipy python packages for some linear algebra functions. You can use cosine similarity functions to check your function.
# Build a neural net on any dataset of your choice (doesn't need to be NLP related). Kaggle has some great datasets for a start, or you can even make up your own with fake data. I mainly want to give you the chance to play around with PyTorch and different NN parameters, e.g. activation functions, number of layers, optimizers, generalization/regularization techniques such as dropout, etc.

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity as sk_cosine

def cosine_similarity(vec1, vec2):
    """
    Compute cosine similarity between two vectors.
    A dot B over Magnitude A times Magnitude B

    Parameters:
        vec1 (array-like): First vector.
        vec2 (array-like): Second vector.

    Returns:
        float: Cosine similarity between vec1 and vec2.
    """
    # Convert to NumPy arrays
    v1 = np.array(vec1)
    v2 = np.array(vec2)

    # Compute dot product using numpy
    dot_product = np.dot(v1, v2)

    # Compute magnitudes using numpy (norms)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)

    # Avoid division by zero
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0

    # Compute cosine similarity using formula
    return dot_product / (norm_v1 * norm_v2)


#Check function using sklearn
a = [1, 2, 3]
b = [4, 5, 6]

my_result = cosine_similarity(a, b)
#convert two vectors to format sklearn is good with
sk_result = sk_cosine([a], [b])[0,0]

print("My cosine similarity:", my_result)
print("sklearn cosine similarity:", sk_result)