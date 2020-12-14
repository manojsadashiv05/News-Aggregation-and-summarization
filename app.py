import streamlit as st
import requests
import pandas as pd
import numpy as np
import nltk
from newspaper import Article
from py_heideltime import py_heideltime
import spacy
from spacy import displacy
nlp = spacy.load('en')


HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""

def analyze_text(text):
	return nlp(text)
def news_extraction(query):
	params = {
	    "access_key":"4cb1272f9aabf2f8a8b97b7a233c3d9b",
	    "query": query,
	    "google_domain": "google.com",
	    "sort":"date",
	    "type":"news"
	}

	api_result = requests.get('http://api.serpstack.com/search', params)
	api_response = api_result.json()
	try:
		news = api_response['news_results']
	except:
		pass
	news=pd.DataFrame.from_dict(news)
	links = news['url']
	articles_info = []
	for i in links:
	    #Intialize dictionary
	    article_dict = {}
	    #Insert link "i" into the dictionary
	    article_dict["link"] = i
	    #Pass link into Article() function
	    art = Article(i)
	    #Download contents of art object
	    art.download()
	    
	    #Try/except is included because not all articles can be parsed
	    try:
	        #If article can be successfully parsed then insert its text, title, publish_date, keywords
	        #and summary into corresponding keys
	        art.download()
	        art.parse()
	        art.nlp()
	        article_dict["text"] = art.text
	        article_dict["title"] = art.title
	        article_dict["date"] = art.publish_date
	        article_dict["keywords"] = art.keywords
	        article_dict["summary"] = art.summary
	    except:
	        #If article cannot be parse then insert null values for the following keys:
	        #"text", "title", "date", "keywords", and "summary"
	        article_dict["text"] = np.nan
	        article_dict["title"] = np.nan
	        article_dict["date"] = np.nan
	        article_dict["keywords"] = np.nan
	        article_dict["summary"] = np.nan
	        
	    #Insert dictionary of article info into the articles_info list
	    articles_info.append(article_dict)
	#Pass the list of dictionaries into a pandas data frame
	corpus = pd.DataFrame(articles_info)
	news['uploaded_utc']=pd.to_datetime(news['uploaded_utc'], utc=True)
	news['uploaded_utc']=news['uploaded_utc'].dt.date
	corpus['date']=news['uploaded_utc']
	return corpus



st.title('News Summarization and Timeline Extraction')
st.subheader('Enter the news you wanna know about')
user_query=st.text_input('')
activities=['Article Links','News Summary','Named Entity Recognition','Timeline']
choice = st.selectbox('Select Activity',activities)

if choice == 'Article Links':
	news_summary=news_extraction(user_query)
	st.subheader('Gathering Article Links')
	for i in range(0,news_summary.shape[0]):
			st.write(i+1,news_summary.iloc[i,3],'->article published date')
			st.write(news_summary.iloc[i,0])

if choice == 'News Summary':
	news_summary=news_extraction(user_query)
	news_summary.to_csv('news_summary.csv',encoding='utf-8', index=False)
	st.subheader('Fetching News summary of the articles')
	for i in range(0,news_summary.shape[0]):
		st.write(i+1,news_summary.iloc[i,3],'->article published date')
		st.write(news_summary.iloc[i,0])
		st.write(news_summary.iloc[i,5])
if choice == 'Named Entity Recognition':
	st.subheader("Named Entity Recogition of news articles")
	news_sum=pd.read_csv('D:\\Manoj\\Documents\\sublime\\project\\news_summary.csv')	
	for i in range(0,news_sum.shape[0]):
		
		st.write(i+1,news_sum.iloc[i,3],'->article published date')
		docx = analyze_text(news_sum.iloc[i,5])
		html = displacy.render(docx,style="ent")
		html = html.replace("\n\n","\n")
		st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)

if choice == 'Timeline':
	st.subheader('Timeline of the events')
	timeline=pd.read_csv('D:\\Manoj\\Documents\\sublime\\project\\timeline.csv')
	for i in range(0,timeline.shape[0]):
		st.write(timeline.iloc[i,0])
		docx = analyze_text(timeline.iloc[i,1])
		html = displacy.render(docx,style="ent")
		html = html.replace("\n\n","\n")
		st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)
	

	#OBJECTIVES
	#run heidel_time
	#run timeline.py
	#all 3 files are in the same directory
	#then display the timeline.csv
	# so while showing it to teachers, if we run the heidel_time.py and the timeline.py manually from sublime, we can 
	#easily display the timeline of the news 