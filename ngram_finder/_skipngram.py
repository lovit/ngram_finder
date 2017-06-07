class SkipNgramFinder:
    def __init__(self, n=4, min_count=10, max_window=6, max_num_skip=2, tokenize=lambda x:x.split(), num_sents_for_pruning=10000, prune_min_count=2, verbose=True):
        assert type(n) == int
        assert type(max_window) == int
        
        self.n = n if n > 0 else 4
        self.min_count = min_count if min_count > 0 else 10
        self.max_window = max_window
        self.max_num_skip = max_num_skip
        self.tokenize = tokenize
        self.num_sents_for_pruning = num_sents_for_pruning
        self.prune_min_count = prune_min_count
        self.verbose = verbose
        
        self._c = {}
        self._templateset={}
        
    def train(self, sentence_iterable_corpus, score_function=None, min_score=None):
        ngrams = self.scan_vocabs(sentence_iterable_corpus)
        if score_function == None:
            return ngrams
        return self.select_ngrams(ngrams, score_function, min_score)
    
    def scan_vocabs(self, sentence_iterable_corpus):
        import sys
        
        for i, sent in enumerate(sentence_iterable_corpus):
            words = self.tokenize(sent)
            wl = len(words)
            ngrams = [(word,) for word in words]
            ngrams += [tuple([words[i] for i in template]) for template in self._get_templates(wl)]
            
            for ngram in ngrams:
                self._c[ngram] = self._c.get(ngram, 0) + 1
            if (i > 0) and (self.num_sents_for_pruning > 0) and (i % self.num_sents_for_pruning == 0):
                self._c = {ngram:freq for ngram, freq in self._c.items() if freq >= self.prune_min_count}
            if self.verbose and i % 1000 == 0:
                args = (len(self._c), i+1, len(sentence_iterable_corpus))
                sys.stdout.write('scanning skip ngram ... # candidates= %d, (%d in %d)' % args)
        if self.verbose:
            print('\rscanning skip ngram was done')
        
        ngrams = {ngram:freq for ngram, freq in self._c.items() if freq >= self.min_count}
        return ngrams

    def _get_templates(self, length):
        from itertools import combinations
        if length in self._templateset:
            return self._templateset[length]

        words_idx = list(range(length))
        idxs = set()
        for w in range(2, min(self.max_window, length)+1):
            for b in range(length-w+1):
                in_window = words_idx[b:b+w]
                for n in range(max(2, w-self.max_num_skip), min(w, 4)+1):
                    idxs.update(set(combinations(in_window, n)))
        self._templateset[length] = sorted(idxs)
        return idxs

    def _is_ordered_sublist(self, sub, expanded):
        if len(sub) >= len(expanded):
            return False
        for subitem in sub:
            if not expanded:
                return False
            matched = -1
            for i, expanditem in enumerate(expanded):
                if subitem == expanditem:
                    matched = i
                    break
            if matched == -1:
                return False
            expanded = expanded[matched+1:]
        return True

    def _parse_ordered_sublist(self, item, n):
        from itertools import combinations
        return combinations(item, n)
    
    def select_ngrams(self, candidates, score_function, min_score):
        # Not implemented
        return candidates