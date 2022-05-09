import nltk
from nltk.tokenize import word_tokenize
import pandas as pd
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import six
from google.cloud import translate_v2 as translate

ps = PorterStemmer()
wl = WordNetLemmatizer()

df = pd.read_csv("tweets_2_2_2022.csv")
df_text = df['text']
df['keywords'] = ''
'''df['grid'] = '''''

stop_words = nltk.corpus.stopwords.words('english')
new_stop_words = ['de','défense','paris','la','france']
stop_words.extend(new_stop_words)

# define function for translating
def translate_text(target, text):
    translate_client = translate.Client()
    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")
    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, source_language='fr', target_language=target)
    return(result["translatedText"])

# define function for natural language process
def NLP(i):
    # read text
    text = str(df_text[i])
    # translate text into English
    text_en = translate_text('en', text)
    # convert text to lower case
    lower_text = text_en.lower()
    # tokenize word
    tokenized_word = word_tokenize(lower_text)
    # remove words that have fewer than 2 characters
    long_word = [word for word in tokenized_word if len(word) > 2]
    # remove stop words
    removed_word = [word for word in long_word if word not in stop_words]
    # lemmatize words
    lemmatized_word = [wl.lemmatize(word) for word in removed_word]
    # stem
    stemmed_word = [ps.stem(word) for word in lemmatized_word]
    # tag POS
    POS_word = nltk.pos_tag(stemmed_word)
    # get NN and VBP
    keywords = []
    for n in POS_word:
        if n[1] == 'NN' or n[1] == 'VBP':
            keywords.append(n[0])
    df.loc[i,'keywords'] = ', '.join(keywords)

# get word frequency
'''fdist = FreqDist(keywords)
print(fdist.most_common(10))'''

# define the location
min_lng = 2.225684
min_lat = 48.885438
max_lng = 2.253922
max_lat = 48.897599
location = [2.225684,48.885438,2.253922,48.897599] #[minimum longitude, minimum latitude, maximum longitude, maximum latitude]
show_coordinates = True # setting this to false will download all tweets within the area, even if they don't have specific coordinates
has_coordinates = True

# divide the location into grids
lat_length = 0.0009
lng_length = 0.0014
grid_number_lat = int((max_lat - min_lat) / lat_length)
grid_number_lng = int((max_lng - min_lng) / lng_length)
print('Grid:', grid_number_lng, '*', grid_number_lat)

# grid and NLP
for n in range(grid_number_lng):
    for m in range(grid_number_lat):
        grid = str(str(n) + ',' + str(m))
        print('Searching grid:', grid)
        lng1 = min_lng + n * lng_length
        lat1 = min_lat + m * lat_length
        lng2 = min_lng + (n + 1) * lng_length
        lat2 = min_lat + (m + 1) * lat_length
        for i in range(len(df)):
            if lng1 < df['lng'][i] < lng2 and lat1 < df['lat'][i] < lat2:
                # put points into grids
                '''df.loc[i,'grid'] = grid'''
                # natural language process
                NLP(i)

# export to csv
df.to_csv("tweets_2_2_2022.csv", index=False)