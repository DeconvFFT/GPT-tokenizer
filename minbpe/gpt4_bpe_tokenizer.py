"""
GPT-4 BPE Tokenizer Implementation.

This module provides a GPT-4 compatible Byte Pair Encoding (BPE) tokenizer
that loads the pretrained `cl100k_base` tokenizer from tiktoken. It serves
as a lightweight wrapper around the RegexTokenizer with GPT-4 specific
patterns, special tokens, and byte permutation handling.

Examples
--------
>>> from minbpe.gpt4_bpe_tokenizer import GPT4Tokenizer
>>> # Create a GPT-4 compatible tokenizer
>>> tokenizer = GPT4Tokenizer()
>>> 
>>> # Encode and decode text
>>> text = "Hello world! This is a test of GPT-4 tokenization."
>>> encoded = tokenizer.encode(text)
>>> print(f"Encoded: {encoded}")
>>> decoded = tokenizer.decode(encoded)
>>> print(f"Decoded: {decoded}")
>>> 
>>> # Check special tokens
>>> print(f"Special tokens: {list(tokenizer.special_tokens.keys())}")

See Also
--------
minbpe.regex_tokenizer.RegexTokenizer : Base regex-based tokenizer
minbpe.base.Tokenizer : Core tokenizer interface
tiktoken : OpenAI's tokenizer library
"""

import tiktoken
from .regex_tokenizer import RegexTokenizer
from typing import Dict, List, Tuple, Optional, Union

def bpe(mergeable_ranks: Dict[bytes, int], token: List[int], max_rank: Optional[int] = None) -> List[bytes]:
    """Helper function to reconstruct the merge forest during BPE decoding.
    
    This function implements the BPE algorithm to reconstruct the original
    byte sequences from merged tokens. It iteratively finds the lowest-rank
    mergeable pairs and reconstructs the token step by step.
    
    Parameters
    ----------
    mergeable_ranks : Dict[bytes, int]
        Dictionary mapping byte sequences to their merge ranks.
    token : List[int]
        List of byte values representing the token to reconstruct.
    max_rank : Optional[int], optional
        Maximum rank to consider during reconstruction, by default None.
        
    Returns
    -------
    List[bytes]
        List of byte sequences representing the reconstructed token.
        
    Examples
    --------
    >>> # Example with simple byte sequence
    >>> ranks = {b'a': 1, b'b': 2, b'ab': 3}
    >>> token = [97, 98]  # 'ab' in ASCII
    >>> result = bpe(ranks, token)
    >>> print(f"Reconstructed: {result}")
    
    Notes
    -----
    This function is used internally by `recover_merges()` to reconstruct
    the original byte pairings from the tiktoken mergeable ranks.
    """
    parts = [bytes([t]) for t in token]
    while True:
        min_idx = None
        min_rank = None
        for i, pair in enumerate(zip(parts[:-1], parts[1:])):
            rank = mergeable_ranks.get(pair[0] + pair[1])
            if rank is not None and (min_rank is None or rank < min_rank):
                min_idx = i
                min_rank = rank
        if min_rank is None or (max_rank is not None and min_rank >= max_rank):
            break
        assert min_idx is not None
        parts = parts[:min_idx] + [parts[min_idx] + parts[min_idx + 1]] + parts[min_idx + 2:]
    return parts

def recover_merges(mergeable_ranks: Dict[bytes, int]) -> Dict[Tuple[int, int], int]:
    """Recover original pairings of merges from tiktoken mergeable ranks.
    
    This function reconstructs the original BPE merge operations by analyzing
    the mergeable ranks from the tiktoken library. It performs a small BPE
    training run on all tokens to recover the original byte pair merges.
    
    Parameters
    ----------
    mergeable_ranks : Dict[bytes, int]
        Dictionary mapping byte sequences to their merge ranks from tiktoken.
        
    Returns
    -------
    Dict[Tuple[int, int], int]
        Dictionary mapping byte pairs to their merge indices.
        
    Examples
    --------
    >>> # Example with mergeable ranks
    >>> ranks = {b'a': 1, b'b': 2, b'ab': 3, b'c': 4, b'abc': 5}
    >>> merges = recover_merges(ranks)
    >>> print(f"Recovered merges: {merges}")
    
    Notes
    -----
    This function is essential for converting tiktoken's mergeable ranks
    format to the standard BPE merges format used by our tokenizer.
    
    References
    ----------
    .. [1] https://github.com/openai/tiktoken/issues/60
    """
    # also see https://github.com/openai/tiktoken/issues/60
    merges = {}
    for token, rank in mergeable_ranks.items():
        if len(token) == 1:
            continue  # skip raw bytes
        pair = tuple(bpe(mergeable_ranks, list(token), max_rank=rank))
        assert len(pair) == 2
        
        # recover integer ranks of pair
        idx0 = mergeable_ranks[pair[0]]
        idx1 = mergeable_ranks[pair[1]]
        merges[(idx0, idx1)] = rank
    return merges

