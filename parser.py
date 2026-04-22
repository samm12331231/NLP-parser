import nltk
import sys
from nltk.tokenize import wordpunct_tokenize

# TERMINAL RULES: define words
TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S
NP -> N | Det N | Det AdjP N | NP PP
VP -> V | V NP | VP PP | Adv VP | VP Adv
AdjP -> Adj | Adj AdjP
PP -> P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()
    else:
        s = input("Sentence: ")

    trees = parse_sentence(s)
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Lowercase all letters, keep only words with alphabetic characters.
    """
    sentence = sentence.lower()
    words = wordpunct_tokenize(sentence)
    result = []

    for word in words:
        cleaned_word = ''.join(char for char in word if char.isalpha())

        if cleaned_word:
            result.append(cleaned_word)

    return result


def parse_sentence(sentence):
    """
    Parse `sentence` and return a list of parse trees.
    Returns an empty list when parsing fails.
    """
    tokens = preprocess(sentence)
    if not tokens:
        return []

    try:
        return list(parser.parse(tokens))
    except ValueError:
        return []


def np_chunk(tree):
    """
    Return a list of all noun phrase (NP) chunks in the sentence tree.
    NP chunk = subtree labeled "NP" that does not contain another NP.
    """
    def _has_nested_np(np_subtree):
        for nested in np_subtree.subtrees():
            if nested is not np_subtree and nested.label() == "NP":
                return True
        return False

    chunks = []
    for subtree in tree.subtrees():
        if subtree.label() == "NP" and not _has_nested_np(subtree):
            chunks.append(subtree)
    return chunks


if __name__ == "__main__":
    main()
