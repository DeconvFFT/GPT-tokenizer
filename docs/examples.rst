Examples
========

This page contains practical examples of how to use the GPT-Tokenizer library.

Basic Usage
-----------

Training a Tokenizer
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from minbpe import Tokenizer
    
    # Initialize tokenizer
    tokenizer = Tokenizer()
    
    # Training text
    training_text = "Hello world! This is a test. The quick brown fox jumps over the lazy dog."
    
    # Train the tokenizer
    tokenizer.train(training_text, vocab_size=1000, verbose=True)
    
    print(f"Vocabulary size: {len(tokenizer.vocab)}")
    print(f"Number of merges: {len(tokenizer.merges)}")

Using Utility Functions
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from minbpe.base import get_pair_frequencies, merge_pair, render_token
    
    # Get pair frequencies from indices
    indices = [72, 101, 108, 108, 111]  # "Hello" in ASCII
    pair_freqs = get_pair_frequencies(indices)
    print(f"Pair frequencies: {pair_freqs}")
    
    # Merge a pair
    merged = merge_pair(indices, (101, 108), 256)
    print(f"After merging (101,108): {merged}")
    
    # Render a token
    token_bytes = b"Hello"
    rendered = render_token(token_bytes)
    print(f"Rendered token: {rendered}")

Working with Control Characters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from minbpe.base import replace_control_characters
    
    # Text with control characters
    text_with_controls = "Hello\nWorld\tTabbed"
    
    # Replace control characters
    cleaned_text = replace_control_characters(text_with_controls)
    print(f"Original: {repr(text_with_controls)}")
    print(f"Cleaned: {cleaned_text}")

Advanced Usage
--------------

Custom Training Workflow
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from minbpe import Tokenizer
    
    # Create tokenizer with custom settings
    tokenizer = Tokenizer()
    
    # Multiple training texts
    training_texts = [
        "Machine learning is fascinating and powerful.",
        "Natural language processing enables AI to understand text.",
        "Deep learning models require large amounts of data."
    ]
    
    # Train on each text
    for i, text in enumerate(training_texts):
        print(f"Training on text {i+1}: {text[:50]}...")
        tokenizer.train(text, vocab_size=500, verbose=False)
        print(f"Current vocab size: {len(tokenizer.vocab)}")
        print()

Vocabulary Analysis
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Analyze the built vocabulary
    print("Vocabulary Analysis:")
    print("=" * 50)
    
    # Show some vocabulary items
    vocab_items = list(tokenizer.vocab.items())[:10]
    for token_id, token_string in vocab_items:
        print(f"ID {token_id}: {repr(token_string)}")
    
    # Show merge rules
    print(f"\nMerge rules: {len(tokenizer.merges)}")
    for (byte1, byte2), new_id in list(tokenizer.merges.items())[:5]:
        print(f"({byte1}, {byte2}) -> {new_id}")

Error Handling
--------------

Robust Tokenization
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def safe_train(tokenizer, text, vocab_size, max_retries=3):
        """Train tokenizer with error handling."""
        for attempt in range(max_retries):
            try:
                tokenizer.train(text, vocab_size, verbose=False)
                print(f"Training successful on attempt {attempt + 1}")
                return True
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    print("All training attempts failed")
                    return False
        return False
    
    # Test with various inputs
    test_inputs = [
        "Normal text",
        "Text with special chars: 🚀🌟",
        "Very long text " * 1000,  # Might cause memory issues
    ]
    
    for text in test_inputs:
        print(f"Training on: {text[:50]}...")
        success = safe_train(tokenizer, text, 100)
        print(f"Result: {'Success' if success else 'Failed'}")
        print()

Performance Optimization
-----------------------

Memory Management
~~~~~~~~~~~~~~~~~

.. code-block:: python

    import gc
    import sys
    
    def train_with_memory_monitoring(tokenizer, text, vocab_size):
        """Train while monitoring memory usage."""
        # Get initial memory
        initial_memory = sys.getsizeof(tokenizer.vocab) + sys.getsizeof(tokenizer.merges)
        
        # Train
        tokenizer.train(text, vocab_size, verbose=False)
        
        # Get final memory
        final_memory = sys.getsizeof(tokenizer.vocab) + sys.getsizeof(tokenizer.merges)
        
        # Calculate increase
        memory_increase = final_memory - initial_memory
        
        print(f"Initial memory: {initial_memory} bytes")
        print(f"Final memory: {final_memory} bytes")
        print(f"Memory increase: {memory_increase} bytes")
        
        # Force garbage collection
        gc.collect()
        
        return memory_increase
    
    # Test memory usage
    large_text = "Sample text " * 1000
    memory_used = train_with_memory_monitoring(tokenizer, large_text, 500)

Integration Examples
-------------------

With Jupyter Notebooks
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # In a Jupyter notebook cell
    %matplotlib inline
    import matplotlib.pyplot as plt
    
    # Analyze vocabulary growth during training
    vocab_sizes = []
    merge_counts = []
    
    # Train in steps and record metrics
    for step in range(5):
        tokenizer.train(f"Training step {step} with sample text", 100 + step * 50)
        vocab_sizes.append(len(tokenizer.vocab))
        merge_counts.append(len(tokenizer.merges))
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    ax1.plot(vocab_sizes)
    ax1.set_title("Vocabulary Growth")
    ax1.set_xlabel("Training Step")
    ax1.set_ylabel("Vocabulary Size")
    
    ax2.plot(merge_counts)
    ax2.set_title("Merge Rules Growth")
    ax2.set_xlabel("Training Step")
    ax2.set_ylabel("Merge Count")
    
    plt.tight_layout()
    plt.show()

Testing and Validation
----------------------

Unit Tests
~~~~~~~~~~

.. code-block:: python

    def test_tokenizer_basic():
        """Test basic tokenizer functionality."""
        tokenizer = Tokenizer()
        
        # Test initialization
        assert hasattr(tokenizer, 'vocab')
        assert hasattr(tokenizer, 'merges')
        assert hasattr(tokenizer, 'pattern')
        print("✓ Initialization test passed")
        
        # Test training
        tokenizer.train("Hello world", 100, verbose=False)
        assert len(tokenizer.vocab) > 0
        print("✓ Training test passed")
        
        print("All basic tests passed!")

Performance Benchmarks
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import time
    
    def benchmark_training(text, vocab_size, iterations=5):
        """Benchmark training performance."""
        times = []
        
        for i in range(iterations):
            tokenizer = Tokenizer()  # Fresh instance each time
            
            start_time = time.time()
            tokenizer.train(text, vocab_size, verbose=False)
            end_time = time.time()
            
            training_time = end_time - start_time
            times.append(training_time)
            
            print(f"Iteration {i+1}: {training_time:.4f}s")
        
        avg_time = sum(times) / len(times)
        print(f"Average training time: {avg_time:.4f}s")
        
        return avg_time
    
    # Test different text sizes
    test_sizes = [100, 1000, 10000]
    for size in test_sizes:
        text = "x" * size
        print(f"\nTesting text size: {size}")
        benchmark_training(text, 100)
