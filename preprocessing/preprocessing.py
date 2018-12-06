import csv
import unidecode
import io
import re
import string
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize

lemmatizer = WordNetLemmatizer()
file_name = "decoded_at.csv"

stop_words = [',', '"', "''", "'", '.', ';', '``', '...', '%', '-', '(', ')', ':', '!', '?', '[', ']', '', '#']
punctuation = string.punctuation

# removes links and @tags, and tokenizes
def clean(tweet):
    tweet = re.sub(r"http\S+", "", tweet)
    tweet = re.sub(r"@\S+", "", tweet)
    tokens = word_tokenize(tweet)
    clean_tokens = []
    for word in tokens:
        lemma = lemmatizer.lemmatize(word)
        clean_tokens.append(str(lemma))
    return clean_tokens


#returns the text with all encoded lower case characters
def encode(text):
    text_array = []
    clean_text = ""
    for character in text:
        try:
            decoded = unidecode.unidecode(character)
        except UnicodeEncodeError:
            decoded = " "
        except UnicodeDecodeError:
            decoded = " "
        if decoded not in punctuation:
            text_array.append(decoded.lower())
        clean_text = "".join(text_array)
    return clean_text


with io.open(file_name, 'rb') as csv_file:
    reader = csv.reader(csv_file)
    data = []
    print()
    print("PREPROCESSING DATA")
    for i,row in enumerate(reader):
        encoded_tweet = encode(row[2])
        clean_tweet = clean(encoded_tweet)
        row[2] = clean_tweet
        time_period = row[3]
        row[3] = " ".join(clean_tweet)
        row.append(time_period)
        if i != 0:
            data.append(row)
    print(data)
