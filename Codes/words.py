# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import os

dirnames = ["A1 (Paris)", "A2 (Nigeria)", "B1 (Belgium)", "B2 (Pakistan)", "C1 (France)", "C2 (Iraq)"]

for dirname in dirnames:
	output = open("..\\Result\\"+dirname+"_aa.txt", "w", encoding = "utf-8")
	dirname = "..\\Data\\"+dirname

	file_list = os.listdir(dirname)
	num = len(file_list)
	i = 0
	file_list.sort()
	for filename in file_list:
		i+=1
		if filename[-4:] != ".txt":
			break
		name = filename.split("_")

		output.write(name[1]+"\n")
	output.close()