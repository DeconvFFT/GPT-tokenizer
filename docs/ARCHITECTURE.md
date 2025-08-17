# System Architecture

## Overview

The GPT-Tokenizer system implements tokenization algorithms used in Large Language Models, with a modular architecture that separates concerns and enables extensibility.

## System Components

### 1. Core Tokenization Engine

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Input Text    │───▶│  UTF-8 Encoder   │───▶│  BPE Processor  │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │  Byte Stream     │    │  Token Output   │
                       │                  │    │                 │
                       └──────────────────┘    └─────────────────┘
```

**Responsibilities:**
- Text preprocessing and normalization
- UTF-8 encoding/decoding
- Byte pair frequency analysis
- Token generation and mapping

### 2. Vocabulary Management System

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Training Data  │───▶│  Frequency       │───▶│  Vocabulary     │
│                 │    │  Analyzer        │    │  Builder        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │  Merge Rules     │    │  Token ID       │
                       │                  │    │  Mapping        │
                       └──────────────────┘    └─────────────────┘
```

**Components:**
- **Frequency Analyzer**: Counts byte pair occurrences
- **Vocabulary Builder**: Constructs token vocabulary
- **Merge Rule Manager**: Maintains BPE merge operations
- **ID Mapper**: Maps tokens to unique identifiers

### 3. Pattern Matching Engine

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Text Input     │───▶│  Regex Pattern   │───▶│  Token          │
│                 │    │  Matcher         │    │  Extractor      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │  Pattern Types   │    │  Token          │
                       │                  │    │  Sequences      │
                       └──────────────────┘    └─────────────────┘
```

**Pattern Types:**
- Contractions: `'s|'t|'re|'ve|'m|'ll|'d`
- Words: `\p{L}+` (Unicode letter sequences)
- Numbers: `\p{N}+` (Unicode number sequences)
- Punctuation: `[^\s\p{L}\p{N}]+`
- Whitespace: `\s+(?!\S)|\s+`

## Data Flow Architecture

### Training Phase

```
1. Text Corpus Input
   ↓
2. UTF-8 Encoding
   ↓
3. Byte Frequency Analysis
   ↓
4. Pair Identification
   ↓
5. Merge Rule Creation
   ↓
6. Vocabulary Update
   ↓
7. Model Persistence
```

**Data Structures:**
```python
class TrainingState:
    corpus_size: int
    byte_frequencies: Counter[Tuple[int, int]]
    merge_rules: Dict[Tuple[int, int], int]
    vocabulary: Dict[int, str]
    iteration_count: int
```

### Inference Phase

```
1. Text Input
   ↓
2. UTF-8 Encoding
   ↓
3. Merge Rule Application
   ↓
4. Token ID Lookup
   ↓
5. Output Generation
```

**Data Structures:**
```python
class InferenceState:
    input_text: str
    byte_sequence: bytes
    applied_merges: List[Tuple[int, int]]
    token_sequence: List[str]
    output_ids: List[int]
```

## Class Architecture

### GPT4BPETokenizer

```python
class GPT4BPETokenizer:
    def __init__(self, vocab_size: int):
        self.vocab_size: int
        self.vocab: Dict[int, str]
        self.merges: Dict[Tuple[int, int], int]
        self.pattern: re.Pattern
        
    def train(self, texts: List[str]) -> None
    def encode(self, text: str) -> List[int]
    def decode(self, token_ids: List[int]) -> str
    def save(self, filepath: str) -> None
    def load(self, filepath: str) -> None
    def _apply_merges(self, texts: List[str], pair: Tuple[int, int], new_token: str) -> List[str]
```

**Design Patterns:**
- **Strategy Pattern**: Different tokenization strategies
- **Factory Pattern**: Token creation and management
- **Observer Pattern**: Training progress monitoring
- **Memento Pattern**: State persistence and restoration

### RegexTokenizer

```python
class RegexTokenizer:
    def __init__(self):
        self.pattern: re.Pattern
        self.special_tokens: Dict[str, int]
        self.vocab: Dict[str, int]
        self.reverse_vocab: Dict[int, str]
        
    def tokenize(self, text: str) -> List[str]
    def encode(self, text: str) -> List[int]
    def decode(self, token_ids: List[int]) -> str
    def analyze_patterns(self, text: str) -> List[Tuple[str, str, int]]
```

