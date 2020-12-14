import requests
import pandas as pd
import numpy as np
import nltk
#nltk.download('punkt')
from newspaper import Article


def query_input(query):
	params = {
	    "access_key":"c3e906214a8a2389a9b3b3a5edd95181",
	    "query": query,
	    "google_domain": "google.com",
	    "sort":"date",
	    "type":"news"
	}

	api_result = requests.get('http://api.serpstack.com/search', params)
	api_response = api_result.json()
	news=api_response['news_results']
	news=pd.DataFrame.from_dict(news)
	return news

def news_info(urls):
	links=urls
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
	#corpus.drop('date1',axis=1,inplace=True)

news=query_input('Karnataka Flood')
print(news.head())	
news_summary=news_info(news['url'])
news_summary.to_csv('Karnataka Flood', encoding='utf-8', index=False)
