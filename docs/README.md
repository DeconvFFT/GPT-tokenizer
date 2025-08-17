# GPT-Tokenizer Technical Documentation

## Overview

This repository contains implementations of tokenization algorithms used in Large Language Models, with a focus on Byte Pair Encoding (BPE) and related techniques.

## Architecture

### Core Components

- **BPE Tokenizer**: Implementation of the Byte Pair Encoding algorithm
- **UTF-8 Handler**: Text encoding and decoding utilities
- **Regex Patterns**: GPT-2 style tokenization patterns
- **Vocabulary Management**: Token-to-ID mapping and management

### File Structure

```
scripts/
├── tokenisation.ipynb          # Main implementation notebook
├── gpt4_bpe_tokenizer.py      # BPE algorithm implementation
├── regex_tokenizer.py          # Regex-based tokenization
├── basic_tokenizer.py          # Basic tokenization utilities
└── helpers.py                  # Utility functions

imgs/
└── tokenizer_diagram_final.svg # System architecture diagram

tests/                          # Unit tests and validation
```

## Implementation Details

### BPE Algorithm

The Byte Pair Encoding implementation follows the standard algorithm:

1. **Initialization**: Start with individual bytes as vocabulary
2. **Frequency Analysis**: Count byte pair occurrences
3. **Merging**: Replace most frequent pairs with new tokens
4. **Iteration**: Repeat until vocabulary size limit reached

### UTF-8 Handling

- **Encoding**: Converts text to UTF-8 byte sequences
- **Decoding**: Reconstructs text from byte sequences
- **Error Handling**: Graceful fallback for invalid sequences

### Tokenization Process

```
Raw Text → UTF-8 Bytes → BPE Merges → Token IDs
    ↓           ↓           ↓          ↓
  "Hello" → [72,101,108,108,111] → [15496, 995, 0]
```

## API Reference

### Core Functions

#### `encode(text: str) -> List[int]`
Converts input text to token IDs using trained BPE merges.

**Parameters:**
- `text`: Input string to tokenize

**Returns:**
- List of integer token IDs

**Example:**
```python
from scripts.gpt4_bpe_tokenizer import GPT4BPETokenizer

tokenizer = GPT4BPETokenizer()
tokens = tokenizer.encode("Hello world!")
# Returns: [15496, 995, 0]
```

#### `decode(token_ids: List[int]) -> str`
Converts token IDs back to text.

**Parameters:**
- `token_ids`: List of token IDs

**Returns:**
- Reconstructed text string

#### `train(texts: List[str], vocab_size: int) -> None`
Trains the BPE tokenizer on provided text corpus.

**Parameters:**
- `texts`: List of training text strings
- `vocab_size`: Maximum vocabulary size

## Configuration

### Environment Variables

- `PYTHON_VERSION`: Python version for development (default: 3.12)
- `REQUIREMENTS_FILE`: Path to requirements.txt (default: requirements.txt)

### Dependencies

```
tiktoken>=0.5.0          # OpenAI tokenizer library
regex>=2023.0.0          # Regular expression library
jupyter>=1.0.0           # Jupyter notebook support
```

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_bpe.py

# Run with coverage
python -m pytest --cov=scripts tests/
```

### Test Structure

- `tests/test_bpe.py`: BPE algorithm tests
- `tests/test_utf8.py`: UTF-8 encoding/decoding tests
- `tests/test_integration.py`: End-to-end workflow tests

## Performance Characteristics

### Time Complexity

- **Training**: O(n × m × log m) where n is corpus size, m is vocabulary size
- **Encoding**: O(t × log v) where t is text length, v is vocabulary size
- **Decoding**: O(t) where t is number of tokens

### Memory Usage

- **Vocabulary**: O(v) where v is vocabulary size
- **Merges**: O(m) where m is number of merge operations
- **Working Memory**: O(t) where t is text length

## Error Handling

### Common Issues

1. **Out-of-Vocabulary Tokens**
   - **Cause**: Token not in training vocabulary
   - **Solution**: Use `<unk>` token or retrain with larger corpus

2. **UTF-8 Decoding Errors**
   - **Cause**: Invalid byte sequences
   - **Solution**: Implement error correction or use replacement characters

3. **Memory Issues**
   - **Cause**: Large vocabulary or long texts
   - **Solution**: Implement streaming or chunked processing

### Error Codes

- `E001`: Vocabulary size limit exceeded
- `E002`: Invalid UTF-8 sequence
- `E003`: Merge operation failed
- `E004`: Token not found in vocabulary

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/DeconvFFT/GPT-tokenizer.git
cd GPT-tokenizer

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### Code Style

- **Formatting**: Black code formatter
- **Linting**: Flake8 with max line length 88
- **Type Hints**: Required for all public functions
- **Documentation**: Google-style docstrings

### Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/name`
3. Make changes following code style guidelines
4. Add tests for new functionality
5. Submit pull request with detailed description

## Troubleshooting

### Build Issues

**Problem**: GitHub Actions workflow fails
**Solution**: Check workflow file syntax and ensure all dependencies are available

**Problem**: Documentation not building
**Solution**: Verify all required files exist and have correct permissions

### Runtime Issues

**Problem**: Tokenization produces unexpected results
**Solution**: Verify vocabulary was trained on similar text corpus

**Problem**: Memory usage too high
**Solution**: Implement streaming tokenization or reduce vocabulary size

## References

- [BPE Paper](https://arxiv.org/abs/1508.07909): Neural Machine Translation of Rare Words with Subword Units
- [GPT-2 Tokenizer](https://github.com/openai/gpt-2): OpenAI's implementation
- [tiktoken](https://github.com/openai/tiktoken): Fast BPE tokenizer implementation

## License

MIT License - see [LICENSE](../LICENSE) file for details.
