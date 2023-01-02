from nltk.tokenize import sent_tokenize, word_tokenize
from string import punctuation
from nltk.probability import FreqDist
from collections import defaultdict
from heapq import nlargest
import nltk
nltk.download("punkt")

with open("stopwords-it.txt", "r", encoding="UTF-8") as f:
    sw_list = list(map(str.strip, f.readlines()))
_stopwords = set(list(punctuation) + sw_list)


def get_frequencies(text: str):
    word_sent = word_tokenize(text.lower())
    word_sent = [word for word in word_sent if word not in _stopwords]
    freq = FreqDist(word_sent)
    return freq


def update_sent_raking(text):
    sents = sent_tokenize(text)
    ranking = defaultdict(int)
    freq = get_frequencies(text)
    for i, sent in enumerate(sents):
        for w in word_tokenize(sent.lower()):
            if w in freq:
                ranking[i] += freq[w]
    return ranking


def get_summary_sent_num_from_percent(text: str, summary_percentage: int = 50):
    sents_num = len(sent_tokenize(text))
    num = int(sents_num*summary_percentage/100)

    return num


def get_summary_percent_num_from_sent(text: str, num):
    sents_num = len(sent_tokenize(text))
    percent_desired_sent = int(num / sents_num * 100)
    return percent_desired_sent


def rules_summary(text, summary_percentage: int = 40):
    sents = sent_tokenize(text)
    ranking = update_sent_raking(text)
    sents_idx = nlargest(get_summary_sent_num_from_percent(text, summary_percentage), ranking, key=ranking.get)
    output = "\n".join([sents[j] for j in sorted(sents_idx)])
    print(output)
    return output