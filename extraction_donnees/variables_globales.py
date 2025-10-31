import nltk
nltk.download("stopwords", quiet=True)

STOP_WORDS_FR = list(set(nltk.corpus.stopwords.words("french")))
DEBUG = 1
