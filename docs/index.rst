GPT-Tokenizer Documentation
============================

A comprehensive implementation of tokenization algorithms used in Large Language Models, with focus on Byte Pair Encoding (BPE), UTF-8 handling, and pattern matching.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   README
   API
   ARCHITECTURE

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   modules

.. toctree::
   :maxdepth: 2
   :caption: Examples:

   examples

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Quick Start
-----------

.. code-block:: python

    from minbpe import GPT4BPETokenizer
    
    # Create and train tokenizer
    tokenizer = GPT4BPETokenizer(vocab_size=1000)
    tokenizer.train(["Hello world!", "Machine learning is fascinating."])
    
    # Encode and decode
    tokens = tokenizer.encode("Hello AI!")
    text = tokenizer.decode(tokens)
    print(f"Tokens: {tokens}")
    print(f"Decoded: {text}")

Installation
------------

.. code-block:: bash

    pip install -e .

Features
--------

* **BPE Implementation**: Complete Byte Pair Encoding algorithm from scratch
* **UTF-8 Support**: Proper handling of Unicode and multi-byte characters  
* **Regex Tokenization**: GPT-2 style pattern matching for text segmentation
* **Interactive Learning**: Jupyter notebook with step-by-step examples
* **Production Ready**: Integration with tiktoken for real-world applications

Performance
-----------

* **Encoding**: O(t × log v) where t is text length, v is vocabulary size
* **Decoding**: O(t) where t is number of tokens
* **Memory**: O(v) vocabulary storage, O(m) merge rules
