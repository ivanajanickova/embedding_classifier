# A `fasttext` emebedding based classfier

This work correponds to the intership work. The result is a streamlit app that reccomends a most related projects implemetented by Radix.Ai, given the description. 

## Web-scraping
A specific corpus is created by web-scrapping StackOverflow website based on keywords related to the project work in Radix.Ai.

## Embedding and classification
Infromation related to projects is represent in an ebedding space. Based on cosine similarity of a query vector a list of the most related projects is returned. 

## App 
The app is implemented with `Streamlit` and was deployed on a aws EC2 instance. 





