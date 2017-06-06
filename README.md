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

Geometric average of conditional probability. cohesion('a-b-c') = {P('a-b'|'a') * P('a-b-c'|'a-b')}^(1/2)
