__name__ = 'ngramfinder'
__version__ = '0.0.1'
__author__ = 'Lovit'

from .utils import DoublespaceLineCorpus
from .skipngram import SkipNgramFinder
from .simplengram import SimpleNgramFinder
from .score import cohesion_score
