Examples
========

This page contains practical examples of how to use the GPT-Tokenizer library.

Basic Usage
-----------

Training a BPE Tokenizer
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from minbpe import GPT4BPETokenizer
    
    # Initialize tokenizer with vocabulary size limit
    tokenizer = GPT4BPETokenizer(vocab_size=1000)
    
    # Training corpus
    training_texts = [
        "Hello world! This is a test.",
        "The quick brown fox jumps over the lazy dog.",
        "Machine learning is fascinating and powerful.",
        "Natural language processing enables AI to understand text."
    ]
    
    # Train the tokenizer
    tokenizer.train(training_texts)
    
    print(f"Vocabulary size: {len(tokenizer.vocab)}")
    print(f"Number of merge rules: {len(tokenizer.merges)}")

Encoding and Decoding
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Encode text to tokens
    text = "Hello AI world!"
    tokens = tokenizer.encode(text)
    print(f"Text: {text}")
    print(f"Tokens: {tokens}")
    
    # Decode tokens back to text
    decoded_text = tokenizer.decode(tokens)
    print(f"Decoded: {decoded_text}")
    print(f"Match: {text == decoded_text}")

Saving and Loading
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Save trained tokenizer
    tokenizer.save("my_tokenizer.json")
    
    # Load tokenizer in new instance
    new_tokenizer = GPT4BPETokenizer()
    new_tokenizer.load("my_tokenizer.json")
    
    # Verify consistency
    test_text = "Test consistency"
    assert tokenizer.encode(test_text) == new_tokenizer.encode(test_text)
    print("Tokenizer loaded successfully!")

Advanced Usage
--------------

Custom Vocabulary Size
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Different vocabulary sizes for different use cases
    small_tokenizer = GPT4BPETokenizer(vocab_size=100)    # For small datasets
    medium_tokenizer = GPT4BPETokenizer(vocab_size=1000)  # For medium datasets
    large_tokenizer = GPT4BPETokenizer(vocab_size=50000)  # For large datasets
    
    # Train on same corpus
    corpus = ["Sample text for training"]
    
    small_tokenizer.train(corpus)
    medium_tokenizer.train(corpus)
    large_tokenizer.train(corpus)
    
    print(f"Small vocab: {len(small_tokenizer.vocab)} tokens")
    print(f"Medium vocab: {len(medium_tokenizer.vocab)} tokens")
    print(f"Large vocab: {len(large_tokenizer.vocab)} tokens")

Batch Processing
~~~~~~~~~~~~~~~~

.. code-block:: python

    # Process multiple texts efficiently
    texts = [
        "First text to tokenize",
        "Second text with different content",
        "Third text for batch processing"
    ]
    
    # Encode all texts
    all_tokens = [tokenizer.encode(text) for text in texts]
    
    # Analyze token distribution
    for i, (text, tokens) in enumerate(zip(texts, all_tokens)):
        print(f"Text {i+1}: {len(tokens)} tokens")
        print(f"  Original: {text}")
        print(f"  Tokens: {tokens}")
        print()

Error Handling
--------------

Robust Tokenization
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def robust_encode(tokenizer, text, fallback_token="<|unk|>"):
        """Encode text with error handling."""
        try:
            return tokenizer.encode(text)
        except Exception as e:
            print(f"Error encoding '{text}': {e}")
            # Return fallback token
            return [tokenizer.vocab.get(fallback_token, 0)]
    
    # Test with various inputs
    test_inputs = [
        "Normal text",
        "Text with special chars: 🚀🌟",
        "Very long text " * 1000,  # Might cause memory issues
    ]
    
    for text in test_inputs:
        tokens = robust_encode(tokenizer, text)
        print(f"Input: {text[:50]}...")
        print(f"Tokens: {len(tokens)} tokens")
        print()

Performance Optimization
-----------------------

Streaming Tokenization
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def stream_tokenize(tokenizer, text, chunk_size=1000):
        """Process text in chunks to reduce memory usage."""
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size]
            yield tokenizer.encode(chunk)
    
    # Process large text efficiently
    large_text = "Sample text " * 10000
    
    print("Processing large text in chunks...")
    total_tokens = 0
    for chunk_tokens in stream_tokenize(tokenizer, large_text):
        total_tokens += len(chunk_tokens)
        print(f"Chunk processed: {len(chunk_tokens)} tokens")
    
    print(f"Total tokens: {total_tokens}")

