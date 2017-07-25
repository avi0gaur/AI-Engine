import re, collections

__author__ = 'avi0gaur'

"""
This script is to provide functionality of spell check and replace the error word with
nearest matching word present in dic.
"""

def collect_w(text):
    return re.findall('[a-z]+', text.lower())

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(collect_w(open('D:\\AI-Engine\\AI-Engine\\res\\spell_corpus.txt','r').read()))
print(NWORDS)
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def e1(word):
    """
    Iterate through the word to boil down the correction process to "delete","transpose","replace" and "insert".
    :param word:
    :return:
    """
    s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in s if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
    replaces = [a + c + b[1:] for a, b in s for c in alphabet if b]
    inserts = [a + c + b for a, b in s for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def known_e2(word):
    """
    As we can find what to do with the word from e1, Now we need to do the same in the process
    :param word:
    :return:
    """
    return set(e2 for e1 in e1(word) for e2 in e1(e1) if e2 in NWORDS)

def known(words):
    """
    Replace the repetitive words from the NWORDS and build known word array
    :param words:
    :return:
    """
    return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(e1(word)) or known_e2(word) or [word]
    return max(candidates, key=NWORDS.get)

print(correct("sear"))