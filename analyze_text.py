from mediawiki import MediaWiki
import string

def open_webpage(page_name):
    """
    open the desired content of any webpage from wikipeda
    """
    wiki = MediaWiki()
    page = wiki.page(page_name)
    content = page.content

    return content


#need to install nltk on command prompt
import nltk
from nltk.tokenize import word_tokenize
# nltk.download('punkt')
# nltk.download('vader_lexicon')

def tokenize_words(content):
    """
    tokenize the words into a list and remove the puntuations
    """
    token = word_tokenize(content)
    token = [word.lower() for word in token if word.isalpha() ]
    return token


def word_freq(hist):
    """
    Characterizing by Word Frequencies:
    To use a dictionary where the keys are words that appear and
    the values are frequencies of words in the text
    """
    d = {}
    for word in hist:
        d[word] = d.get(word, 0) + 1
    return d


def print_freq_list(hist):
    """
    print the dictionary of word frequencies in a neat format
    """
    print("{:<8} {:<15}".format('Word','Number of Frequncies'))
    for word, value in hist.items():
        print("{:<8} {:<15}".format(word, value))


def process_file(filename, skip_header):
    """Makes a histogram that contains the words from a file.
    filename: string
    skip_header: boolean, whether to skip the Gutenberg header
    returns: map from each word to the number of times it appears.
    """
    hist = {}
    fp = open(filename, encoding='utf8')

    if skip_header:
        skip_gutenberg_header(fp)

    for line in fp:
        if line.startswith('*** END OF THIS PROJECT'):
            break
        line = line.replace('-', ' ')
        strippables = string.punctuation + string.whitespace

        for word in line.split():
            # remove punctuation and convert to lowercase
            word = word.strip(strippables)
            word = word.lower()
            # update the histogram
            hist[word] = hist.get(word, 0) + 1
    return hist


def most_common(hist, excluding_stopwords=True):
    t = []
    stopwords = process_file("stopwords.txt", False)
    stopwords = list(stopwords.keys())
    for word, freq in hist.items():
        if excluding_stopwords:
            if word in stopwords:
                continue
        t.append((freq, word))
    t.sort(reverse=True)
    return t


def top_10_words(hist, num = 10):
    """
    Finding the top 10 words in our text with their frequencies
    """
    t = most_common(hist)
    for freq, word in t[:num]:
        print(word,"\t", freq)


from nltk.sentiment.vader import SentimentIntensityAnalyzer
# nltk.download('averaged_perceptron_tagger')

def webpage_content(page_name):
    """
    open the desired summary of any webpage from wikipeda
    """
    wiki = MediaWiki()
    page = wiki.page(page_name)
    summary = page.summary

    return summary

def nltk_sentiment_analyzer(summary):
    """
    checking the polarity of the summary portion of the webpage
    """
    score = SentimentIntensityAnalyzer().polarity_scores(summary)
    print(score)
        

def main():
    text = open_webpage("Wikipedia")
    summary = webpage_content("Wikipedia")
    hist = tokenize_words(text)
    freq = word_freq(hist)

    print("Characterizing by Word Frequencies:")
    print_freq_list(freq)

    print('\n')

    print("The Top 10 Most Frequent Words on this Wikipedia Page is:")
    top_10_words(freq)
    
    print('\n')

    print("Sentiment Analysis of the Summary Portion of the Wikipedia Page:")
    nltk_sentiment_analyzer(summary)


if __name__ == '__main__':
    main()