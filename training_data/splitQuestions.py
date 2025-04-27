# This is a script to update the long bits of text in star_wars_data.jsonl into many smaller questions
# These questions need to have different formats

# pipeline to take these questions about x character
import json
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

filename = "processed_data/star_wars_data.jsonl"
with open(filename, 'r') as file:
    for line in file:
        data = json.loads(line)
        text = data['text']
        # chunk the data into paragraphs
        paragraphs = text.split("\n")
        # for each paragraph we will assess keywords
        for para in paragraphs:
            if len(para) < 20:
                continue
            # now find most unique/important ngrams (these could be the topic)
            tfidf = TfidfVectorizer(ngram_range=(2,3), stop_words='english')
            X = tfidf.fit_transform([text])
            ngrams = tfidf.get_feature_names_out()
            scores = X.toarray()[0]

            ranked_phrases = sorted(zip(ngrams, scores), key=lambda x: x[1], reverse=True)
            print(ranked_phrases[:5], para)

            

        