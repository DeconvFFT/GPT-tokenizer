GPT-Tokenizer Documentation
============================

A comprehensive implementation of tokenization algorithms used in Large Language Models, with focus on Byte Pair Encoding (BPE), UTF-8 handling, and pattern matching.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   README

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

    from minbpe import Tokenizer
    
    # Create tokenizer instance
    tokenizer = Tokenizer()
    
    # Train the tokenizer
    tokenizer.train("Hello world! This is a test.", vocab_size=1000)
    
    # Use the tokenizer
    print(f"Vocabulary size: {len(tokenizer.vocab)}")

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

* **Training**: O(n × m × v²) where n=corpus size, m=text length, v=vocabulary size
* **Encoding**: O(t × (r + log v)) where t=text length, r=merge rules, v=vocabulary size
* **Decoding**: O(t) where t=number of tokens
* **Memory**: O(v) vocabulary storage, O(m) merge rules
