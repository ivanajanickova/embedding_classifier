"""The `preprocessing.py` module performs text preprocessing for the purpose of corpus extension."""

import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import regex as re
from nltk import sent_tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


def extract_sentences(
    new_data_path: str,
    selected_cols: Optional[List[int]] = None,
    include_confidential: bool = False,
) -> List[List[str]]:
    """
    Process text from specified columns of a data frame.

    :param new_data_path: a path to csv file containing projects implemented by Radix
    :param selected_cols: a list of selected col numbers
    :param include_confidential: stating if confidential projects should be included
    :return: a list of all sentences
    """
    data_frame = pd.read_csv(new_data_path)
    if selected_cols is None:  # Default columns for corpus
        selected_cols = [2, 3, 4]

    if include_confidential is False:  # Discard the confidential data
        selected_rows = [i for i in range(0, len(data_frame)) if data_frame.iloc[i, -1] != "Yes"]
    else:
        selected_rows = list(range(0, len(data_frame)))

    sentences = []
    for i in selected_rows:
        for j in selected_cols:
            for s in sent_tokenize(data_frame.iloc[i, j]):
                sentences.append(process_sentence(s))

    return sentences


def append_to_corpus(sentences: List[List[str]], boosting_percentage: float = 0.05) -> None:
    """Append the sentences to corpus.

    :param sentences: a list of sentences returned from `extract_sentences` :param corpus_path: path to the corpus
    :param boosting_percentage: specifies the number of repetitions by which the `sentences` are added to the corpus
        refers to the proportion of lines from the corpus
    """
    old_corpus_path = str(Path(__file__).parent / "corpus/corpus-without-radix-data.txt")

    corpus_path = str(Path(__file__).parent / "corpus/corpus-merged.txt")
    shutil.copyfile(old_corpus_path, corpus_path)
    num_lines = sum(1 for line in open(corpus_path))
    with open(corpus_path, "a") as file:
        iteration = 0
        while iteration < round(num_lines * boosting_percentage):
            for sentence in sentences:
                file.write(str(sentence) + "\n")
                iteration += 1

    make_clean_corpus_file(corpus_path)


def make_clean_corpus_file(corpus_path: str) -> None:
    """Clean the original corpus file and save changes into a new file.

    :param corpus_path: path to the original corpus file
    """
    with open(str(Path(__file__).parent / "corpus/corpus-merged-cleaned.txt"), "w") as cleaned_cor:
        ps = PorterStemmer()
        with open(corpus_path, "r") as cor:
            for sent in cor:
                words = word_tokenize(sent)
                for i in range(0, len(words)):
                    words[i] = "".join(e for e in words[i] if e.isalnum())  # delete special chars
                    words[i] = ps.stem(words[i])

                cleaned_cor.write(" ".join(words) + "\n")


def process_sentence(sentence: str) -> Any:
    """Process sentences."""
    # remove hyperlinks
    sent = re.sub(r"(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)", "", sentence)
    # lowercase
    sent = sent.lower()
    # remove \n char
    sent = re.sub(r"\n", " ", sent)

    return sent


def make_metadata_file(
    filepath: str, selected_cols: Optional[List[int]] = None, append: bool = True
) -> None:
    """Save information about projects from project descriptions."""
    if selected_cols is None:  # Default columns for metadata
        selected_cols = [4, 5, 6, 7, 8]
    data_frame = pd.read_csv(filepath)
    metadata = {}

    if append is False:
        # if new metadata file is created
        columns = data_frame.columns
        metadata["header"] = [columns[i] for i in selected_cols]

    for row in range(0, len(data_frame)):
        project_title = data_frame.iloc[row, 2]
        metadata[project_title] = [
            re.sub("\n", " ", data_frame.iloc[row, i]) for i in selected_cols
        ]

    save_metadata(metadata=metadata, append=append)


def save_metadata(metadata: Dict[str, List[str]], append: bool = True) -> None:
    """Save metadata dictionary to a json file."""
    if append is True:
        with open(str(Path(__file__).parent / "corpus/metadata.json"), "a") as json_file:
            json.dump(metadata, json_file)
    else:
        with open(str(Path(__file__).parent / "corpus/metadata.json"), "w") as json_file:
            json.dump(metadata, json_file)


def load_metadata(path: str) -> Any:
    """Load metadata from json file."""
    with open(path) as json_file:
        metadata = json.load(json_file)
    return metadata


def metadata_to_df(metadata: Dict[str, List[str]], project_names: List[str]) -> pd.DataFrame:
    """Create a data frame from metadata dict."""
    data_dict = {}  # type: ignore
    for name in project_names:
        for i in range(0, len(metadata.get("header"))):  # type: ignore
            if i not in data_dict.keys():
                data_dict[i] = [metadata[name][i]]
            else:
                data_dict[i] = data_dict.get(i) + [metadata[name][i]]  # type: ignore

    df = pd.DataFrame.from_dict(data_dict)
    df = df.set_axis(metadata.get("header"), axis=1)
    df["Project name"] = project_names
    return df


def save_project_names_to_file(filepath: str, include_confidential: bool) -> None:
    """Save project names to a file.

    :param filepath: path to the new Radix project dataset (saved as csv file)
    :param include_confidential: stating if confidential projects should be included
    """
    df = pd.read_csv(filepath)
    if include_confidential is True:
        project_names = [df.iloc[i, 2] for i in range(0, len(df))]
    else:
        project_names = [df.iloc[i, 2] for i in range(0, len(df)) if df.iloc[i, -1] == "No"]

    with open(str(Path(__file__).parent / "corpus/project_names.txt"), "w") as file:
        for name in project_names:
            file.write(name + "\n")


def save_as_labelled_text_to_json(filepath: str, include_confidential: bool) -> None:
    """Extract and save data form the  Radix project dataset.

    :param filepath: path to the new Radix project dataset (saved as csv file)
    :param include_confidential: stating if confidential projects should be included
    """
    df = pd.read_csv(filepath)
    if include_confidential is True:
        labelled_text = {}
        for i in range(0, len(df)):
            sentences = sent_tokenize(df.iloc[i, 3])
            labelled_text[df.iloc[i, 2]] = [process_sentence(sentence) for sentence in sentences]
    else:
        labelled_text = {}
        for i in range(0, len(df)):
            if df.iloc[i, -1] == "Yes":  # check if the record in the row is confidential
                break
            sentences = sent_tokenize(df.iloc[i, 3])
            labelled_text[df.iloc[i, 2]] = [process_sentence(sentence) for sentence in sentences]

    with open(str(Path(__file__).parent / "corpus/labelled-text.json"), "w") as json_file:
        json.dump(labelled_text, json_file)
