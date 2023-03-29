from task1 import textProcessing

file = "task1/text.txt"
text_for_processing = open(file, "r").read()

textProcessing.count_sentences("lhf", None)
