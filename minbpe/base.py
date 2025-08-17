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
    
    def save(self, file_prefix:str)->None:
        """
        Saves two files: file_prefix.vocab and file_prefix.model
        Similar to sentencepiece's model saving format
        - Model file: The one that should be loaded
        - Vocab file: Only for human readability

        Args:
            file_prefix (str): File path prefix
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
            for idx1, idx2 in self.merges.items():
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
                    pairs = inverted_merges[idx]
                    pairs[0] = render_token(pairs[0])
                    pairs[1] = render_token(pairs[1])
                    f.write(f'[{pairs[0]}][{pairs[1]}] -> [{s}]{idx}\n')
                else:
                    # Else this is a leaf token, just print it
                    f.write(f'[{s}] {idx}\n')
    
    def load(self, model_file:str)->None:
        """
        Loads a model from a file
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
                token, idx = f.readline().strip().split()
                special_tokens[token] = int(idx)
            # Step 4: Read merges
            for line in f:
                idx1, idx2 = map(int, line.split())
                # we are increasing our vocab size by 1 for each merge
                merges[(idx1, idx2)] = idx # merges at idx 
                idx+=1 # increment index to make it ready fo next set of merges
        
        self.merges = merges
        self.pattern = pattern
        self.special_tokens = special_tokens
        self.vocab = self._build_vocab() # building vocab for human readability
                
                
        
        
        
        