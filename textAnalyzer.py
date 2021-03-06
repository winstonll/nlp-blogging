import collections
import nltk
from textstat.textstat import textstat
import math
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class TextAnalyzer:

    def __init__(self, text):
        self.text = text
        self.tok = nltk.word_tokenize(self.text)
        self.nchar = len(self.text)
        self.nword = len(self.tok)

    def paragraph_counter(self):
        linecount = 0
        paragraph_count = 0
        for line in self.text:
            if line in ('\n', '\r\n'):
                if linecount == 0:
                    paragraph_count += 1
                    linecount += 1
                else:
                    linecount = 0
        return paragraph_count

    def lexical_diversity(self):
        lex = len(set(self.text))/self.nword
        return lex

    def descriptive_words_porp(self):
        freq = nltk.pos_tag(self.tok)
        count = [w[1] for w in freq]
        table = collections.Counter(count)
        sub_table = dict((k, table[k]) for k in ('JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS'))
        porp = sum(sub_table.values())/self.nword
        return porp

    def read_time(self):
        required_time = round(self.nword/275, 1)
        return required_time

    def reading_difficulty(self):
        diff_words = textstat.difficult_words(self.text)/self.nword
        flesch_kincaid = textstat.flesch_kincaid_grade(self.text)
        coleman_liau = textstat.coleman_liau_index(self.text)
        ari = textstat.automated_readability_index(self.text)
        dale_chall = textstat.dale_chall_readability_score(self.text)
        linsear = textstat.linsear_write_formula(self.text)
        gunning_fog = textstat.gunning_fog(self.text) - 6
        smog = textstat.smog_index(self.text)
        avg_grade = max(math.ceil((flesch_kincaid + coleman_liau + ari + dale_chall + linsear + gunning_fog + smog)/7), 12)
        return avg_grade, diff_words

    def sentiment(self):
        analyser = SentimentIntensityAnalyzer()
        sent = analyser.polarity_scores(self.text)
        return sent['pos']/(sent['neg'] + sent['neu'] + sent['pos'])