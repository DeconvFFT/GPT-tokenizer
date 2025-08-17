# API Reference

## GPT4BPETokenizer Class

### Constructor

```python
GPT4BPETokenizer(vocab_size: int = 50000)
```

**Parameters:**
- `vocab_size`: Maximum size of the vocabulary (default: 50000)

**Initialization:**
- Creates empty vocabulary and merges dictionaries
- Sets up GPT-2 style regex pattern for tokenization
- Initializes special tokens

### Methods

#### `train(texts: List[str]) -> None`

Trains the BPE tokenizer on a list of texts.

**Algorithm:**
1. Count byte frequencies in all texts
2. Initialize vocabulary with most common bytes
3. Iteratively find most frequent byte pairs
4. Replace pairs with new tokens
5. Update vocabulary and merge rules

**Parameters:**
- `texts`: List of training text strings

**Time Complexity:** O(n × m × log m) where n is corpus size, m is vocabulary size

**Example:**
```python
tokenizer = GPT4BPETokenizer(vocab_size=1000)
training_texts = [
    "Hello world! This is a test.",
    "The quick brown fox jumps over the lazy dog."
]
tokenizer.train(training_texts)
```

#### `encode(text: str) -> List[int]`

Encodes text to token IDs using the trained BPE merges.

**Process:**
1. Convert text to UTF-8 bytes
2. Apply learned merge rules
3. Map resulting tokens to IDs
4. Handle unknown tokens

**Parameters:**
- `text`: Input text string

**Returns:**
- List of integer token IDs

**Time Complexity:** O(t × log v) where t is text length, v is vocabulary size

**Example:**
```python
tokens = tokenizer.encode("Hello world!")
# Returns: [15496, 995, 0]
```

#### `decode(token_ids: List[int]) -> str`

Decodes token IDs back to text.

**Process:**
1. Map token IDs to token strings
2. Concatenate tokens
3. Handle unknown token IDs

**Parameters:**
- `token_ids`: List of token IDs

**Returns:**
- Decoded text string

**Time Complexity:** O(t) where t is number of tokens

**Example:**
```python
text = tokenizer.decode([15496, 995, 0])
# Returns: "Hello world!"
```

#### `save(filepath: str) -> None`

Saves the tokenizer state to a JSON file.

**Saved Data:**
- Vocabulary size
- Token-to-ID mapping
- Merge rules

**Parameters:**
- `filepath`: Path to save the tokenizer file

**File Format:**
```json
{
  "vocab_size": 1000,
  "vocab": {"0": "H", "1": "e", "2": "l", "3": "o"},
  "merges": {"(72,101)": 4, "(108,108)": 5}
}
```

#### `load(filepath: str) -> None`

Loads the tokenizer state from a JSON file.

**Parameters:**
- `filepath`: Path to the saved tokenizer file

**Restored State:**
- Vocabulary
- Merge rules
- Token mappings

### Internal Methods

#### `_apply_merges(texts: List[str], pair: Tuple[int, int], new_token: str) -> List[str]`

Applies BPE merges to a list of texts.

**Parameters:**
- `texts`: List of texts to process
- `pair`: Byte pair to replace
- `new_token`: New token to insert

**Returns:**
- Updated list of texts with merges applied

## RegexTokenizer Class

### Constructor

```python
RegexTokenizer()
```

**Initialization:**
- Sets up GPT-2 style regex pattern
- Initializes special tokens
- Creates vocabulary mappings

### Methods

#### `tokenize(text: str) -> List[str]`

Tokenizes text using regex patterns.

**Pattern Components:**
- Contractions: `'s|'t|'re|'ve|'m|'ll|'d`
- Words: `\p{L}+` (Unicode letter sequences)
- Numbers: `\p{N}+` (Unicode number sequences)
- Punctuation: `[^\s\p{L}\p{N}]+`
- Whitespace: `\s+(?!\S)|\s+`

**Parameters:**
- `text`: Input text string

**Returns:**
- List of token strings

**Example:**
```python
tokens = tokenizer.tokenize("I'm going to the store.")
# Returns: ["I", "'m", " going", " to", " the", " store", "."]
```

#### `encode(text: str) -> List[int]`

Encodes text to token IDs.

**Process:**
1. Tokenize text using regex patterns
2. Add new tokens to vocabulary if needed
3. Return list of token IDs

**Parameters:**
- `text`: Input text string

**Returns:**
- List of integer token IDs

#### `decode(token_ids: List[int]) -> str`

Decodes token IDs back to text.

