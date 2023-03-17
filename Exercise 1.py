num_words = int(input()) 
word_counts = {} 
words_list = [] 
# Read in words and count their occurrences
for i in range(num_words): 
    word = input() 
    words_list.append(word) 
    if word in word_counts: 
        word_counts[word] += 1 
    else:
        word_counts[word] = 1 
# Print the number of unique words and their counts
print(len(word_counts))
for word, count in word_counts.items():
 print(count)
 
 
