import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')
STOPWORDS = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\s+', ' ', text)     # Normalize whitespace
    words = [word for word in text.split() if word not in STOPWORDS]
    return ' '.join(words)

def match_resume_to_jd(jd_text, resume_text):
    jd_clean = clean_text(jd_text)
    resume_clean = clean_text(resume_text)

    if not jd_clean or not resume_clean:
        return 0.0

    docs = [jd_clean, resume_clean]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=1000)
    tfidf = vectorizer.fit_transform(docs)
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])
    return float(score[0][0])
