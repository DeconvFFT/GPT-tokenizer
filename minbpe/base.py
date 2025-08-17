"""
Contains base Tokenizer class used by all other tokenizers. 
It also contains some helper functions like save and load functionality
"""

import unicodedata

def get_pair_frequencies(indices:list[int], counts:dict[tuple[int, int], int]=None)->dict[tuple[int, int], int]:
    """_summary_

    Args:
        indices (list[int]): Integer mapped tokens(indices)
        counts (dict[tuple[int, int], int]): Dictionary to store the frequencies of pairs

    Returns:
        dict[tuple[int, int], int]: Returns a dictionary of pairs and their frequencies
    """
    counts = {} if counts is None else counts
    for byte_pair in zip(indices, indices[1:]):
        counts[byte_pair] = counts.get(byte_pair, 0) + 1
    return counts

def merge_pair(indices:list[int], pair:tuple[int, int], new_idx: int)->list[int]:
    """_summary_

    Args:
        indices (list[int]): List of indices
        pair (tuple[int, int]): Pair to merge
        new_idx (int): New index to replace the pair with

    Returns:
        list[int]: List of new indices after merging the pair
    """
    new_indices = []
    i = 0
    while i<len(indices):
        if i<len(indices)-1 and indices[i]==pair[0] and indices[i+1] == pair[1]:
            new_indices.append(new_idx)  
            i+=2
        else:
            new_indices.append(indices[i])
            i+=1
    return new_indices

def replace_control_characters(s:str)->str:
    """ Avoid printing control characters that can destort the output.
    Like \n, \t, \r, etc.
    

    Args:
        s (str): _description_

    Returns:
        str: _description_
    """
    #https://stackoverflow.com/questions/4324790/removing-control-characters-from-a-string-in-python/19016117#19016117
    #http://www.unicode.org/reports/tr44/#GC_Values_Table
    chars = []
    for ch in s:
        if unicodedata.category(ch)[0] != "C":
            chars.append(ch) # character is OK
        else:
            chars.append(f'\\u{ord(ch):04x}') # escape control characters
    return "".join(chars)


def render_token(t:bytes)->str:
    """ Pretty prints token

    Args:
        t (bytes): Token

    Returns:
        str: Pretty print of the token
    """
    s = t.decode("utf-8", errors="replace")
    s = replace_control_characters(s)
    return s

class Tokenizer:
    """ Base class for all tokenizers
    """
    
    def __init__(self):
        self.merges = {}
        self.pattern = ""
        self.special_tokens = {} # Special tokens like <|endoftext|>
        self.vocab = self._build_vocab()
        
    def _build_vocab(self)->dict[int, bytes]:
        """
        Build vocbulary of bytes from indices and merges

        Returns:
            dict[int, bytes]: Vocabulary of bytes
        """
        vocab = {idx:bytes(idx) for idx in range(256)}
        for (p0,p1), idx in self.merges.items():
            vocab[idx] = vocab[p0] + vocab[p1] # merges two bytes
        for special_token, idx in self.special_tokens.items():
            vocab[idx] = special_token.encode('utf-8') # UTF-8 encoding for special tokens
        return vocab
    
    def train(self, text:str, vocab_size:int, verbose:bool=False)->None:
        """_summary_

        Args:
            text (str): Text you want to train the tokenizer on
            vocab_size (int): Maximum vocab size you want to have
            verbose (bool, optional): Show logs or not. Defaults to False.

        Raises:
            NotImplementedError: Error when training module is not implemented

        Returns:
            None
        """
        raise NotImplementedError("Tokenizer.train() not implemented")
    def encode(self, text:str):
        # Tokenizer can encode a string into a list of integers
        raise NotImplementedError("Encoder not implemented")

    def decode(self, ids:list[int])->str:
        # Tokenizer can decode a list of integers into a string
        raise NotImplementedError("Decoder not implemented")
    
    