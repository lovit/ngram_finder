# Ngram Finder

## Candidate extraction methods

### Simple Ngram

It extracts all ngrams composed of sequential words. Configuration parameters are [ngram length: n, minimum count: min_count]

[i, was, a, hansome, boy] -> [i-was-a, was-a-hansome, ...]

### Skip Ngram

It extracts ngrams skipping infrequent middle words. Configuration parameters are [ngram length:n, minimum count: min_count, maximum window: max_window]. The maximum window must be larger than ngram length n.

[i, was, a, hansome, boy] -> [i-was-a, i-was-boy, ...]

## Score methods

### Cohesion score

Geometric average of conditional probability. cohesion(abc) = {P(ab|a) * P(abc|ab)}^(1/2)

    eg) '무단 - 배포 - 금지'

### Branching entropy

entropy of left/right-side expansion tokens

    eg) '에 - 대한' in [사건, 에, 대한, 의견] ...

### Mutual information

( count(wi, wj) - delta ) / ( count(wi) * count(wj) ) in Word2Vec paper

Three options for n >= 3 case; max, average, top3_average
