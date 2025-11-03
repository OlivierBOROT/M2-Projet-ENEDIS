import nltk
from nltk.corpus import stopwords
nltk.download("stopwords", quiet=True)

STOP_WORDS_FR = list(set(stopwords.words("french")))