# GPT-4 specific configuration
GPT4_SPLIT_PATTERN = r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+"""
GPT4_SPECIAL_TOKENS = {
    '<|endoftext|>': 100257,
    '<|fim_prefix|>': 100258,
    '<|fim_middle|>': 100259,
    '<|fim_suffix|>': 100260,
    '<|endofprompt|>': 100276
}

class GPT4Tokenizer(RegexTokenizer):
    """GPT-4 compatible BPE Tokenizer with tiktoken integration.
    
    This tokenizer provides GPT-4 compatible tokenization by wrapping
    the tiktoken `cl100k_base` tokenizer. It handles the byte permutation
    scheme used by GPT-4 and provides the same interface as other MinBPE
    tokenizers.
    
    Attributes
    ----------
    merges : Dict[Tuple[int, int], int]
        Dictionary mapping byte pairs to their merge indices.
    vocab : Dict[int, bytes]
        Complete vocabulary mapping indices to byte sequences.
    byte_shuffle : Dict[int, int]
        Mapping from original byte values to permuted values.
    inverse_byte_shuffle : Dict[int, int]
        Inverse mapping from permuted values to original values.
    special_tokens : Dict[str, int]
        GPT-4 specific special tokens.
        
    Examples
    --------
    >>> tokenizer = GPT4Tokenizer()
    >>> print(f"Vocabulary size: {len(tokenizer.vocab)}")
    >>> print(f"Special tokens: {list(tokenizer.special_tokens.keys())}")
    
    >>> # Encode text
    >>> text = "Hello world!"
    >>> encoded = tokenizer.encode(text)
    >>> print(f"Encoded tokens: {len(encoded)}")
    
    Notes
    -----
    This implementation:
    - Loads pretrained weights from tiktoken cl100k_base
    - Handles GPT-4's byte permutation scheme
    - Uses GPT-4 specific regex pattern
    - Includes GPT-4 special tokens
    - Cannot be saved/loaded (read-only)
    """
    
    def __init__(self):
        """Initialize a new GPT4Tokenizer instance.
        
        This method:
        1. Sets up the GPT-4 regex pattern
        2. Loads the tiktoken cl100k_base tokenizer
        3. Recovers BPE merges from mergeable ranks
        4. Reconstructs vocabulary from merges
        5. Sets up byte permutation mappings
        6. Registers GPT-4 special tokens
        
        Examples
        --------
        >>> tokenizer = GPT4Tokenizer()
        >>> print(f"Using pattern: {tokenizer.pattern[:50]}...")
        >>> print(f"Byte shuffle size: {len(tokenizer.byte_shuffle)}")
        
        Notes
        -----
        The initialization process:
        - Loads tiktoken's pretrained cl100k_base model
        - Recovers original BPE merge operations
        - Handles GPT-4's byte permutation scheme
        - Sets up special token handling
        """
        super().__init__(split_pattern=GPT4_SPLIT_PATTERN)
        # CLK100_base tokenizer and merge ranks
        enc = tiktoken.get_encoding("cl100k_base")
        mergeable_ranks = enc._mergeable_ranks
        # merges are of gpt4 but we have to recover them
        self.merges = recover_merges(mergeable_ranks)
        # reconstruct the vocab from merges
        vocab = {idx: bytes([idx]) for idx in range(256)}
        for (p0, p1), idx in self.merges.items():
            vocab[idx] = vocab[p0] + vocab[p1]
        self.vocab = vocab
        ## the tokens corresponding to individual bytes are permuted weirdly 
        ## handling this is a bit tricky
        self.byte_shuffle = {i: mergeable_ranks[bytes([i])] for i in range(256)}
        self.inverse_byte_shuffle = {v: i for i, v in self.byte_shuffle.items()}        
        
        self.register_special_tokens(GPT4_SPECIAL_TOKENS)
        
    def _encode_chunk(self, text_bytes: str) -> List[int]:
        """Encode a text chunk using GPT-4 byte permutation.
        
        This method overrides the parent's `_encode_chunk` to handle
        GPT-4's byte permutation scheme. It permutes the input bytes
        before applying the standard BPE encoding.
        
        Parameters
        ----------
        text_bytes : str
            Text chunk to encode (will be converted to bytes).
            
        Returns
        -------
        List[int]
            List of token indices representing the encoded chunk.
            
        Examples
        --------
        >>> tokenizer = GPT4Tokenizer()
        >>> # Encode a simple chunk
        >>> chunk = "Hello"
        >>> encoded = tokenizer._encode_chunk(chunk)
        >>> print(f"Chunk encoded to {len(encoded)} tokens")
        
        Notes
        -----
        The encoding process:
        1. Converts text to bytes
        2. Permutes bytes using GPT-4's byte_shuffle mapping
        3. Applies standard BPE encoding to permuted bytes
        4. Returns token indices
        """
        # Convert to bytes and permute before using them
        permuted_bytes = text_bytes.encode("utf-8")
        permuted_bytes = bytes(self.byte_shuffle[b] for b in permuted_bytes)
        ids = super()._encode_chunk(permuted_bytes)
        return ids
    
    def decode(self, ids: List[int]) -> str:
        """Decode a list of token indices back to text.
        
        This method overrides the parent's `decode` to handle
        GPT-4's byte permutation scheme. It unpermutes the decoded
        bytes before converting to text.
        
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
        >>> tokenizer = GPT4Tokenizer()
        >>> # Decode some tokens
        >>> encoded = tokenizer.encode("Hello world!")
        >>> decoded = tokenizer.decode(encoded)
        >>> print(f"Decoded: {decoded}")
        
        Notes
        -----
        The decoding process:
        1. Looks up token indices in vocabulary
        2. Concatenates byte sequences
        3. Unpermutes bytes using inverse_byte_shuffle
        4. Decodes to UTF-8 text
        """
        # unpermuting bytes before decoding
        text_bytes = b"".join(self.vocab[idx] for idx in ids)
        text_bytes = bytes(self.inverse_byte_shuffle[b] for b in text_bytes)
        text = text_bytes.decode("utf-8", errors="replace")
        return text
    
    def save(self, file_prefix: str) -> None:
        """Save the tokenizer model (not implemented).
        
        GPT4Tokenizer cannot be saved because it's a read-only wrapper
        around the tiktoken library. The model weights are loaded from
        tiktoken and cannot be modified.
        
        Parameters
        ----------
        file_prefix : str
            File path prefix (ignored).
            
        Raises
        ------
        NotImplementedError
            Always raised, as GPT4Tokenizer cannot be saved.
            
        Examples
        --------
        >>> tokenizer = GPT4Tokenizer()
        >>> try:
        ...     tokenizer.save("my_model")
        ... except NotImplementedError as e:
        ...     print(f"Expected error: {e}")
        
        Notes
        -----
        This method is not implemented because:
        - GPT4Tokenizer is a read-only wrapper
        - Model weights come from tiktoken library
        - No training or modification is possible
        """
        raise NotImplementedError("GPT4Tokenizer cannot be saved.")

    def load(self, model_file: str) -> None:
        """Load a tokenizer model (not implemented).
        
        GPT4Tokenizer cannot be loaded because it's a read-only wrapper
        around the tiktoken library. The model is always loaded from
        tiktoken during initialization.
        
        Parameters
        ----------
        model_file : str
            Model file path (ignored).
            
        Raises
        ------
        NotImplementedError
            Always raised, as GPT4Tokenizer cannot be loaded.
            
        Examples
        --------
        >>> tokenizer = GPT4Tokenizer()
        >>> try:
        ...     tokenizer.load("my_model.model")
        ... except NotImplementedError as e:
        ...     print(f"Expected error: {e}")
        
        Notes
        -----
        This method is not implemented because:
        - GPT4Tokenizer is always initialized with tiktoken weights
        - No custom model loading is supported
        - The tokenizer is read-only
        """
        raise NotImplementedError("GPT4Tokenizer cannot be loaded.")
    
    def save_vocab(self, vocab_file: str) -> None:
        """Save the vocabulary to a human-readable file.
        
        This method saves the GPT-4 vocabulary in a readable format,
        showing the byte sequences and merge relationships. It handles
        the byte permutation scheme by unpermuting the bytes before
        writing to the file.
        
        Parameters
        ----------
        vocab_file : str
            Path to the vocabulary file to create.
            
        Examples
        --------
        >>> tokenizer = GPT4Tokenizer()
        >>> 
        >>> # Save vocabulary to file
        >>> tokenizer.save_vocab("gpt4_vocab.txt")
        >>> 
        >>> # Check the file contents
        >>> with open("gpt4_vocab.txt", "r") as f:
        ...     lines = f.readlines()[:5]  # First 5 lines
        ...     for line in lines:
        ...         print(line.strip())
        
        Notes
        -----
        The vocabulary file format:
        - Each line represents one vocabulary item
        - Format: [byte_sequence] index
        - For merged tokens: [byte1][byte2] -> [merged] index
        - Bytes are unpermuted for readability
        - Uses UTF-8 encoding with error handling
        """
        from .base import render_token
        vocab = {idx: bytes([self.inverse_byte_shuffle[idx]]) for idx in range(256)}
        for (p0, p1), idx in self.merges.items():
            vocab[idx] = vocab[p0] + vocab[p1]
            
        # now merge the shuffled bytes and write to file
        inverted_merges = {idx: pair for pair, idx in self.merges.items()}
        with open(vocab_file, "w", encoding="utf-8") as f:
            for idx, token in vocab.items():
                s = render_token(token)
                if idx in inverted_merges:
                    idx0, idx1 = inverted_merges[idx]
                    s0 = render_token(vocab[idx0])
                    s1 = render_token(vocab[idx1])
                    f.write(f"[{s0}][{s1}] -> [{s}] {idx}\n")
                else:
                    f.write(f"[{s}] {idx}\n")
        
    