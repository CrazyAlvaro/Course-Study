import math, collections
from functools import reduce

class TrigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.unigram = collections.defaultdict(lambda: 0)
    self.bigram  = collections.defaultdict(lambda:
                            collections.defaultdict(lambda:0)
                          )
    self.trigram = collections.defaultdict(lambda:
                            collections.defaultdict(lambda:
                              collections.defaultdict(lambda:0)
                            )
                          )
    self.total = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model.
        Compute any counts or other corpus statistics in this function.
    """
    for sentence in corpus.corpus:
      prev_word = None
      prev_prev_word = None
      for datum in sentence.data:
        word = datum.word
        self.unigram[word] += 1

        # Update bigram count
        if prev_word != None:
          self.bigram[prev_word][word] += 1

        # Update trigram count
        if prev_prev_word != None:
          self.trigram[prev_prev_word][prev_word][word] += 1

        # Update variables
        prev_prev_word = prev_word
        prev_word = word

        self.total += 1

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0
    prev_prev_token = sentence[0]
    prev_token      = sentence[1]

    ########################################
    ## use unsmoothed trigram model combined
    ## with unsmoothed bigram model and
    ## add-1 smoothed unigram model,
    ########################################
    for token in sentence[2:]:
      trigram_count = self.trigram[prev_prev_token][prev_token][token]
      bigram_count  = self.bigram[prev_token][token]

      if trigram_count > 0:
        bitri_count = self.bigram[prev_prev_token][prev_token]
        score += math.log(trigram_count) - math.log(bitri_count)
      elif bigram_count > 0:
        # stupid backoff, use unsmoothed bigram model
        unibi_count = self.unigram[prev_token]
        score += math.log(bigram_count) - math.log(unibi_count)
      else:
        # stupid backoff, use add-one smoothed unigram
        score += math.log(self.unigram[token]+1) - math.log(self.total + len(sentence))

      prev_prev_token = prev_token
      prev_token = token

    return score