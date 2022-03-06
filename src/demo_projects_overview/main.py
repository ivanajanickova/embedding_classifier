"""Creates streamlit app."""

import sys

import streamlit as st
from model import Model
from streamlit import cli as stcli


def main() -> None:
    """Run the streamlit app."""
    st.title("Demo of projects implemented by Radix")
    st.write(
        """
    *Search for the Radix's projects most related to what you are looking for*
    """
    )
    model = Model()

    with st.form(key="my_form"):
        user_input = st.text_input("Key words", "sentiment analysis, aws")
        submit_button = st.form_submit_button(label="Submit")

        if submit_button:
            with st.spinner("Finding the best matches..."):
                best_project_scores = model.get_best_project_scores(user_input, 3)
                project_names = [project_score[0] for project_score in best_project_scores]

                st.header("Related Projects")
                confidence_df = model.get_best_projects_df(best_project_scores, include_scores=True)
                st.dataframe(confidence_df)

                st.header("More Info")
                metadata_df = model.get_metadata_df(project_names)
                st.dataframe(metadata_df)


if __name__ == "__main__":
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
