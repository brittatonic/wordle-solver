import requests
from bs4 import BeautifulSoup
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

html = requests.get('https://www.techradar.com/news/past-wordle-answers')

bs = BeautifulSoup(html.content, 'html.parser')

df = pd.DataFrame(columns=['Number', 'Date', 'Wordle Word'])

for table in bs.find_all('table'):
    for row in table.tbody.find_all('tr'):
        column = row.find_all('td')
        # print(column)
        
        if ([] != column):
            number = column[0].text.strip()
            date = column[1].text.strip()
            word = column[2].text.strip()

            df = df.append({'Number': number, 'Date': date, 'Wordle Word': word}, ignore_index=True)

# print(str(df['Wordle Word']))

file = 'WordleAnswers.txt'
fid = open(file, 'w')
fid.write(df['Wordle Word'].to_string(index=False))
fid.close()





