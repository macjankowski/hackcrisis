import pickle

import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class Word2VecClient:

    def __init__(self, model_path, facts_path):
        self.wv_from_text = pickle.load(open(model_path, "rb"))
        vocab = self.wv_from_text.wv.vocab
        self.all_words = []
        for k, v in vocab.items():
            self.all_words.append(k)

        self.stop_words = stopwords.words('polish')
        self.facts = pd.read_pickle(facts_path)

    def sentence_to_tokens(self, sentence):
        try:
            all_tokens = word_tokenize(sentence)
            tokens = [x for x in all_tokens if x not in self.stop_words]
            tokens = [x for x in tokens if x in self.all_words]

            all_tokens_lower = [x.lower() for x in all_tokens]
            tokens_lower = [x for x in all_tokens_lower if x not in self.stop_words]
            tokens_lower = [x for x in tokens_lower if x in self.all_words]

            return set(set(tokens) | set(tokens_lower))
        except:
            return []

    def calculate_score(self, query_tokens, candidate_tokens):
        if (len(query_tokens) > 0) & (len(candidate_tokens) > 0):
            return self.wv_from_text.n_similarity(query_tokens, candidate_tokens)
        else:
            return 0

    def find_top_matches(self, query_sentence, k=10):
        query_tokens = self.sentence_to_tokens(query_sentence)
        scores = [self.calculate_score(query_tokens, tokens) for tokens in self.facts['tokens']]
        facts_scores = self.facts[['text', 'source', 'is_true']].copy()
        facts_scores['score'] = scores
        result = facts_scores.sort_values(by=['score'], ascending=False).head(k)
        return result
