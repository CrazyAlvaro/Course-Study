import math, collections
from functools import reduce

class StupidBackoffLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.unigram_counts = collections.defaultdict(lambda: 0)
    self.bigram_counts  = collections.defaultdict(lambda: collections.defaultdict(lambda:0))
    self.total = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model.
        Compute any counts or other corpus statistics in this function.
    """
    for sentence in corpus.corpus:
      prev_word = None
      for datum in sentence.data:
        word = datum.word
        self.unigram_counts[word] += 1

        # Update bigram count
        if prev_word == None:
          prev_word = word
          continue
        else:
          self.bigram_counts[prev_word][word] += 1
          prev_word = word

        self.total += 1

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0
    prev_token = sentence[0]

    ########################################
    ## use unsmoothed bigram model combined
    ## with add-1 smoothed unigram model,
    ########################################
    for token in sentence[1:]:
      bigram_count  = self.bigram_counts[prev_token][token]

      if bigram_count > 0:
        unigram_count = self.unigram_counts[prev_token]
        score += math.log(bigram_count) - math.log(unigram_count)
      else:
        # stupid backoff, use add-one smoothed unigram
        score += math.log(self.unigram_counts[token]+1) - math.log(self.total + len(sentence))

      prev_token = token

    return score
