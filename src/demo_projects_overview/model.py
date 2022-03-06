"""Handles predictions based on serialized model."""
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import fasttext
import numpy as np
import pandas as pd
import preprocessing


class Model:
    """Handles predictions based on serialized model."""

    def __init__(self) -> None:
        self.embeddings = fasttext.load_model(
            str(Path(__file__).parent / "embeddings/fasttext-embeddings.bin")
        )
        self.project_names = self.load_project_names()

    def load_project_names(self) -> List[str]:
        """Load project names to list from `project_names.txt`.

        :return: the loaded list of project names
        """
        project_names = []
        with open(Path(__file__).parent / "corpus/project_names.txt", "r") as file:
            for name in file:
                project_names.append(name.strip())
        return project_names

    def get_best_project_scores(self, user_input: str, num_outputs: int) -> List[Tuple[str, float]]:
        """
        Calculate the best scores.

        :param user_input: the string of user's query
        :param num_outputs: the number of desired outputs (predictions)
        :return: 2D nested list where each nested list consists of a pair `[project_name, score]`
        """
        scores: Dict[str, float] = {}
        # get vector of query sent
        query_vec = self.embeddings.get_sentence_vector(preprocessing.process_sentence(user_input))
        # load dict of text labelled with the project title
        with open(Path(__file__).parent / "corpus/labelled-text.json", "r") as file:
            labelled_text = json.load(file)

        for key in labelled_text.keys():
            scores[key] = 0
            scores_list = []
            sentences = labelled_text.get(key)

            for sentence in sentences:
                sentence_vec = self.embeddings.get_sentence_vector(sentence)
                scores_list.append(self.calculate_cosine_similarity(sentence_vec, query_vec))

            scores[key] = sum(scores_list) / len(scores_list)

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores[0:num_outputs]

    def calculate_cosine_similarity(self, query_vec: str, sent_vec: str) -> Any:
        """Calculate the cosine similarity of two sentence vectors (indicates the closeness of two vectors).

        :param query_vec: the vector representing user's query
        :param sent_vec: the vector representing sentence
        """
        cos_sim = np.dot(query_vec, sent_vec) / (
            np.linalg.norm(query_vec) * np.linalg.norm(sent_vec)
        )
        return cos_sim

    def get_metadata_df(self, project_names: List[str]) -> pd.DataFrame:
        """Get dataframe of metadata.

        :param project_names: names of projects to which metadata will be returned
        :return: a pd.DataFrame of metadata for each project in `project_names`.
        """
        metadata = preprocessing.load_metadata(str(Path(__file__).parent / "corpus/metadata.json"))
        df = preprocessing.metadata_to_df(metadata, project_names)
        return df

    def get_best_projects_df(
        self, best_project_scores: List[Tuple[str, float]], include_scores: bool = False
    ) -> pd.DataFrame:
        """Get dataframe of project and cosine similarity score.

        :param best_project_score: 2D nested list containing a pair `[project_name, score]` for every project considered
        :param include_scores: if the cosine similarity score should be included
        :return: a pd.DataFrame of project and cosine similarity score of its predictions.
        """
        if include_scores is True:
            df = pd.DataFrame(best_project_scores, columns=("Project", "Similarity score"))
            return df
        else:
            best_projects = [best_project_scores[i][0] for i in range(0, len(best_project_scores))]
            df = pd.DataFrame(best_projects)
            return df
