__name__ = 'ngram_finder'
__version__ = '0.0.1'
__author__ = 'Lovit'

from ._util import Corpus
from ._skipngram import SkipNgramFinder
from ._simplengram import SimpleNgramFinder
from ._score import cohesion_score