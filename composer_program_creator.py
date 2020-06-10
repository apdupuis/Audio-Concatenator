# Get a string of the creator name for each file
# Could be used to make a program for all the concatenated audio

import os

# the directory of the audio files
rootdir = ''

# The proper name of each creator, paired with the name's representationin each filename
class_list = {
	"lastnamefirstname":"Firstname Lastname",
	"lastname2firstname2":"Firstname2 Lastname2"
}

for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		file_split = file.split("_")
		if file_split[0] in class_list:
			we = "good"
		else:
			print("no match for "+file_split[0])