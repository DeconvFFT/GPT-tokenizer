"""
Base tokenizer implementation for Byte Pair Encoding (BPE).

This module provides the core Tokenizer class and utility functions for implementing
BPE-based tokenization algorithms. The Tokenizer class serves as an abstract base
for specific tokenizer implementations.

Examples
--------
>>> from minbpe.base import Tokenizer, get_pair_frequencies
>>> # Create a basic tokenizer instance
>>> tokenizer = Tokenizer()
>>> # Analyze byte pair frequencies in text
>>> text_bytes = [72, 101, 108, 108, 111]  # "Hello" in ASCII
>>> freqs = get_pair_frequencies(text_bytes)
>>> print(freqs)
{(72, 101): 1, (101, 108): 2, (108, 111): 1}

See Also
--------
minbpe.gpt4_bpe_tokenizer : GPT-4 style BPE implementation
minbpe.regex_tokenizer : Regex-based tokenization
"""

import unicodedata
from typing import Dict, List, Tuple, Optional, Union

def get_pair_frequencies(indices: List[int], counts: Optional[Dict[Tuple[int, int], int]] = None) -> Dict[Tuple[int, int], int]:
    """Calculate frequency of adjacent byte pairs in a sequence of indices.
    
    This function analyzes a list of integer indices to find how often each pair
    of adjacent values occurs. It's used in the BPE algorithm to identify the
    most frequent byte pairs for merging.
    
    Parameters
    ----------
    indices : List[int]
        Integer mapped tokens (indices) representing byte values.
    counts : Dict[Tuple[int, int], int], optional
        Dictionary to store the frequencies of pairs. If None, creates a new dict.
        
    Returns
    -------
    Dict[Tuple[int, int], int]
        Dictionary mapping byte pairs (as tuples) to their frequency counts.
        
    Examples
    --------
    >>> text_bytes = [72, 101, 108, 108, 111]  # "Hello" in ASCII
    >>> freqs = get_pair_frequencies(text_bytes)
    >>> print(freqs)
    {(72, 101): 1, (101, 108): 2, (108, 111): 1}
    
    >>> # Use existing counts dictionary
    >>> existing_counts = {(72, 101): 5}
    >>> freqs = get_pair_frequencies(text_bytes, existing_counts)
    >>> print(freqs)
    {(72, 101): 6, (101, 108): 2, (108, 111): 1}
    
    See Also
    --------
    merge_pair : Replace byte pairs with new indices
    """
    counts = {} if counts is None else counts
    for byte_pair in zip(indices, indices[1:]):
        counts[byte_pair] = counts.get(byte_pair, 0) + 1
    return counts

def merge_pair(indices: List[int], pair: Tuple[int, int], new_idx: int) -> List[int]:
    """Replace all occurrences of a byte pair with a new index in a sequence.
    
    This function implements the core BPE merge operation by replacing all
    instances of a specific byte pair with a new vocabulary index.
    
    Parameters
    ----------
    indices : List[int]
        List of integer indices representing the sequence.
    pair : Tuple[int, int]
        Tuple of (byte1, byte2) to replace.
    new_idx : int
        New index to replace the pair with.
        
    Returns
    -------
    List[int]
        New list with all occurrences of the pair replaced by new_idx.
        
    Examples
    --------
    >>> indices = [72, 101, 108, 108, 111]  # "Hello" in ASCII
    >>> merged = merge_pair(indices, (101, 108), 256)
    >>> print(merged)
    [72, 256, 111]
    
    >>> # No pairs to merge
    >>> indices = [72, 101, 108, 111]
    >>> merged = merge_pair(indices, (100, 101), 256)
    >>> print(merged)
    [72, 101, 108, 111]
    
    See Also
    --------
    get_pair_frequencies : Calculate byte pair frequencies
    """
    new_indices = []
    i = 0
    while i < len(indices):
        if i < len(indices) - 1 and indices[i] == pair[0] and indices[i + 1] == pair[1]:
            new_indices.append(new_idx)  
            i += 2
        else:
            new_indices.append(indices[i])
            i += 1
    return new_indices

