import nltk
from nltk.corpus import stopwords
from langdetect import detect

# Download NLTK resources (if not already downloaded)
nltk.download('punkt')

# Function to create a frequency table of words
def create_word_frequency_table(text, language, custom_stopwords):
    # Tokenize the text
    words = nltk.word_tokenize(text)
    # Filter out custom stop words
    stop_words = set(custom_stopwords)
    words = [word for word in words if word.lower() not in stop_words]
    # Create a frequency table
    frequency_table = {}
    for word in words:
        if word in frequency_table:
            frequency_table[word] += 1
        else:
            frequency_table[word] = 1
    return frequency_table

# Function to score sentences based on word frequency
def score_sentences(sentences, frequency_table):
    sentence_scores = {}
    for sentence in sentences:
        for word, freq in frequency_table.items():
            if word in sentence:
                if sentence in sentence_scores:
                    sentence_scores[sentence] += freq
                else:
                    sentence_scores[sentence] = freq
    return sentence_scores

# Function to extract the summary
def extract_summary(text, language, custom_stopwords, num_sentences=3):
    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)
    # Create the word frequency table
    frequency_table = create_word_frequency_table(text, language, custom_stopwords)
    # Score the sentences
    sentence_scores = score_sentences(sentences, frequency_table)
    # Get the top 'num_sentences' sentences as the summary
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    summary = ' '.join(summary_sentences)
    return summary

if __name__ == '__main__':
    # User input
    text = input("Enter the Tamil text: ")
    try:
        detected_language = detect(text)
    except:
        detected_language = 'en'  # Default to English if language detection fails
    if detected_language == 'ta':
        # Load custom Tamil stop words from a file
        with open('TamilStopWords.txt', 'r', encoding='utf-8') as f:
            tamil_stop_words = set(f.read().splitlines())
        f.close()
        # Extract the summary
        summary = extract_summary(text, 'tamil', tamil_stop_words, num_sentences=3)
        print("\nSummary:")
        print(summary)
    else:
        print("Language is not Tamil. Please provide Tamil text.")
