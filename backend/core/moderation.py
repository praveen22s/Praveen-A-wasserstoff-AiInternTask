banned_words = ["badword1", "badword2"]

def is_clean_input(text: str) -> bool:
    return not any(word in text.lower() for word in banned_words)
