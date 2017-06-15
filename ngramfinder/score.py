from collections import namedtuple
from collections import defaultdict
from math import log

MutualInformationNgram = namedtuple('ngram', 'words length frequency score')
CohesionScoreNgram = namedtuple('ngram', 'words length frequency cohesion_forward cohesion_backward score')
BranchingEntropyNgram = namedtuple('ngram', 'words length frequency leftside_entropy rightside_entropy score')

def cohesion_score(counter, min_count=30, expansion_method='max'):
    def _max(cf, cb):
        return max(cf, cb)
    def _average(cf, cb):
        return (cf + cb) / 2
    
    ngrams = []
    for ngram, freq in counter.items():
        n = len(ngram)
        if n <=1 or freq < min_count: continue
        
        cohesion_forward = pow(freq / counter.get(tuple(ngram[:1]), 0), 1/(n-1))
        cohesion_backward = pow(freq / counter.get(tuple(ngram[-1:]), 0), 1/(n-1))
        
        if expansion_method == 'max': score = _max(cohesion_forward, cohesion_backward)
        elif expansion_method == 'average': score = _average(cohesion_forward, cohesion_backward)
        elif expansion_method == 'backward': score = cohesion_backward
        else: score = cohesion_forward
        
        ngrams.append(CohesionScoreNgram(' - '.join(ngram), 
                                         n, 
                                         freq, 
                                         cohesion_forward, 
                                         cohesion_backward,
                                         score))
    return ngrams

def branching_entropy(counter, min_count=10):
    def entropy(dic):
        if not dic: return 0.0
        sum_ = sum(dic.values())
        entropy = 0
        for freq in dic.values():
            prob = freq / sum_
            entropy += prob * log(prob)
        return -1 * entropy
    def parse_left(extension):
        return extension[:-1]
    def parse_right(extension):
        return extension[1:]
    def sort_by_length(counter, min_count):
        sorted_by_length = defaultdict(lambda: [])
        for ngram, freq in counter.items():
            if freq < min_count or len(ngram) <= 2: continue
            sorted_by_length[len(ngram)].append(ngram)
        return sorted_by_length
    def get_entropy_table(parse, sorted_by_length):        
        be = {}
        for n, ngram_list in sorted_by_length.items():
            extensions = defaultdict(lambda: [])
            for ngram in ngram_list:
                extensions[parse(ngram)].append(ngram)
            for ngram, extension_ngrams in extensions.items():
                extension_frequency = {ext:counter.get(ext, 0) for ext in extension_ngrams if ext in counter}
                be[ngram] = entropy(extension_frequency)
        return be

    sorted_by_length = sort_by_length(counter, min_count)
    be_l = get_entropy_table(parse_right, sorted_by_length)
    be_r = get_entropy_table(parse_left, sorted_by_length)
    bes = {ngram: (bel, be_r.get(ngram, 0)) for ngram, bel in be_l.items()}
    for ngram, ber in be_r.items():
        if not (ngram in be_l):
            bes[ngram] = (0, ber)
    
    ngrams = []
    for ngram, (bel, ber) in bes.items():
        ngrams.append(BranchingEntropyNgram(' - '.join(ngram), 
                                           len(ngram), 
                                           counter.get(ngram, 0), 
                                           bel, 
                                           ber, 
                                           bel*ber))
    return ngrams

def mutual_information(counter, delta=0.0, expansion_method='average'):
    def _average(scores):
        return 0 if not scores else sum(scores) / len(scores)
    def _max(scores):
        return 0 if not scores else max(scores)
    def _top3_average(scores):
        return 0 if not scores else sum(sorted(scores, reverse=True)[:3]) / min(3, len(scores))
    
    max_n = max([len(ngram) for ngram in counter.keys()])
    ngrams = []
    
    for ngram, ab in counter.items():
        if (len(ngram) == 1) or (ab <= delta):
            continue
        score_candidates = {}
        for i in range(1, len(ngram)):
            a = counter.get(tuple(ngram[:i]), 0)
            b = counter.get(tuple(ngram[i:]), 0)
            if (a == 0) or (b == 0):
                continue
            score = (ab - delta) / (a * b)
            if score > 0:
                score_candidates[i] = score
        
        if not score_candidates:
            continue
        
        if expansion_method == 'max':
            score = _max(score_candidates.values())
        elif expansion_method == 'top3_average':
            score = _top3_average(score_candidates.values())
        else:
            score = sum(score_candidates.values()) / len(score_candidates)
        
        ngrams.append(MutualInformationNgram(' - '.join(ngram), len(ngram), ab, score))    
    return ngrams