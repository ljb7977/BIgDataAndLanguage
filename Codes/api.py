# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import os

dirnames = ["A1 (Paris)", "A2 (Nigeria)", "B1 (Belgium)", "B2 (Pakistan)", "C1 (France)", "C2 (Iraq)"]

for dirname in dirnames:
	output = open("..\\Result\\"+dirname+".txt", "w", encoding = "utf-8")
	dirname = "..\\Data\\"+dirname

	# Instantiates a client
	client = language.LanguageServiceClient()

	file_list = os.listdir(dirname)
	num = len(file_list)
	score = 0
	i = 0
	file_list.sort()
	for filename in file_list:
		i+=1
		if filename[-4:] != ".txt":
			break
		#print(dirname+"\\"+filename)
		file = open(dirname+"\\"+filename, "r", encoding="utf-8")
		title = file.readline().strip()
		text = file.read()

		words = text.split()
		# The text to analyze
		document = types.Document(
			content=text,
			type=enums.Document.Type.PLAIN_TEXT)

		# Detects the sentiment of the text
		sentiment = client.analyze_sentiment(document=document).document_sentiment

		output.write("|".join([title, str(round(sentiment.score, 2))]))
		output.write("\n")
		
		print(title, end=", ")
		print(round(sentiment.score, 2), end=", ")
		print(round(sentiment.magnitude, 2), end=", ")
		print(len(words))
		print(i, "of", num)
		#score += sentiment.score
		file.close()
	output.close()
	#print(dirname+" score : ", score/num)