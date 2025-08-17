"""
Minimal BPE Tokenizer with Regex Splitting.

This module provides a regex-based Byte Pair Encoding (BPE) tokenizer implementation
that handles regex splitting and special tokens. It implements the GPT-2 and GPT-4
style text segmentation patterns for improved tokenization quality.

Examples
--------
>>> from minbpe.regex_tokenizer import RegexTokenizer
>>> # Create a regex tokenizer with default GPT-4 pattern
>>> tokenizer = RegexTokenizer()
>>> text = "Hello world! This is a test of the regex BPE algorithm."
>>> tokenizer.train(text, vocab_size=300, verbose=True)
>>> 
>>> # Encode and decode text
>>> encoded = tokenizer.encode("Hello world!")
>>> print(f"Encoded: {encoded}")
>>> decoded = tokenizer.decode(encoded)
>>> print(f"Decoded: {decoded}")
>>> 
>>> # Use with special tokens
>>> tokenizer.register_special_tokens({"<|endoftext|>": 100257})
>>> encoded = tokenizer.encode("Hello <|endoftext|>", allowed_special_tokens="all")

See Also
--------
minbpe.base.Tokenizer : Base tokenizer class
minbpe.base.get_pair_frequencies : Calculate byte pair frequencies
minbpe.base.merge_pair : Merge byte pairs in sequences
minbpe.basic_tokenizer.BasicTokenizer : Basic BPE implementation
"""

from .base import Tokenizer, get_pair_frequencies, merge_pair
import regex as re
from typing import List, Dict, Union, Set, Optional