def replace_control_characters(s: str) -> str:
    """Replace control characters with their Unicode escape sequences.
    
    This function handles control characters that can distort output display,
    such as newlines, tabs, carriage returns, etc. It converts them to
    readable Unicode escape sequences.
    
    Parameters
    ----------
    s : str
        Input string that may contain control characters.
        
    Returns
    -------
    str
        String with control characters replaced by Unicode escape sequences.
        
    Examples
    --------
    >>> text = "Hello\nWorld\tTabbed"
    >>> cleaned = replace_control_characters(text)
    >>> print(cleaned)
    Hello\\u000aWorld\\u0009Tabbed
    
    >>> # No control characters
    >>> text = "Hello World"
    >>> cleaned = replace_control_characters(text)
    >>> print(cleaned)
    Hello World
    
    Notes
    -----
    Uses Unicode General Category values to identify control characters.
    Control characters have category starting with 'C' (Control).
    
    References
    ----------
    .. [1] https://stackoverflow.com/questions/4324790/removing-control-characters-from-a-string-in-python
    .. [2] http://www.unicode.org/reports/tr44/#GC_Values_Table
    """
    chars = []
    for ch in s:
        if unicodedata.category(ch)[0] != "C":
            chars.append(ch)  # character is OK
        else:
            chars.append(f'\\u{ord(ch):04x}')  # escape control characters
    return "".join(chars)

def render_token(t: bytes) -> str:
    """Convert a byte token to a human-readable string representation.
    
    This function safely decodes byte tokens to strings, handling any
    encoding issues gracefully and replacing control characters with
    readable representations.
    
    Parameters
    ----------
    t : bytes
        Byte token to render.
        
    Returns
    -------
    str
        Human-readable string representation of the token.
        
    Examples
    --------
    >>> token = b"Hello"
    >>> rendered = render_token(token)
    >>> print(rendered)
    Hello
    
    >>> # Token with control characters
    >>> token = b"Hello\nWorld"
    >>> rendered = render_token(token)
    >>> print(rendered)
    Hello\\u000aWorld
    
    See Also
    --------
    replace_control_characters : Handle control character replacement
    """
    s = t.decode("utf-8", errors="replace")
    s = replace_control_characters(s)
    return s

