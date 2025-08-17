"""
Minimal Implementation of BPE Tokenizer.

This module provides a basic Byte Pair Encoding (BPE) tokenizer implementation
that doesn't handle regex splitting or special tokens. It implements the core
BPE algorithm for learning merge operations from text data.

Examples
--------
>>> from minbpe.basic_tokenizer import BasicTokenizer
>>> # Create and train a basic tokenizer
>>> tokenizer = BasicTokenizer()
>>> text = "Hello world! This is a test of the BPE algorithm."
>>> tokenizer.train(text, vocab_size=300, verbose=True)
>>> 
>>> # Encode and decode text
>>> encoded = tokenizer.encode("Hello world!")
>>> print(f"Encoded: {encoded}")
>>> decoded = tokenizer.decode(encoded)
>>> print(f"Decoded: {decoded}")

See Also
--------
minbpe.base.Tokenizer : Base tokenizer class
minbpe.base.get_pair_frequencies : Calculate byte pair frequencies
minbpe.base.merge_pair : Merge byte pairs in sequences
"""

from .base import Tokenizer, get_pair_frequencies, merge_pair
from typing import List

class BasicTokenizer(Tokenizer):
    """Basic BPE Tokenizer implementation.
    
    This tokenizer implements the core Byte Pair Encoding algorithm without
    regex splitting or special token handling. It learns merge operations
    by iteratively finding the most frequent byte pairs and merging them
    into new vocabulary tokens.
    
    Attributes
    ----------
    merges : dict
        Dictionary mapping byte pairs to their merged indices.
    vocab : dict
        Complete vocabulary mapping indices to byte sequences.
        
    Examples
    --------
    >>> tokenizer = BasicTokenizer()
    >>> tokenizer.train("Hello world", 300)
    >>> print(f"Vocabulary size: {len(tokenizer.vocab)}")
    >>> print(f"Number of merges: {len(tokenizer.merges)}")
    
    Notes
    -----
    This implementation:
    - Starts with a base vocabulary of 256 bytes (0-255)
    - Learns merge operations through frequency analysis
    - Builds vocabulary incrementally during training
    - Uses simple byte-level encoding without regex patterns
    """
    
    def __init__(self):
        """Initialize a new BasicTokenizer instance.
        
        Sets up an empty tokenizer with no learned merges.
        The base vocabulary of 256 bytes is created during training.
        """
        super().__init__()
        
    def train(self, text: str, vocab_size: int, verbose: bool = False) -> None:
        """Train the tokenizer on input text using BPE algorithm.
        
        This method implements the core BPE training algorithm:
        1. Convert text to byte indices
        2. Iteratively find most frequent byte pairs
        3. Merge pairs into new vocabulary tokens
        4. Update vocabulary and merge mappings
        
        Parameters
        ----------
        text : str
            Input text corpus to train the tokenizer on.
        vocab_size : int
            Target vocabulary size. Must be at least 256.
        verbose : bool, optional
            Whether to print training progress, by default False.
            
        Raises
        ------
        AssertionError
            If vocab_size is less than 256.
            
        Examples
        --------
        >>> tokenizer = BasicTokenizer()
        >>> # Train on a simple text
        >>> text = "Hello world! This is a test."
        >>> tokenizer.train(text, vocab_size=300, verbose=True)
        >>> print(f"Final vocab size: {len(tokenizer.vocab)}")
        >>> print(f"Number of merges learned: {len(tokenizer.merges)}")
        
        >>> # Train on longer text
        >>> long_text = "The quick brown fox jumps over the lazy dog. " * 10
        >>> tokenizer.train(long_text, vocab_size=500)
        >>> print(f"Vocabulary size: {len(tokenizer.vocab)}")
        
        Notes
        -----
        The training process:
        - Starts with base vocabulary of 256 bytes
        - Finds most frequent adjacent byte pairs
        - Merges pairs into new tokens with indices 256+
        - Continues until target vocabulary size is reached
        """
        assert vocab_size >= 256, "Vocab size must be at least 256"
        
        # How many merges to do?
        n_merges = vocab_size - 256
        if verbose:
            print(f"Training tokenizer with {n_merges} merges")
            
        # input text processing
        text_bytes = text.encode("utf-8")
        indices = list(text_bytes)  # list of integers from 0 to 255
        
        # build merges
        merges = {}
        # Build the initial vocabulary
        vocab = {idx: bytes([idx]) for idx in range(256)}
        for i in range(n_merges):
            idx = 256 + i
            byte_pair_freqs = get_pair_frequencies(indices)
            max_freq_pair = max(byte_pair_freqs.keys(), key=lambda p: byte_pair_freqs[p])
            merges[max_freq_pair] = idx
            indices = merge_pair(indices, max_freq_pair, idx)
            vocab[idx] = vocab[max_freq_pair[0]] + vocab[max_freq_pair[1]]
            if verbose:
                print(f"Merged {max_freq_pair} into {idx}")
            
        # Set attributes
        self.merges = merges
        self.vocab = vocab
    
    def decode(self, ids: List[int]) -> str:
        """Decode a list of token indices back to text.
        
        This method reconstructs the original text by looking up each
        token index in the vocabulary and concatenating the byte sequences.
        
        Parameters
        ----------
        ids : List[int]
            List of integer token indices to decode.
            
        Returns
        -------
        str
            Reconstructed text string.
            
        Examples
        --------
        >>> tokenizer = BasicTokenizer()
        >>> tokenizer.train("Hello world", 300)
        >>> 
        >>> # Decode some token indices
        >>> encoded = tokenizer.encode("Hello")
        >>> print(f"Encoded tokens: {encoded}")
        >>> decoded = tokenizer.decode(encoded)
        >>> print(f"Decoded text: {decoded}")
        
        >>> # Decode with unknown tokens (handled gracefully)
        >>> unknown_tokens = [72, 101, 108, 108, 111, 999]  # "Hello" + unknown
        >>> try:
        ...     decoded = tokenizer.decode(unknown_tokens)
        ... except KeyError as e:
        ...     print(f"Unknown token found: {e}")
        
        Notes
        -----
        - Uses UTF-8 decoding with error handling
        - Unknown token indices will raise KeyError
        - Decoding is deterministic and reversible
        """
        text_bytes = b"".join(self.vocab[idx] for idx in ids)
        text = text_bytes.decode("utf-8", errors="replace")
        return text
    
    def encode(self, text: str) -> List[int]:
        """Encode a text string into a list of token indices.
        
        This method implements the BPE encoding algorithm by iteratively
        applying learned merge operations to the input text. It finds
        the lowest-index merge operations and applies them until no
        more merges are possible.
        
        Parameters
        ----------
        text : str
            Input text string to encode.
            
        Returns
        -------
        List[int]
            List of integer token indices representing the encoded text.
            
        Examples
        --------
        >>> tokenizer = BasicTokenizer()
        >>> tokenizer.train("Hello world! This is a test.", 300)
        >>> 
        >>> # Encode simple text
        >>> encoded = tokenizer.encode("Hello")
        >>> print(f"Encoded: {encoded}")
        >>> print(f"Number of tokens: {len(encoded)}")
        
        >>> # Encode longer text
        >>> long_text = "The quick brown fox jumps over the lazy dog."
        >>> encoded = tokenizer.encode(long_text)
        >>> print(f"Original length: {len(long_text)}")
        >>> print(f"Encoded tokens: {len(encoded)}")
        >>> print(f"Compression ratio: {len(long_text) / len(encoded):.2f}")
        
        >>> # Encode text with repeated patterns
        >>> repeated = "Hello " * 5 + "World " * 3
        >>> encoded = tokenizer.encode(repeated)
        >>> print(f"Repeated text encoded to {len(encoded)} tokens")
        
        Notes
        -----
        The encoding process:
        1. Convert text to byte indices
        2. Find pairs with lowest merge indices
        3. Apply merges iteratively
        4. Stop when no more merges are possible
        
        The algorithm prioritizes learned merge operations
        based on their training order (lower indices = learned earlier).
        """
        text_bytes = text.encode("utf-8")
        indices = list(text_bytes)
        while len(indices) >= 2:
            # find the pair with the lowest merge index
            byte_pair_freqs = get_pair_frequencies(indices)
            pair = min(byte_pair_freqs, key=lambda p: self.merges.get(p, float("inf")))
            # If there are no merges, every pair has an infinite merge index.
            # So we can break out of the loop if the min returns an infinite merge index.
            if pair not in self.merges:
                break  # nothing can be merged anymore
            # if we can merge a pair, do it
            idx = self.merges[pair]
            indices = merge_pair(indices, pair, idx)
        return indices
    
    
            
        
            
        
        