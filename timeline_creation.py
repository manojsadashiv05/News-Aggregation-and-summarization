import numpy as np
import pandas as pd
import re
data= pd.read_csv('D:\\Manoj\\Documents\\sublime\\project\\temporal_extracted.csv')
from nltk.tokenize import sent_tokenize
def tokenizerr(text):
    sent = sent_tokenize(text)
    return sent
    

def remove_first_sent(text):
    del text[0]
    return text
data['tokenized_data'] = data['temporal_extracted_summary'].apply(lambda row: tokenizerr(row))
data['removed_first_sentence'] = data['tokenized_data'].apply(lambda row: remove_first_sent(row))
print(data['tokenized_data'])
print(data['removed_first_sentence'])
for i in range(0,data.shape[0]):
    date=data.iloc[i,3]
    for j in data.iloc[i,8]:
        re.sub('PRESENT_REF',str(date),j)

time_temp=pd.DataFrame(columns=['date','news'])

for i in range(data.shape[0]):
    for sent in data.iloc[i,8]:
        for k in range(0,2):
            result = re.search('<d>([^<]*)</d>', sent)
            #print(result)
            if result != None:
                sent = re.sub('<d>', '<D>', sent,1)
                #print(result.group(1))
                if result.group(1) == 'PRESENT_REF':
                    result = data.iloc[i,3]
                    temp_df = {'date': result, 'news': sent}
                else:
                    temp_df = {'date': result.group(1), 'news': sent}
                time_temp= time_temp.append(temp_df, ignore_index=True)

for i in range(time_temp.shape[0]):
    ans = re.match('[0-9]+(-[0-9]+)*', time_temp['date'][i])
    if ans == None:
        time_temp = time_temp.drop([i])
    else:
        #print(ans)
        time_temp['date'][i] = ans.group(0)

time_temp.sort_values(by = 'date',inplace=True)
print(time_temp)
time_temp.to_csv('timeline.csv', encoding='utf-8', index=False)