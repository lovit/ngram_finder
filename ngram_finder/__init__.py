__name__ = 'ngram_finder'
__version__ = '0.0.1'
__author__ = 'Lovit'

from .util import DoublespaceLineCorpus
from .skipngram import SkipNgramFinder
from .simplengram import SimpleNgramFinder
from .score import cohesion_score