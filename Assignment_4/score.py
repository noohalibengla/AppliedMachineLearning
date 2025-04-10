import pickle
import numpy as np
from sklearn.base import BaseEstimator
import nltk
from nltk.corpus import stopwords
import string
from auxilary import simple_split



nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')



def clean_text(text):

    """ This converts the text to lowercase,
    tokenizes it, and removes stopwords, punctuation,
    and non-alphanumeric words"""

    text = str(text)
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    filtered_tokens = []
    for token in tokens:
        if token.isalnum() and token not in stopwords.words('english') and token not in string.punctuation:
            filtered_tokens.append(token)
    cleaned_text = ' '.join(filtered_tokens)

    return cleaned_text

def score(text: str, model: BaseEstimator, threshold: float) -> tuple[bool, float]:
    """
    Scores a trained model on a given text.
    
    Parameters:
    text (str): Input text to classify.
    model (sklearn.BaseEstimator): Trained model for prediction.
    threshold (float): Decision threshold for classification.
    
    Returns:
    tuple[bool, float]: (prediction, propensity)
        - prediction (bool): 1 if probability >= threshold, else 0.
        - propensity (float): Probability score from the model.

    """
    text = clean_text(text)
    # Transform text into feature format (assuming model expects vectorized input)
    with open("custom_vectorizer.pkl", "rb") as file:
        vectorizer = pickle.load(file)
    text_vector = vectorizer.transform([text])
    
    # Get model prediction probability
    probability = model.predict_proba(text_vector)[:, 1][0]  # Extract spam probability
    
    # Determine prediction based on threshold
    prediction = probability >= threshold
    
    return prediction, probability
