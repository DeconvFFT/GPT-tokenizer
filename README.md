# GPT-Tokenizer

A comprehensive implementation of tokenization algorithms used in Large Language Models, including Byte Pair Encoding (BPE), UTF-8 handling, and interactive examples.

## 🚀 Features

- **BPE Implementation**: Complete Byte Pair Encoding algorithm from scratch
- **UTF-8 Support**: Proper handling of Unicode and multi-byte characters
- **Regex Tokenization**: GPT-2 style pattern matching for text segmentation
- **Interactive Learning**: Jupyter notebook with step-by-step examples
- **Production Ready**: Integration with tiktoken for real-world applications

## 📚 Documentation

- **[Diagram Creation Prompt](diagram_creation_prompt.md)** - Optimized prompt for creating professional diagrams
- **[Usage Guide](usage_guide.md)** - How to use the tokenization tools
- **[GitHub Pages Setup](GITHUB_PAGES_SETUP.md)** - Enable automatic documentation deployment

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

This project automatically deploys documentation to GitHub Pages with every commit. To enable:

1. Go to repository Settings → Pages
2. Select "GitHub Actions" as source
3. Documentation will be available at: `https://yourusername.github.io/gpt-tokenizer`

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
└── .github/workflows/        # GitHub Actions for automation
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