import re
from collections import Counter

ABBREVIATIONS = ["etc.", "i.e.", "e.g.", "c.", "Mr.", "Mrs.", "Dr.", "Lt.", "Rep.", "p.m.", "a.m."]


def count_sentences(text):
    unwanted_dots_count = 0
    sentence_in_quotes = 0
    for abbreviation in ABBREVIATIONS:
        unwanted_dots_count += text.count(abbreviation) * abbreviation.count(".")
    quotes = re.findall(r"\"([^\"]+)\"",text)
    for quote in quotes:
        sentence_in_quotes += count_sentences(quote)
    return len(re.findall(r"[A-z\s0-9]+(?:\.+|\?|!)", text)) - unwanted_dots_count - sentence_in_quotes


def count_non_declarative(text):
    return len(re.findall(r"[A-z\s]+(\?|!)", text))


def get_all_words(text):
    numbers = re.findall(r"[0-9]+", text)
    word_and_numbers = re.findall(r"[A-z0-9]+", text)
    return [word for word in word_and_numbers if word not in numbers]


def count_sentence_length(text):
    text_len = count_sentences(text)
    char_num = sum(len(word) for word in get_all_words(text))
    return char_num / text_len if text_len != 0 else 0


def count_word_length(text):
    words = get_all_words(text)
    return sum(len(word) for word in words) / len(words) if len(words) != 0 else 0
    return 0


def get_top_k_ngrams(text, k=10, n=4):
    try:
        words = get_all_words(text)
        all_ngrams = [" ".join(words[i:i + int(n)]) for i in range(len(words) - int(n) + 1)]
        return Counter(all_ngrams).most_common(int(k))
    except TypeError:
        print("invalid input")
        return None

