import json
import random
from itertools import chain
import os


def get_corpus(data):
  """
  get corpus from pushkin.json
  """
  THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
  data = os.path.join(THIS_FOLDER, data) # make absolute path
  with open(data, 'r') as f:
    corpus = json.load(f)
    return corpus


def n_gram(iter, index, length=10):
  """
  yield a string with maximum length = 20(10+10)
  if the size is too big, decrement length
  
  iter = string with length bigger than 50
  index = index of keyword
  length = 10
  """
  high = index + length
  low = index - length
  if high < len(iter) and low >= 0: # check high and low are in the range of iter
    yield iter[low:high]
  elif high < len(iter):            # to retrieve key word at the low index
    yield iter[index:high]
  elif low >= 0:                    # to retrieve key word at the high index
    yield iter[low:index]
  else:                             # if length is too big, decrement and recursive
    length -= 1
    n_gram(iter, index, length)
  
  
def word_in_pushkin(word, window=2):
  """
  yield fragment with the keyword
  length of fragment = 4(double window size)
  if fragment size with the keyword is bigger than 50, call n_gram function
  
  word - keyword
  """
  for works in get_corpus(r'pushkin.json'):
    work = list(chain.from_iterable(works.values())) # flatten nested list
    for i in range(len(work)):
      if word in work[i].lower():
        if len(work[i]) > 50:
          sent = work[i].split()  # convert a string to a list
          for k in range(len(sent)):
            if word in sent[k]:   # get an index of keyword and call n_gram func
              n_gram(sent, k)
        else:
          yield work[i-window:i+window]
          
def sample_work(works, num=3):
  fragments = None # to prevent error in the line 69
  try:
    samples = [x for x in works]
    for i in range(num):
      fragments = [sent for sent in random.sample(samples, i+1)] # 
    return fragments
  except ValueError:  
    if fragments: # if there's the keyword, but not in 3 fragments
      return fragments
    else:     # if there's not the keyword in the corpus
      return [['Даже Пушкин не знает обо всем...']]