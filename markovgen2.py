#!/usr/bin/python2.7

import random
import sys


class Markov(object):

    def __init__(self, open_file, ngram_size):
        self.cache = {}
        self.open_file = open(open_file, 'r')
        self.words = self.file_to_words()
        self.word_size = len(self.words)
        self.database(ngram_size)

    def file_to_words(self):
        self.open_file.seek(0)
        data = self.open_file.read()
        #data = data.lower()
        words = data.split()
        return words

    def quints(self, ngr):
        """ Generates ngrams from the given data string. So if our string were
        "What a lovely day", we'd generate (What, a, lovely) and then
        (a, lovely, day) and if longer so on and so forth
        """

        if len(self.words) < ngr:
            return
        for i in range(len(self.words) - ngr + 1):
            l = []
            for j in range(ngr):
                l.append(self.words[j+i])
            yield tuple(l)

    def database(self, ngram):
        for l in self.quints(ngram):
            key = l[:-1]
            if key in self.cache:
                self.cache[key].append(l[-1])
            else:
                self.cache[key] = [l[-1]]

    def generate_markov_text(self, size=25):
        ran_key = random.choice(self.cache.keys())
        words = list(ran_key)
        words.append('')  # the last element is the value
        gen_words = []
        for i in words[:-1]:
            gen_words.append(i)  # append the initial key

        for i in xrange(size):
            key = []
            for i in words[:-1]:
                key.append(i)
            key = tuple(key)
            words[-1] = random.choice(self.cache[key])
            gen_words.append(words[-1])  ## append new random word to output
            for i in range(len(words) - 1):  ## move it all on over
                words[i] = words[i+1]
        return ' '.join(gen_words)

    def unitTest(self):
        for r in self.quints(4):
            print r

mg = Markov('big', int(sys.argv[3]))
for i in xrange(int(sys.argv[1])):
    print mg.generate_markov_text(int(sys.argv[2])) + '\n'
    #mg.unitTest()
