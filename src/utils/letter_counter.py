def count_letters(text: str) -> dict:
    """
    Count the occurrence of each letter in the input text.
    
    Args:
        text (str): Input text to analyze
        
    Returns:
        dict: Dictionary with letters as keys and their counts as values
    """
    letter_count = {}
    for char in text.lower():
        if char.isalpha():
            letter_count[char] = letter_count.get(char, 0) + 1
    return letter_count 