class Tokenizer:
    """Base class for all tokenizers implementing the BPE algorithm.
    
    This abstract base class provides the foundation for implementing
    various tokenization strategies. It includes common functionality
    for vocabulary management, model persistence, and basic tokenization
    operations.
    
    Attributes
    ----------
    merges : Dict[Tuple[int, int], int]
        Dictionary mapping byte pairs to their merged indices.
    pattern : str
        Regex pattern used for tokenization.
    special_tokens : Dict[str, int]
        Dictionary of special tokens and their indices.
    vocab : Dict[int, bytes]
        Complete vocabulary mapping indices to byte sequences.
        
    Examples
    --------
    >>> from minbpe.base import Tokenizer
    >>> # Create a basic tokenizer instance
    >>> tokenizer = Tokenizer()
    >>> print(f"Vocabulary size: {len(tokenizer.vocab)}")
    Vocabulary size: 256
    >>> print(f"Special tokens: {len(tokenizer.special_tokens)}")
    Special tokens: 0
    
    Notes
    -----
    This is an abstract base class. Subclasses must implement the
    `train`, `encode`, and `decode` methods.
    """
    
    def __init__(self):
        """Initialize a new Tokenizer instance.
        
        Sets up empty merges, pattern, special tokens, and builds
        the initial vocabulary from individual bytes.
        """
        self.merges = {}
        self.pattern = ""
        self.special_tokens = {}  # Special tokens like <|endoftext|>
        self.vocab = self._build_vocab()
        
    def _build_vocab(self) -> Dict[int, bytes]:
        """Build vocabulary of bytes from indices and merges.
        
        This method constructs the complete vocabulary by starting with
        individual bytes (0-255) and then incorporating all learned
        merge operations and special tokens.
        
        Returns
        -------
        Dict[int, bytes]
            Dictionary mapping indices to their corresponding byte sequences.
            
        Examples
        --------
        >>> tokenizer = Tokenizer()
        >>> vocab = tokenizer._build_vocab()
        >>> print(f"Base vocab size: {len(vocab)}")
        Base vocab size: 256
        >>> print(f"First few entries: {list(vocab.items())[:3]}")
        First few entries: [(0, b'\\x00'), (1, b'\\x01'), (2, b'\\x02')]
        """
        vocab = {idx: bytes([idx]) for idx in range(256)}
        for (p0, p1), idx in self.merges.items():
            vocab[idx] = vocab[p0] + vocab[p1]  # merges two bytes
        for special_token, idx in self.special_tokens.items():
            vocab[idx] = special_token.encode('utf-8')  # UTF-8 encoding for special tokens
        return vocab
    
    def train(self, text: str, vocab_size: int, verbose: bool = False) -> None:
        """Train the tokenizer on a corpus of text.
        
        This is an abstract method that must be implemented by subclasses.
        It should implement the BPE training algorithm to learn merge
        operations from the input text.
        
        Parameters
        ----------
        text : str
            Text corpus to train the tokenizer on.
        vocab_size : int
            Maximum vocabulary size to build.
        verbose : bool, optional
            Whether to show training progress logs, by default False.
            
        Raises
        ------
        NotImplementedError
            This method must be implemented by subclasses.
            
        Examples
        --------
        >>> tokenizer = Tokenizer()
        >>> try:
        ...     tokenizer.train("Hello world", 1000)
        ... except NotImplementedError as e:
        ...     print(f"Expected error: {e}")
        Expected error: Tokenizer.train() not implemented
        
        See Also
        --------
        encode : Convert text to token indices
        decode : Convert token indices back to text
        """
        raise NotImplementedError("Tokenizer.train() not implemented")
        
    def encode(self, text: str) -> List[int]:
        """Encode a text string into a list of token indices.
        
        This is an abstract method that must be implemented by subclasses.
        It should convert input text into a sequence of vocabulary indices
        using the learned merge operations.
        
        Parameters
        ----------
        text : str
            Input text string to encode.
            
        Returns
        -------
        List[int]
            List of integer token indices.
            
        Raises
        ------
        NotImplementedError
            This method must be implemented by subclasses.
            
        Examples
        --------
        >>> tokenizer = Tokenizer()
        >>> try:
        ...     tokens = tokenizer.encode("Hello world")
        ... except NotImplementedError as e:
        ...     print(f"Expected error: {e}")
        Expected error: Encoder not implemented
        
        See Also
        --------
        decode : Convert token indices back to text
        train : Learn tokenization from text corpus
        """
        raise NotImplementedError("Encoder not implemented")

    def decode(self, ids: List[int]) -> str:
        """Decode a list of token indices back to text.
        
        This is an abstract method that must be implemented by subclasses.
        It should reconstruct the original text from a sequence of
        vocabulary indices.
        
        Parameters
        ----------
        ids : List[int]
            List of integer token indices.
            
        Returns
        -------
        str
            Reconstructed text string.
            
        Raises
        ------
        NotImplementedError
            This method must be implemented by subclasses.
            
        Examples
        --------
        >>> tokenizer = Tokenizer()
        >>> try:
        ...     text = tokenizer.decode([72, 101, 108, 108, 111])
        ... except NotImplementedError as e:
        ...     print(f"Expected error: {e}")
        Expected error: Decoder not implemented
        
        See Also
        --------
        encode : Convert text to token indices
        """
        raise NotImplementedError("Decoder not implemented")
    
    def save(self, file_prefix: str) -> None:
        """Save the trained tokenizer model to files.
        
        Saves two files: file_prefix.vocab and file_prefix.model
        Similar to sentencepiece's model saving format:
        - Model file: The one that should be loaded
        - Vocab file: Only for human readability
        
        Parameters
        ----------
        file_prefix : str
            File path prefix for saving the model.
            
        Examples
        --------
        >>> import tempfile
        >>> import os
        >>> tokenizer = Tokenizer()
        >>> # Add some special tokens for demonstration
        >>> tokenizer.special_tokens = {"<|endoftext|>": 256}
        >>> tokenizer.merges = {(72, 101): 257}  # "He" -> 257
        >>> 
        >>> with tempfile.TemporaryDirectory() as temp_dir:
        ...     file_prefix = os.path.join(temp_dir, "test_model")
        ...     tokenizer.save(file_prefix)
        ...     # Check files were created
        ...     model_file = file_prefix + ".model"
        ...     vocab_file = file_prefix + ".vocab"
        ...     print(f"Model file exists: {os.path.exists(model_file)}")
        ...     print(f"Vocab file exists: {os.path.exists(vocab_file)}")
        Model file exists: True
        Vocab file exists: True
        
        See Also
        --------
        load : Load a trained model from file
        """
        model_file = file_prefix + ".model"
        vocab_file = file_prefix + ".vocab"
        
        with open(model_file, 'w') as f:
            # Storing version, pattern and merges
            f.write('minbpe v1\n')
            f.write(f'{self.pattern}\n')
            # Write special tokens. First len of special tokens
            f.write(f'{len(self.special_tokens)}\n')
            # Write special tokens
            for token, idx in self.special_tokens.items():
                f.write(f'{token} {idx}\n')
            # write merges
            for (idx1, idx2) in self.merges.keys():
                f.write(f'{idx1} {idx2}\n')
        
        ## Write vocab file
        inverted_merges = {idx: pairs for pairs, idx in self.merges.items()}
        with open(vocab_file, 'w', encoding='utf-8') as f:
            for idx, token in self.vocab.items():
                ## Some tokens are partial utf-8 sequences which we escaped using 'replace' and replaced them
                ## with special character
                ## We can't load them for our model because this is a lossy decoding. 
                ## So we don't use .vocab for loading this model
                s = render_token(token)
                if idx in inverted_merges:
                    # If the token has children, render them as merges
                    idx0, idx1 = inverted_merges[idx]
                    s0 = render_token(self.vocab[idx0])
                    s1 = render_token(self.vocab[idx1])
                    f.write(f"[{s0}][{s1}] -> [{s}] {idx}\n")
                else:
                    # Else this is a leaf token, just print it
                    f.write(f'[{s}] {idx}\n')
    
    def load(self, model_file: str) -> None:
        """Load a trained tokenizer model from a file.
        
        This method reconstructs the tokenizer state from a previously
        saved model file, including merges, patterns, and special tokens.
        
        Parameters
        ----------
        model_file : str
            Path to the .model file to load.
            
        Raises
        ------
        AssertionError
            If the file doesn't end with .model or isn't a valid minbpe model.
            
        Examples
        --------
        >>> import tempfile
        >>> import os
        >>> tokenizer = Tokenizer()
        >>> # Create a test model file
        >>> with tempfile.NamedTemporaryFile(mode='w', suffix='.model', delete=False) as f:
        ...     f.write('minbpe v1\\n')
        ...     f.write('\\n')  # empty pattern
        ...     f.write('0\\n')  # no special tokens
        ...     test_file = f.name
        ... 
        >>> try:
        ...     tokenizer.load(test_file)
        ...     print("Model loaded successfully")
        ...     print(f"Pattern: '{tokenizer.pattern}'")
        ...     print(f"Special tokens: {len(tokenizer.special_tokens)}")
        ...     print(f"Merges: {len(tokenizer.merges)}")
        ... finally:
        ...     os.unlink(test_file)
        Model loaded successfully
        Pattern: ''
        Special tokens: 0
        Merges: 0
        
        See Also
        --------
        save : Save a trained model to file
        """
        assert model_file.endswith('.model'), "Model file must end with .model"
        merges = {}
        special_tokens = {}
        idx = 256
        with open(model_file, 'r') as f:
            # Step 1: Read the version
            version = f.readline().strip()
            assert version == 'minbpe v1', "Model file is not a minbpe model"
            # Step 2: Read the pattern
            pattern = f.readline().strip()
            # Step 3: Read special tokens
            n_special_tokens = int(f.readline().strip())
            for _ in range(n_special_tokens):
                token, idx_val = f.readline().strip().split()
                special_tokens[token] = int(idx_val)
            # Step 4: Read merges
            for line in f:
                idx1, idx2 = map(int, line.split())
                # we are increasing our vocab size by 1 for each merge
                merges[(idx1, idx2)] = idx  # merges at idx 
                idx += 1  # increment index to make it ready fo next set of merges
        
        self.merges = merges
        self.pattern = pattern
        self.special_tokens = special_tokens
        self.vocab = self._build_vocab()  # building vocab for human readability
                
                
        
        
        
        