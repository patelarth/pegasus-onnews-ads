from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import pandas as pd

class scrap:

    src = []
    summary = []
    df = pd.DataFrame()

    def __init__(self):
        ''' constructor method for an class'''
        self.src = []
        self.summary = []


    def preprocess_data(self,text):
        '''it will preprocess the text which contain the number and any other special charaters and return the preprocess text'''
        text = re.sub(r'\s+',' ',text)  # remove the special char. from the text
        text = re.sub(r'\d','',text)
        return text


    def scrap_via_bs4(self,links):
        'input link, it will scrap the data from the link and store in variable'
        for link in links:
            url = link
            html = urlopen(url) # make an connection to the link and apply bs4
            soup = BeautifulSoup(html, 'html.parser')
            text = ""
            title = ""
            for paragraph in soup.find_all('p'):
                text += paragraph.get_text()
                process_text = self.preprocess_data(text)
                process_text = '.'.join(process_text.split('.')) + '.'
            for paragraph in soup.find_all('h1'):
                title += paragraph.get_text()
                process_title = self.preprocess_data(text)
                process_title = '.'.join(process_title.split('.')) + '.'
            self.src.append(text)
            self.summary.append (title)

    def genrate_data_frame(self):
        ''' this function will genrate the data frame of the form the src and summary data.
         first have to genrate scrape data from the url'''
        self.df = pd.DataFrame({'text': self.src,
                                'summary': self.summary})
        return self.df

    def create_csv(self,name):
        ''' this function require file name with and extension .csv (other excel format are accepted) with the file path and create file of the scrapped dataset'''
        self.df.to_csv(name)
        print('File created')