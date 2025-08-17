"""
MinBPE: Minimal Byte Pair Encoding Tokenizer Implementation

This package provides a clean, educational implementation of Byte Pair Encoding (BPE)
tokenization algorithms used in modern language models. It includes the base Tokenizer
class and utility functions for building custom tokenizers.

Examples
--------
>>> from minbpe import Tokenizer, BasicTokenizer
>>> # Create a basic tokenizer instance
>>> tokenizer = Tokenizer()
>>> print(f"Base vocabulary size: {len(tokenizer.vocab)}")
Base vocabulary size: 256

>>> # Use the BasicTokenizer for training
>>> basic_tokenizer = BasicTokenizer()
>>> basic_tokenizer.train("Hello world", 300)
>>> print(f"Trained vocabulary size: {len(basic_tokenizer.vocab)}")
>>> print(f"Number of merges: {len(basic_tokenizer.merges)}")

>>> from minbpe.base import get_pair_frequencies
>>> freqs = get_pair_frequencies([72, 101, 108, 108, 111])
>>> print(f"Byte pair frequencies: {freqs}")
Byte pair frequencies: {(72, 101): 1, (101, 108): 2, (108, 111): 1}

See Also
--------
minbpe.base : Core tokenizer implementation and utilities
minbpe.basic_tokenizer : Basic BPE implementation with training
"""

from .base import Tokenizer
from .basic_tokenizer import BasicTokenizer

__version__ = "0.1.0"
__all__ = ["Tokenizer", "BasicTokenizer"]