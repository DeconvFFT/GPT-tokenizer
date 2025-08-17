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