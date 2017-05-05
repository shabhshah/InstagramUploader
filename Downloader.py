# Copyright (c) 2017 Rishabh Shah

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Imports
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import re
from InstagramAPI import InstagramAPI
import getpass
from random import randint
import random
import time

igUserName = raw_input("Enter your IG username: ")
igPassword = getpass.getpass()


#Google Drive authentication stuff
gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.

drive = GoogleDrive(gauth) # Create GoogleDrive instance with authenticated GoogleAuth instance

#Designates Google Drive Folder
folderID = '0B77gCYHoIAkAd29sREZBNlhPclk'
while True:
	file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % folderID}).GetList()

	#Writes the Google Drive information to a text file
	fileNamesWrite = open('fileNames.txt', 'wr')
	for item in file_list:
		fileNamesWrite.write(str(item) + "\n")
	fileNamesWrite.close()

	#Randomize order of upload
	with open('fileNames.txt', 'rb') as inFile:
		lines = inFile.readlines()
	random.shuffle(lines)
	with open('fileNames.txt', 'wb') as outFile:
		outFile.writelines(lines)

	#Reads the text file to get file IDs and names
	fileNamesRead = open('fileNames.txt', 'r')
	fileNamesReadRow = fileNamesRead.readlines()

	#Get the file IDs
	IDList = []
	for line in fileNamesReadRow:
		start = line.index("id': u'") + len("id': u'")
		end = line.index("',", start)
		IDList.append(line[start:end])

	#Get the filenames
	nameList = []
	for line in fileNamesReadRow:
		start = line.index("originalFilename': u'") + len("originalFilename': u'")
		end = line.index("',", start)
		nameList.append(line[start:end])

	#Remove the .jpg from the filename
	nameList[0] = nameList[0][:-4]

	#Tag Brady or Rishabh based on ending
	if nameList[0][-2:] == "-b":
		nameList[0] = '"' + nameList[0][:-2] + '"' + ' - by @bradymokrzycki'
	elif nameList[0][-2:] == "-r"
		nameList[0] = '"' + nameList[0][:-2] + '"' + ' - by @theyungherbivore'

	#Sets the caption
	caption = nameList[0]

	#Download the first image from the folder and then delete from Google Drive
	imageToDownload = drive.CreateFile({'id': IDList[0]})
	imageToDownload.GetContentFile(nameList[0] + ".jpg")
	imageToDownload.Delete()

	#Login to Insta
	igapi = InstagramAPI(igUserName,igPassword)
	igapi.login()

	#Upload to Insta
	igapi.uploadPhoto(nameList[0] + ".jpg",caption=caption,upload_id=None)
	print("Image " + caption + " uploaded.")

	#Delay
	time.sleep(randint(25200,32400))