import pandas as pd
import nltk
import re

# Read the CSV file
df = pd.read_csv("./input/input_tweets.csv")
df = df.sort_values(by="tweet", key=lambda x: x.str.len())

nltk.download('punkt')  # Download the necessary resources if not already downloaded

def split_into_sentences(text):
    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)
    return sentences

tweet_file = open('./input/tweets.txt', 'w')
label_file = open('./input/correct_labels.txt', 'w')

for index, row in df.iterrows():
    tweet_text = row["tweet"]
    label = row["label"]
    
    if "vacc" in tweet_text.lower():
        # print(tweet_text)
        tweet_text = re.sub(r"@([A-Za-z0-9_]{1,15})",'', tweet_text)
        tweet_text = re.sub(r"#([A-Za-z0-9_]+)",'', tweet_text)
        tweet_text = re.sub(r"(?:https?:\/\/)?(?:www\.)?[A-Za-z0-9\-]+\.[A-Za-z]{2,}(?:\/\S*)?",'', tweet_text)
        tweet_text = re.sub('\n','', tweet_text)
        tweet_text = re.sub(r'[^\x00-\x7F]+','', tweet_text)
        tweet_text = re.sub(r'\?\?','', tweet_text)
        tweet_text = re.sub(r'\.','. ', tweet_text)
        tweet_text = re.sub(r'\"[A-Za-z0-9_]+\"','', tweet_text)

        # print(tweet_text)
        # doc = nlp(tweet_text)
        # for sent in doc.sents:
        sentences = split_into_sentences(tweet_text)
        for sent in sentences:
            if "vacc" in sent.lower() and not sent.strip().endswith("?"):
                tweet_file.write(sent.strip() + '\n')
                if(label=='fake'):
                    label_file.write(str(1) + '\n' )
                else:
                    label_file.write(str(0) + '\n' )

