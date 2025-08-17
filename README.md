# GPT-Tokenizer

A comprehensive implementation of tokenization algorithms used in Large Language Models, including Byte Pair Encoding (BPE), UTF-8 handling, and interactive examples.

## 🚀 Features

- **BPE Implementation**: Complete Byte Pair Encoding algorithm from scratch
- **UTF-8 Support**: Proper handling of Unicode and multi-byte characters
- **Regex Tokenization**: GPT-2 style pattern matching for text segmentation
- **Interactive Learning**: Jupyter notebook with step-by-step examples
- **Production Ready**: Integration with tiktoken for real-world applications

## 📚 Documentation

- **[Technical Overview](docs/README.md)** - System architecture and implementation details
- **[API Reference](docs/API.md)** - Complete function documentation and examples
- **[System Architecture](docs/ARCHITECTURE.md)** - Component design and data flow
- **[ReadTheDocs Setup](README_RTD_SETUP.md)** - How to enable automatic documentation generation

## 🔧 Quick Start

```bash
# Clone and setup
git clone https://github.com/yourusername/gpt-tokenizer.git
cd gpt-tokenizer
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Start learning
jupyter notebook scripts/tokenisation.ipynb
```

## 🌐 Live Documentation

This project automatically generates and deploys documentation to ReadTheDocs with every commit. The documentation includes:

- **API Reference**: Auto-generated from Python docstrings
- **Architecture Guide**: System design and implementation details
- **Examples**: Practical usage examples and tutorials
- **Performance Analysis**: Time complexity and memory usage

**Documentation URL**: `https://gpt-tokenizer.readthedocs.io/`

### Automatic Updates

- Every commit to `main` branch triggers documentation rebuild
- API documentation automatically extracted from code
- Multiple formats: HTML, PDF, and ePub
- Version control for different releases

## 📁 Project Structure

```
├── scripts/
│   ├── tokenisation.ipynb    # Main Jupyter notebook
│   ├── gpt4_bpe_tokenizer.py # BPE tokenizer implementation
│   ├── regex_tokenizer.py    # Regex-based tokenizer
│   ├── basic_tokenizer.py    # Basic tokenizer
│   └── helpers.py            # Utility functions
├── imgs/                     # Diagrams and visualizations
├── tests/                    # Test files
└── .github/workflows/        # CI/CD automation for docs and testing
```

## 🎯 What You'll Learn

- **Tokenization Fundamentals**: How text becomes numbers for AI models
- **BPE Algorithm**: Step-by-step implementation of the compression algorithm
- **Unicode Handling**: Proper text encoding and decoding
- **Vocabulary Building**: Creating and managing token vocabularies
- **Real-world Applications**: Using production tokenizers like tiktoken

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for the tiktoken library
- The AI/ML community for inspiration and feedback

---

**Made with ❤️ for the AI/ML community**