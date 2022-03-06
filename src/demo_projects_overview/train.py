"""The `train.py` module provides functionality to re-train embedding model with new dataset."""
from pathlib import Path

import fasttext
import preprocessing


def train(
    new_data_path: str, include_confidential: bool = False, boosting_percentage: float = 0.05
) -> None:
    """Append the new dataset to the existing corpus.Train new fasttext embedding model with new extended corpus.

    :param new_data_path: path to a csv file containing projects implemented by Radix
    :param include_confidential: indicates if confidential projects should be included
    :param boosting_percentage: the percentage by which the new data should be duplicated in the corpus
        (the percentage corresponds to percentage from the initial stack overflow corpus). The default is set to 5%.
    """
    sentences = preprocessing.extract_sentences(
        new_data_path=new_data_path,
        selected_cols=None,
        include_confidential=include_confidential,
    )
    preprocessing.append_to_corpus(sentences=sentences, boosting_percentage=boosting_percentage)
    preprocessing.make_metadata_file(filepath=new_data_path, append=False)
    preprocessing.save_project_names_to_file(
        filepath=new_data_path, include_confidential=include_confidential
    )
    preprocessing.save_as_labelled_text_to_json(
        filepath=new_data_path, include_confidential=include_confidential
    )

    model = fasttext.train_unsupervised(
        str(Path(__file__).parent / "corpus/corpus-merged-cleaned.txt"), epoch=50, dim=50
    )
    model.save_model(str(Path(__file__).parent / "embeddings/fasttext-embeddings.bin"))


train(str(Path(__file__).parent / "Project-description.csv"), include_confidential=False)
