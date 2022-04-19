import pandas as pd

from textblob import TextBlob

text = '''
The titular threat of The Blob has always struck me as the ultimate movie
monster: an insatiably hungry, amoeba-like mass able to penetrate
virtually any safeguard, capable of--as a doomed doctor chillingly
describes it--"assimilating flesh on contact.
Snide comparisons to gelatin be damned, it's a concept with the most
devastating of potential consequences, not unlike the grey goo scenario
proposed by technological theorists fearful of
artificial intelligence run rampant.
'''

blob = TextBlob(text)
tags = blob.tags          
noun_phrases = blob.noun_phrases  
sentences = blob.sentences

for sentence in sentences:
    print("objectivity:", sentence.sentiment.polarity)
    print("subjectivity:", sentence.sentiment.subjectivity)


df = pd.read_csv("../data/crypto.csv")


def run() -> None:
    pass


if __name__ == "__main__":

    run()
