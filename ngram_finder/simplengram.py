class SimpleNgramFinder:
    def __init__(self, n=4, min_count=10, tokenize=lambda x:x.split(), num_sents_for_pruning=10000, prune_min_count=2, verbose=True):
        assert type(n) == int
        self.n = n if n > 0 else 4
        self.min_count = min_count if min_count > 0 else 10
        self.tokenize = tokenize
        self.num_sents_for_pruning = num_sents_for_pruning
        self.prune_min_count = prune_min_count
        self.verbose = verbose
        self._c = {}
    
    def train(self, sentence_iterable_corpus, score_function=None, min_score=None):
        ngrams = self.scan_vocabs(sentence_iterable_corpus)
        if score_function == None:
            return ngrams
        return self.select_ngrams(ngrams, score_function, min_score)
    
    def scan_vocabs(self, sentence_iterable_corpus):
        import sys
        
        for i, sent in enumerate(sentence_iterable_corpus):
            words = self.tokenize(sent)
            ngrams = [tuple(words[b:b+w]) for w in range(1, self.n+1) for b in range(0, len(words) - w + 1)]
            for ngram in ngrams:
                self._c[ngram] = self._c.get(ngram, 0) + 1
            if (i > 0) and (self.num_sents_for_pruning > 0) and (i % self.num_sents_for_pruning == 0):
                self._c = {ngram:freq for ngram, freq in self._c.items() if freq >= self.prune_min_count}
            if self.verbose and i % 1000 == 0:
                args = (len(self._c), i+1, len(sentence_iterable_corpus))
                sys.stdout.write('scanning simple ngram ... # candidates= %d, (%d in %d)' % args)
        if self.verbose:
            print('\rscanning simple ngram was done')
        
        ngrams = {ngram:freq for ngram, freq in self._c.items() if freq >= self.min_count}
        return ngrams
    
    def select_ngrams(self, candidates, score_function, min_score):
        # Not implemented
        return candidates