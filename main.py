#!/usr/bin/env python3
"""
Main entry point for the GPT-Tokenizer package.

This module provides the command-line interface and main execution
logic for the tokenizer application. It serves as a simple demonstration
of the package functionality.

Examples
--------
>>> from main import main
>>> main()
Hello from gpt-tokenizer!

>>> # Import and use the tokenizer directly
>>> from minbpe import Tokenizer
>>> tokenizer = Tokenizer()
>>> print(f"Tokenizer initialized with {len(tokenizer.vocab)} vocabulary items")
Tokenizer initialized with 256 vocabulary items

See Also
--------
minbpe : Main tokenizer package
minbpe.base : Core tokenizer implementation
"""

def main():
    """Main entry point for the GPT-Tokenizer application.
    
    This function initializes the tokenizer system and provides
    a simple demonstration of the package functionality.
    
    Returns
    -------
    None
        
    Examples
    --------
    >>> main()
    Hello from gpt-tokenizer!
    
    Notes
    -----
    This is a simple demonstration function. For actual tokenizer
    usage, import and use the classes from the minbpe package.
    """
    print("Hello from gpt-tokenizer!")


if __name__ == "__main__":
    main()
