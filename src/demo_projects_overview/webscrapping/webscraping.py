"""Module provide functionality for scrapping the StackOverflow website with a purpose of creating a corpus."""
import re
import time
from typing import List

import pandas as pd
import requests
import text_processing
from bs4 import BeautifulSoup
from tqdm import tqdm


def run_scraping_pipeline(path_to_project_data: str) -> None:
    """Run the pipeline for scraping the StackOverflow website.

    :param path_to_project_data: path to the .csv file of project dataset.
    """
    tech_list = create_tech_list(path_to_project_data)
    links = extract_links_from_web(tech_list)
    extract_text_from_links(links)


def create_tech_list(path_to_project_data: str) -> List[str]:
    """Create a list of technologies used by Radix. The technologies are extracted from the project dataset.

    :param path_to_project_data: path to the .csv file of project dataset.
    :return: a list of technologies used
    """
    data = pd.read_csv(path_to_project_data)
    techs_2D = [re.split(r"\n|,", row) for row in data.iloc[:, 4]]
    # Make list of unique vals
    unique = set()

    technologies = []

    for arr in techs_2D:
        for s in arr:
            # Favour shorcut over full text
            if s.find("(") != -1:
                s = re.findall(r"\((.*)\)", s)
                s = "".join(s)

            # Delete empty strings
            if s == "" or s == " ":
                break

            # Connect multi-word terms
            if s[0] == " ":
                s = s.replace(" ", "")
            else:
                s = s.replace(" ", "-")
            s = s.lower()

            if s not in unique:
                technologies.append(s)
                unique.add(s)

    # manual append of generic terms
    technologies.append("machine-learning")
    technologies.append("nlp")
    technologies.append("cv")

    return technologies


def extract_links_from_web(technologies: List[str]) -> List[str]:
    """Get a list of links to questions from stack overflow.

    :param technologies: a list of technologies used
    :return: a list of links scraped from stack overflow web.
    """
    links = []
    link_start = "https://stackoverflow.com"
    link_base = "https://stackoverflow.com/questions/tagged/"
    link_page = "?tab=newest&page="

    for tech in tqdm(technologies):

        for i in range(1, 4):  # First 3 pages
            link = ""
            time.sleep(1)
            link = link_base + tech + link_page + str(i)
            res = requests.get(link)
            soup = BeautifulSoup(res.text, "html.parser")
            try:
                summaries = soup.select(".question-summary")

                for s in summaries:
                    question = s.select_one(".question-hyperlink")
                    link = question.get("href")
                    links.append(link_start + link)
            except Exception as e:
                print(f"the technology: {tech} has no questions at stack overflow")
                print(e)

    return links


def extract_text_from_links(links: List[str]) -> None:
    """Scrape the paragraph text from the links and process the text.

    :param links: a list of links to the stack overflow questions
    """
    # scraping the links in 10 batches and saving each batch
    for i in range(1, 11):  # 10 batches

        time.sleep(1)

        print(f"Batch number: {i}")
        corpus = []
        start_index = len(links) // 10 * (i - 1)
        end_index = len(links) // 10 * i

        batch_links = links[start_index:end_index]

        for link in tqdm(batch_links):

            time.sleep(1)
            try:
                res = requests.get(link)
                soup = BeautifulSoup(res.text, "html.parser")

                corpus.append(str(soup.find("title")))  # append titles
                corpus.append(text_processing.process_paragraphs(soup.findAll("p")))  # type: ignore

            except ConnectionError as e:
                print(e)

        # process the corpus
        corpus_processed = text_processing.process_corpus(corpus)

        # save the batch corpus to a file
        filename = "corpus" + str(i) + ".txt"
        text_processing.save(corpus_processed, filename)
