# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import os

# Instantiates a client
client = language.LanguageServiceClient()

dirname = "B2 (Pakistan)"
file_list = os.listdir(dirname)
num = len(file_list)
score = 0
i = 0
file_list.sort()
for filename in file_list:
	i+=1
	if filename[-4:] != ".txt":
		break
	file = open(dirname+"\\"+filename, "r", encoding="utf-8")
	title = file.readline()
	text = file.read()
	# The text to analyze
	document = types.Document(
		content=text,
		type=enums.Document.Type.PLAIN_TEXT)

	# Detects the sentiment of the text
	sentiment = client.analyze_sentiment(document=document).document_sentiment

	print(title, end=" ")
	print('Sentiment: {}'.format(sentiment.score)+"\n")
	print(i, " of ", num)
	score += sentiment.score
	file.close()
print(dirname+" score : ", score/num)