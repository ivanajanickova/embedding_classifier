"""The module provides functionality for text precessing of corpus of text scraped from the StackOverflow."""
import re
from typing import List

from nltk import sent_tokenize


def save(corpus: List[str], filename: str) -> None:
    """Save the corpus ito a file.

    :param corpus: a list of processed strings scraped from the StackOverflow.
    :param filename: name by which the file will be saved
    """
    with open(filename, "w") as file:
        for sent in corpus:
            file.write(str(sent) + "\n")


def process_paragraphs(paragraphs) -> List[str]:  # type: ignore
    """Identify paragraphs based on the html tag and process the text inside.

    :param paragraphs: a result of `soup.findall('p')`
    :return: a list of containing processed text from paragraph.
    """
    processed_text = []
    text = re.findall("<p>(.*)</p>", str(paragraphs))

    for t in text:
        t = t.replace("<p>", "")
        t = t.replace("</p>", "")

        processed_text.append(t)

    return processed_text


def process_sentence(sentence: str) -> str:
    """Clean data and text processing of a sentence.

    :param sentence: a sentence
    :return: processed sentence
    """
    # remove html residues
    html_pattern = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
    sentence = re.sub(html_pattern, "", sentence)

    # remove hyperlinks
    sentence = re.sub(r"(https?://)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)", "", sentence)

    # lowercase
    sentence = sentence.lower()

    # remove \n char
    sentence = re.sub(r"\n", " ", sentence)  # flake8: noqa

    # remove stack overflow mark
    stack_pattern1 = re.compile(
        "thanks for contributing an answer to stack overflow .*? required, but never shown"
    )
    stack_pattern2 = re.compile("thanks for contributing an answer to stack overflow")
    stack_pattern3 = re.compile("stack overflow")

    sentence = re.sub(stack_pattern1, "", sentence)
    sentence = re.sub(stack_pattern2, "", sentence)
    sentence = re.sub(stack_pattern3, "", sentence)

    return sentence


def process_corpus(corpus: List[str]) -> List[str]:
    """Process text from the corpus.

    :param corpus: processed paragraphs from the StackOverflow web
    """
    corpus_processed = []

    for entry in corpus:

        # identify title or code text
        if type(entry) == str:
            corpus_processed.append(process_sentence(entry))

        # paragraph list
        else:
            for doc in entry:
                # tokenize into sentences
                sent_tokens = sent_tokenize(doc)

                for sent in sent_tokens:
                    # process the sentences
                    corpus_processed.append(process_sentence(sent))

    return corpus_processed
