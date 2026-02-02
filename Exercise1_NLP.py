import numpy as np
import urllib.request
import re
import matplotlib.pyplot as plt
from collections import defaultdict

# Open the URL with urllib.request.urlopen()
# Read the HTTP response body as bytes
# Decode the bytes into a UTF-8 string
# Resources are from Gutenberg project
def read_book(book_url):
    book = urllib.request.urlopen(book_url)
    book = book.read()
    book = book.decode("utf-8")
    return book

book_url_en = 'https://www.gutenberg.org/cache/epub/16776/pg16776.txt'
book_en = read_book(book_url_en)

book_url_es = 'https://www.gutenberg.org/cache/epub/50341/pg50341.txt'
book_es = read_book(book_url_es)

# Using re.sub() function, we replace all the carriage returns and newlines, by spaces.
book_en = re.sub(r"\r\n"," ",book_en)
book_en = re.sub(r"\r"," ",book_en)
book_en = re.sub(r".*CONTENTS","",book_en) # Delete the part that is not main content of the book
book_en = re.sub(r"unavailing.*","unavailing.",book_en) # Delete the part that is not main content of the book
book_en = re.sub(r"\[illustration:.*?\]", "", book_en, flags=re.IGNORECASE) # Delete the illustrations (that should not consider as main content)
# The "illustration" actually affected the results making words that have length equal to 13 abnormal!
book_en = book_en.lower() # Get lower case for further analysis
# print(book_en)
# Using re.sub() function, we replace all the carriage returns and newlines, by spaces.
book_es = re.sub(r"\r\n"," ",book_es)
book_es = re.sub(r"\n"," ",book_es)
book_es = re.sub(r".*RIGHT R. D.","", book_es) # Delete the part that is not main content of the book
book_es = re.sub(r"MCMXVIII].*","MCMXVIII].",book_es) # Delete the part that is not main content of the book
book_es = re.sub(r"\[image:.*?\]", "", book_es, flags=re.IGNORECASE) # Delete the illustrations (imagen) (that should not consider as main content)
book_es = book_es.lower() # Get lower case for further analysis
# print(book_es)

words_en = re.findall(r"[a-z]+(?:['’][a-z]*)*(?:-[a-z]+)*", book_en)
# [a-z]+ : match any letter, it appears at least 1 time
# (?:['’][a-z]*)* : An independent group of REx, which means match single quote with or without any number of letters followed (e.g.: "student's, students'").
# The "quote" structure allows multiple match (e.g.: "rock'n'roll")
# The quote structure is not necessary (in order to match normal words).
# (?:-[a-z]+)* : For compounds like "good-bye, mother-in-law". But dash "--" is not allowed (good-bye--yes = good-bye + yes)
# print(words_en)

words_es = re.findall(r"[a-záéíóúüñ]+(?:['’][a-záéíóúüñ]*)*(?:-[a-záéíóúüñ]+)*", book_es)
# Similar REx to the English one, considering words like "pa' = para", "a'lante = adelante", "ex-presidente".
# print(words_es)

# Count the frequencies and their corresponding words for the English poems.
# Count the frequencies and their corresponding words for the Spanish poems.
def count_words(book_text):

    count_list = []
    book_words = []

    for i in book_text:
      if i not in book_words:
        book_words.append(i)
        count_list.append(1)
      else:
        count_list[int(book_words.index(i))] += 1

    return book_words, count_list

book_en_words, count_list_en = count_words(words_en)
book_es_words, count_list_es = count_words(words_es)

print(f"{book_en_words}")
print(f"{count_list_en}")
print(f"{book_es_words}")
print(f"{count_list_es}")

def computation_plotting(book_words, count_list, language):
    # Initialize dictionary: length = all word frequencies
    length_freq = defaultdict(list)

    for word, freq in zip(book_words, count_list):
        length_freq[len(word)].append(freq)

    # Computing the average frequency for each word length
    lengths = sorted(length_freq.keys())
    avg_freqs = [np.mean(length_freq[l]) for l in lengths]

    # Plot it using linear axis.
    plt.figure(figsize=(8,5))
    plt.bar(lengths, avg_freqs, color='skyblue')
    plt.xlabel('Word Length')
    plt.ylabel('Average Frequency')
    plt.title(f"{language}: Average Frequency by Word Length")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

# English poems plotting
computation_plotting(book_en_words, count_list_en, "English")
# Spanish poems plotting
computation_plotting(book_es_words, count_list_es, "Spanish")

# Search words with length of 15 to see why there is higher frequency
for word in book_en_words:
    if len(word) == 15:
        print(word)