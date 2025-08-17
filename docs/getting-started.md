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
