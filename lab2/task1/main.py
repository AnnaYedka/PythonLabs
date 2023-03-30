import textProcessing
with open("text.txt", "r") as file:
    text = file.read()

print("Amount of sentences in the text: ", textProcessing.count_sentences(text))
print("Amount of non-declarative sentences in the text: ", textProcessing.count_non_declarative(text))
print("Average length of the sentence: ", round(textProcessing.count_sentence_length(text), 2))
print("Average length of the word: ", round(textProcessing.count_word_length(text), 2))
print("Top K ngrams: ", textProcessing.get_top_k_ngrams(text, input("Enter k: "), input("Enter n: ")))
