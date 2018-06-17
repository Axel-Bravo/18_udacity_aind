"""Splitting text data into tokens."""

import re


def sent_tokenize(text):
    """Split text into sentences."""
    sentences =  re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)(\s|[A-Z].*)',text)
    sentences = [value for value in sentences if value != ' ']
    sentences = [re.sub(r"[^a-zA-Z0-9]", " ", value) for value in sentences]
    sentences = [value.strip() for value in sentences]
    return sentences


def word_tokenize(sent):
    """Split a sentence into words."""
    sent_splitted = sent.split()
    return sent_splitted

def test_run():
    """Called on Test Run."""

    text = "The first time you see The Second Renaissance it may look boring. Look at it at least twice and definitely watch part 2. It will change your view of the matrix. Are the human people the ones who started the war? Is AI a bad thing?"
    print("--- Sample text ---", text, sep="\n")

    sentences = sent_tokenize(text)
    print("\n--- Sentences ---")
    print(sentences)

    print("\n--- Words ---")
    for sent in sentences:
        print(sent)
        print(word_tokenize(sent))
        print()  # blank line for readability