## Memory Management

### Vocabulary Storage

```python
# Efficient vocabulary representation
class Vocabulary:
    def __init__(self, max_size: int):
        self.tokens: Dict[int, str] = {}
        self.reverse_lookup: Dict[str, int] = {}
        self.frequency_cache: Dict[int, int] = {}
        self.max_size: int = max_size
        
    def add_token(self, token: str) -> int:
        if len(self.tokens) >= self.max_size:
            raise VocabularyFullError(self.max_size, len(self.tokens))
        
        token_id = len(self.tokens)
        self.tokens[token_id] = token
        self.reverse_lookup[token] = token_id
        return token_id
```

### Merge Rule Optimization

```python
# Efficient merge rule storage
class MergeRules:
    def __init__(self):
        self.rules: Dict[Tuple[int, int], int] = {}
        self.reverse_rules: Dict[int, Tuple[int, int]] = {}
        self.frequency_cache: Dict[Tuple[int, int], int] = {}
        
    def add_rule(self, pair: Tuple[int, int], new_token_id: int) -> None:
        self.rules[pair] = new_token_id
        self.reverse_rules[new_token_id] = pair
        
    def apply_merges(self, text: bytes) -> bytes:
        # Optimized merge application
        result = bytearray(text)
        i = 0
        while i < len(result) - 1:
            pair = (result[i], result[i + 1])
            if pair in self.rules:
                # Apply merge
                new_token = self.rules[pair]
                result[i:i + 2] = bytes([new_token])
            i += 1
        return bytes(result)
```

## Performance Characteristics

### Time Complexity Analysis

**Training Phase:**
- **Byte Frequency Counting**: O(n × m) where n is corpus size, m is average text length
- **Pair Identification**: O(v²) where v is vocabulary size
- **Merge Application**: O(n × m × r) where r is number of merge rules
- **Total Training**: O(n × m × v²)

**Inference Phase:**
- **Text Encoding**: O(t) where t is text length
- **Merge Application**: O(t × r) where r is number of merge rules
- **Token Lookup**: O(t × log v) where v is vocabulary size
- **Total Inference**: O(t × (r + log v))

### Memory Usage Analysis

**Static Memory:**
- **Vocabulary**: O(v) where v is vocabulary size
- **Merge Rules**: O(m) where m is number of merge rules
- **Pattern Cache**: O(p) where p is number of regex patterns

**Dynamic Memory:**
- **Working Buffer**: O(t) where t is text length
- **Temporary Tokens**: O(t) for intermediate results
- **Frequency Counters**: O(b²) where b is byte alphabet size (256²)

### Optimization Strategies

**1. Memory Pooling:**
```python
class MemoryPool:
    def __init__(self, chunk_size: int = 1024):
        self.chunks: List[bytearray] = []
        self.chunk_size = chunk_size
        
    def get_buffer(self, size: int) -> bytearray:
        if size <= self.chunk_size:
            return self.chunks.pop() if self.chunks else bytearray(self.chunk_size)
        return bytearray(size)
        
    def return_buffer(self, buffer: bytearray) -> None:
        if len(buffer) == self.chunk_size:
            buffer.clear()
            self.chunks.append(buffer)
```

**2. Lazy Evaluation:**
```python
class LazyTokenizer:
    def __init__(self, tokenizer: GPT4BPETokenizer):
        self.tokenizer = tokenizer
        self.cache: Dict[str, List[int]] = {}
        
    def encode(self, text: str) -> List[int]:
        if text not in self.cache:
            self.cache[text] = self.tokenizer.encode(text)
        return self.cache[text]
```

**3. Streaming Processing:**
```python
def stream_tokenize(text: str, chunk_size: int = 1000):
    """Process text in chunks to reduce memory usage."""
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        yield tokenizer.encode(chunk)
```

## Error Handling Architecture

### Exception Hierarchy

