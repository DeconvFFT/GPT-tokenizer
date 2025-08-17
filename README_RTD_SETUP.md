# ReadTheDocs Setup Guide

This guide explains how to set up automatic documentation generation using ReadTheDocs, Sphinx, and autodoc.

## 🚀 What This Setup Provides

- **Automatic Documentation**: Every commit automatically updates your docs
- **Professional Appearance**: Clean, searchable documentation with ReadTheDocs theme
- **API Documentation**: Automatically generated from your Python code
- **Multiple Formats**: HTML, PDF, and ePub output
- **Version Control**: Documentation for different versions of your code
- **Free Hosting**: No cost for hosting your documentation

## 📋 Prerequisites

1. **GitHub Repository**: Your code must be in a public GitHub repository
2. **Python Package**: Your code should be structured as a Python package
3. **Sphinx Configuration**: Already configured in this repository

## 🔧 Step-by-Step Setup

### Step 1: Connect to ReadTheDocs

1. Go to [ReadTheDocs.org](https://readthedocs.org/)
2. Sign in with your GitHub account
3. Click **"Import a Project"**
4. Select your `GPT-tokenizer` repository
5. Click **"Import"**

### Step 2: Configure Project Settings

In your ReadTheDocs project dashboard:

1. **General Settings**:
   - **Name**: `gpt-tokenizer` (or your preferred name)
   - **Repository**: `https://github.com/DeconvFFT/GPT-tokenizer`
   - **Default Branch**: `main`
   - **Documentation Type**: `Sphinx`

2. **Advanced Settings**:
   - **Install Project**: Check this box
   - **Use virtualenv**: Check this box
   - **Requirements file**: `requirements-dev.txt`

### Step 3: Build Configuration

The `.readthedocs.yml` file is already configured with:

```yaml
version: 2
sphinx:
  configuration: docs/conf.py
python:
  version: "3.12"
  install:
    - method: pip
      path: .
      extra_requirements:
        - docs
```

### Step 4: Trigger First Build

1. Go to your project's **"Builds"** tab
2. Click **"Build Version"**
3. Select **"latest"** version
4. Click **"Build"**

## 🔍 How It Works

### Automatic Documentation Generation

1. **On Every Commit**: ReadTheDocs detects changes to your repository
2. **Installation**: Installs your package with development dependencies
3. **API Generation**: Runs `sphinx-apidoc` to extract docstrings
4. **Build Process**: Compiles Sphinx documentation to HTML/PDF
5. **Deployment**: Publishes to `https://yourproject.readthedocs.io`

### File Structure

```
docs/
├── conf.py              # Sphinx configuration
├── index.rst            # Main documentation page
├── README.md            # Technical overview
├── API.md               # API reference
├── ARCHITECTURE.md      # System architecture
├── examples.rst         # Usage examples
├── Makefile             # Build commands
└── _build/              # Generated documentation (auto-created)
```

### Sphinx Extensions Used

- **`sphinx.ext.autodoc`**: Automatically extract docstrings
- **`sphinx.ext.napoleon`**: Support for Google/NumPy docstring formats
- **`sphinx.ext.viewcode`**: Link to source code
- **`sphinx.ext.intersphinx`**: Link to other documentation
- **`sphinx_rtd_theme`**: ReadTheDocs theme

## 📚 Documentation Features

### Auto-Generated API Docs

Your Python classes and functions automatically appear in the documentation:

```python
class GPT4BPETokenizer:
    """A BPE tokenizer implementation."""
    
    def encode(self, text: str) -> List[int]:
        """Encode text to token IDs.
        
        Args:
            text: Input text string
            
        Returns:
            List of token IDs
        """
        pass
```

### Cross-References

- **Function links**: Click on function names to see definitions
- **Class inheritance**: Visual representation of class hierarchies
- **Source code**: Direct links to GitHub source files
- **External links**: Links to Python standard library docs

### Search and Navigation

- **Full-text search**: Search across all documentation
- **Table of contents**: Hierarchical navigation
- **Index**: Alphabetical listing of all functions/classes
- **Version selector**: Switch between different versions

## 🛠️ Local Development

### Building Documentation Locally

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install package in development mode
pip install -e .

# Build documentation
cd docs
make apidoc    # Generate API documentation
make html      # Build HTML documentation
make pdf       # Build PDF documentation
```

### Preview Documentation

```bash
# Start local server
cd docs/_build/html
python -m http.server 8000

# Open browser to http://localhost:8000
```

### Testing Documentation

```bash
# Check for broken links
make linkcheck

# Run doctests
make doctest

# Validate HTML
make html
```

## 🔄 Continuous Integration

### GitHub Actions Integration

The `.github/workflows/docs.yml` workflow:

1. **Builds documentation** on every push/PR
2. **Runs tests** across multiple Python versions
3. **Uploads artifacts** for inspection
4. **Checks documentation** for errors

### Automatic Deployment

1. **Push to main**: Triggers GitHub Actions build
2. **Build success**: Documentation is built and tested
3. **ReadTheDocs**: Automatically pulls and builds
4. **Live update**: Documentation goes live at your URL

## 📖 Writing Good Documentation

### Docstring Standards

Use Google-style docstrings for best autodoc support:

```python
def train(self, texts: List[str], vocab_size: int = 50000) -> None:
    """Train the BPE tokenizer on a corpus of texts.
    
    This method implements the Byte Pair Encoding algorithm to build
    a vocabulary of tokens from the input texts.
    
    Args:
        texts: List of training text strings
        vocab_size: Maximum size of the vocabulary
        
    Raises:
        ValueError: If texts list is empty
        MemoryError: If vocabulary size exceeds available memory
        
    Example:
        >>> tokenizer = GPT4BPETokenizer(vocab_size=1000)
        >>> tokenizer.train(["Hello world", "Goodbye world"])
        >>> len(tokenizer.vocab)
        1000
    """
    pass
```

### RST File Structure

```rst
Section Title
============

Subsection
----------

Subsubsection
~~~~~~~~~~~~

.. code-block:: python

    # Your code examples here
    tokenizer = GPT4BPETokenizer()
    
.. note::

    Important notes and warnings go here.
    
.. warning::

    Warnings about potential issues.
```

## 🚨 Troubleshooting

### Common Issues

**Build Failures**:
- Check Python version compatibility
- Verify all dependencies are installed
- Check for syntax errors in Python code
- Ensure docstrings are properly formatted

**Missing API Documentation**:
- Verify `sphinx.ext.autodoc` is enabled
- Check that classes/functions have docstrings
- Ensure package is properly installed
- Run `make apidoc` locally to test

**Import Errors**:
- Check `sys.path` configuration in `conf.py`
- Verify package structure and `__init__.py` files
- Test imports locally before pushing

### Debugging Steps

1. **Check Build Logs**: Look at ReadTheDocs build output
2. **Test Locally**: Build documentation on your machine
3. **Verify Dependencies**: Ensure all requirements are met
4. **Check Configuration**: Validate Sphinx configuration
5. **Review Code**: Look for syntax or import issues

## 🌟 Best Practices

### Documentation Standards

1. **Keep it Updated**: Update docs with every code change
2. **Use Examples**: Include practical code examples
3. **Be Consistent**: Follow consistent formatting and style
4. **Test Everything**: Verify all examples work
5. **Version Control**: Tag releases for documentation versions

### Maintenance

1. **Regular Reviews**: Periodically review and update docs
2. **User Feedback**: Incorporate user questions and feedback
3. **Automated Checks**: Use CI/CD to catch documentation issues
4. **Performance**: Monitor build times and optimize if needed

## 🎯 Next Steps

After setup:

1. **Customize Theme**: Modify `docs/conf.py` for custom styling
2. **Add Examples**: Create more comprehensive usage examples
3. **Performance**: Optimize build times for large codebases
4. **Analytics**: Enable ReadTheDocs analytics for insights
5. **Custom Domain**: Set up custom domain if desired

## 📞 Support

- **ReadTheDocs Documentation**: [docs.readthedocs.io](https://docs.readthedocs.io/)
- **Sphinx Documentation**: [www.sphinx-doc.org](https://www.sphinx-doc.org/)
- **GitHub Issues**: Report issues in your repository
- **Community**: Stack Overflow, Reddit, etc.

---

**Your documentation will now automatically update with every commit!** 🎉