Caching
~~~~~~~~

.. code-block:: python

    from functools import lru_cache
    
    # Cache frequent tokenizations
    @lru_cache(maxsize=1000)
    def cached_encode(tokenizer, text):
        return tokenizer.encode(text)
    
    # Test caching performance
    import time
    
    # First call (cache miss)
    start_time = time.time()
    tokens1 = cached_encode(tokenizer, "Hello world!")
    time1 = time.time() - start_time
    
    # Second call (cache hit)
    start_time = time.time()
    tokens2 = cached_encode(tokenizer, "Hello world!")
    time2 = time.time() - start_time
    
    print(f"First call: {time1:.6f}s")
    print(f"Second call: {time2:.6f}s")
    print(f"Speedup: {time1/time2:.1f}x")

Integration Examples
-------------------

With Jupyter Notebooks
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # In a Jupyter notebook cell
    %matplotlib inline
    import matplotlib.pyplot as plt
    
    # Analyze token distribution
    text = "This is a sample text for analysis"
    tokens = tokenizer.encode(text)
    
    # Create visualization
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(tokens)), tokens)
    plt.title("Token Distribution")
    plt.xlabel("Position")
    plt.ylabel("Token ID")
    plt.show()

With Pandas
~~~~~~~~~~~

.. code-block:: python

    import pandas as pd
    
    # Process DataFrame of texts
    df = pd.DataFrame({
        'text': [
            "First document",
            "Second document", 
            "Third document"
        ]
    })
    
    # Add tokenized column
    df['tokens'] = df['text'].apply(tokenizer.encode)
    df['token_count'] = df['tokens'].apply(len)
    
    print(df)

Testing and Validation
----------------------

Unit Tests
~~~~~~~~~~

.. code-block:: python

    def test_encode_decode_roundtrip():
        """Test that encoding then decoding returns original text."""
        test_texts = [
            "Hello world!",
            "Special chars: 🚀🌟",
            "Numbers: 12345",
            "Mixed: Hello123!@#"
        ]
        
        for text in test_texts:
            tokens = tokenizer.encode(text)
            decoded = tokenizer.decode(tokens)
            assert text == decoded, f"Failed for: {text}"
            print(f"✓ {text}")
        
        print("All roundtrip tests passed!")

Performance Benchmarks
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import time
    import statistics
    
    def benchmark_encoding(text, iterations=100):
        """Benchmark encoding performance."""
        times = []
        
        for _ in range(iterations):
            start_time = time.time()
            tokenizer.encode(text)
            end_time = time.time()
            times.append(end_time - start_time)
        
        avg_time = statistics.mean(times)
        std_time = statistics.stdev(times)
        
        print(f"Text length: {len(text)} characters")
        print(f"Average time: {avg_time:.6f}s ± {std_time:.6f}s")
        print(f"Tokens per second: {len(text) / avg_time:.0f}")
        
        return avg_time
    
    # Test different text sizes
    test_sizes = [100, 1000, 10000]
    for size in test_sizes:
        text = "x" * size
        benchmark_encoding(text)
        print()

Memory Usage Analysis
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import psutil
    import os
    
    def analyze_memory_usage():
        """Analyze memory usage during tokenization."""
        process = psutil.Process(os.getpid())
        
        # Baseline memory
        baseline_memory = process.memory_info().rss
        
        # Tokenize large text
        large_text = "x" * 100000
        tokens = tokenizer.encode(large_text)
        
        # Final memory
        final_memory = process.memory_info().rss
        
        # Calculate increase
        memory_increase = final_memory - baseline_memory
        
        print(f"Baseline memory: {baseline_memory / 1024 / 1024:.1f} MB")
        print(f"Final memory: {final_memory / 1024 / 1024:.1f} MB")
        print(f"Memory increase: {memory_increase / 1024 / 1024:.1f} MB")
        print(f"Tokens generated: {len(tokens)}")
        
        return memory_increase
    
    memory_used = analyze_memory_usage()