```python
class TokenizerError(Exception):
    """Base exception for tokenizer errors."""
    pass

class VocabularyFullError(TokenizerError):
    """Raised when vocabulary size limit is reached."""
    def __init__(self, max_size: int, current_size: int):
        self.max_size = max_size
        self.current_size = current_size
        super().__init__(f"Vocabulary full: {current_size}/{max_size}")

class InvalidUTF8Error(TokenizerError):
    """Raised when invalid UTF-8 sequence is encountered."""
    def __init__(self, position: int, bytes_sequence: bytes):
        self.position = position
        self.bytes_sequence = bytes_sequence
        super().__init__(f"Invalid UTF-8 at position {position}")

class TokenNotFoundError(TokenizerError):
    """Raised when token ID is not found in vocabulary."""
    def __init__(self, token_id: int, vocab_size: int):
        self.token_id = token_id
        self.vocab_size = vocab_size
        super().__init__(f"Token ID {token_id} not found in vocabulary of size {vocab_size}")
```

### Error Recovery Strategies

**1. Graceful Degradation:**
```python
def robust_encode(text: str, fallback_token: str = "<|unk|>") -> List[int]:
    try:
        return tokenizer.encode(text)
    except InvalidUTF8Error:
        # Clean text and retry
        cleaned_text = clean_utf8(text)
        return tokenizer.encode(cleaned_text)
    except VocabularyFullError:
        # Use fallback tokenization
        return [tokenizer.vocab.get(fallback_token, 0)]
```

**2. Retry Mechanisms:**
```python
def retry_encode(text: str, max_retries: int = 3) -> List[int]:
    for attempt in range(max_retries):
        try:
            return tokenizer.encode(text)
        except TokenizerError as e:
            if attempt == max_retries - 1:
                raise
            # Apply recovery strategy based on error type
            text = apply_recovery_strategy(text, e)
```

## Testing Architecture

### Test Structure

```
tests/
├── unit/
│   ├── test_bpe.py          # BPE algorithm tests
│   ├── test_utf8.py         # UTF-8 handling tests
│   ├── test_vocabulary.py   # Vocabulary management tests
│   └── test_patterns.py     # Pattern matching tests
├── integration/
│   ├── test_end_to_end.py   # Complete workflow tests
│   ├── test_performance.py  # Performance benchmarks
│   └── test_memory.py       # Memory usage tests
└── fixtures/
    ├── sample_texts.txt     # Test corpus
    ├── expected_tokens.json # Expected outputs
    └── performance_data.csv # Benchmark data
```

### Test Patterns

**1. Property-Based Testing:**
```python
from hypothesis import given, strategies as st

@given(st.text(min_size=1, max_size=100))
def test_encode_decode_roundtrip(text):
    """Encoding then decoding should return original text."""
    tokens = tokenizer.encode(text)
    decoded = tokenizer.decode(tokens)
    assert decoded == text
```

**2. Performance Testing:**
```python
def test_encoding_performance():
    """Encoding should complete within performance budget."""
    import time
    
    start_time = time.time()
    tokens = tokenizer.encode("x" * 10000)
    end_time = time.time()
    
    assert end_time - start_time < 0.1  # 100ms budget
    assert len(tokens) > 0
```

**3. Memory Testing:**
```python
def test_memory_usage():
    """Memory usage should be within acceptable bounds."""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Perform tokenization
    tokenizer.encode("x" * 100000)
    
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    # Memory increase should be less than 10MB
    assert memory_increase < 10 * 1024 * 1024
```

## Deployment Architecture

### GitHub Actions Workflow

```yaml
name: Deploy to GitHub Pages
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Build Documentation
        run: |
          mkdir -p docs
          cp README.md docs/index.md
          cp *.md docs/
          cp -r scripts docs/
          cp -r imgs docs/
      - name: Deploy
        uses: actions/deploy-pages@v4
```

### Documentation Structure

```
docs/
├── index.md              # Main documentation entry point
├── README.md             # Technical overview
├── ARCHITECTURE.md       # System architecture
├── API.md                # API reference
├── scripts/              # Code examples
└── imgs/                 # Architecture diagrams
```

## Future Enhancements

### Planned Features

1. **Multi-Language Support**: Extend UTF-8 handling to other encodings
2. **Distributed Training**: Support for large-scale corpus processing
3. **Model Compression**: Optimize vocabulary storage and lookup
4. **Real-time Updates**: Incremental vocabulary updates without retraining
5. **Plugin Architecture**: Extensible tokenization strategies

### Performance Targets

- **Training Speed**: 10x improvement through parallel processing
- **Memory Usage**: 50% reduction through optimized data structures
- **Inference Latency**: Sub-millisecond tokenization for typical texts
- **Scalability**: Support for vocabularies up to 1M tokens