**Process:**
1. Map token IDs to token strings
2. Concatenate tokens
3. Handle unknown tokens with `<|unk|>`

**Parameters:**
- `token_ids`: List of token IDs

**Returns:**
- Decoded text string

#### `analyze_patterns(text: str) -> List[Tuple[str, str, int]]`

Analyzes how regex patterns match text.

**Returns:**
- List of (match_text, pattern_type, position) tuples

**Pattern Types:**
- `contraction`: 's, 't, 're, 've, 'm, 'll, 'd
- `word`: Alphabetic sequences
- `number`: Numeric sequences
- `whitespace`: Space and newline characters
- `punctuation`: Special characters

## Utility Functions

### `get_byte_pair_frequencies(texts: List[str]) -> Counter`

Counts byte pair frequencies in a list of texts.

**Parameters:**
- `texts`: List of text strings

**Returns:**
- Counter object with byte pair frequencies

**Example:**
```python
freqs = get_byte_pair_frequencies(["Hello", "World"])
# Returns: Counter({(72, 101): 1, (101, 108): 2, ...})
```

### `replace_byte_pair(text: str, pair: Tuple[int, int], new_token: str) -> str`

Replaces a byte pair with a new token in text.

**Parameters:**
- `text`: Input text string
- `pair`: Byte pair to replace
- `new_token`: New token to insert

**Returns:**
- Text with byte pair replaced

## Special Tokens

### Default Special Tokens

```python
SPECIAL_TOKENS = {
    '<|endoftext|>': 50256,
    '<|pad|>': 50257,
    '<|unk|>': 50258,
    '<|startoftext|>': 50259
}
```

### Usage

```python
# Add special token to text
text = "<|startoftext|>Hello world<|endoftext|>"

# Encode with special tokens
tokens = tokenizer.encode(text)

# Decode preserving special tokens
decoded = tokenizer.decode(tokens)
```

## Error Handling

### Exception Types

#### `VocabularyFullError`
Raised when vocabulary size limit is reached during training.

**Attributes:**
- `max_size`: Maximum allowed vocabulary size
- `current_size`: Current vocabulary size

#### `TokenNotFoundError`
Raised when a token ID is not found in vocabulary during decoding.

**Attributes:**
- `token_id`: The missing token ID
- `vocab_size`: Current vocabulary size

#### `InvalidUTF8Error`
Raised when text contains invalid UTF-8 sequences.

**Attributes:**
- `position`: Position of invalid sequence
- `bytes`: Invalid byte sequence

### Error Recovery

```python
try:
    tokens = tokenizer.encode(text)
except InvalidUTF8Error as e:
    # Clean text and retry
    cleaned_text = clean_utf8(text)
    tokens = tokenizer.encode(cleaned_text)
except VocabularyFullError as e:
    # Reduce vocabulary size and retrain
    tokenizer.vocab_size = e.current_size - 1000
    tokenizer.train(texts)
```

## Performance Optimization

### Memory Management

```python
# Use streaming for large texts
def stream_encode(text: str, chunk_size: int = 1000):
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        yield tokenizer.encode(chunk)

# Process large corpus in batches
def batch_train(texts: List[str], batch_size: int = 1000):
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        tokenizer.train(batch)
```

### Caching

```python
# Cache frequent tokenizations
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_encode(text: str) -> Tuple[int, ...]:
    return tuple(tokenizer.encode(text))
```

## Testing

### Unit Tests

```python
def test_bpe_training():
    tokenizer = GPT4BPETokenizer(vocab_size=100)
    texts = ["Hello world", "Goodbye world"]
    tokenizer.train(texts)
    
    assert len(tokenizer.vocab) <= 100
    assert len(tokenizer.merges) > 0

def test_encoding_decoding():
    tokenizer = GPT4BPETokenizer()
    original_text = "Hello world!"
    
    tokens = tokenizer.encode(original_text)
    decoded_text = tokenizer.decode(tokens)
    
    assert decoded_text == original_text
```

### Integration Tests

```python
def test_end_to_end_workflow():
    # Test complete training and usage workflow
    tokenizer = GPT4BPETokenizer(vocab_size=1000)
    
    # Training
    training_texts = load_training_corpus()
    tokenizer.train(training_texts)
    
    # Save and load
    tokenizer.save("test_tokenizer.json")
    new_tokenizer = GPT4BPETokenizer()
    new_tokenizer.load("test_tokenizer.json")
    
    # Test consistency
    test_text = "Test input text"
    assert tokenizer.encode(test_text) == new_tokenizer.encode(test_text)
```
