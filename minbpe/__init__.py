"""
MinBPE: Minimal Byte Pair Encoding Tokenizer Implementation

This package provides a clean, educational implementation of Byte Pair Encoding (BPE)
tokenization algorithms used in modern language models. It includes the base Tokenizer
class and utility functions for building custom tokenizers.

The package is designed to be:
- Educational: Clear, well-documented code for learning BPE
- Minimal: Focused implementation without unnecessary complexity
- Extensible: Easy to subclass and customize for specific needs

Examples
--------
>>> from minbpe import Tokenizer
>>> tokenizer = Tokenizer()
>>> print(f"Base vocabulary size: {len(tokenizer.vocab)}")
Base vocabulary size: 256

>>> from minbpe.base import get_pair_frequencies
>>> freqs = get_pair_frequencies([72, 101, 108, 108, 111])
>>> print(f"Byte pair frequencies: {freqs}")
Byte pair frequencies: {(72, 101): 1, (101, 108): 2, (108, 111): 1}

See Also
--------
minbpe.base : Core tokenizer implementation and utilities
"""

from .base import Tokenizer

__version__ = "0.1.0"
__all__ = ["Tokenizer"]