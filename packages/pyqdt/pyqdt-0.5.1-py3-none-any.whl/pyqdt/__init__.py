# -*- coding: utf-8 -*-

from .wraps import *
from .quote_base import *
from .quote_data import *
from .quote_archive import *
# from .technical_analysis import *
import multiprocessing

try:
    if multiprocessing.get_start_method() != 'spawn':
        multiprocessing.set_start_method('spawn')
except:
    pass

__version__ = '0.5.1'

__all__ = [
    'JQWraps',
    'QuoteData',
    'QuoteArchive',
    '__version__'
]
