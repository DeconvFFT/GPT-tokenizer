# Getting Started with MinBPE

Welcome to MinBPE, a minimal implementation of Byte Pair Encoding (BPE) tokenization algorithms used in modern language models.

## Installation

### Prerequisites

- Python 3.12 or higher
- pip or uv package manager

### Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/gpt-tokenizer.git
cd gpt-tokenizer

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Install for Development

```bash
# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

## Quick Start

### Basic Usage

```python
from minbpe import Tokenizer

# Create a tokenizer instance
tokenizer = Tokenizer()

# Check basic vocabulary
print(f"Base vocabulary size: {len(tokenizer.vocab)}")
# Output: Base vocabulary size: 256
```

### Using the BasicTokenizer

```python
from minbpe import BasicTokenizer

# Create and train a basic tokenizer
tokenizer = BasicTokenizer()
text = "Hello world! This is a test of the BPE algorithm."
tokenizer.train(text, vocab_size=300, verbose=True)

# Check the trained vocabulary
print(f"Trained vocabulary size: {len(tokenizer.vocab)}")
print(f"Number of merges learned: {len(tokenizer.merges)}")

# Encode and decode text
encoded = tokenizer.encode("Hello world!")
print(f"Encoded: {encoded}")
decoded = tokenizer.decode(encoded)
print(f"Decoded: {decoded}")
```

### Using the RegexTokenizer

```python
from minbpe import RegexTokenizer

# Create a regex tokenizer with default GPT-4 pattern
tokenizer = RegexTokenizer()
text = "Hello world! This is a test of the regex BPE algorithm."
tokenizer.train(text, vocab_size=300, verbose=True)

# Check the trained vocabulary
print(f"Trained vocabulary size: {len(tokenizer.vocab)}")
print(f"Using pattern: {tokenizer.pattern[:50]}...")

# Encode and decode text
encoded = tokenizer.encode("Hello world!")
print(f"Encoded: {encoded}")
decoded = tokenizer.decode(encoded)
print(f"Decoded: {decoded}")

# Use with special tokens
tokenizer.register_special_tokens({"<|endoftext|>": 100257})
encoded = tokenizer.encode("Hello <|endoftext|>", allowed_special_tokens="all")
print(f"With special tokens: {encoded}")
```

### Using Custom Regex Patterns

```python
# Create tokenizer with custom pattern
custom_pattern = r"\w+|\s+|[^\w\s]"
custom_tokenizer = RegexTokenizer(custom_pattern)

# Train on text
custom_tokenizer.train("Hello world! This is a test.", 300)
print(f"Custom pattern: {custom_tokenizer.pattern}")

# Compare with default pattern
default_tokenizer = RegexTokenizer()
default_tokenizer.train("Hello world! This is a test.", 300)

# Encode same text with different patterns
text = "Hello world!"
custom_encoded = custom_tokenizer.encode(text)
default_encoded = default_tokenizer.encode(text)

print(f"Custom pattern tokens: {len(custom_encoded)}")
print(f"Default pattern tokens: {len(default_encoded)}")
```

### Using Utility Functions

```python
from minbpe.base import get_pair_frequencies, merge_pair

# Analyze byte pair frequencies
text_bytes = [72, 101, 108, 108, 111]  # "Hello" in ASCII
freqs = get_pair_frequencies(text_bytes)
print(f"Frequencies: {freqs}")
# Output: Frequencies: {(72, 101): 1, (101, 108): 2, (108, 111): 1}

# Merge a byte pair
merged = merge_pair(text_bytes, (101, 108), 256)
print(f"Merged: {merged}")
# Output: Merged: [72, 256, 111]
```

### Working with Control Characters

```python
from minbpe.base import replace_control_characters, render_token

# Handle control characters
text = "Hello\nWorld\tTabbed"
cleaned = replace_control_characters(text)
print(f"Cleaned: {cleaned}")
# Output: Cleaned: Hello\u000aWorld\u0009Tabbed

# Render byte tokens
token = b"Hello\nWorld"
rendered = render_token(token)
print(f"Rendered: {rendered}")
# Output: Rendered: Hello\u000aWorld
```

## Working with Special Tokens

### Understanding Special Tokens

Special tokens are reserved vocabulary items that have specific meanings in language models:

```python
from minbpe import RegexTokenizer

# Common special tokens
special_tokens = {
    "<|endoftext|>": 100257,  # End of text marker
    "<|pad|>": 100258,        # Padding token
    "<|unk|>": 100259,        # Unknown token
    "<|start|>": 100260,      # Start of sequence
    "<|end|>": 100261         # End of sequence
}

tokenizer = RegexTokenizer()
tokenizer.register_special_tokens(special_tokens)
print(f"Registered {len(tokenizer.special_tokens)} special tokens")
```

### Special Token Encoding Modes

```python
# Different ways to handle special tokens during encoding
text = "Hello <|endoftext|> world!"

# Mode 1: Process all special tokens
encoded_all = tokenizer.encode(text, allowed_special_tokens="all")
print(f"All special tokens: {encoded_all}")

# Mode 2: Ignore all special tokens
encoded_none = tokenizer.encode(text, allowed_special_tokens="none")
print(f"No special tokens: {encoded_none}")

# Mode 3: Raise error if special tokens found
try:
    encoded_strict = tokenizer.encode(text, allowed_special_tokens="none_raise")
except AssertionError as e:
    print(f"Strict mode error: {e}")

# Mode 4: Selective special token processing
encoded_selective = tokenizer.encode(text, allowed_special_tokens={"<|endoftext|>"})
print(f"Selective tokens: {encoded_selective}")
```

### Advanced Regex Pattern Usage

```python
# Compare different regex patterns
patterns = {
    "Simple": r"\w+|\s+|[^\w\s]",
    "GPT-2": r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+""",
    "GPT-4": r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+"""
}

# Test each pattern
test_text = "Hello world! This is a test. Don't worry about it."

for name, pattern in patterns.items():
    tokenizer = RegexTokenizer(pattern)
    tokenizer.train(test_text, 300)
    encoded = tokenizer.encode(test_text)
    print(f"{name} pattern: {len(encoded)} tokens")
```

## Training Your Own Tokenizer

### Basic Training

```python
from minbpe import BasicTokenizer

# Create a tokenizer
tokenizer = BasicTokenizer()

# Train on your text corpus
training_text = """
This is a sample text for training a BPE tokenizer.
The tokenizer will learn to merge frequent byte pairs.
You can use any text corpus for training.
"""

# Train with a target vocabulary size
tokenizer.train(training_text, vocab_size=500, verbose=True)

# Save the trained model
tokenizer.save("my_trained_tokenizer")
```

### Advanced Training

```python
# Train on larger corpus
with open("large_text_file.txt", "r") as f:
    large_corpus = f.read()

# Train with larger vocabulary
tokenizer.train(large_corpus, vocab_size=1000, verbose=True)

# Check compression efficiency
test_text = "This is a test of the trained tokenizer."
original_bytes = len(test_text.encode('utf-8'))
encoded_tokens = len(tokenizer.encode(test_text))
compression_ratio = original_bytes / encoded_tokens

print(f"Original: {original_bytes} bytes")
print(f"Encoded: {encoded_tokens} tokens")
print(f"Compression ratio: {compression_ratio:.2f}")
```

## Examples

See the `scripts/` directory for Jupyter notebook examples:

```bash
# Start Jupyter
jupyter notebook scripts/tokenisation.ipynb
```

## Getting Help

- **Documentation**: This site contains comprehensive guides and API reference
- **Issues**: Report bugs or request features on GitHub
- **Discussions**: Join community discussions for questions and ideas
