# fake_news_detector/modules/preprocessing.py
import re
import unicodedata
from html import unescape

# small contractions map (expand as needed)
_CONTRACTIONS = {
    "don't": "do not", "won't": "will not", "can't": "cannot", "it's": "it is",
    "i'm": "i am", "you're": "you are", "he's": "he is", "she's": "she is",
    "they're": "they are", "we're": "we are", "isn't": "is not", "aren't": "are not",
    "didn't": "did not", "doesn't": "does not", "that's": "that is"
}

def expand_contractions(text: str) -> str:
    text = text
    for k, v in _CONTRACTIONS.items():
        text = re.sub(r"\b" + re.escape(k) + r"\b", v, text)
    return text

def simple_clean(text: str) -> str:
    """
    Lightweight cleaning:
    - normalize unicode
    - remove HTML tags, URLs, emails
    - expand small set of contractions
    - remove non-alphanumeric characters
    - collapse whitespace
    """
    if not isinstance(text, str):
        return ""
    # normalize
    text = unicodedata.normalize("NFKD", text)
    text = unescape(text)
    text = text.lower()

    # remove URLs and emails
    text = re.sub(r'http\S+|www\.\S+|mailto:\S+', " ", text)

    # remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)

    # expand contractions (optional)
    text = expand_contractions(text)

    # remove non-alphanumeric except spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)

    # collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text
