if __name__ == '__main__':
	import numpy as np
	from py_heideltime import py_heideltime
	from nltk.tokenize import sent_tokenize 
	import pandas as pd
	import nltk

	#nltk.download('perluniprops')
	#news_data=pd.read_csv('C:\\Users\\Manoj\\Desktop\\data.csv')
	news_data=pd.read_csv('D:\\Manoj\\Documents\\sublime\\project\\news_summary.csv')
	def preprocess_data(data):
		data["summary"] = data["date"] +" . "+ data["summary"]
		data['summary'] = 'Today is ' + data['summary'].astype(str)
		return(data)
	
	def temporal_extraction(news_text):
	    temporal_tags=py_heideltime(news_text)
	    temporal_tags=temporal_tags[1]
	    return temporal_tags

	processed_news_data= preprocess_data(news_data)
	print('hi')
	processed_news_data['temporal_extracted_summary'] = processed_news_data['summary'].apply(lambda row: temporal_extraction(row))
	print('hi1')
	#processed_news_data['first_sentence_removed'] = processed_news_data['temporal_extracted_summary'].apply(lambda row: remove_first_sentence(row))
	print(processed_news_data['temporal_extracted_summary'].head(1))
	processed_news_data.to_csv('temporal_extracted.csv', encoding='utf-8', index=False)