# Predefined regex patterns for text segmentation
GPT2_SPLIT_PATTERN = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
GPT4_SPLIT_PATTERN = r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+"""

class RegexTokenizer(Tokenizer):
    """Regex-based BPE Tokenizer with special token support.
    
    This tokenizer extends the basic BPE algorithm with regex-based text
    segmentation and special token handling. It uses predefined patterns
    (GPT-2 or GPT-4 style) to split text into meaningful chunks before
    applying BPE merges, resulting in higher quality tokenization.
    
    Attributes
    ----------
    pattern : str
        Regex pattern used for text segmentation.
    compiled_pattern : regex.Pattern
        Compiled regex pattern for efficient matching.
    special_tokens : Dict[str, int]
        Dictionary mapping special token strings to their indices.
    inverse_special_tokens : Dict[int, str]
        Inverse mapping from indices to special token strings.
        
    Examples
    --------
    >>> tokenizer = RegexTokenizer()
    >>> print(f"Using pattern: {tokenizer.pattern[:50]}...")
    >>> print(f"Special tokens: {len(tokenizer.special_tokens)}")
    
    >>> # Custom pattern
    >>> custom_tokenizer = RegexTokenizer(r"\w+|\s+|[^\w\s]")
    >>> custom_tokenizer.train("Hello world!", 300)
    
    Notes
    -----
    This implementation:
    - Uses regex patterns for intelligent text segmentation
    - Supports GPT-2 and GPT-4 style patterns by default
    - Handles special tokens with flexible encoding options
    - Applies BPE merges within regex-defined chunks
    - Maintains compatibility with the base Tokenizer interface
    """
    
    def __init__(self, split_pattern: Optional[str] = None):
        """Initialize a new RegexTokenizer instance.
        
        Parameters
        ----------
        split_pattern : str, optional
            Custom regex pattern for text segmentation. If None, uses
            the default GPT-4 pattern.
            
        Examples
        --------
        >>> # Default GPT-4 pattern
        >>> tokenizer = RegexTokenizer()
        >>> print(f"Pattern: {tokenizer.pattern[:30]}...")
        
        >>> # Custom pattern for simple word splitting
        >>> custom = RegexTokenizer(r"\w+|\s+")
        >>> print(f"Custom pattern: {custom.pattern}")
        
        Notes
        -----
        The default GPT-4 pattern handles:
        - Contractions (e.g., "don't", "can't")
        - Words with optional prefixes
        - Numbers (1-3 digits)
        - Punctuation and special characters
        - Whitespace and newlines
        """
        super().__init__()
        self.pattern = GPT4_SPLIT_PATTERN if split_pattern is None else split_pattern
        self.compiled_pattern = re.compile(self.pattern)
        self.special_tokens = {}
        self.inverse_special_tokens = {}
        
    def train(self, text: str, vocab_size: int, verbose: bool = False) -> None:
        """Train the tokenizer on input text using regex-based BPE algorithm.
        
        This method implements the regex-enhanced BPE training algorithm:
        1. Split text into chunks using regex pattern
        2. Convert chunks to byte indices
        3. Iteratively find most frequent byte pairs across all chunks
        4. Merge pairs into new vocabulary tokens
        5. Update vocabulary and merge mappings
        
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
        >>> tokenizer = RegexTokenizer()
        >>> # Train on simple text
        >>> text = "Hello world! This is a test."
        >>> tokenizer.train(text, vocab_size=300, verbose=True)
        >>> print(f"Final vocab size: {len(tokenizer.vocab)}")
        >>> print(f"Number of merges learned: {len(tokenizer.merges)}")
        
        >>> # Train on longer text with regex chunks
        >>> long_text = "The quick brown fox jumps over the lazy dog. " * 10
        >>> tokenizer.train(long_text, vocab_size=500)
        >>> print(f"Vocabulary size: {len(tokenizer.vocab)}")
        
        Notes
        -----
        The training process:
        - Splits text using regex pattern into meaningful chunks
        - Applies BPE merges within each chunk independently
        - Aggregates pair frequencies across all chunks
        - Learns merges that work well with the regex segmentation
        - Results in higher quality tokenization than byte-level BPE
        """
        assert vocab_size >= 256, "Vocab size must be at least 256"
        
        # How many merges to do?
        n_merges = vocab_size - 256
        if verbose:
            print(f"Training tokenizer with {n_merges} merges")
        
        # Split the text into chunks
        text_chunks = re.findall(self.compiled_pattern, text)
        
        # input text processing
        indices = [list(chunk.encode("utf-8")) for chunk in text_chunks]  # list of integers from 0 to 255
        
        # build merges
        merges = {}
        # Build the initial vocabulary
        vocab = {idx: bytes([idx]) for idx in range(256)}
        for i in range(n_merges):
            idx = 256 + i
            byte_pair_freqs = {}
            for chunk_ids in indices:
                get_pair_frequencies(chunk_ids, byte_pair_freqs)
            max_freq_pair = max(byte_pair_freqs.keys(), key=lambda p: byte_pair_freqs[p])
            # replace all occurences of pair with new index
            indices = [merge_pair(chunk_ids, max_freq_pair, idx) for chunk_ids in indices]
            merges[max_freq_pair] = idx
            vocab[idx] = vocab[max_freq_pair[0]] + vocab[max_freq_pair[1]]
            if verbose:
                print(f'Merge {i+1}/{n_merges}: {max_freq_pair} -> {idx} had {byte_pair_freqs[max_freq_pair]} occurrences')
            
        # Set attributes
        self.merges = merges  # encode()
        self.vocab = vocab  # decode()
        
    def register_special_tokens(self, special_tokens: Dict[str, int]) -> None:
        """Register special tokens for the tokenizer.
        
        Special tokens are reserved vocabulary items that have specific
        meanings (e.g., end-of-text, padding, unknown tokens). They are
        handled specially during encoding and decoding.
        
        Parameters
        ----------
        special_tokens : Dict[str, int]
            Dictionary mapping special token strings to their indices.
            Example: {"<|endoftext|>": 100257, "<|pad|>": 100258}
            
        Examples
        --------
        >>> tokenizer = RegexTokenizer()
        >>> # Register common special tokens
        >>> specials = {
        ...     "<|endoftext|>": 100257,
        ...     "<|pad|>": 100258,
        ...     "<|unk|>": 100259
        ... }
        >>> tokenizer.register_special_tokens(specials)
        >>> print(f"Registered {len(tokenizer.special_tokens)} special tokens")
        
        >>> # Check inverse mapping
        >>> print(f"Index 100257 maps to: {tokenizer.inverse_special_tokens[100257]}")
        
        Notes
        -----
        - Special tokens are added to both forward and inverse mappings
        - They are handled specially during encoding/decoding
        - Indices should not conflict with learned BPE tokens
        - Common practice is to use high indices (e.g., 100000+)
        """
        self.special_tokens = special_tokens
        self.inverse_special_tokens = {v: k for k, v in special_tokens.items()}
    
    def decode(self, ids: List[int]) -> str:
        """Decode a list of token indices back to text.
        
        This method reconstructs the original text by looking up each
        token index in the vocabulary or special tokens mapping.
        
        Parameters
        ----------
        ids : List[int]
            List of integer token indices to decode.
            
        Returns
        -------
        str
            Reconstructed text string.
            
        Raises
        ------
        ValueError
            If an unknown token index is encountered.
            
        Examples
        --------
        >>> tokenizer = RegexTokenizer()
        >>> tokenizer.train("Hello world", 300)
        >>> 
        >>> # Decode regular tokens
        >>> encoded = tokenizer.encode("Hello")
        >>> decoded = tokenizer.decode(encoded)
        >>> print(f"Decoded: {decoded}")
        
        >>> # Decode with special tokens
        >>> tokenizer.register_special_tokens({"<|endoftext|>": 100257})
        >>> special_ids = [100257]  # Special token
        >>> decoded = tokenizer.decode(special_ids)
        >>> print(f"Special token decoded: {decoded}")
        
        >>> # Handle unknown tokens
        >>> try:
        ...     decoded = tokenizer.decode([99999])  # Unknown index
        ... except ValueError as e:
        ...     print(f"Error: {e}")
        
        Notes
        -----
        - Regular tokens are looked up in the vocabulary
        - Special tokens are looked up in inverse_special_tokens
        - Unknown indices raise ValueError
        - Decoding is deterministic and reversible
        """
        part_bytes = []
        for idx in ids:
            if idx in self.vocab:
                part_bytes.append(self.vocab[idx])
            elif idx in self.inverse_special_tokens:
                part_bytes.append(self.inverse_special_tokens[idx].encode("utf-8"))
            else:
                raise ValueError(f"Unknown token index: {idx}")
        text_bytes = b"".join(part_bytes)
        text = text_bytes.decode("utf-8", errors="replace")
        return text
    
    def _encode_chunk(self, text_bytes: str) -> List[int]:
        """Encode a single text chunk using BPE algorithm.
        
        This internal method applies the BPE encoding algorithm to a
        single chunk of text, finding and applying merge operations
        until no more merges are possible.
        
        Parameters
        ----------
        text_bytes : str
            Text chunk to encode (will be converted to bytes).
            
        Returns
        -------
        List[int]
            List of token indices for the encoded chunk.
            
        Examples
        --------
        >>> tokenizer = RegexTokenizer()
        >>> tokenizer.train("Hello world", 300)
        >>> 
        >>> # Encode a single chunk
        >>> chunk_ids = tokenizer._encode_chunk("Hello")
        >>> print(f"Chunk encoded to {len(chunk_ids)} tokens")
        
        Notes
        -----
        - Converts text to bytes internally
        - Applies learned BPE merges iteratively
        - Stops when no more merges are possible
        - Returns list of integer indices
        """
        ids = list(text_bytes.encode("utf-8"))
        while len(ids) >= 2:
            # find the pair with the lowest merge index
            byte_pairs_freq = get_pair_frequencies(ids)
            pair = min(byte_pairs_freq, key=lambda p: self.merges.get(p, float("inf")))
            if pair not in self.merges:
                break  # nothing else can be merged anymore
            # otherwise let's merge the best pair (lowest merge index)
            idx = self.merges[pair]
            ids = merge_pair(ids, pair, idx)
        return ids
        
    def encode_ordinary(self, text: str) -> List[int]:
        """Encode ordinary text without special token handling.
        
        This method encodes text using only the regex-based BPE algorithm,
        ignoring any special tokens. It's useful when you want to ensure
        no special tokens are processed.
        
        Parameters
        ----------
        text : str
            Input text string to encode.
            
        Returns
        -------
        List[int]
            List of token indices representing the encoded text.
            
        Examples
        --------
        >>> tokenizer = RegexTokenizer()
        >>> tokenizer.train("Hello world! This is a test.", 300)
        >>> 
        >>> # Encode without special tokens
        >>> encoded = tokenizer.encode_ordinary("Hello world!")
        >>> print(f"Encoded: {encoded}")
        >>> print(f"Number of tokens: {len(encoded)}")
        
        >>> # Compare with regular encode
        >>> regular_encoded = tokenizer.encode("Hello world!", allowed_special_tokens="none")
        >>> print(f"Same result: {encoded == regular_encoded}")
        
        Notes
        -----
        - Splits text using regex pattern
        - Encodes each chunk independently
        - Concatenates results in order
        - No special token processing
        - Useful for controlled encoding scenarios
        """
        text_chunks = re.findall(self.compiled_pattern, text)
        ids = []
        for chunk in text_chunks:
            chunk_bytes = chunk.encode("utf-8")
            chunk_ids = self._encode_chunk(chunk_bytes)
            ids.extend(chunk_ids)
        return ids
    
    def encode(self, text: str, allowed_special_tokens: Union[str, Set[str]] = "none_raise") -> List[int]:
        """Encode text with configurable special token handling.
        
        This method provides flexible encoding with different levels of
        special token support. It can handle special tokens automatically,
        ignore them, or raise errors when they're encountered.
        
        Parameters
        ----------
        text : str
            Input text string to encode.
        allowed_special_tokens : Union[str, Set[str]], optional
            Controls how special tokens are handled:
            - "all": Process all registered special tokens
            - "none": Ignore all special tokens
            - "none_raise": Raise error if special tokens found
            - Set[str]: Only process specified special tokens
            Default is "none_raise".
            
        Returns
        -------
        List[int]
            List of token indices representing the encoded text.
            
        Raises
        ------
        AssertionError
            If "none_raise" is set and special tokens are found.
        ValueError
            If allowed_special_tokens has an invalid value.
            
        Examples
        --------
        >>> tokenizer = RegexTokenizer()
        >>> tokenizer.train("Hello world", 300)
        >>> tokenizer.register_special_tokens({"<|endoftext|>": 100257})
        
        >>> # Encode with no special tokens
        >>> encoded = tokenizer.encode("Hello world", "none")
        >>> print(f"Encoded: {encoded}")
        
        >>> # Encode with all special tokens
        >>> encoded = tokenizer.encode("Hello <|endoftext|>", "all")
        >>> print(f"With special tokens: {encoded}")
        
        >>> # Encode with specific special tokens only
        >>> encoded = tokenizer.encode("Hello <|endoftext|>", {"<|endoftext|>"})
        >>> print(f"Specific tokens: {encoded}")
        
        >>> # Raise error for unexpected special tokens
        >>> try:
        ...     encoded = tokenizer.encode("Hello <|endoftext|>", "none_raise")
        ... except AssertionError as e:
        ...     print(f"Error: {e}")
        
        Notes
        -----
        The encoding process:
        1. Identifies special tokens in the text
        2. Splits text around special tokens
        3. Encodes ordinary text using regex BPE
        4. Interleaves special token indices with encoded text
        5. Returns combined list of indices
        
        Special token handling modes:
        - "all": Most permissive, processes everything
        - "none": Ignores special tokens completely
        - "none_raise": Strict mode, fails on special tokens
        - Set: Selective processing of specific tokens
        """
        special_tokens = None
        if allowed_special_tokens == "all":
            special_tokens = self.special_tokens
        elif allowed_special_tokens == "none":
            special_tokens = {}
        elif allowed_special_tokens == "none_raise":
            special_tokens = {}
            assert all(token not in text for token in self.special_tokens)
        elif isinstance(allowed_special_tokens, set):
            special_tokens = {k: v for k, v in self.special_tokens.items() if k in allowed_special_tokens}
        else:
            raise ValueError(f"Invalid allowed_special_tokens: {allowed_special_tokens}")
        
        if not special_tokens:
            # if no special tokens are found, use the ordinary encoding
            return self.encode_ordinary(text)
        
        # Creating a capture group for each special tokens
        special_patterns = "(" + "|".join(re.escape(token) for token in special_tokens) + ")"
        special_chunks = re.findall(special_patterns, text)
        
        ids = []
        for part in special_chunks:
            if part in special_tokens:
                ids.append(special_tokens[part])
            else:
                ids.extend(self.encode_ordinary(part))
        return ids
    