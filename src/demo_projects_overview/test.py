"""Run the test for the embedding model."""

from model import Model

expected_1 = {
    "Sentiment Analysis of Citizen Wellbeing": 0,
    "Vacancy parsing": 1,
    "AI-supported email processing": 1,
    "Carbon monitoring of agricultural fields": -1,
    "Field boundary detection": -1,
    "Financial news article selection and summarisation": 0,
    "Orient": 1,
    "Macadam": -1,
    "Tender Pricing": 0,
    "CFU Counting R&D": -1,
    "CFU counting Production": -1,
    "Robot Reporter": 1,
    "Formulation Assistant": 0,
    "Forecasting queuing time at metal detector in Brussels Airport": -1,
    "VDAB NLP sentences similarity": 1,
    "Gender Bias": 0,
    "Question Answering / Suggestion Engine for Trade Cases": 1,
}

expected_2 = {
    "Sentiment Analysis of Citizen Wellbeing": 1,
    "Vacancy parsing": 0,
    "AI-supported email processing": 0,
    "Carbon monitoring of agricultural fields": -1,
    "Field boundary detection": -1,
    "Financial news article selection and summarisation": 1,
    "Orient": 0,
    "Macadam": -1,
    "Tender Pricing": 0,
    "CFU Counting R&D": -1,
    "CFU counting Production": -1,
    "Robot Reporter": 0,
    "Formulation Assistant": -1,
    "Forecasting queuing time at metal detector in Brussels Airport": -1,
    "VDAB NLP sentences similarity": 0,
    "Gender Bias": 0,
    "Question Answering / Suggestion Engine for Trade Cases": 0,
}

expected_3 = {
    "Sentiment Analysis of Citizen Wellbeing": -1,
    "Vacancy parsing": -1,
    "AI-supported email processing": -1,
    "Carbon monitoring of agricultural fields": 0,
    "Field boundary detection": 0,
    "Financial news article selection and summarisation": -1,
    "Orient": -1,
    "Macadam": 1,
    "Tender Pricing": 0,
    "CFU Counting R&D": 1,
    "CFU counting Production": 1,
    "Robot Reporter": 1,
    "Formulation Assistant": 0,
    "Forecasting queuing time at metal detector in Brussels Airport": -1,
    "VDAB NLP sentences similarity": -1,
    "Gender Bias": -1,
    "Question Answering / Suggestion Engine for Trade Cases": -1,
}

expected_4 = {
    "Sentiment Analysis of Citizen Wellbeing": 1,
    "Vacancy parsing": 1,
    "AI-supported email processing": -1,
    "Carbon monitoring of agricultural fields": 1,
    "Field boundary detection": -1,
    "Financial news article selection and summarisation": -1,
    "Orient": 1,
    "Macadam": -1,
    "Tender Pricing": 1,
    "CFU Counting R&D": -1,
    "CFU counting Production": -1,
    "Robot Reporter": -1,
    "Formulation Assistant": -1,
    "Forecasting queuing time at metal detector in Brussels Airport": -1,
    "VDAB NLP sentences similarity": -1,
    "Gender Bias": -1,
    "Question Answering / Suggestion Engine for Trade Cases": -1,
}

expected_5 = {
    "Sentiment Analysis of Citizen Wellbeing": 0,
    "Vacancy parsing": 1,
    "AI-supported email processing": 0,
    "Carbon monitoring of agricultural fields": 0,
    "Field boundary detection": 0,
    "Financial news article selection and summarisation": 0,
    "Orient": 0,
    "Macadam": 0,
    "Tender Pricing": 0,
    "CFU Counting R&D": 0,
    "CFU counting Production": 0,
    "Robot Reporter": 0,
    "Formulation Assistant": 0,
    "Forecasting queuing time at metal detector in Brussels Airport": 0,
    "VDAB NLP sentences similarity": 0,
    "Gender Bias": 0,
    "Question Answering / Suggestion Engine for Trade Cases": 0,
}

expected_6 = {
    "Sentiment Analysis of Citizen Wellbeing": 1,
    "Vacancy parsing": 0,
    "AI-supported email processing": 0,
    "Carbon monitoring of agricultural fields": 0,
    "Field boundary detection": 0,
    "Financial news article selection and summarisation": 0,
    "Orient": 0,
    "Macadam": 0,
    "Tender Pricing": 0,
    "CFU Counting R&D": 0,
    "CFU counting Production": 0,
    "Robot Reporter": 0,
    "Formulation Assistant": 0,
    "Forecasting queuing time at metal detector in Brussels Airport": 0,
    "VDAB NLP sentences similarity": 0,
    "Gender Bias": 0,
    "Question Answering / Suggestion Engine for Trade Cases": 0,
}

expected_7 = {
    "Sentiment Analysis of Citizen Wellbeing": 0,
    "Vacancy parsing": 0,
    "AI-supported email processing": 0,
    "Carbon monitoring of agricultural fields": 1,
    "Field boundary detection": 0,
    "Financial news article selection and summarisation": 0,
    "Orient": 0,
    "Macadam": 0,
    "Tender Pricing": 0,
    "CFU Counting R&D": 0,
    "CFU counting Production": 0,
    "Robot Reporter": 0,
    "Formulation Assistant": 0,
    "Forecasting queuing time at metal detector in Brussels Airport": 0,
    "VDAB NLP sentences similarity": 0,
    "Gender Bias": 0,
    "Question Answering / Suggestion Engine for Trade Cases": 0,
}

correct_results = [
    expected_1,
    expected_2,
    expected_3,
    expected_4,
    expected_5,
    expected_6,
    expected_7,
]

model = Model()

test_queries = [
    # queries for matching multiple projects
    "text mining and nlp with fasttext",
    "nlp with transformers, huggingface transformers, robbert",
    "pytorch and computer vision, image processing",
    "aws app deployment, ec2",
    # queries form matching one project
    "vacancy parsing over languages",
    "sentiment analysis of human well-being",
    "climate change, emissions, remote sensing",
]

total_correct = 0
total_incorrect = 0
total_ambiguous = 0

for i in range(0, len(test_queries)):
    best_project_scores = model.get_best_project_scores(test_queries[i], 3)
    project_names = [project_score[0] for project_score in best_project_scores]

    correct = 0
    incorrect = 0
    ambiguous = 0
    for project in project_names:
        if i <= 3:
            # queries for matching multiple projects
            score = correct_results[i].get(project)
            if score == 1:
                correct += 1
            elif score == 0:
                ambiguous += 1
            elif score == -1:
                incorrect += 1

        else:
            # queries for matching one project
            # (keeps track only of the desired project appeared in the top 3 guesses)
            score = correct_results[i].get(project)
            if score == 1:
                correct += 1

    total_correct += correct
    total_incorrect += incorrect
    total_ambiguous += ambiguous

    print(
        f"For query number: {i} the performance in predictions was: "
        + "\n"
        + f"correct = {correct}/3; incorrect = {incorrect}/3; ambiguous = {ambiguous}/3"
    )
    print(f"Query: {test_queries[i]}")
    print(f"Projects: {project_names}")

print("---------------------------------------------------------------------------------")
print(
    "Overall performance on predictions: "
    + "\n"
    + f"total correct = {total_correct}; total incorrect = {total_incorrect}; total ambiguous = {total_ambiguous}"
)
