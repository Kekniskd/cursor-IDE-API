from src.utils.letter_counter import count_letters

def test_count_letters():
    # Test with normal string
    assert count_letters("Hello") == {"h": 1, "e": 1, "l": 2, "o": 1}

    # Test with empty string
    assert count_letters("") == {}

    # Test with numbers and special characters
    assert count_letters("Hello123!@#") == {"h": 1, "e": 1, "l": 2, "o": 1}

    # Test with mixed case
    assert count_letters("HeLLo") == {"h": 1, "e": 1, "l": 2, "o": 1}

    # Test with spaces
    assert count_letters("Hello World") == {
        "h": 1, "e": 1, "l": 3, "o": 2, "w": 1, "r": 1, "d": 1
    } 