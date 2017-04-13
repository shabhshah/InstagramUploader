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

#Google Drive authentication stuff
gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.

drive = GoogleDrive(gauth) # Create GoogleDrive instance with authenticated GoogleAuth instance

#Designates Google Drive Folder
folderID = '0B77gCYHoIAkAd29sREZBNlhPclk'
file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % folderID}).GetList()

#Writes the Google Drive information to a text file
fileNamesWrite = open('fileNames.txt', 'wr')

for item in file_list:
	fileNamesWrite.write(str(item) + "\n")
fileNamesWrite.close()

#Reads the text file to get file IDs and names
fileNamesRead = open('fileNames.txt', 'r')
fileNamesReadRow = fileNamesRead.readlines()

#Get the file IDs
IDList = []
for line in fileNamesReadRow:
	start = line.index("id': u'") + len("id': u'")
	end = line.index("',", start)
	print(line[start:end])
	IDList.append(line[start:end])

#Get the filenames
nameList = []
for line in fileNamesReadRow:
	start = line.index("originalFilename': u'") + len("originalFilename': u'")
	end = line.index("',", start)
	nameList.append(line[start:end])

#Remove the .jpg from the filename
for item in nameList:
	item = item[:-4]

#Download the first image from the folder and then delete from Google Drive
imageToDownload = drive.CreateFile({'id': IDList[0]})
imageToDownload.GetContentFile('imageToUpload.jpg')
imageToDownload.Delete()